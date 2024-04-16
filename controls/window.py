from flet import (
    CrossAxisAlignment,
    IconButton,
    MainAxisAlignment,
    Row,
    Text,
    TextThemeStyle,
    WindowDragArea,
    icons,
)

from .menu import MenuControl


class WindowControl(Row):
    def __init__(self, title: str = ""):
        super().__init__()
        self.title = title
        self.vertical_alignment = CrossAxisAlignment.CENTER

    def build(self):
        self.page.title = self.title
        self.controls = [
            Row(
                controls=[
                    Text(
                        value=self.page.title,
                        theme_style=TextThemeStyle.TITLE_MEDIUM,
                    )
                ],
                expand=True,
                alignment=MainAxisAlignment.END,
                vertical_alignment=CrossAxisAlignment.CENTER,
            ),
            Row(
                controls=[
                    WindowDragArea(content=IconButton(icon=icons.DRAG_INDICATOR)),
                    MenuControl(),
                ],
                expand=True,
                alignment=MainAxisAlignment.END,
                vertical_alignment=CrossAxisAlignment.CENTER,
            ),
        ]
