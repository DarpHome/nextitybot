import aiohttp
import nextcord
from nextcord.ext import commands
from ..core import NextityBot
from ..utils import itoa, atoi
from typing import Callable, Protocol, Optional

class CalculatorAddModal(nextcord.ui.Modal):
    def __init__(self, view: "CalculatorView") -> None:
        super().__init__(title="Add", timeout=None, auto_defer=False)
        self.right_operand = nextcord.ui.TextInput(
            label="Value",
            min_length=1,
            max_length=64,
            placeholder="42",
            required=True,
        )
        self.add_item(self.right_operand)
        self.view = view

    async def callback(self, inter: nextcord.Interaction) -> None:
        try:
            right_operand: int = atoi(self.right_operand.value, radix=self.view.radix, case_sensitive=True)
        except ValueError:
            await inter.send("Invalid number", ephemeral=True)
        else:
            self.view.value = self.view.value + right_operand
            await self.view.update(inter)


class CalculatorSubtractModal(nextcord.ui.Modal):
    def __init__(self, view: "CalculatorView") -> None:
        super().__init__(title="Subtract", timeout=None, auto_defer=False)
        self.right_operand = nextcord.ui.TextInput(
            label="Value",
            min_length=1,
            max_length=64,
            placeholder="42",
            required=True,
        )
        self.add_item(self.right_operand)
        self.view = view

    async def callback(self, inter: nextcord.Interaction) -> None:
        try:
            right_operand: int = atoi(self.right_operand.value, radix=self.view.radix, case_sensitive=True)
        except ValueError:
            await inter.send("Invalid number", ephemeral=True)
        else:
            self.view.value = self.view.value - right_operand
            await self.view.update(inter)


class CalculatorDivideModal(nextcord.ui.Modal):
    def __init__(self, view: "CalculatorView") -> None:
        super().__init__(title="Divide", timeout=None, auto_defer=False)
        self.right_operand = nextcord.ui.TextInput(
            label="Value",
            min_length=1,
            max_length=64,
            placeholder="42",
            required=True,
        )
        self.add_item(self.right_operand)
        self.view = view

    async def callback(self, inter: nextcord.Interaction) -> None:
        try:
            right_operand: int = atoi(self.right_operand.value, radix=self.view.radix, case_sensitive=True)
        except ValueError:
            await inter.send("Invalid number", ephemeral=True)
        else:
            if right_operand == 0:
                await inter.response.send_message("Error: division by zero", ephemeral=True)
                return
            self.view.value = self.view.value // right_operand
            await self.view.update(inter)


class CalculatorMultiplyModal(nextcord.ui.Modal):
    def __init__(self, view: "CalculatorView") -> None:
        super().__init__(title="Multiply", timeout=None, auto_defer=False)
        self.right_operand = nextcord.ui.TextInput(
            label="Value",
            min_length=1,
            max_length=64,
            placeholder="42",
            required=True,
        )
        self.add_item(self.right_operand)
        self.view = view

    async def callback(self, inter: nextcord.Interaction) -> None:
        try:
            right_operand: int = atoi(self.right_operand.value, radix=self.view.radix, case_sensitive=True)
        except ValueError:
            await inter.send("Invalid number", ephemeral=True)
        else:
            self.view.value = self.view.value * right_operand
            await self.view.update(inter)


class CalculatorAssignModal(nextcord.ui.Modal):
    def __init__(self, view: "CalculatorView") -> None:
        super().__init__(title="Assign new value", timeout=None, auto_defer=False)
        self.right_operand = nextcord.ui.TextInput(
            label="Value",
            min_length=1,
            max_length=64,
            placeholder="42",
            required=True,
        )
        self.add_item(self.right_operand)
        self.view = view

    async def callback(self, inter: nextcord.Interaction) -> None:
        try:
            right_operand: int = atoi(self.right_operand.value, radix=self.view.radix, case_sensitive=True)
        except ValueError:
            await inter.send("Invalid number", ephemeral=True)
        else:
            self.view.value = right_operand
            await self.view.update(inter)

