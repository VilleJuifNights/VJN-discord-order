import uuid
from typing import Tuple

import discord
from discord.app_commands import AppCommandError

from src import exceptions
from src.utils import setup_logging

_log = setup_logging(__name__)


def get_error_message(error: AppCommandError) -> Tuple[str, int]:
    match type(error):
        case discord.errors.NotFound:
            return "The interaction was not found", 404
        case discord.errors.Forbidden:
            return "The bot does not have the permission to send messages to this user", 403
        case discord.errors.HTTPException:
            return "An HTTP error occurred", 500
        case discord.errors.InteractionResponded:
            return "The interaction has already been responded to", 400
        case discord.app_commands.CheckFailure:
            return "You are not allowed to use this command", 403
        case discord.app_commands.CommandInvokeError:
            return "An error occurred while invoking the command", 500
        case discord.app_commands.CommandNotFound:
            return "The command was not found", 404
        case _:
            return "Unknown error", 500


async def errors(interaction: discord.Interaction, error: AppCommandError):
    message, code_err = get_error_message(error)
    id_err = uuid.uuid4()
    embed = discord.Embed(title="Error",
                          description=f"**An error occurred:** {message}.\n\nPlease try again later or contact a staff member if the issue persists.",
                          color=discord.Color.red())
    embed.add_field(name="ID Error", value=id_err, inline=False)
    embed.add_field(name="Error code", value=code_err, inline=False)
    embed.set_footer(text="We are sorry for the inconvenience.")
    try:
        await interaction.response.send_message(embed=embed, ephemeral=True)
    except discord.errors.NotFound:  # interaction not found
        try:
            await interaction.user.send(embed=embed)
        except discord.errors.Forbidden:  # user blocked the bot
            _log.error(f"User {interaction.user} blocked the bot, could not send error message")
    except discord.errors.InteractionResponded:  # interaction already responded
        pass
    _log.error(f"Error {id_err}: {message}, {error}")
