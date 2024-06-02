from typing import Optional

from flet import (
    CircleAvatar,
    Column,
    Container,
    CrossAxisAlignment,
    MainAxisAlignment,
    Row,
    Text,
    TextOverflow,
    border_radius,
    colors,
    padding,
)

from utils import Preference


class Message:
    def __init__(
        self,
        author: Optional[str] = None,
        body: Optional[str] = None,
        match_accent: bool = False,
    ):
        self.author = author if author is not None else "You"
        self.author_initial = "".join(
            map(lambda x: x[0].title(), self.author.split(maxsplit=2))
        )
        self.body = body
        self.accent = match_accent

    def avatar(self):
        """
        Return avatar's background color

        :param self.match_accent decides whether to match Page accent or a randomly choosen color
        """
        if self.accent:
            return Preference.COLORS[hash(self.author) % len(Preference.COLORS)]
        else:
            return colors.PRIMARY_CONTAINER


class MessageControl(Row):
    """
    Formatted messages
    """

    def __init__(self, message: Message):
        super().__init__()
        self.message = message
        self.vertical_alignment = CrossAxisAlignment.START
        self.expand = True
        self.expand_loose = True

    def build(self):
        self.controls = [
            CircleAvatar(
                content=Text(
                    value=self.message.author_initial,
                ),
                bgcolor=self.message.avatar(),
                tooltip=self.message.author,
            ),
            Column(
                controls=[
                    Text(
                        value=self.message.author,
                        weight="bold",
                    ),
                    Container(
                        content=Text(
                            value=self.message.body,
                            no_wrap=False,
                            max_lines=4,
                            overflow=TextOverflow.FADE,
                        ),
                        border=None,
                        border_radius=border_radius.only(
                            top_left=0,
                            top_right=25,
                            bottom_left=25,
                            bottom_right=25,
                        ),
                        bgcolor=colors.SECONDARY_CONTAINER,
                        padding=padding.symmetric(8, 12),
                        expand=True,
                        expand_loose=True,
                    ),
                ],
                spacing=4,
                alignment=MainAxisAlignment.START,
                expand=True,
                expand_loose=True,
            ),
        ]
