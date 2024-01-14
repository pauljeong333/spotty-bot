# Spotty Bot

Hello! Welcome to Spotty Bot, a Discord bot used to discover and listen to music and musical artists. Spotty Bot leverages the Discord and Spotify APIs to help users explore new music while utilizing the Discord Bot medium to provide an interactive, responsive, and enjoyable experience. This program was coded on Python.

## Usage

If you would like to try this code out for yourself, you will need to create an application on the Discord Developer Portal as well as an application on Spotify for Developers.
I recommend watching [this video](https://www.youtube.com/watch?v=UYJDKSah-Ww) up to the "Imports" section for help regarding setting up the Discord application, and [this video](https://www.youtube.com/watch?v=WAmEZBEeNmg) up to the "How does Authorization Work?" for help regarding setting up the Spotify Application.

Once finished, you will also need to create a .env file in addition to the provided files. The .env file should contain the following variables:

**DISCORD_TOKEN** - the token of your Discord bot

**SPOTIFY_CLIENT_ID** - the client ID of your Spotify for Developers account

**SPOTIFY_SECRET_ID** - the client secret of your Spotify for Developers account

_(All the variable names should be named exactly as stated.)_

The .env file should be placed in the root directory of the project.

## Commands

Here are a list of Spotty Bot slash commands:

**hello** - Say Hi!

**search** - Search for a musical artist. Spotty Bot will provide you with the artist's name, genres, and top 5 songs.

**rec** - Get a recommendation based on a genre, artist, and track. Spotty Bot will provide a track based on your tastes.

**help** - View the list of available commands.
