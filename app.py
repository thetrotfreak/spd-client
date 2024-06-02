from typing import Any

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


class Application:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.page.window_title_bar_hidden = True
        Preference(page).load()
        self.page.add(
            WindowControl(title="Oracle"),
            Row(
                controls=[
                    SideRail(),
                    Column(
                        controls=[
                            Container(
                                content=ChatWindowControl(),
                                border=border.all(
                                    width=1.25,
                                    color=colors.OUTLINE_VARIANT,
                                ),
                                expand=True,
                                border_radius=border_radius.all(25),
                            ),
                            ChatBoxControl(),
                        ],
                        expand=True,
                        alignment=MainAxisAlignment.START,
                    ),
                ],
                expand=True,
            ),
        )

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass


if __name__ == "__main__":
    app(Application)
