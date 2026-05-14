Project: Sentiment Analysis
Author: Nora Westol

1) If the LLM is still incorrect, have it explain its decision--do you agree with the analysis?

My LLM was correct in its classification of the tweet

2) Can you write a tweet that is subtly incorrect due to language which your Naive Bayes classifier will mislabel given that it doesn't care about word ordering? Will the LLM classify it correctly?

tweet = "I hate my job, being a popstar is the worst! :)"
My LLM did not classify this correctly, as the intention is sarcasm and the message is actually positive, however the LLM noted that
it was a tweet with negative sentiment.