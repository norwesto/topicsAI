from openai import OpenAI
import os
from pydantic import BaseModel
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
# OpenAI.models.list()
# models = client.models.list()
# for model in models:
#     print(model.id)

# responses = client.responses.create(model = "gpt-4o-mini", input = "what is 2 + 2")
# print(responses.output_text)

# 5.1 DELIMETERS

def delineate(text: str):
    """
    Analyzes whether a given text is happy or sad using ### as delimiters.
    """

    prompt = f"""Tell me if the text between the ### delimiters is happy or sad.
    
    ###
    {text}
    ###
    
    """

    responses = client.responses.create(model = "gpt-4o-mini", input = prompt)
    return responses.output_text


# 5.2 SPECIFYING OUTPUT
class input_analysis(BaseModel):
    author: str
    summarize: str
    tone: str


def specify_amount(text:str):
    """
    Analyzes a piece of text and returns the author, a summary, and the tone.
    """

    responses = client.responses.parse(
        model = "gpt-4o-mini", 
        input = [
            {"role": "system","content": "Tell me the author and tone of the content. Summarize the content"},
            {"role":"user",
             "content": text}
             ],
             text_format=input_analysis
        )
    return responses.output_parsed


# 5.3 CHECKING INPUT

def check_input(text: str):
    """
    Summarizes a Harry Potter book given its title. If the input is not a 
    valid Harry Potter book title, returns an error message instead.
    """

    prompt = f"""Summarize the Harry Potter book based on its title between the ### delimiters.
    ###
    {text}
    ###
    
    If it is not a Harry Potter book title, just say \"this is not a Harry Potter book\"."""

    responses = client.responses.create(model = "gpt-4o-mini", input = prompt)
    return responses.output_text


# 5.4 FEW SHOT PROMPTING

def few_shot_prompting(text:str):
    """
    Answers a computer science student's question by following the pattern 
    of a provided example Q&A using few-shot prompting.
    """
    prompt = f"""I am a computer science student in college. Below is an example Q&A
that my teacher has provided. Follow the pattern and answer the new
student's question from the text between the ### delineators.
Q1: What is a variable in programming?
A1: A variable in programming is a storage location paired with an
associated symbolic name, which contains some known or unknown quantity of
information referred to as a value.
    
    ###
    {text}
    ###
    
    """
    responses = client.responses.create(model = "gpt-4o-mini", input = prompt)
    return responses.output_text

# 5.5 SUMMARIZE
def summarize(reviews: list):
    """
    Summarizes a list of reviews focusing on food quality, tone, and customer service using ### as delimiters.
    """
    prompt = f"""Summarize the items in the list between the ### delimiters on food quality, tone, and customer service

    ###
    {reviews}
    ###
    
    """
    responses = client.responses.create(model = "gpt-4o-mini", input = prompt)
    return responses.output_text
reviews = [
    """Love love love having a veggie dog option here! It's not a common enough find in the veg/vegan options at restaurants. The bun was fresh and delicious, and I think they use the Field Roast frankfurters, which are my favorite veggie dog on the market. The fries are perfection and the "just a taste" portion size option is BRILLIANT.
    I'm in town from Austin, TX and I am bummed we don't have a place like this there. I will be stopping by before I leave to try their tempeh burger and their tofu Rueben!""",
    """Mediocre at best! I ordered a corn dog, and rather than it being a fresh one, it was just a frozen one warmed up. Extremely tough and dry. Not only was that a failure, my partner also got a hotdog and it was lacking. Rather than spending $33 for two on some terrible hot dogs, go to Sam's club and spend $5 and enjoy a decent hotdog. The only positive here are the French fries, but that's hard to mess up.""",
    """I am big dog fan but this one was NOT IT!!! I have never in my life left a dog unfinished, but tonight was a first. I saw the highlighter green relish and I knew it was over.""",
    """High expectations because it's a cute place. The service was great. The food was not worth it at all. Going to culver's""",
    """The rare instances that I crave a hot dog, I crave it the way I got them in my home town of Chicago. This place has it dialed in!""",
    """A must stop when in Denver being from Chicago originally. Best beef, dogs and fresh cut fries around.""",
    """Came in here for a quick bite. Was in the mood for some chicago hotdogs. Did not disappoint to say the least. Service was quick and ambiance was homey. Food is great. Corn dogs are pretty good too""",
    """After 9 months of not being able to eat hot dogs (due to pregnancy) and we randomly stopped on the way home from the hospital. Great spot and tasty hot dogs and sausages!""",
    """Customer service was great...but the food was not. We got a corn dog and the Chicago dog and they were both pretty basic. The corn dog was not crispy at all and the hotdog had mediocre flavor. The only thing we liked was their fries.""",
    """Just okay. Harley's in Littleton is much better in every possible way. No drink refills is crazy."""]

# 5.6 INFER

class output_style(BaseModel):
    food_sold: str
    product_quality: str
    cities_mentioned: str

