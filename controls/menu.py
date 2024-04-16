from flet import Divider, PopupMenuButton, PopupMenuItem, Ref, ThemeMode, icons

from controls.material import MaterialYouCustomizationDialog
from controls.theme import ChooseThemeDialog


class MenuControl(PopupMenuButton):
    def __init__(self):
        super().__init__()
        self.__theme_mode_popup_menu_item = Ref[PopupMenuItem]()

    def _theme_mode_icon(self) -> str:
        match ThemeMode(self.page.theme_mode):
            case ThemeMode.LIGHT:
                return icons.LIGHT_MODE
            case ThemeMode.DARK:
                return icons.DARK_MODE
            case ThemeMode.SYSTEM:
                return icons.CONTRAST

    def _callback_theme_mode_icon(self):
        self.__theme_mode_popup_menu_item.current.icon = self._theme_mode_icon()
        self.__theme_mode_popup_menu_item.current.update()

    def build(self):
        self.items = [
            PopupMenuItem(
                ref=self.__theme_mode_popup_menu_item,
                icon=self._theme_mode_icon(),
                text="app theme".title(),
                on_click=lambda _: self.page.show_dialog(
                    dialog=ChooseThemeDialog(
                        on_dismiss=lambda _: self._callback_theme_mode_icon()
                    )
                ),
            ),
            PopupMenuItem(
                icon=icons.COLOR_LENS,
                text="accent color".title(),
                on_click=lambda _: self.page.show_dialog(
                    dialog=MaterialYouCustomizationDialog()
                ),
            ),
            Divider(),
            PopupMenuItem(
                icon=icons.EXIT_TO_APP,
                text="exit".capitalize(),
                on_click=lambda _: self.page.window_destroy(),
            ),
        ]
