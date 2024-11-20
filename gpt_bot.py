import discord
import openai

discord_bot_token = "discord bot token here"
openai_api_key = "openai api key here"
channel_id = "1308389878630711309"

openai.api_key = openai_api_key

history_messages = [{"role": "system", "content": "너는 똑똑한 helper"}]

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
           return  
    
        history_messages.append({"role": "user", "content": message.content})

        try:
            completion = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=history_messages
            )
            answer = completion.choices[0].message['content']
        
            await message.channel.send(answer)

            history_messages.append({"role": "assistant", "content": answer})

        except Exception as e:
            print(f"Error during OpenAI request: {e}")
            await message.channel.send("Something went wrong, please try again later.")

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(discord_bot_token)