class CalculatorBitwiseANDModal(nextcord.ui.Modal):
    def __init__(self, view: "CalculatorView") -> None:
        super().__init__(title="Bitwise AND", timeout=None, auto_defer=False)
        self.right_operand = nextcord.ui.TextInput(
            label="Value",
            min_length=1,
            max_length=64,
            placeholder="42",
            required=True,
        )
        self.add_item(self.right_operand)
        self.view = view

    async def callback(self, inter: nextcord.Interaction) -> None:
        try:
            right_operand: int = atoi(self.right_operand.value, radix=self.view.radix, case_sensitive=True)
        except ValueError:
            await inter.send("Invalid number", ephemeral=True)
        else:
            self.view.value = self.view.value & right_operand
            await self.view.update(inter)


class CalculatorBitwiseORModal(nextcord.ui.Modal):
    def __init__(self, view: "CalculatorView") -> None:
        super().__init__(title="Bitwise OR", timeout=None, auto_defer=False)
        self.right_operand = nextcord.ui.TextInput(
            label="Value",
            min_length=1,
            max_length=64,
            placeholder="42",
            required=True,
        )
        self.add_item(self.right_operand)
        self.view = view

    async def callback(self, inter: nextcord.Interaction) -> None:
        try:
            right_operand: int = atoi(self.right_operand.value, radix=self.view.radix, case_sensitive=True)
        except ValueError:
            await inter.send("Invalid number", ephemeral=True)
        else:
            self.view.value = self.view.value | right_operand
            await self.view.update(inter)


class CalculatorBitwiseXORModal(nextcord.ui.Modal):
    def __init__(self, view: "CalculatorView") -> None:
        super().__init__(title="Bitwise XOR", timeout=None, auto_defer=False)
        self.right_operand = nextcord.ui.TextInput(
            label="Value",
            min_length=1,
            max_length=64,
            placeholder="42",
            required=True,
        )
        self.add_item(self.right_operand)
        self.view = view

    async def callback(self, inter: nextcord.Interaction) -> None:
        try:
            right_operand: int = atoi(self.right_operand.value, radix=self.view.radix, case_sensitive=True)
        except ValueError:
            await inter.send("Invalid number", ephemeral=True)
        else:
            self.view.value = self.view.value ^ right_operand
            await self.view.update(inter)


class CalculatorSetRadixModal(nextcord.ui.Modal):
    def __init__(self, view: "CalculatorView") -> None:
        super().__init__(title="New radix", timeout=None, auto_defer=False)
        self.view = view
        self.radix = nextcord.ui.TextInput(
            label="Radix",
            min_length=1,
            max_length=2,
            default_value=str(view.radix),
            required=True,
        )
        self.add_item(self.radix)

    async def callback(self, inter: nextcord.Interaction) -> None:
        try:
            radix: int = atoi(self.radix.value, radix=10, case_sensitive=True)
        except ValueError:
            await inter.send("Invalid number", ephemeral=True)
        else:
            self.view.radix = radix
            await self.view.update(inter)

def author_only(
    f: Callable[["CalculatorView", nextcord.ui.Button, nextcord.MessageInteraction], None],
) -> Callable[["CalculatorView", nextcord.ui.Button, nextcord.MessageInteraction], None]:
    async def wrapper(self: "CalculatorView", button: nextcord.ui.Button, inter: nextcord.MessageInteraction) -> None:
        if inter.user.id != self.author_id:
            await inter.response.send_message("Thats not your calculator.", ephemeral=True)
            return
        await f(self, button, inter)
    return wrapper


