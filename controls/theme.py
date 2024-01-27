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
    TextThemeStyle,
    ThemeMode,
    UserControl,
)

from utils import Preference


class ChooseThemeDialog(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.pref = Preference(page)
        self.page = page
        self.dialog = AlertDialog(
            title=Text(
                value="Choose theme",
                font_family="sans",
                theme_style=TextThemeStyle.TITLE_LARGE,
            ),
            content=Column(
                controls=[
                    RadioGroup(
                        value=self.page.theme_mode,
                        content=Column(
                            controls=[
                                Radio(value=ThemeMode.LIGHT.value, label="Light"),
                                Radio(value=ThemeMode.DARK.value, label="Dark"),
                                Radio(
                                    value=ThemeMode.SYSTEM.value,
                                    label="Follow System",
                                ),
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
        self.page.theme_mode

    def open(self):
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def build(self):
        return self.dialog
