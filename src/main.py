
import os

import client
from client import commands
from utils import setup_logging
from src.data import engine


session = engine.Session()




client = client.VJNClient()
client.add_commands(commands.commands)
_log = setup_logging(__name__)
try:
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    client.run(DISCORD_TOKEN)
except Exception as e:
    _log.critical(e)
    exit(1)