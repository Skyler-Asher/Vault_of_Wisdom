import sys
import json
import os
from datetime import datetime

# Target directory (Current directory of the script)
TARGET_DIR = os.path.dirname(os.path.abspath(__file__))

def log_to_obsidian():
    try:
        # Read the hook payload from stdin
        input_data = sys.stdin.read()
        if not input_data:
            return
        
        payload = json.loads(input_data)
        
        # Get date and time
        now = datetime.now()
        date_str = now.strftime("%d-%m-%Y")
        time_str = now.strftime("%H:%M:%S")
        
        # Extract messages from the request
        messages = payload.get("llm_request", {}).get("messages", [])
        
        # Get the latest user message
        # Note: In AfterModel, the last user message is the prompt we just answered
        last_user_message = next((msg.get("content", "") for msg in reversed(messages) if msg.get("role") == "user"), "Unknown Prompt")
        
        # Extract model response from the response
        candidates = payload.get("llm_response", {}).get("candidates", [])
        if not candidates:
            return
            
        model_parts = candidates[0].get("content", {}).get("parts", [])
        # Parts can be strings or objects (e.g., function calls, but the user wants "cleaned")
        # We only take strings
        model_response = ""
        for part in model_parts:
            if isinstance(part, str):
                model_response += part + "\n"
            elif isinstance(part, dict) and "text" in part:
                model_response += part["text"] + "\n"
        
        # Format the entry
        markdown_entry = f"### [{time_str}]\n**You:** {last_user_message.strip()}\n\n**Gemini:** {model_response.strip()}\n\n---\n"
        
        # Define file path
        file_path = os.path.join(TARGET_DIR, f"{date_str}.md")
        
        # Write to file
        file_exists = os.path.exists(file_path)
        with open(file_path, "a", encoding="utf-8") as f:
            if not file_exists or os.path.getsize(file_path) == 0:
                f.write(f"# Chat History - {date_str}\n\n")
            f.write(markdown_entry)
            
    except Exception as e:
        # Fail silently
        pass

if __name__ == "__main__":
    log_to_obsidian()
