from flet import (
    Container,
    CrossAxisAlignment,
    ListView,
    MainAxisAlignment,
    Page,
    app,
    border,
    colors,
    border_radius,
    Column,
)

from controls import MessageControl, WindowControl, Message, ChatControl
from utils import Preference


def main(page: Page):
    page.window_title_bar_hidden = True
    page.horizontal_alignment = "stretch"
    page.session.set(key="user", value="bivas")

    Preference(page).load()

    page.add(WindowControl(page=page))

    chat = ListView(
        expand=True,
        spacing=12,
        auto_scroll=True,
        padding=12,
    )

    def on_message(message: Message):
        chat.controls.append(
            ChatControl(page=page, message=message),
        )
        page.update()

    page.add(
        Container(
            content=chat,
            border=border.all(
                width=1.25,
                color=colors.OUTLINE_VARIANT,
            ),
            expand=True,
            border_radius=border_radius.all(value=32),
        )
    )
    page.add(MessageControl(page=page))
    page.pubsub.subscribe(on_message)
    page.update()


if __name__ == "__main__":
    app(main)
