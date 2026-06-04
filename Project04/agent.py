from openai import OpenAI
import os, time
from datetime import datetime
import json
from dotenv import load_dotenv
from tools import get_all_upcoming_assignments, add_study_session, get_events_for_week, clear_calendar, delete_event, save_calendar, load_calendar, get_assignments, get_courses

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key = api_key)
load_dotenv()

os.environ['TZ'] = 'America/Denver'
time.tzset()

now = datetime.now()
today = datetime.now().strftime("%B %d, %Y")
current_time = now.strftime("%I:%M %p")

SYSTEM_PROMPT = f"""
You are a helpful academic planning assistant. Your job is to help students manage their assignments and schedule study sessions.

Today's date is {today} and the exact current time is {current_time}, timezone is America/Denver. Do not say you don't know the time.
Do not guess. Use exactly these values when asked. When displaying due dates, convert them from UTC to MDT (subtract 6 hours) before 
showing them to the user. All booking should be done in America/Denver time.

You have access to the following tools:
    - get_all_upcoming_assignments: fetches all upcoming assignments from Canvas with due dates and course names
    - add_study_session: adds a study session to the calendar with a title, date, start time, end time, and course name
    - get_events_for_week: retrieves all scheduled study sessions for a given week

When the user asks for help planning, you must:
    1. First fetch their assignments using get_all_upcoming_assignments
    2. Prioritize assignments by due date, soonest first
    3. Suggest study sessions that give the student enough time before each deadline
    4. Add those sessions to the calendar using add_study_session

Always explain what you are doing and why. Be concise. If an assignment is due soon, flag it as urgent."""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_study_session",
            "description": "Add a study session to the calendar",
            "parameters": {
                "type": "object",
                "properties": {
                    "title":      {"type": "string"},
                    "date":       {"type": "string", "description": "YYYY-MM-DD"},
                    "start_time": {"type": "string", "description": "HH:MM 24hr"},
                    "end_time":   {"type": "string", "description": "HH:MM 24hr"},
                    "course":     {"type": "string"},
                    "notes":      {"type": "string"}
                },
                "required": ["title", "date", "start_time", "end_time", "course"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "clear_calendar",
            "description": "Clear all events from the local calendar",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_event",
            "description": "Delete a specific study session from the calendar by event ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_id": {"type": "integer", "description": "The ID of the event to delete"}
                },
                "required": ["event_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_all_upcoming_assignments",
            "description": "Fetch all upcoming assignments from Canvas sorted by due date",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_assignments",
            "description": "Fetch upcoming assignments for a specific Canvas course by course ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_id": {"type": "integer", "description": "The Canvas course ID"}
                },
                "required": ["course_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_courses",
            "description": "Fetch all active Canvas courses for the current user",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_events_for_week",
            "description": "Get all scheduled study sessions for a given week",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {"type": "string", "description": "Start date in YYYY-MM-DD format"}
                },
                "required": ["start_date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "load_calendar",
            "description": "Load all events from the local calendar",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    }
]

def run_tool(tool_name: str, tool_args: dict):

    """
    Runs the chosen tool and returns the result as a string
    """

    print(f"\n[AGENT] Using tool: {tool_name}")
    if tool_name == "get_all_upcoming_assignments":
        return str(get_all_upcoming_assignments())
    elif tool_name == "get_events_for_week":
        return str(get_events_for_week(**tool_args))
    elif tool_name == "add_study_session":
        return str(add_study_session(**tool_args))
    elif tool_name == "get_assignments":
        return str(get_assignments(**tool_args))
    elif tool_name == "get_courses":
        return str(get_courses())
    elif tool_name == "load_calendar":
        return str(load_calendar())
    elif tool_name == "save_calendar":
        return str(save_calendar(**tool_args))
    elif tool_name == "delete_event":
        return str(delete_event(**tool_args))
    elif tool_name == "clear_calendar":
        return str(clear_calendar())
    return "Tool not found"

def chat(messages: list):

    """
    Helper function that takes list of prompts/responses and
    returns new response.
    """

    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = messages,
        tools = TOOLS,
        tool_choice = "auto"
    )
    message = response.choices[0].message

    if message.tool_calls:
        messages.append(message)
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            observation = run_tool(tool_name, tool_args)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": observation
            })
        # call again with tool results
        followup = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = messages,
            tools = TOOLS,
            tool_choice = "auto"
        )
        return followup.choices[0].message.content

    return message.content

def main():

    messages = []
    messages.append({"role": "system", "content": SYSTEM_PROMPT})
 
    print()
    print("Welcome! I am your Canvas Planning Assistant. How can I help you today?\n")
 
    while True:
        user_input = input("").strip()
 
        if user_input.lower() in ("quit", "exit"):
            print("Thanks for chatting with me. Have a great day!")
            break
 
        # add user message
        messages.append({"role": "user", "content": user_input})
        reply = chat(messages)
 
        # store assistant reply
        messages.append({"role": "assistant", "content": reply})
 
        print(f"\n{reply}\n")

if __name__ == "__main__":
    main()
