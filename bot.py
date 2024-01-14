import typing
from discord import Client, Message, Intents, Interaction, app_commands
from discord.ext import commands
import responses
import os
from typing import Final
from dotenv import load_dotenv
from spotify import get_token
from statics import HELLO_DESC, HELP_DESC, SEARCH_DESC, GENRES_LIST, REC_DESC


# this function begins running the Spotify bot and handles all bot events
def run_disc_bot():
    # retrieve env variables
    load_dotenv()
    D_TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
    CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

    # get Spotify access token
    S_TOKEN = get_token(CLIENT_ID, CLIENT_SECRET)

    intents = Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix="/", intents=intents)

    @bot.event
    async def on_ready():
        print(f"{bot.user} is now running")
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)

    # @bot.event
    # async def on_message(message: Message):
    #     # prevent infinite loop
    #     if message.author == bot.user:
    #         return

    #     username = str(message.author)
    #     user_message = str(message.content)
    #     channel = str(message.channel)
    #     print(f"[{channel}] {username}: {user_message}")

    #     # don't respond if first token does not start with !
    #     message_tokens = user_message.lower().split(" ", 1)
    #     if not message_tokens or not message_tokens[0].startswith("!"):
    #         return

    #     await send_message(message, message_tokens, S_TOKEN, is_private=False)

    @bot.tree.command(name="hello", description=HELLO_DESC)
    async def hello(interaction: Interaction):
        response = responses.handle_response(["hello"], S_TOKEN)
        await interaction.response.send_message(response)

    @bot.tree.command(name="search", description=SEARCH_DESC)
    @app_commands.describe(search_query="Artist to search for")
    async def search(interaction: Interaction, search_query: str):
        response = responses.handle_response(["search", search_query], S_TOKEN)
        await interaction.response.send_message(response)

    @bot.tree.command(name="help", description=HELP_DESC)
    async def bot_help(interaction: Interaction):
        response = responses.handle_response(["help"], S_TOKEN)
        await interaction.response.send_message(response)

    @bot.tree.command(name="rec", description=REC_DESC)
    @app_commands.describe(genre="Genre that you like!")
    @app_commands.describe(artist="Artist that you like!")
    @app_commands.describe(track="Track that you like")
    async def recommendation(
        interaction: Interaction, genre: str, artist: str, track: str
    ):
        response = responses.handle_response(["rec", genre, artist, track], S_TOKEN)
        await interaction.response.send_message(response)

    @recommendation.autocomplete("genre")
    async def genre_autocompletion(
        interaction: Interaction, current: str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        for genre in GENRES_LIST:
            if current.lower() in genre:
                data.append(app_commands.Choice(name=genre, value=genre))
        return data

    @bot.event
    async def on_command_error(ctx, error):
        pass

    bot.run(D_TOKEN)


# handles where the message should be sent
# async def send_message(
#     message: Message, user_message: str, spotify_token: str, is_private: bool
# ):
#     try:
#         response = responses.handle_response(user_message, spotify_token)
#         # with open("downloaded_image.jpg", "wb") as f:
#         #     f.write(image)
#         await message.author.send(
#             response
#         ) if is_private else await message.channel.send(response)
#     except Exception as e:
#         print(e)
