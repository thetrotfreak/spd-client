from flet import (
    CrossAxisAlignment,
    IconButton,
    MainAxisAlignment,
    Page,
    Row,
    UserControl,
    WindowDragArea,
    icons,
    Text,
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
                Row(controls=[Text(self.page.title)]),
                Row(
                    controls=[
                        WindowDragArea(content=IconButton(icon=icons.DRAG_INDICATOR)),
                        MenuControl(page=self.page),
                    ],
                    expand=True,
                    alignment=MainAxisAlignment.END,
                    vertical_alignment=CrossAxisAlignment.CENTER,
                ),
            ],
            alignment=MainAxisAlignment.CENTER,
            vertical_alignment=CrossAxisAlignment.CENTER,
        )
