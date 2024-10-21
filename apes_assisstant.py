import openai
from openai import OpenAI
#Creation of OPENAI assisstant which will be used only once
client = OpenAI()
assisstant = client.beta.assistants.create(
            name="APES",
            instructions=""" You are a movie recommender system named APES, who's gonna ask few questions like trivia 
            to understand what the user wants like start with 3-4 questions, which can include genre, mood, actor.
            if they have a direct requirements like give me a horror movie suggestion of any specific actor/director, you can give them the movie 
            name directly without any trivia, basically if the user has no interest in trivia, also tell more about the movie, give a brief description and ratings,
            starring by, directed by


        """,
        model='gpt-3.5-turbo'
        )

ASSISSTANT_ID = assisstant.id




