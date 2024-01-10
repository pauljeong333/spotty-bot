HELLO = ["Hi!", "Greetings.", "How do you do?"]
INVALID = 'invalid command, use "!help" for list of commands'
HELP = (
    "Hello and thank you for using Spotty Bot!\n"
    "Here are a list of commands that you can use:\n\n"
    "**!hello** - Say hi!\n"
    "**![s]earch** - Search for your favorite artist\n"
    "**!help** - View all available commands\n"
)


def arg_message(command: str):
    return (
        f"Please provide an argument with the !{command} command.\n"
        f"ex. !{command} Ariana Grande"
    )
