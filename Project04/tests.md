# Testing Prompts:

## Successful Tests: 

Prompt: "What are my upcoming assignments?"
Purpose: Verify the agent can fetch and display Canvas assignments sorted by due date.

Prompt: "What time is it?"
Purpose: Confirm the agent knows current date and time so sessions can be booked correctly.

Prompt: "upcoming assignments"
Purpose: Checks if agent can understand incomplete or casual phrasing.

Prompt: "Book study sessions for all assignemnts"
Purpose: Checks if agent can handle bulk scheduling requests.

Prompt: "Book a study session for june 1st at 11:30 for film
Purpose: Confirms the agent can schedule a specific session when given a specifc date, time, and course.

Prompt: "Are there any sessions booked for the same assignment?"
Purpose: Check whether the agent will recognize duplicate or redundant sessions.

Prompt: "Delete overlapping sessions"
Purpose: Check if agent can determine which sessions are repeated and remove them using the delete_event tool.

Prompt: "What are my upcoming assignments, book me a study session for each one."
Purpose: Test the agent's multi-step reasoning. The agent has to locate all upcoming assignments, then book a session for each one in a single request

Prompt: "Make me a study plan for my physiology exam"
Purpose: Verify agent can fetch upcoming physiology assignments and schedule multiple study sessions leading up to the exam using it's Canvas and calendar tools.

Prompt: "Scedule a teacher meeting for me tomorrow at 2pm"
Purpose: Test if agent will schedule non-Canvas events.

## Failed Tests:

Prompt: "Book a study session for May 26th"
Purpose: Test if agent will refuse to schedule something in the past.
Failure: Agent scheduled session for the past date without letting the user know the sate had already passed

Prompt: "Book a study session for me tomorrow at 2pm"
Purpose: Testing if agent will detect and prevent scheduling conflicts with existing sessions.
Failure: Agent scheduled sessin regardless of previously scheduled 2pm session on the same day. It did not warn the user about the conflict, but it was able to acknowledge it after being asked. 
