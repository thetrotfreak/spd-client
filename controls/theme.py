from typing import Callable

from flet import (
    AlertDialog,
    Column,
    ControlEvent,
    CrossAxisAlignment,
    MainAxisAlignment,
    Page,
    Radio,
    RadioGroup,
    Text,
    TextAlign,
    TextThemeStyle,
    ThemeMode,
    UserControl,
)

from utils import Preference


class ChooseThemeDialog(UserControl):
    def __init__(self, page: Page, callback: Callable[[], None]):
        super().__init__()
        self.pref = Preference(page)
        self.page = page
        self.callback = callback
        self.dialog = AlertDialog(
            title=Text(
                value="app theme".title(),
                theme_style=TextThemeStyle.TITLE_LARGE,
                expand=True,
                text_align=TextAlign.CENTER,
            ),
            content=Column(
                controls=[
                    RadioGroup(
                        value=self.page.theme_mode,
                        content=Column(
                            controls=[
                                *map(
                                    lambda enum: Radio(
                                        value=enum[1].value, label=enum[1].value.title()
                                    ),
                                    ThemeMode._member_map_.items(),
                                )
                            ]
                        ),
                        on_change=self.__theme_mode__,
                    )
                ],
                alignment=MainAxisAlignment.START,
                horizontal_alignment=CrossAxisAlignment.START,
                tight=True,
            ),
        )

    def __theme_mode__(self, event: ControlEvent):
        self.pref.update(k="theme", v=event.control.value)
        self.page.theme_mode = event.control.value
        self.callback()

    def open(self):
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def build(self):
        return self.dialog
