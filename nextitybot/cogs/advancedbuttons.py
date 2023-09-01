import json
import nextcord
from nextcord.ext import commands
from ..core import NextityBot
from typing import Any, Literal, NotRequired, Optional, TypedDict, cast

ButtonStyle = Literal["primary", "secondary", "success", "danger", "blurple", "grey", "gray", "green", "red"]
class Button(TypedDict):
    action: str
    style: NotRequired[ButtonStyle] = 'secondary'
    label: NotRequired[str]
    emoji: NotRequired[str]
    url: NotRequired[str]

ActionRow = list[Button]

Error = tuple[list[str], str]
def validate_data(data: Any) -> list[Error]:
    if not isinstance(data, list):
        return [(["data"], "expected List[ActionRow]")]
    if len(data) > 5:
        return [(["data"], "limited to 5 rows")]
    errors: list[Error] = []
    styles: list[str] = list(ButtonStyle.__args__)
    for i, row in enumerate(cast(list[Any], data)):
        if not isinstance(row, list):
            errors.append((["data", str(i)]), "expected List[Button]")
            continue
        if len(row) > 5:
            errors.append((["data", str(i)]), "limited to 5 buttons")
        for j, btn in enumerate(cast(list[Any], row[:5])):
            if 'action' not in btn and 'url' not in btn:
                errors.append((["data", str(i), str(j)], "action or url fields are required"))
            if 'action' in btn and not isinstance(btn["action"], str):
                errors.append((["data", str(i), str(j), "action"], "expected String"))
            if 'url' in btn and not isinstance(btn["url"], str):
                errors.append((["data", str(i), str(j), "url"], "expected String"))
            if 'label' not in btn and 'emoji' not in btn:
                errors.append((["data", str(i), str(j)], "label or emoji are required"))
            if 'label' in btn and not isinstance(btn["label"], str):
                errors.append((["data", str(i), str(j), "label"], "expected String"))
            if 'emoji' in btn and not isinstance(btn["emoji"], str):
                errors.append((["data", str(i), str(j), "emoji"], "expected String"))
            if 'style' in btn:
                if not isinstance(btn["style"], str):
                    errors.append((["data", str(i), str(j), "style"], "expected String"))
                elif btn["style"] not in styles:
                    errors.append((["data", str(i), str(j), "style"], f"style should be one of: {', '.join(styles)}"))
    return errors



class AdvancedButton(nextcord.ui.Button):
    payload: Button
    def __init__(
        self,
        payload: Button,
        row: int = 0,
    ) -> None:
        super().__init__(
            style=nextcord.ButtonStyle[payload.get("style", "secondary")],
            label=payload.get("label", None),
            emoji=payload.get("emoji", None),
            row=row,
        )
        self.payload = payload

    async def callback(self, inter: nextcord.Interaction) -> None:
        await inter.response.send_message(self.payload['action'], ephemeral=True)


class AdvancedButtonsView(nextcord.ui.View):
    def __init__(
        self,
        payload: list[ActionRow],
    ) -> None:
        super().__init__(timeout=None, auto_defer=False)
        for i, row in enumerate(payload):
            for btn in row:
                self.add_item(nextcord.ui.Button(
                    emoji=btn.get('emoji', None),
                    label=btn.get('label', None),
                    url=btn["url"],
                ) if "url" in btn else AdvancedButton(btn, i))


class AdvancedButtonsCog(commands.Cog):
    def __init__(self, bot: NextityBot) -> None:
        self.bot = bot

    @nextcord.slash_command(
        name="abutton",
        description="Advanced button",
    )
    async def abutton(
        self,
        inter: nextcord.Interaction,
        data: str = nextcord.SlashOption(
            name="data",
            description="JSON data",
            min_length=1,
            max_length=3000,
            required=True,
        ),
        note: str = nextcord.SlashOption(
            name="note",
            description="Note to include in message with button",
            required=False,
            default="Not specified",
        ),
    ) -> None:
        payload: Optional[Any] = None
        try:
            payload = json.loads(data)
        except Exception as exception:
            await inter.response.send_message(
                f"Invalid JSON: {exception.args[0]}",
                ephemeral=True,
            )
            return
        errors = validate_data(payload)
        if len(errors) != 0:
            DOT: str = '.'
            NL: str = '\n'
            await inter.response.send_message(
                f"Errors in payload:\n{NL.join(map(lambda error: f'{DOT.join(error[0])}: {error[1]}', errors))}",
                ephemeral=True,
            )
            return
        try:
            await inter.response.send_message(
                f"Note: {note}",
                allowed_mentions=nextcord.AllowedMentions.none(),
                view=AdvancedButtonsView(payload),
            )
        except Exception as exception:
           await inter.response.send_message(
                f"Failed to reply with components: {exception.args[0]}",
                ephemeral=True,
            )


def setup(bot: NextityBot) -> None:
    bot.add_cog(AdvancedButtonsCog(bot))
