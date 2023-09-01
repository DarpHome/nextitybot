import nextcord
from nextcord.ext import commands
from ..core import NextityBot
from typing import Optional

class UserButton(nextcord.ui.Button):
    def __init__(
        self,
        response: str,
        style: nextcord.ButtonStyle,
        emoji: Optional[str] = None,
        label: Optional[str] = None,
    ) -> None:
        super().__init__(
            style=style,
            emoji=emoji,
            label=label,
        )
        self.response = response

    async def callback(self, inter: nextcord.Interaction) -> None:
        await inter.response.send_message(
            content=self.response,
            ephemeral=True,
        )


class UserButtonView(nextcord.ui.View):
    def __init__(
        self,
        response: str,
        style: nextcord.ButtonStyle,
        emoji: Optional[str] = None,
        label: Optional[str] = None,
    ) -> None:
        super().__init__(timeout=None, auto_defer=False)
        self.add_item(UserButton(
            response=response,
            style=style,
            emoji=emoji,
            label=label,
        ))


class UserButtonLinkView(nextcord.ui.View):
    def __init__(
        self,
        url: str,
        emoji: Optional[str] = None,
        label: Optional[str] = None,
    ) -> None:
        super().__init__(timeout=None, auto_defer=False)
        self.add_item(nextcord.ui.Button(
            style=nextcord.ButtonStyle.link,
            url=url,
            emoji=emoji,
            label=label,
        ))


class UserButtonsCog(commands.Cog):
    def __init__(self, bot: NextityBot) -> None:
        self.bot = bot

    @nextcord.slash_command(
        name="button",
        description="Create button",
    )
    async def button(
        self,
        inter: nextcord.Interaction,
        note: str = nextcord.SlashOption(
            name="note",
            description="Note to include in message with button",
            required=False,
            default="Not specified",
        ),
        style: int = nextcord.SlashOption(
            name="style",
            description="Button style",
            choices={
                "Primary": nextcord.ButtonStyle.primary.value,
                "Secondary": nextcord.ButtonStyle.secondary.value,
                "Success": nextcord.ButtonStyle.success.value,
                "Danger": nextcord.ButtonStyle.danger.value,
            },
            required=False,
            default=nextcord.ButtonStyle.secondary,
        ),
        emoji: str = nextcord.SlashOption(
            name="emoji",
            description="Emoji used in button",
            required=False,
            default=None,
        ),
        label: str = nextcord.SlashOption(
            name="label",
            description="Label used in button",
            required=False,
            default=None,
        ),
        response: str = nextcord.SlashOption(
            name="response",
            description="Response that sent when clicking the button",
            required=False,
            default=None,
        ),
        url: str = nextcord.SlashOption(
            name="url",
            description="If specified, button will an link",
            required=False,
            default=None,
        ),
    ) -> None:
        if url is not None:
            try:
                await inter.response.send_message(
                    f"Note: {note}",
                    allowed_mentions=nextcord.AllowedMentions.none(),
                    view=UserButtonLinkView(
                        style=nextcord.ButtonStyle.link,
                        label=label,
                        url=url,
                        emoji=emoji,
                    ),
                )
            except Exception as exception:
                await inter.response.send_message(
                    f"Failed to reply with components: {exception.args[0]}",
                    ephemeral=True,
                )
            return
        if response is None:
            await inter.response.send_message(
                "You cannot create button without response!",
                ephemeral=True,
            )
            return
        try:
            await inter.response.send_message(
                f"Note: {note}",
                allowed_mentions=nextcord.AllowedMentions.none(),
                view=UserButtonView(
                    response=response,
                    style=nextcord.ButtonStyle(
                        style,
                    ),
                    emoji=emoji,
                    label=label,
                ),
            )
        except Exception as exception:
           await inter.response.send_message(
                f"Failed to reply with components: {exception.args[0]}",
                ephemeral=True,
            )


def setup(bot: NextityBot) -> None:
    bot.add_cog(UserButtonsCog(bot))
