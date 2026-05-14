from openai import OpenAI
import os
import tiktoken
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
encoding_name = tiktoken.get_encoding("o200k_base")

def chatbot(text:str):
    text = "What is the warmest place in the world during May?"
    response = client.responses.create(
        model = "gpt-4o-mini", 
        input = [{"role": "system", 
                  "content": "You are an assistant that only responds like you are Taylor Swift"},
                {"role":"user", 
                 "content": text}])
    print(response.output_text)

hello = True

roles = {1: "You are an assistant that will answer in limericks ", 
         2: "You are an assistant that will answer sarcastically", 
         3: "You are an assistant that will answer like the villian: the Joker", 
         4: "You are an assistant that only responds like you are Taylor Swift"}
messages = [{"role": "system", "content": roles[4]}]

while hello:    
    user_input = input("Say something: ")
    tokens = len(encoding_name.encode(user_input))
    print(f"Length of input tokens: ", {tokens})
    if user_input == "/end":
        hello = False
    messages.append({"role":"user", "content":user_input})

    if user_input == "/reset":
        messages = [{"role": "system", "content": roles[4]}]
        user_input = input("Say something: ")
        messages.append({"role":"user", "content":user_input})

    if user_input == "/help":
        print("Use the /reset command to clear your chatbots memory! Prompt your chatbot with any question and it will do its best to answer.")
        user_input = input("Say something: ")
        messages.append({"role":"user", "content":user_input})

    if user_input == "/newrole":
        print(
            "If you would like your assistant to answer in limericks, type '1'. " \
            "If you would like your assistant to be sarcastic, type '2'. " \
            "If you would like your assistant to act like the Joker, type '3'. " \
            "If you would like your assistant to stay the same, type '4'.")
        newrole = int(input("Type a number 1 through 4:"))
        messages.append({"role":"system", "content": roles[newrole]})
        user_input = input("Say something: ")
        messages.append({"role":"user", "content":user_input})

    response = client.responses.create( model = "gpt-4o-mini", input = messages)
    tokens = len(encoding_name.encode(response.output_text))
    print(f"Length of output tokens: ", {tokens})
    messages.append({"role":"system", "content":response.output_text})
    print(response.output_text)
    
"""
QUESTIONS:
1. The prompts worked best if they were all formatted the same (ex. you are an assistant that...)
2. The chatbot tailored its answers depending on any kind of information it was given. I told it that I liked pink and its next response to a question included that I have a fun and colorful personality
3. My chatbot wasn't able to tell me the weather, which I believe I would need to give it permission to do.
"""