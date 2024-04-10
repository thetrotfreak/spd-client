from flet import (
    Column,
    Container,
    MainAxisAlignment,
    Page,
    Row,
    app,
    border,
    border_radius,
    colors,
)

from controls import ChatBoxControl, ChatWindowControl, SideRail, WindowControl
from utils import Preference


def main(page: Page):
    page.window_title_bar_hidden = True

    Preference(page).load()

    page.add(
        WindowControl(page=page, title="Flet"),
        Row(
            controls=[
                SideRail(page=page),
                # VerticalDivider(width=1),
                Column(
                    controls=[
                        Container(
                            content=ChatWindowControl(page),
                            border=border.all(
                                width=1.25,
                                color=colors.OUTLINE_VARIANT,
                            ),
                            expand=True,
                            border_radius=border_radius.all(25),
                        ),
                        ChatBoxControl(page=page),
                    ],
                    expand=True,
                    alignment=MainAxisAlignment.START,
                ),
            ],
            expand=True,
        ),
    )


if __name__ == "__main__":
    app(main)
