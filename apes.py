import discord
from openai import OpenAI
import asyncio
import time
import logging
from apes_assisstant import ASSISSTANT_ID


opclient = OpenAI(
)

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)


Discord_BOT_API_KEY = "MTI5NzEwNTQ5NTQ5NjA2OTE2MQ.G2HGQa.Mn2as2TGwfwDBDZeIVWQkaF3sEq3OrhRh_5FYs"
assisstant_id = ASSISSTANT_ID
thread_id = None

async def get_thread_option():
    global thread_id
    if thread_id:
        return thread_id
    else:
        thread = opclient.beta.threads.create(
            messages=[
                {
                    'role':'user',
                    'content':"Start Conversation"
                }
            ]
        )
        thread_id = thread.id

        return thread_id


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    global thread_id

    if message.author.bot or client.user not in message.mentions:
        return 
    
    user_message = message.content.replace(f"<@{client.user.id}>", "").strip()

    response_message = await message.reply("Typing...")

    thread_id = await get_thread_option()


    prompts = opclient.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content = user_message
    )
    
    #Running Assisstant
    run = opclient.beta.threads.runs.create(
        thread_id = thread_id,
        assistant_id=assisstant_id
    )

    while True:
        try:
            run = opclient.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if run.completed_at:
                messages = opclient.beta.threads.messages.list(
                    thread_id=thread_id
                )
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                await response_message.edit(content = response)
                break
        except Exception as e:
            logging.error(f"Error occured while retreiving the data : {e}")
            break
        await asyncio.sleep(1)

    run_step = opclient.beta.threads.runs.steps.list(
        thread_id=thread_id,
        run_id = run.id
    )

client.run(Discord_BOT_API_KEY)
