import discord
import yaml
from discord import app_commands, Interaction
from discord._types import ClientT
from discord.app_commands import Command
from discord.state import ConnectionState
from jsonschema.exceptions import ValidationError
from sqlalchemy import select

from src.domain.entity.Config import Config
from src.utils import setup_logging
from . import error, events
from src.commands.order.OrderStatusChange import ChangeStatusButton
from src.data.models import Order
from src.data.utils import get_session
from src.domain.entity.OrderStatus import OrderStatus, next_status

_log = setup_logging(__name__)


class VJNClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

        self.tree.error(error.errors)
        self.config: Config = self.__load_config()

        # add update command

        self.tree.add_command(
            Command(name="update", description="Update commands (Admin only)", callback=self.updateCommands),
            guilds=[discord.Object(id=1033684799912677388)])

    @staticmethod
    def __load_config() -> Config:
        try:

            with open(f"config.yaml", 'r') as raw_file:
                data = yaml.safe_load(raw_file)
            config = Config(**data)

            _log.info(f"Loaded config file")
            return config
        except ValidationError as e:
            _log.error(f"Error while loading config file config.yaml: {e}")

    async def on_ready(self):
        _log.info(f'{self.user} has connected to Discord!')
        # await self.tree.sync()

        commands = await self.tree.fetch_commands()
        _log.info(f"Global commands available: {', '.join([f'{command.name}' for command in commands])}")
        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.playing, name="/order"))

        self.regenerate_payment_views()

    def regenerate_payment_views(self):
        session = get_session()

        orders = session.execute(select(Order).where(Order.status != OrderStatus.RETRIEVED)).scalars().all()
        for order in orders:
            view = discord.ui.View(timeout=None)
            view.add_item(ChangeStatusButton(order.id, next_status(order.status)))
            self.add_view(view)

    async def updateCommands(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        await self.tree.sync()
        # await self.tree.sync(guild=discord.Object(id=1033684799912677388))  # TODO: change ID
        # await self.tree.sync(guild=discord.Object(id=890357045138690108))  # TODO: change ID
        self.config = self.__load_config()

        _log.info(f"Loaded config file")

        await interaction.followup.send("Done updating commands and configuration")

    ############################
    #  Events
    ############################

    # async def on_message(self, message: discord.Message):
    #     _log.debug(f"Event on_message triggered")
    #     await events.on_message(self, message)

    def add_commands(self, commands):
        for command in commands:
            if 'guilds' in command:
                guilds = [discord.Object(id=guild) for guild in command['guilds']]
                self.tree.add_command(command['command'], guilds=guilds)
            else:
                self.tree.add_command(command['command'])


class VJNInteraction(Interaction[VJNClient]):
    def __init__(self, interaction: Interaction, *, data, state: ConnectionState[ClientT]):
        super().__init__(data=data, state=state)