def infer(reviews:list):
    """
    Analyzes a list of reviews and infers what food is sold, the overall 
    product quality, and any cities mentioned using a structured output.
    """

    all_text = ""
    for review in reviews:
        all_text += review
        
    responses = client.responses.parse(
        model = "gpt-4o-mini", 
        input = [
            {"role": "system","content": "Analyze the following reviews and return what food is sold, the quality of the products overall, and the cities mentioned in the content."},
            {"role":"user",
             "content": all_text}
             ],
             text_format=output_style
        )
    return responses.output_parsed 

# 5.7 TRANSFORM

def transform(reviews_to_translate:list):
    """
    Takes a list of reviews (some already in foreign languages) and generates 
    an HTML table with columns for source language, English translation, 
    food quality, and customer service.
    """ 
    html_rows = ""
    languages = ["Spanish", "French", "German", "Japanese", "Portuguese", 
                 "Italian", "Dutch", "Korean", "Arabic", "Russian"]
    
    prompt = f"""Create an HTML table from each review in the lst between the ### delimiters. The columns of the table should be the source language, the enlgish translation, the food quality, and the customer service. Make sure you return HTML code
    
    ###
    {reviews_to_translate}
    ###
    
    """

    responses = client.responses.create(model = "gpt-4o-mini", input = prompt)
    return responses.output_text
    
reviews_to_translate = [
    """Love love love having a veggie dog option here! It's not a common enough find in the veg/vegan options at restaurants. The bun was fresh and delicious, and I think they use the Field Roast frankfurters, which are my favorite veggie dog on the market. The fries are perfection and the "just a taste" portion size option is BRILLIANT.
    I'm in town from Austin, TX and I am bummed we don't have a place like this there. I will be stopping by before I leave to try their tempeh burger and their tofu Rueben!""",
    """Mediocre at best! I ordered a corn dog, and rather than it being a fresh one, it was just a frozen one warmed up. Extremely tough and dry. Not only was that a failure, my partner also got a hotdog and it was lacking. Rather than spending $33 for two on some terrible hot dogs, go to Sam's club and spend $5 and enjoy a decent hotdog. The only positive here are the French fries, but that's hard to mess up.""",
    """Sono un grande appassionato di hot dog, ma questo proprio non ci siamo!!! Non ho mai lasciato un hot dog a metà in tutta la mia vita, ma stasera è stata la prima volta. Ho visto quella relish verde fosforescente e ho capito che era finita.""",
    """High expectations because it's a cute place. The service was great. The food was not worth it at all. Going to culver's""",
    """The rare instances that I crave a hot dog, I crave it the way I got them in my home town of Chicago. This place has it dialed in!""",
    """Een absolute aanrader als je in Denver bent — zeker als je oorspronkelijk uit Chicago komt. Het beste rundvlees, de lekkerste hotdogs en de verste friet in de omtrek.""",
    """Came in here for a quick bite. Was in the mood for some chicago hotdogs. Did not disappoint to say the least. Service was quick and ambiance was homey. Food is great. Corn dogs are pretty good too""",
    """After 9 months of not being able to eat hot dogs (due to pregnancy) and we randomly stopped on the way home from the hospital. Great spot and tasty hot dogs and sausages!""",
    """Customer service was great...but the food was not. We got a corn dog and the Chicago dog and they were both pretty basic. The corn dog was not crispy at all and the hotdog had mediocre flavor. The only thing we liked was their fries.""",
    """可もなく不可もなく、といったところ。リトルトンにある「Harley's」の方が、あらゆる面で断然優れています。ドリンクのおかわりができないなんて、正気の沙汰ではありません。"""]

# 5.8 EXPAND

def expand(reviews:list):
    """
    Summarizes a list of reviews on food quality, tone, and customer service, 
    then formats the summary as an email directed to the user
    """
    prompt = f"""Summarize the items in the list between the ### delimiters on food quality, tone, and customer service. Put this information into an email format directed to the user.

    ###
    {reviews}
    ###
    
    """
    responses = client.responses.create(model = "gpt-4o-mini", input = prompt)
    return responses.output_text

def main():

    # delineate
    user_input = "I can't believe how amazing this concert was, best night of my life!"
    print(delineate(user_input))

    # specify amount
    user_input = """Once upon a midnight dreary, while I pondered, weak and weary,
    Over many a quaint and curious volume of forgotten lore—
        While I nodded, nearly napping, suddenly there came a tapping,
    As of some one gently rapping, rapping at my chamber door.
    “’Tis some visitor,” I muttered, “tapping at my chamber door—
                Only this and nothing more.”

        Ah, distinctly I remember it was in the bleak December;
    And each separate dying ember wrought its ghost upon the floor.
        Eagerly I wished the morrow;—vainly I had sought to borrow
        From my books surcease of sorrow—sorrow for the lost Lenore—
    For the rare and radiant maiden whom the angels name Lenore—
                Nameless here for evermore.
                    """
    print(specify_amount(user_input))

    # check input
    user_input = """The Lightning Thief"""
    print(check_input(user_input))

    # few shot prompting
    user_input = """Q2: What is a for loop?"""
    print(few_shot_prompting(user_input))

    # summarize
    print(summarize(reviews))

    # infer
    print(infer(reviews))

    # transform
    print(transform(reviews_to_translate))

    # expand
    print(expand(reviews))

if __name__ == '__main__':
    main()