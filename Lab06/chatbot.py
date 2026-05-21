from openai import OpenAI
import os
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

prompt = "Write me lines as a shopkeeper selling potions to the player"
response = client.chat.completions.create(
    model = "gpt-4o-mini", 
    messages = [{"role": "system", 
                  "content": "You are an assistant that helps write game NPC dialogue"},
                  {"role":"user", 
                 "content": prompt}],
                 max_completion_tokens = 200,
                 presence_penalty = -1,
                 top_p = 0.6)
print(response.choices[0].message.content)

# question 1: 
# question 2: top p more creative, pond is gone.-2 presence led to ldistraction
# 1:

# formal email generator: Write an email to my boss Kathy about why I missed work today: max= 400, pp = -1, temp = 0.2
   # these parameters were picked to make sure the bot wrote a detailed email that wasn't too long (max = 400 tokens).  The temp = 0.2
   # was selected so the conversation stayed focused, and the prensence penalty was given a lower number because 
   # repetition of words isn't something necessary to moderate in this instance, and words in a real email are likely to be repeated  
# poem assistant - Write me a poem about the sky about to rain: max = 200, pp = 2, top_p = 0.9
   # This poem assistant writes a brief poem. The max tokens at 200 keeps it a normal length for this medium, the presence penalty
   # was set to 2 to encourage new words and creativity, which is also why the top_p was set at 0.9. In total, this bot provides you with 
   # a detailed and interesting poem.
# Game NPC - Write me lines as a shopkeeper selling potions to the player: max = 200, pp = -1, top_p = 0.6
   # As an NPC, the goal wouldn't be to have the player interact with it long, so the max_tokens = 200 keeps the dialogue short
   # which is befitting of an NPC such as this one. The presence penalty was decreased because the shopkeeper likely wouldn't
   # have a very advanced vocabulary, and conversations in real life tend to have repeating words and phrases. Lastly, the top_p was set at 
   # an increased number to encourage the bot to give more creative answers, which helped to establish the world 




























