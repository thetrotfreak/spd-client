from flet import (
    CrossAxisAlignment,
    IconButton,
    MainAxisAlignment,
    Page,
    Row,
    UserControl,
    WindowDragArea,
    icons,
)

from .menu import MenuControl


class WindowControl(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page

    def build(self):
        return Row(
            controls=[
                WindowDragArea(content=IconButton(icon=icons.DRAG_INDICATOR)),
                MenuControl(page=self.page),
            ],
            expand=True,
            alignment=MainAxisAlignment.END,
            vertical_alignment=CrossAxisAlignment.CENTER,
        )
