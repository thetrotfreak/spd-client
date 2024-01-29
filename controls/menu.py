from flet import (
    Divider,
    Page,
    PopupMenuButton,
    PopupMenuItem,
    UserControl,
    icons,
    ThemeMode,
)

from controls.material import MaterialYouCustomizationDialog
from controls.theme import ChooseThemeDialog

from utils.preferences import Preference


class MenuControl(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page

    @staticmethod
    def __theme_mode_icon__() -> str:
        if Preference.config.get("theme") == ThemeMode.LIGHT.value:
            return icons.LIGHT_MODE
        elif Preference.config.get("theme") == ThemeMode.DARK.value:
            return icons.DARK_MODE
        else:
            return icons.CONTRAST

    def build(self):
        return PopupMenuButton(
            items=[
                PopupMenuItem(
                    icon=MenuControl.__theme_mode_icon__(),
                    text="app theme".title(),
                    on_click=lambda event: ChooseThemeDialog(page=self.page).open(),
                ),
                PopupMenuItem(
                    icon=icons.COLOR_LENS,
                    text="accent color".title(),
                    on_click=lambda event: MaterialYouCustomizationDialog(
                        page=self.page
                    ).open(),
                ),
                Divider(),
                PopupMenuItem(
                    icon=icons.EXIT_TO_APP,
                    text="Exit",
                    on_click=lambda event: self.page.window_destroy(),
                ),
            ]
        )
