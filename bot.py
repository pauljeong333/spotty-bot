from discord import Client, Message, Intents
import responses
import os
from typing import Final
from dotenv import load_dotenv
from spotify import get_token


# this function begins running the Spotify bot and handles all bot events
def run_disc_bot():
    # retrieve env variables
    load_dotenv()
    D_TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
    CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

    # get Spotify access token
    S_TOKEN = get_token(CLIENT_ID, CLIENT_SECRET)

    intents: Intents = Intents.default()
    intents.message_content = True
    client: Client = Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} is now running")

    @client.event
    async def on_message(message: Message):
        # prevent infinite loop
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        print(f"[{channel}] {username}: {user_message}")

        # don't respond if first token does not start with !
        message_tokens = user_message.lower().split(" ", 1)
        if not message_tokens or not message_tokens[0].startswith("!"):
            return

        await send_message(message, message_tokens, S_TOKEN, is_private=False)

    client.run(D_TOKEN)


# handles where the message should be sent
async def send_message(
    message: Message, user_message: str, spotify_token: str, is_private: bool
):
    try:
        response = responses.handle_response(user_message, spotify_token)
        # with open("downloaded_image.jpg", "wb") as f:
        #     f.write(image)
        await message.author.send(
            response
        ) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)
