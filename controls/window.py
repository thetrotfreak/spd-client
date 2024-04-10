from flet import (
    CrossAxisAlignment,
    IconButton,
    MainAxisAlignment,
    Page,
    Row,
    Text,
    TextThemeStyle,
    UserControl,
    WindowDragArea,
    icons,
)

from .menu import MenuControl


class WindowControl(UserControl):
    def __init__(self, page: Page, title: str = ""):
        super().__init__()
        self.page = page
        self.page.title = title

    def build(self):
        # return Row(
        #     controls=[
        #         WindowDragArea(content=IconButton(icon=icons.DRAG_INDICATOR)),
        #         MenuControl(page=self.page),
        #     ],
        #     expand=True,
        #     alignment=MainAxisAlignment.END,
        #     vertical_alignment=CrossAxisAlignment.CENTER,
        # )
        return Row(
            controls=[
                Row(
                    controls=[
                        Text(
                            value=self.page.title,
                            theme_style=TextThemeStyle.TITLE_LARGE,
                        )
                    ]
                ),
                Row(
                    controls=[
                        WindowDragArea(content=IconButton(icon=icons.DRAG_INDICATOR)),
                        MenuControl(page=self.page),
                    ],
                    alignment=MainAxisAlignment.END,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                ),
            ],
            expand=True,
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=CrossAxisAlignment.CENTER,
        )
