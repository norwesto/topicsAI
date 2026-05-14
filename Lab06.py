from openai import OpenAI
import os
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

prompt = "Explain recursion to a 12-year old"
response = client.responses.create(
    model = "gpt-4o-mini", 
    input = [{"role": "system", 
                  "content": "You are an assistant"},
                {"role":"user", 
                 "content": prompt}],
                 temperature = 0.2)
print(response.output_text)