# 🧠 M365 Assistant — Microsoft 365 AI via MCP

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)
![Microsoft Graph](https://img.shields.io/badge/Microsoft-Graph_API-0078D4?logo=microsoft)
![MCP](https://img.shields.io/badge/MCP-Model_Context_Protocol-black)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent_Orchestration-purple)
![Groq](https://img.shields.io/badge/Groq-LLM-red)

---

# 🎯 Project Overview

This project builds a **Microsoft 365 AI Assistant** using:

- 🐍 Python
- 🔗 Model Context Protocol (MCP)
- 📧 Microsoft Graph API
- 💬 Claude Desktop integration
- 🤖 Optional Agent layer using LangGraph + Groq

---

# 🔥 Core Objective (Primary Goal)

The main aim of this project is:

> ✅ Create an MCP server exposing Microsoft Outlook and Calendar tools  
> ✅ Connect it to Claude Desktop using a `claude_desktop_config.json` file  
> ✅ Allow natural language interaction with real Microsoft 365 data  

This means you can:

- Ask Claude to read your emails
- Send emails
- Reply to emails
- Check calendar events
- Create folders
- Mark emails read/unread
- Search Outlook
- Check meeting availability

All directly through Claude.

---

# 🏗 Core Architecture

```
Claude Desktop
      ↓
MCP Client (JSON config)
      ↓
Python MCP Server
      ↓
Microsoft Graph API
      ↓
Outlook & Calendar
```

---

# 📂 Project Structure

```
m365_assistant/
│
├── m365_assistant/
│   ├── main.py              ← MCP server entry
│   │
│   ├── core/                ← Auth + Graph client
│   ├── services/            ← Mail + Calendar logic
│   ├── mcp/                 ← Tool definitions
│   │
│   └── agent/               ← (Optional AI agent layer)
```

---

# 🚀 Running the Core MCP Server

## Step 1 — Install dependencies

```bash
uv sync
```

## Step 2 — Add environment variables

Create `.env`:

```env
MICROSOFT_CLIENT_ID=your_client_id
```

(No tenant ID required — uses `common` authority.)

---

## Step 3 — Run MCP Server

```bash
uv run python -m m365_assistant.main
```

This starts the Microsoft 365 MCP server.

---

# 💬 Connect to Claude Desktop

Add this to your `claude_desktop_config.json` go to settings then developer and then edit config then open the file claude_desktop_config and add the below JSON

```json
{
  "mcpServers": {
    "m365": {
      "command": "uv",
      "args": [
        "--directory",
        "path to your\\m365_assistant",
        "run",
        "python",
        "-m",
        "m365_assistant.main"
      ],
     "env": {
        "MICROSOFT_CLIENT_ID": "your_client_id"
      }
    }
  }
}
```

Restart Claude Desktop.

Now you can chat with your Microsoft account.

---

## 📧 Email Tools

- **list_emails** – Retrieves recent emails from a selected mailbox folder.
- **get_email** – Fetches complete details of a specific email by its ID.
- **search_emails** – Searches mailbox emails using keywords or filters.
- **send_email** – Sends a new email to specified recipients.
- **reply_email** – Replies directly to the sender of an email.
- **reply_all_email** – Replies to all recipients in an email thread.
- **forward_email** – Forwards an existing email to new recipients.
- **mark_email_read** – Marks a specific email as read.
- **mark_email_unread** – Marks a specific email as unread.
- **flag_email** – Flags or updates the follow-up status of an email.
- **create_mail_folder** – Creates a new custom folder in the mailbox.


## 📅 Calendar Tools

- **list_events** – Lists upcoming calendar events within a specified date range.
- **check_availability** – Checks free/busy availability for scheduling meetings.
- **unified_search** – Searches across mail, calendar, and drive items in one query.


---

# 🔐 Authentication Flow

The system uses Microsoft Device Flow:

On first tool call you will see:

```
Go to https://microsoft.com/devicelogin
Enter code: XXXXX
```

After login:
- Tokens are cached
- Future calls use silent refresh
- No repeated login required

---

# 🧠 Example Claude Usage

You can ask:

- "Show my last 5 emails"
- "Reply to the latest email"
- "Mark this as unread"
- "What meetings do I have today?"
- "Create a new folder called Projects"

Claude will automatically call the correct MCP tools.

# 🧠 Example Claude Usage

You can ask:

- "Show my last 5 emails"
- "Reply to the latest email"
- "Mark this as unread"
- "What meetings do I have today?"
- "Create a new folder called Projects"

Claude will automatically call the correct MCP tools.

---

## 📸 Screenshots

### 🔐 Authentication Flow

When first connecting, you will see the Microsoft device login prompt:

![Authentication Flow](assets/authentication.png)

---

### 📧 Listing Emails

Claude retrieving recent emails using the `list_emails` tool:

![List Emails](assets/list_emails.png)

---

### 📅 Viewing Calendar Events

Claude fetching today's meetings:

![Calendar Events](assets/calendar_events.png)

---

### 📁 Creating a Mail Folder

Claude creating a new folder:

![Create Folder](assets/create_folder.png)

---

### 🤖 Agent Mode (Optional)

AI-generated daily routine using LangGraph + Groq:

![Agent Routine](assets/agent_routine.png)


---

# 🤖 Secondary Layer — Agent Mode (Optional)

Beyond Claude Desktop integration, this project includes an optional **Agentic AI system**.

This agent:

- Uses MCP tools to fetch real Microsoft data
- Uses GPT-style Groq model to collect relevant context
- Uses LLaMA model to generate a prioritized daily routine

---

# 🏗 Agent Architecture

```
User Input
     ↓
LangGraph Orchestrator
     ↓
Groq GPT Model (Tool Executor)
     ↓
MCP Tools (Mail + Calendar)
     ↓
Groq LLaMA Model (Routine Planner)
     ↓
Final Daily Schedule
```

---

# 🚀 Running Agent Mode

Add Groq key:

```env
GROQ_API_KEY=your_key
```

Run:

```bash
uv run python -m m365_assistant.agent.runner
```

Example:

```
Plan my workday today
```

The system will:

- Fetch recent emails
- Fetch calendar events
- Identify urgent items
- Generate a structured time-blocked schedule

---

# 🎯 Clear Separation of Responsibilities

## Core Layer (Primary Project)

✔ MCP Server  
✔ Claude Desktop Integration  
✔ Outlook & Calendar Automation  

This is the main production use-case.

---

## Agent Layer (Extended Capability)

✔ Multi-LLM Orchestration  
✔ LangGraph  
✔ Groq Integration  
✔ AI-powered daily planning  

This is an advanced extension built on top of the MCP foundation.

---

# 🧰 Tech Stack

- Python 3.11+
- FastMCP
- Microsoft Graph API
- MSAL
- HTTPX
- LangChain
- LangGraph
- Groq LLM API
- Claude Desktop MCP

---

# 📌 Future Enhancements

- Long-term memory
- Task persistence
- Email priority classification
- Autonomous scheduling
- Teams integration

---
# 🤝 Contributing

Contributions are welcome! and I will also be keep on adding tools

---

## 🚀 How to Add a New Tool

### Step 1 — Add Business Logic

Add your function inside:

```
m365_assistant/services/
```

Example:

```python
def delete_email(self, email_id: str):
    """Deletes an email by ID."""
```

---

### Step 2 — Register MCP Tool

Open:

```
m365_assistant/mcp/tools.py
```

Register:

```python
@mcp.tool
def delete_email(email_id: str):
    """Delete an email by ID."""
    return mail_service.delete_email(email_id)
```

---

### Step 3 — Update README

Add:
- One-line tool description
- Usage example (if needed)

---

### Step 4 — Create Branch & PR

```bash
git checkout -b feature/add-new-tool
git add .
git commit -m "Add delete_email tool"
git push origin feature/add-new-tool
```

Then open a Pull Request on GitHub.

---

# 📌 Contribution Guidelines

- Keep code modular
- Add proper docstrings
- Use environment variables (no hardcoded secrets)
- Handle errors properly
- Update documentation when adding features
- Never commit `.env` or token files

---

# 🌟 Areas Open for Contribution

- More Outlook tools
- Calendar enhancements
- Teams integration
- Task automation
- Performance improvements
- Long-term memory support
- Autonomous scheduling improvements

---

# 🛡 Security Notice

Never commit:
- `.env` files
- Client secrets
- Access tokens
- Authentication cache files

Add them to `.gitignore`.

---
# 📄 License

MIT License.

---

# 🧑‍💻 Author

AI-powered Microsoft 365 automation system built using MCP + LangGraph + Groq.

