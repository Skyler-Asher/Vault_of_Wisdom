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

        # Prepare entries
        topic = get_short_topic(last_user_message)
        timeline_line = f"- **{time_str}**: {topic}\n"
        raw_entry = f"\n<details>\n<summary><b>{time_str} | Raw Data:</b> {topic}</summary>\n\n**You:** {last_user_message.strip()}\n\n**Gemini:** {model_response.strip()}\n\n</details>\n"

        # Define file path
        file_path = os.path.join(TARGET_DIR, f"{date_str}.md")
        
        # 1. Ensure file exists and has basic structure
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            initial_content = f"# {date_header} – {day_name}\n\n> [!NOTE] Daily Journal\n> *Insert human-readable story here.*\n\n## 📝 Daily Summary\n> [!ABSTRACT] Summary of Achievements\n> *The structured summary of today's work will be added here at the end of the session.*\n\n## 🕓 Timeline\n\n## 📂 Detailed Logs\n"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(initial_content)

        # 2. Read content and use Regex for resilient insertion
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Find Timeline and Detailed Logs sections using flexible regex
        # This matches "##" followed by anything, then "Timeline" or "Detailed Logs"
        timeline_pattern = re.compile(r"^##.*Timeline.*$", re.MULTILINE | re.IGNORECASE)
        logs_pattern = re.compile(r"^##.*Detailed Logs.*$", re.MULTILINE | re.IGNORECASE)

        timeline_match = timeline_pattern.search(content)
        logs_match = logs_pattern.search(content)

        # Robust Reconstruction Logic
        if timeline_match and logs_match:
            # We have both. Insert timeline entry before logs header, and raw entry at the very end.
            parts = content.split(logs_match.group(0))
            new_content = parts[0].strip() + "\n" + timeline_line + "\n\n" + logs_match.group(0) + "\n" + parts[1].strip() + "\n" + raw_entry
        elif logs_match:
            # Missing Timeline? Add it back before Logs.
            parts = content.split(logs_match.group(0))
            new_content = parts[0].strip() + "\n\n## 🕓 Timeline\n" + timeline_line + "\n\n" + logs_match.group(0) + "\n" + parts[1].strip() + "\n" + raw_entry
        elif timeline_match:
            # Missing Logs? Add it at the end.
            new_content = content.strip() + "\n" + timeline_line + "\n\n## 📂 Detailed Logs\n" + raw_entry
        else:
            # Total chaos? Just append everything safely.
            new_content = content.strip() + "\n\n## 🕓 Timeline\n" + timeline_line + "\n\n## 📂 Detailed Logs\n" + raw_entry

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
            
    except Exception as e:
        pass

if __name__ == "__main__":
    log_to_obsidian()
