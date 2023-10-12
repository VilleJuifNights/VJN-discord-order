import datetime

import discord


def urlButton(url: str) -> discord.ui.Button:
    """
    Create a button with a link
    @rtype: object
    @param url: Url of the link
    @return: Button
    """
    return discord.ui.Button(label="Link", style=discord.ButtonStyle.link, url=url)