""" TEMP
1: Sure! Imagine you have a big stack of pancakes, and you want to count how many pancakes are in the stack. Instead of counting them one by one, you can use a trick called recursion.

Here’s how it works:

1. **Base Case**: First, you check if the stack is empty. If it is, you know there are 0 pancakes. This is your base case.

2. **Recursive Case**: If there is at least one pancake in the stack, you

_____
2: Sure! Imagine you have a big stack of pancakes, and you want to count how many pancakes are in the stack. Instead of counting them one by one, you can use a clever trick called recursion.

Here’s how it works:

1. **Base Case**: First, you check if there are no pancakes left in the stack. If there are none, you say, "There are 0 pancakes." This is your base case, which stops the counting.

2. **Recursive Step**
---
Sure! Imagine you have a big stack of pancakes, and you want to count how many pancakes are in the stack. Instead of counting them all at once, you can use a simple trick: you take the top pancake off the stack and put it aside, then you count the rest of the pancakes in the stack.

Here’s how it works step by step:

1. **Take one pancake off the top**: You remove the top pancake from the stack.
2. **Count the rest**: Now you look at the remaining pancakes and ask, "How many pancakes are left?"
3. **Repeat**: You keep doing this—taking one pancake off and asking how many are left—until there are no pancakes left in the stack.

When there are no pancakes left, you know that you've reached the end. At this point, you can say that there are zero pancakes. 

Now, as you start putting the pancakes back on the stack, you remember how many you took off. For every pancake you took off, you add one to your count. So if you took off 5 pancakes, you would end up with a total count of 5 when you put them all back.

In programming, recursion is like this process. A function (which is a piece of code that does something) can call itself to solve smaller parts of a problem until it reaches a simple case that it can solve easily. Then, it combines those solutions to get the final answer.

So, just like counting pancakes by taking them off one by one, recursion helps break down big problems into smaller, easier ones!

----
1. **Base Case**: First, you check if there are no pancakes in the stack. If there are no pancakes, you can say, "There are 0 pancakes." This is your base case, and it stops the counting.

2. **Recursive Case**: If there is at least one pancake, you can take one pancake off the top of the stack and say, "Okay, I have one pancake, and now I need to count the rest of the pancakes in the stack." 

Now, you can use the same trick to count the remaining pancakes. You keep doing this: taking one pancake off and counting the rest, until you reach the base case where there are no pancakes left.

So, if you had 5 pancakes, it would look like this:

- You take one off: "1 pancake + count the rest."
- You take another one off: "1 pancake + count the rest."
- You take another one off: "1 pancake + count the rest."
- You take another one off: "1 pancake + count the rest."
- You take the last one off: "1 pancake + count the rest."
- Now there are no pancakes left, so you say, "0 pancakes."

Now you can add them all up: 1 + 1 + 1 + 1 + 1 + 0 = 5 pancakes!

So, recursion is like a way of solving a problem by breaking it down into smaller, simpler versions of the same problem, until you reach a point where you can easily solve it. Just like counting pancakes!

---- 0.9
Sure! Imagine you have a big stack of building blocks, and you want to count how many blocks you have. Instead of counting them one by one, you decide to use a special method called recursion.

Here’s how it works:

1. **Base Case**: First, if you only have one block, you can just say, “I have 1 block.” That's the easiest case.

2. **Break it Down**: Now, if you have more than one block, like 
-----
Sure! Imagine you have a task to complete, like climbing a big staircase. Instead of trying to jump to the top in one go, you can just take it one step at a time. 

Recursion is a bit like that! It’s a way of solving a problem where the solution involves solving smaller versions of the same problem. 

Let’s say you want to find the answer to a question, like how many steps are in that staircase. Instead of counting all the steps at once,

---
Sure! Imagine you have a big box of Lego bricks, and you want to build a huge tower using those bricks. But instead of building the entire tower all at once, you decide to build it in a special way.

First, you say, "To build this big tower, I need to build a smaller tower first." So, you build a small tower. But then you realize, "Oh, to build this smaller tower, I need to build an even smaller one!" So, you keep breaking it down into smaller towers until you finally reach a tower that you can build easily, like a single Lego brick.

Once you build that tiny tower (the single brick), you take that tiny tower and use it to build the small tower. After you finish that, you use the small tower to build the medium tower, and then finally, you use the medium tower to build the big tower.

In programming and math, recursion works in a similar way. It's a method where a function (like a little robot that does tasks) calls itself to solve a problem. Each time it calls itself, it works on a smaller piece of the problem until it reaches the simplest version of that problem, which it can solve easily.

Once it solves the simplest problem, it uses that solution to help solve the next bigger problem, and so on, until it works all the way back up to the original problem. 

So, in short, recursion is like building something big by breaking it down into smaller and smaller parts, until you can easily solve those little parts!

____
Sure! Imagine you have a set of Russian nesting dolls. Each doll can open up to reveal a smaller doll inside it. You keep opening the dolls until you reach the tiniest one that doesn’t open anymore.

Recursion is kind of like that! It’s when a process calls itself to solve a problem by breaking it down into smaller parts. 

Let’s say you want to count how many dolls there are in total. Instead of counting them all at once, you could:

1. Count the biggest doll (1).
2. Open the biggest doll and count the dolls inside it.
3. Repeat this process until you get to the smallest doll.

Each time you open a doll, you're doing the same action but with fewer dolls, just like calling a function in programming that does the same thing over and over with smaller problems.

So, in computer programming, recursion is when a function calls itself to help solve a problem step by step, just like how you keep opening those dolls until you find the last one!


"""
""" TOP P

Sure! Imagine you have a big stack of pancakes, and you want to count how many pancakes are in the stack. Instead of counting them one by one, you can use a clever trick called recursion.

Here’s how it works:

1. **Base Case**: First, you check if there are no pancakes left in the stack. If there are none, you know that the count is 0. This is your base case, which stops the counting.

2. **Recursive Step**:
-----
Sure! Imagine you have a big stack of boxes, and you want to find a special toy that’s hidden inside one of them. Instead of just looking through all the boxes one by one, you can use a special trick called recursion.

Here’s how it works:

1. **Open the top box.** If you find the toy, great! You’re done.
2. **If the box is empty or doesn’t have the toy,** you can look inside that box to see if
____

Sure! Imagine you have a big stack of pancakes, and you want to count how many pancakes are in the stack. Instead of counting them one by one, you can use a special trick called recursion.

Here’s how it works:

1. **Base Case**: First, you check if the stack is empty. If it is, you know there are 0 pancakes. This is your base case, the simplest situation.

2. **Recursive Case**: If there is at least one pancake, you can take the top pancake off the stack and count it as 1. Then, you ask the same question about the smaller stack of pancakes that’s left. So, you say, "How many pancakes are in the smaller stack?"

3. **Putting it Together**: When you get the answer from the smaller stack, you add 1 (for the pancake you took off) to that answer. This way, you keep breaking the problem down into smaller and smaller pieces until you reach the base case.

So, if you have 5 pancakes, it would look like this:

- You take one pancake off (1) and ask, "How many pancakes are in the stack of 4?"
- Then, you take one pancake off that stack (1) and ask, "How many pancakes are in the stack of 3?"
- You keep doing this until you reach the empty stack, which is 0.

Finally, you add all the 1s together: 1 (for the first pancake) + 1 (for the second) + 1 (for the third) + 1 (for the fourth) + 1 (for the fifth) + 0 (for the empty stack) = 5 pancakes!

So, recursion is like solving a big problem by breaking it down into smaller, easier problems until you can solve them. It’s a way to make counting (or many other tasks) easier!
(.venv) norawestol@noras-MacBook-Air-3355 topics % 
----

1. **Base Case**: First, you need to know when to stop counting. If there are no pancakes in the stack (the stack is empty), then you know that the count is 0. This is your base case.

2. **Recursive Step**: Now, if there is at least one pancake in the stack, you can take one pancake off the top and set it aside. Then, you ask yourself, "How many pancakes are left in the stack?" You keep doing this until you reach the base case where there are no pancakes left.

3. **Counting Up**: Each time you take a pancake off, you add 1 to the count of pancakes you took off. When you finally get to the bottom of the stack (where there are no more pancakes), you start adding up all the 1s you counted.

So, in simple terms, recursion is like asking the same question again and again, but with a smaller problem each time, until you reach a point where you can easily answer it. Then, you combine all those answers to get the final result!

In programming, we often use recursion to solve problems by breaking them down into smaller versions of the same problem. Just like counting pancakes, we keep solving smaller parts until we can put everything together!
----

0.9 1 100
Sure! Imagine you have a big stack of books, and you want to count how many books there are. You could take the top book off the stack and say, "Okay, I have one book," and then ask your little brother or sister to count the rest of the books for you.

Now, here’s where recursion comes in: instead of just counting, you can tell your little brother or sister to do the same thing! They would take the top book off their smaller stack and say
----
0.9 -1 100
Sure! Imagine you have a big stack of your favorite building blocks. If you want to count how many blocks are in the stack, you could do it in a fun way using recursion.

Let’s say you have a big stack of blocks. You can count them one by one, but recursion means you can use a shortcut. Here’s how it works:

1. **Base Case**: If your stack is empty, you know there are 0 blocks. This is your stopping point.

2
-----
0.9 -1 500
Sure! Imagine you're at home and you want to clean up your room. You look under your bed and see a bunch of toys. You could just take them all out and clean them up, but instead, you decide to do something different. You pick up one toy, and you realize that it’s actually a box of smaller toys. 

So, instead of cleaning up the room all at once, you do this: 

1. You take the box out and open it. 
2. Inside the box, you find even smaller toys, and you decide to clean up those first. 
3. You pick up a small toy, and find out that it also has smaller toys inside it. 

You keep doing this, opening boxes and cleaning the toys, one by one, until you finally get to the tiniest toy that doesn’t have anything inside it. At that point, you can clean it up and put it away. 

Then, you go back to the small box, clean it up, and put it away. Next, you clean up the larger box, and finally, you can clean up your room. 

In this example, you keep breaking down the task of cleaning your room into smaller tasks until you reach a point where the task is very simple. That’s what recursion is! 

In programming, recursion is a way of solving a problem by having a function call itself to break the problem down into smaller, easier parts. Just like you keep cleaning those toys until everything is neat and tidy, a recursive function keeps calling itself until it gets to the simplest part of the problem. 

So, recursion is like cleaning your room by breaking down tasks into smaller and smaller pieces until everything is done!

----
0.9 1 500

Sure! Imagine you have a big box of LEGO bricks, and you want to build a really tall tower. Instead of building the whole tower at once, you decide to take it step by step.

Here's how you can think about recursion:

1. **Base Case**: First, you need to know when to stop. Let's say you want to build a tower that is 5 blocks high. If you already have 1 block, you can keep going until you reach 5. But if you have 5 blocks, you just stop because your tower is done!

2. **Recursive Step**: Now, let’s say you are trying to figure out how to get to 5 blocks from where you are. You look at your current tower height:
   - If you have 1 block, you can add one more block to it.
   - Then, you check again how many blocks you have now (which would be 2), and repeat the process until you reach 5.

So, each time you add a block, you’re using the same idea over and over again (that’s the "recursion"). You're solving the same problem in smaller steps—until you finally reach your goal of 5 blocks!

In computer programming, recursion works similarly. A function might call itself with a simpler version of the original problem until it gets to a point where it can easily give an answer. Just like you built your tower one block at a time!

"""