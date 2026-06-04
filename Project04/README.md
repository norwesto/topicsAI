# Canvas Planning Assistant
**Author:** Nora Westol
**Course:** Topics in AI
**Date:** June 2026
**Collaborators:** LEP Tutor (Catherine Tifft)


## What It Does
The Canvas Planning Assistant is an agentic AI system that helps students manage their academic workload. It connects to your Canvas account to fetch upcoming assignments and their due dates, then helps you schedule study sessions on a local calendar. You can ask it questions like "what assignments do I have this week?" or "schedule a study session for my physiology homework" and it will reason through the request, call the right tools, and respond with a plan.

## How To Use It
Run the terminal version:
    python3 agent.py

Run the Streamlit UI:
    streamlit run app.py

Examples of viable requests:
- "What assignments do I have coming up?"
- "Schedule a study session for my film criticism assignment"
- "Show me my schedule for this week"
- "Delete study session 3"
- "Clear my calendar"

Type `quit` or `exit` to close the terminal version.

## Tools

### Canvas API Tool (`get_courses`, `get_assignments`, `get_all_upcoming_assignments`)
Connects to the Canvas API at canvas.du.edu to fetch active courses and upcoming assignments sorted by due date. I used this because Canvas is where all assignment data lives and without it, the agent would have no real information to plan around.

### Calendar Tools (`add_study_session`, `get_events_for_week`, `load_calendar`, `delete_event`, `clear_calendar`)
A local JSON-based calendar stored in `calendar.json` inside the project folder. I chose a local calendar over Google Calendar to avoid complex setup. This tool stores study sessions with a title, date, start/end time, course name, points, and notes.

### OpenAI Function Calling (gpt-4o-mini)
The agent uses OpenAI's function calling feature to decide which tool to use based on the user's request. Rather than parsing the model's text output, the tool definitions are passed directly to the API and the model will select and use them automatically. This makes tool selection reliable and easy to extend.

## Limitations and Known Failure Cases

- Time awareness: The agent knows today's date and time from when the script starts, but if you leave it running for hours the time will be stale.
- SL certificate: DU's Canvas server requires `verify=False` on API requests due to a certificate issue, which suppresses SSL verification warnings.
- Canvas only fetches upcoming assignments: Past or unsubmitted assignments are not retrieved — only assignments in the "upcoming" bucket.
- Local calendar only: Study sessions are stored in a local JSON file and are not synced to Google Calendar or any other external calendar.
- No conflict detection: The agent will schedule overlapping study sessions without warning if you ask it to.
- Model guessing: Occasionally the gpt-4o-mini will guess a date or time instead of using the values provided, especially for scheduling far in the future. Specific instructions had to be included in the prompt in order for proper functioning.