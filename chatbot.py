import os
from dotenv import load_dotenv
import anthropic

from tools import TOOL_DEFINITIONS, run_tool
from memory import ShortTermMemory, LongTermMemory

# Load .env (if it exists) but priority goes to GitHub Secrets
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise ValueError("❌ API Key not found! Please check your GitHub Codespace Secrets.")

client = anthropic.Anthropic(api_key=api_key)
MODEL = "claude-sonnet-4-6"


short_term = ShortTermMemory()
long_term = LongTermMemory("memory.json")

def build_system_prompt():
    facts = long_term.get_all_facts()
    memory_context = ""
    if facts:
        memory_context = "\n\nFacts I know about you:\n" + "\n".join([f"- {k}: {v}" for k, v in facts.items()])
    
    return f"You are a helpful, context-aware AI assistant.{memory_context}"

def chat(user_input: str):
    short_term.add("user", user_input)
    
    # 1. Send to Claude
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=build_system_prompt(),
        messages=short_term.get_messages(),
        tools=TOOL_DEFINITIONS
    )

    # 2. Handle the "Agentic Loop" (Tool Calling)
    while response.stop_reason == "tool_use":
        # Add Claude's request to call a tool to history
        short_term.add("assistant", response.content)
        
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"🔧 [AI calling tool: {block.name}]")
                result = run_tool(block.name, block.input, long_term)
                
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })

        # Add results to history and call Claude back for a final answer
        short_term.add("user", tool_results)
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=build_system_prompt(),
            messages=short_term.get_messages(),
            tools=TOOL_DEFINITIONS
        )

    # 3. Get final text reply
    final_text = response.content[0].text
    short_term.add("assistant", final_text)
    return final_text

if __name__ == "__main__":
    print("==========================================")
    print("   🤖 Memory Chatbot is now LIVE!")
    print("   Type 'quit' to exit.")
    print("==========================================")
    
    while True:
        try:
            inp = input("\nYou: ").strip()
            if not inp: continue
            if inp.lower() in ["quit", "exit"]: 
                print("Goodbye!")
                break
                
            print("AI: ", end="", flush=True)
            print(chat(inp))
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")