class CalculatorView(nextcord.ui.View):
    message: nextcord.InteractionMessage
    def __init__(self, author_id: int, value: int, radix: int) -> None:
        super().__init__()
        self.author_id = author_id
        self.value = value
        self.radix = radix

    async def update(self, inter: nextcord.MessageInteraction) -> None:
        await inter.response.edit_message(content=itoa(self.value, radix=self.radix))

    @nextcord.ui.button(emoji="➕", style=nextcord.ButtonStyle.primary, row=0)
    @author_only
    async def add(self, _: nextcord.ui.Button, inter: nextcord.MessageInteraction) -> None:
        await inter.response.send_modal(CalculatorAddModal(self))

    @nextcord.ui.button(emoji="➖", style=nextcord.ButtonStyle.primary, row=0)
    @author_only
    async def subtract(self, _: nextcord.ui.Button, inter: nextcord.MessageInteraction) -> None:
        await inter.response.send_modal(CalculatorSubtractModal(self))

    @nextcord.ui.button(emoji="➗", style=nextcord.ButtonStyle.primary, row=0)
    @author_only
    async def divide(self, _: nextcord.ui.Button, inter: nextcord.MessageInteraction) -> None:
        await inter.response.send_modal(CalculatorDivideModal(self))

    @nextcord.ui.button(emoji="✖️", style=nextcord.ButtonStyle.primary, row=0)
    @author_only
    async def multiply(self, _: nextcord.ui.Button, inter: nextcord.MessageInteraction) -> None:
        await inter.response.send_modal(CalculatorMultiplyModal(self))

    @nextcord.ui.button(emoji="🟰", style=nextcord.ButtonStyle.primary, row=0)
    @author_only
    async def assign(self, _: nextcord.ui.Button, inter: nextcord.MessageInteraction) -> None:
        await inter.response.send_modal(CalculatorAssignModal(self))

    @nextcord.ui.button(label="???", style=nextcord.ButtonStyle.secondary, disabled=True, row=1)
    async def reserved1(self, _: nextcord.ui.Button, inter: nextcord.MessageInteraction) -> None:
        ...
    
    @nextcord.ui.button(emoji="⏪", style=nextcord.ButtonStyle.secondary, row=1)
    @author_only
    async def decrement(self, _: nextcord.ui.Button, inter: nextcord.MessageInteraction) -> None:
        self.value -= 1
        await self.update(inter)
        
    @nextcord.ui.button(emoji="*️⃣", style=nextcord.ButtonStyle.secondary, row=1)
    @author_only
    async def negate(self, _: nextcord.ui.Button, inter: nextcord.MessageInteraction) -> None:
        self.value = -self.value
        await self.update(inter)

    @nextcord.ui.button(emoji="⏩", style=nextcord.ButtonStyle.secondary, row=1)
    @author_only
    async def increment(self, _: nextcord.ui.Button, inter: nextcord.MessageInteraction) -> None:
        self.value += 1
        await self.update(inter)

    @nextcord.ui.button(label="???", style=nextcord.ButtonStyle.secondary, disabled=True, row=1)
    @author_only
    async def reserved2(self, _: nextcord.ui.Button, inter: nextcord.MessageInteraction) -> None:
        ...

    @nextcord.ui.button(label="Get radix", style=nextcord.ButtonStyle.danger, row=2)
    async def get_radix(self, _: nextcord.ui.Button, inter: nextcord.MessageInteraction) -> None:
        await inter.response.send_message(
            f"Current radix is: {self.radix} (42 in that radix: {itoa(42, radix=self.radix)})",
            ephemeral=True,
        )

    @nextcord.ui.button(label="AND", style=nextcord.ButtonStyle.danger, row=2)
    @author_only
    async def bitwise_and(self, _: nextcord.ui.Button, inter: nextcord.MessageInteraction) -> None:
        await inter.response.send_modal(CalculatorBitwiseANDModal(self))

    @nextcord.ui.button(label="OR", style=nextcord.ButtonStyle.danger, row=2)
    @author_only
    async def bitwise_or(self, _: nextcord.ui.Button, inter: nextcord.MessageInteraction) -> None:
        await inter.response.send_modal(CalculatorBitwiseORModal(self))

    @nextcord.ui.button(label="XOR", style=nextcord.ButtonStyle.danger, row=2)
    @author_only
    async def bitwise_xor(self, _: nextcord.ui.Button, inter: nextcord.MessageInteraction) -> None:
        await inter.response.send_modal(CalculatorBitwiseXORModal(self))

    @nextcord.ui.button(label="Set radix", style=nextcord.ButtonStyle.danger, row=2)
    @author_only
    async def set_radix(self, _: nextcord.ui.Button, inter: nextcord.MessageInteraction) -> None:
        await inter.response.send_modal(CalculatorSetRadixModal(self))


class CalculatorCog(commands.Cog):
    bot: NextityBot
    def __init__(self, bot: NextityBot) -> None:
        self.bot = bot

    @nextcord.slash_command(
        name="calculator",
        description="Make calculator",
        dm_permission=True,
    )
    async def calculator(
        self,
        inter: nextcord.Interaction,
        value: int = 0,
        radix: int = nextcord.SlashOption(
            name="radix",
            description="Radix used for calculator",
            required=False,
            min_value=2,
            max_value=36,
            default=10,
        ),
    ) -> None:
        await inter.response.send_message(
            itoa(value, radix=radix),
            view=CalculatorView(inter.user.id, value, radix),
        )


def setup(bot: NextityBot) -> None:
    bot.add_cog(CalculatorCog(bot))