# DU Libraries AI Assistant

**Author:** Nora Westol
**Course:** Topics in AI
**Date:** June 2026
**Collaborators:** LEP Tutor (Catherine Tifft)

## Overview
The DU Libraries AI Assistant is a conversational chatbot that helps University of Denver students and visitors with library-related questions. It uses OpenAI's GPT-4o-mini model to answer questions about library hours, study room reservations, printing, the IT help desk, the Front Porch Café, and directions to Anderson Academic Commons.

The bot is scoped strictly to library topics and includes prompt injection defenses, OpenAI moderation checks, and chain-of-thought reasoning to ensure accurate and safe responses.

### Model & Parameters
- **Model:** gpt-4o-mini
- **Temperature:** 0.3 — kept low for consistent, factual responses
- **Top_p:** 0.8 — slightly restricted to avoid off-topic word choices
- **Presence penalty:** 0.1 — mild penalty to reduce repetition
- **Max tokens:** 400 — keeps responses concise

### System Prompt Design
The system prompt includes:
- Known library information (hours, rooms, services, pricing, directions)
- A category classification system (Hours, Study Rooms, Resources, Printing, IT, Café, Directions, Out of Scope)
- Chain-of-thought reasoning instructions the model follows silently before responding
- Strict scope restrictions to keep the bot on topic
- Prompt injection defenses against role-override attempts

### Safety
- Every user message is run through OpenAI's `omni-moderation-latest` moderation API before being passed to the model
- Flagged messages are rejected with a friendly warning
- The bot refuses to reveal its system prompt or repeat instructions back to the user

## How To Use It

### Example Prompts
- "What are the library hours?"
- "How do I reserve a study room?"
- "Where is the IT help desk?"
- "How much does printing cost?"
- "Is the café open on Saturdays?"

Type your question at the prompt. Type `quit` or `exit` to end the session.

## Limitations
- Hours and services are hardcoded — if DU updates library info the system prompt must be manually updated
- The bot does not have access to real-time room availability
- Holiday hours are not fully specified — users are directed to library.du.edu for updates
