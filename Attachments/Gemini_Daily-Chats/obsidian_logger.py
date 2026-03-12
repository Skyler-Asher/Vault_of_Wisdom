import sys
import json
import os
import re
from datetime import datetime

# Target directory
TARGET_DIR = "/home/crimson-crow/Documents/Vault of the Wisdom /Attachments/Gemini_Daily-Chats/"

def get_short_topic(text):
    """Creates a short 5-7 word summary for the toggle title."""
    text = text.strip().split('\n')[0] # Take first line
    text = re.sub(r'[^\w\s]', '', text) # Remove punctuation
    words = text.split()
    return " ".join(words[:7]) + "..." if len(words) > 7 else " ".join(words)

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
        day_name = now.strftime("%A")
        time_str = now.strftime("%H:%M:%S")
        date_header = now.strftime("%d / %m / %Y")
        
        # Extract messages
        messages = payload.get("llm_request", {}).get("messages", [])
        last_user_message = next((msg.get("content", "") for msg in reversed(messages) if msg.get("role") == "user"), "New Interaction")
        
        # Extract model response
        candidates = payload.get("llm_response", {}).get("candidates", [])
        if not candidates:
            return
        model_parts = candidates[0].get("content", {}).get("parts", [])
        model_response = ""
        for part in model_parts:
            if isinstance(part, str):
                model_response += part + "\n"
            elif isinstance(part, dict) and "text" in part:
                model_response += part["text"] + "\n"

        # 1. Create the Summary Bullet
        topic = get_short_topic(last_user_message)
        summary_line = f"- **{time_str}**: {topic}\n"

        # 2. Create the Toggleable Raw Entry
        raw_entry = f"""
<details>
<summary><b>{time_str} | Raw Data:</b> {topic}</summary>

**You:** {last_user_message.strip()}

**Gemini:** {model_response.strip()}

</details>
"""

        # Define file path
        file_path = os.path.join(TARGET_DIR, f"{date_str}.md")
        
        # Read existing content
        content = ""
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

        # Initialize file if empty
        if not content:
            content = f"# {date_header} – {day_name}\n\n> [!NOTE] Daily Journal\n> *A human-readable summary of today's work will be written here at the end of the session.*\n\n## 📝 Daily Summary\n\n\n## 📂 Detailed Logs\n"

        # Insert Summary Bullet
        if "## 📂 Detailed Logs" in content:
            parts = content.split("## 📂 Detailed Logs")
            new_content = parts[0].strip() + "\n" + summary_line + "\n## 📂 Detailed Logs\n" + parts[1].strip() + "\n" + raw_entry
        else:
            new_content = content + "\n" + summary_line + "\n" + raw_entry

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
            
    except Exception as e:
        pass

if __name__ == "__main__":
    log_to_obsidian()
