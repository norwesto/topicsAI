from ollama import chat

# creates an iterator that will be filled with chunks as they arrive
stream = chat(
    model = 'llama3.2:1b',
    messages = [{'role': 'user', 'content': 'What is the most common injury for female soccer players?'}],
    stream = True, options = {
        "num_predict": 100 }
)

# this won't complete until chat says it's done, so it will keep sending
# chunks for you to display
for chunk in stream:
  print(chunk['message']['content'], end = '', flush = True)

# QUESTIONS
# Q1: Explain what a word vector is in simple terms.
# A1: A word vector, also known as an embedding or token, is a way to represent words in a numerical format that can be used in machine 
# learning algorithms. Think of it like a label for each word. Imagine you have a book with many different authors and their writing 
# styles. Each author has a unique voice, style, and personality. To represent this "voice" mathematically, researchers created a 
# way to assign a numerical value to each word based on its usage in the text. The idea is%

# Q2: How deep is the deepest part of the ocean?
# A2: The deepest part of the ocean is called the Challenger Deep, and it's located in the Mariana Trench in the western Pacific Ocean. It 
# has a depth of approximately 36,000 feet (10,973 meters). To put that in perspective, that's deeper than Mount Everest, the highest 
# mountain on Earth, is tall. The Challenger Deep was first discovered in 1960 by a Swiss engineer and explorer named Jacques Piccard, 
# who led an expedition to the bottom of the trench using a% 

# Q3: How old was the oldest llama to ever live?
# A3: I couldn't find any information on an "oldest llama" that holds a record for being the longest-lived. Llamas are known for their 
# longevity, with some individuals reported to have lived up to 20 years or more in captivity. However, one notable llama is Pampa the 
# llama, who was born in 1969 and passed away at the age of 54 in 2023. He holds the Guinness World Record for being the oldest 
# llama to be living on its own when it%  

# Q4: What does .gitignore do?
# A4: `.gitignore` is a file that tells Git, a version control system, what files and directories to ignore when you're working on a 
# project. It's essentially a blacklist of files or directories that shouldn't be tracked by Git. When you add a file or directory to 
# `.gitignore`, it tells Git to exclude that specific item from being tracked in the repository. This means that even if someone else 
# clones your project, they won't see those files unless they explicitly ask for them. `.git%    

# Q5: What is the purpose of a virtual environment?
# A5: The primary purpose of a virtual environment (also known as a virtual setup or sandbox) is to isolate and manage a specific set 
# of dependencies, libraries, and tools within a controlled environment. This allows developers to:
# 1. **Test and develop** software in a separate, isolated space from the production environment, reducing the risk of errors and data corruption.
# 2. **Conduct testing and validation** without affecting the main application or infrastructure.
# 3. **Maintain a consistent set of dependencies** across multiple% 

# Q6: When was the University of Denver founded?
# A6: The University of Denver was founded in 1869. It is a private research university located in Colorado Springs, Colorado.

# Q7: What is the most common injury for female soccer players?
# A7:
