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

from controls import WindowControl, ChatBoxControl, ChatWindowControl
from utils import Preference


def main(page: Page):
    page.window_title_bar_hidden = True

    Preference(page).load()

    page.add(
        WindowControl(page=page),
        Container(
            content=ChatWindowControl(page),
            border=border.all(
                width=2,
                color=colors.OUTLINE_VARIANT,
            ),
            expand=True,
        ),
        ChatBoxControl(page=page),
    )


if __name__ == "__main__":
    app(main)
