# Gemini CLI - Obsidian Vault Logging

## Directory Overview
This directory is part of an **Obsidian Vault** specifically designed to store and manage daily chat history from the **Gemini CLI**. It uses an automated, real-time logging system to record interactions as they happen, ensuring no data is lost even in the event of a system crash.

The goal is to keep a "cleaned" history (direct messages only, excluding tool calls and system messages) in a format that is easily searchable and readable within Obsidian.

## Key Files & Infrastructure

*   **`DD-MM-YYYY.md`**: These are the daily log files (e.g., `12-03-2026.md`). Each file contains the full record of interactions for that specific date.
*   **`obsidian_logger.py`**: A Python helper script that processes the Gemini CLI's internal hook payload. It extracts the user's prompt and Gemini's response, formats them into Markdown with timestamps, and appends them to the daily file.
*   **`.gemini/settings.json`**: A local (project-level) configuration file. It registers the `AfterModel` hook, which triggers the `obsidian_logger.py` script automatically after every model response.

## Usage & Workflow

### 1. Activating the Logger
The logging system is activated by starting the Gemini CLI from this directory. Because the `.gemini/settings.json` file is located here, the CLI will automatically load the project-specific hook.

```bash
cd "/home/crimson-crow/Documents/Vault of the Wisdom /Attachments/Gemini_Daily-Chats/"
gemini
```

### 2. Log Format
Each entry in the daily `.md` files follows this structure:

```markdown
### [HH:MM:SS]
**You:** [The User's Prompt]

**Gemini:** [The AI's Response]

---
```

### 3. Crash Protection
The system uses the `AfterModel` hook rather than a `SessionEnd` hook. This ensures that every response is saved **immediately** after it is generated. If the terminal is closed abruptly or the PC crashes, everything up to the last message is already safely stored in the daily Markdown file.

## Maintenance
*   **Python Requirement**: The system requires `python3` to be available in the system path.
*   **Pathing**: The `obsidian_logger.py` script uses absolute paths to ensure it can correctly locate the target directory even if run from different subfolders (though starting the CLI from the root is recommended).
