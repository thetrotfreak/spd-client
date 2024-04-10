from flet import (
    Container,
    Page,
    app,
    border,
    colors,
    BoxShape,
    border_radius,
    Row,
    VerticalDivider,
    Column,
    MainAxisAlignment,
)

from controls import WindowControl, ChatBoxControl, ChatWindowControl, SideRail
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
