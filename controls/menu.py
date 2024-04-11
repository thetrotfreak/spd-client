from flet import (
    Divider,
    Page,
    PopupMenuButton,
    PopupMenuItem,
    Ref,
    ThemeMode,
    UserControl,
    icons,
)

from controls.material import MaterialYouCustomizationDialog
from controls.theme import ChooseThemeDialog
from utils.preferences import Preference


class MenuControl(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.__theme_mode_popup_menu_item = Ref[PopupMenuItem]()

    @staticmethod
    def __theme_mode_icon__() -> str:
        if Preference.config.get("theme") == ThemeMode.LIGHT.value:
            return icons.LIGHT_MODE
        elif Preference.config.get("theme") == ThemeMode.DARK.value:
            return icons.DARK_MODE
        else:
            return icons.CONTRAST

    def __callback_theme_mode_icon__(self) -> None:
        if self.page.theme_mode == ThemeMode.LIGHT.value:
            self.__theme_mode_popup_menu_item.current.icon = icons.LIGHT_MODE
        elif self.page.theme_mode == ThemeMode.DARK.value:
            self.__theme_mode_popup_menu_item.current.icon = icons.DARK_MODE
        else:
            self.__theme_mode_popup_menu_item.current.icon = icons.CONTRAST
        self.__theme_mode_popup_menu_item.current.update()

    def build(self):
        return PopupMenuButton(
            items=[
                PopupMenuItem(
                    ref=self.__theme_mode_popup_menu_item,
                    icon=MenuControl.__theme_mode_icon__(),
                    text="app theme".title(),
                    on_click=lambda _: ChooseThemeDialog(
                        page=self.page, callback=self.__callback_theme_mode_icon__
                    ).open(),
                ),
                PopupMenuItem(
                    icon=icons.COLOR_LENS,
                    text="accent color".title(),
                    on_click=lambda _: MaterialYouCustomizationDialog(
                        page=self.page
                    ).open(),
                ),
                Divider(),
                PopupMenuItem(
                    icon=icons.EXIT_TO_APP,
                    text="Exit",
                    on_click=lambda _: self.page.window_destroy(),
                ),
            ]
        )
