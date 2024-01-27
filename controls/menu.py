from flet import Divider, Page, PopupMenuButton, PopupMenuItem, UserControl, icons

from controls.material import MaterialYouCustomizationDialog
from controls.theme import ChooseThemeDialog


class MenuControl(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page

    def build(self):
        return PopupMenuButton(
            items=[
                PopupMenuItem(
                    icon=icons.BRIGHTNESS_4,
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
