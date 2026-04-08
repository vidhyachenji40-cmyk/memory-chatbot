import datetime

TOOL_DEFINITIONS = [
    {
        "name": "get_datetime",
        "description": "Returns the current date and time. Use this when the user asks for the time or date.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "save_memory",
        "description": "Saves a personal fact about the user (name, location, likes).",
        "input_schema": {
            "type": "object",
            "properties": {
                "key": {"type": "string", "description": "The category, e.g., 'name'"},
                "value": {"type": "string", "description": "The fact, e.g., 'Vidhya'"}
            },
            "required": ["key", "value"]
        }
    }
]

def run_tool(tool_name: str, tool_input: dict, long_term_memory) -> str:
    if tool_name == "get_datetime":
        now = datetime.datetime.now()
        return f"The current date and time is {now.strftime('%A, %B %d, %Y at %I:%M %p')}."
    
    elif tool_name == "save_memory":
        long_term_memory.save_fact(tool_input['key'], tool_input['value'])
        return f"✅ Success: I have remembered that {tool_input['key']} is {tool_input['value']}."
    
    return f"Error: Tool {tool_name} not found."