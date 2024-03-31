from flet import (
    AlertDialog,
    ButtonStyle,
    CircleBorder,
    ControlEvent,
    Dropdown,
    ElevatedButton,
    Page,
    Ref,
    ResponsiveRow,
    Text,
    TextThemeStyle,
    UserControl,
    icons,
    IconButton,
)

from utils import Preference


class MaterialYouCustomizationDialog(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.preference = Preference(page)
        self.page = page
        self.dropdown = Ref[Dropdown]()
        self.dialog = AlertDialog(
            title=Text(
                value="material accent".title(),
                theme_style=TextThemeStyle.TITLE_LARGE,
            ),
            content=ResponsiveRow(
                controls=[*map(lambda color: self.button(color), Preference.__COLORS__)]
            ),
        )

    def button(self, color: str) -> IconButton | ElevatedButton:
        if color.casefold() == self.page.theme.color_scheme_seed.casefold():
            return IconButton(
                icon=icons.DONE,
                col=2,
                bgcolor=color,
                style=ButtonStyle(shape=CircleBorder()),
                tooltip=color.title(),
                on_click=lambda event: self.__accent__(event),
            )
        else:
            return ElevatedButton(
                col=2,
                bgcolor=color,
                style=ButtonStyle(shape=CircleBorder()),
                tooltip=color.title(),
                on_click=lambda event: self.__accent__(event),
            )

    def __accent__(self, event: ControlEvent):
        if isinstance(event.control, IconButton):
            pass
        else:
            event.control = IconButton(
                icon=icons.DONE,
                col=2,
                bgcolor=event.control.bgcolor,
                style=ButtonStyle(shape=CircleBorder()),
                tooltip=event.control.bgcolor.title(),
                on_click=lambda event: self.__accent__(event),
            )
            self.preference.update(k="accent", v=event.control.bgcolor)
            event.control.update()
            self.page.update()

    def open(self):
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def build(self):
        return self.dialog
