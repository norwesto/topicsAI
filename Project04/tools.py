import requests
import os
from datetime import timezone, datetime, timedelta
from dotenv import load_dotenv
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

CANVAS_API_TOKEN = os.getenv("CANVAS_API_TOKEN")
CANVAS_URL = os.getenv("CANVAS_URL")
CALENDAR_FILE = "calendar.json"

HEADERS = {
    "Authorization": f"Bearer {CANVAS_API_TOKEN}"
}

# CANVAS API TOOL

def get_courses():
    '''Get all active courses for  current user'''
    url = f"{CANVAS_URL}/api/v1/courses"
    parameters = {
        "enrollment_state": "active",
        "per_page": 50
    }
    response = requests.get(url, headers = HEADERS, params = parameters, verify = False)
    if response.status_code != 200:
        return f"Error fetching courses: {response.status_code}"
    
    courses = response.json()
    result = []
    for course in courses:
        if "name" in course:
            result.append({
                "id": course["id"],
                "name": course["name"]
            })
    return result


def get_assignments(course_id: int):
    '''Get upcoming assignments for a specific course ID'''
    url = f"{CANVAS_URL}/api/v1/courses/{course_id}/assignments"
    parameters = {
        "order_by": "due_at",
        "per_page": 50,
        "bucket": "upcoming"
    }
    response = requests.get(url, headers = HEADERS, params = parameters, verify = False)
    if response.status_code != 200:
        return f"Error fetching assignments: {response.status_code}"
    
    assignments = response.json()
    result = []
    for a in assignments:
        result.append({
            "name": a.get("name"),
            "due_at": a.get("due_at"),
            "course_id": course_id,
            "points": a.get("points_possible"),
            "description": (a.get("description") or "")[:200]
        })
    return result


def get_all_upcoming_assignments():
    '''Get upcoming assignments across all active courses'''
    courses = get_courses()
    if isinstance(courses, str):  # error string
        return courses
    
    all_assignments = []
    for course in courses:
        assignments = get_assignments(course["id"])
        if isinstance(assignments, list):
            for a in assignments:
                a["course_name"] = course["name"]
                all_assignments.append(a)
    
    # sort by due date
    all_assignments.sort(key = lambda x: x["due_at"] or "9999")
    return all_assignments

# CALENDAR TOOL

def load_calendar():
    '''Load calendar events from JSON file'''
    if not os.path.exists(CALENDAR_FILE):
        print("did not find")
        return []
    with open(CALENDAR_FILE, "r") as f:
        return json.load(f)


def save_calendar(events):
    '''Save calendar events to JSON file'''
    with open(CALENDAR_FILE, "w") as f:
        json.dump(events, f, indent = 2)


def add_study_session(title: str, date: str, start_time: str, end_time: str, course: str, notes: str = ""):
    '''
    Add a study session to local calendar.
    
    Parameters:
        title -- name of the study session
        date -- date in YYYY-MM-DD format
        start_time -- start time in HH:MM format (24hr)
        end_time -- end time in HH:MM format (24hr)
        course -- course name this session is for
        notes -- optional notes
    '''
    events = load_calendar()
    event = {
        "id": len(events) + 1,
        "title": title,
        "date": date,
        "start_time": start_time,
        "end_time": end_time,
        "course": course,
        "notes": notes,
        "created_at": datetime.now().isoformat()
    }
    events.append(event)
    save_calendar(events)
    return event


def get_events_for_week(start_date: str):
    '''
    Get all events for the week starting on start_date.
    
    Parameters:
        start_date -- start date in YYYY-MM-DD format
    '''
    events = load_calendar()
    

    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = start + timedelta(days = 7)
    
    week_events = []
    for e in events:
        event_date = datetime.strptime(e["date"], "%Y-%m-%d")
        if start <= event_date < end:
            week_events.append(e)
    
    week_events.sort(key = lambda x: (x["date"], x["start_time"]))
    return week_events


def clear_calendar():
    '''Clear all events from the calendar'''
    save_calendar([])
    return "Calendar cleared"


def delete_event(event_id: int):
    '''Delete a specific event by ID'''
    events = load_calendar()
    events = [e for e in events if e["id"] != event_id]
    save_calendar(events)
    return f"Event {event_id} deleted"

def main():

    print("COURSES:")
    courses = get_courses()
    for c in courses:
        print(c)
    
    print("\nUPCOMING ASSIGNMENTS:")
    assignments = get_all_upcoming_assignments()
    for a in assignments:
        raw = a['due_at']
        if raw:
            dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
            local_dt = dt.astimezone()
            friendly = local_dt.strftime("%b %d, %Y %I:%M %p")
        else:
            friendly = "No due date"
        print(f"{friendly} | {a['course_name']} | {a['name']}")

if __name__ == "__main__":
    main()