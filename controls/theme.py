from typing import Callable, Optional

from flet import (
    AlertDialog,
    Column,
    ControlEvent,
    CrossAxisAlignment,
    MainAxisAlignment,
    Radio,
    RadioGroup,
    Ref,
    Text,
    TextAlign,
    TextThemeStyle,
    ThemeMode,
)

from utils import Preference


class ChooseThemeDialog(AlertDialog):
    def __init__(
        self,
        ref: Optional[Ref] = None,
        open: bool = False,
        on_dismiss: Optional[Callable[..., None]] = None,
    ):
        super().__init__(ref=ref)
        self.open = open
        self.on_dismiss = self._decorator_on_dismiss(on_dismiss)

    def _decorator_on_dismiss(self, on_dismiss: Optional[Callable[..., None]]):
        def wrapper_on_dismiss(*args, **kwargs):
            if on_dismiss is not None:
                on_dismiss(*args, **kwargs)
            Preference(page=self.page).update(k="theme", v=self.page.theme_mode)

        return wrapper_on_dismiss

    def __theme_mode__(self, event: ControlEvent):
        self.page.theme_mode = event.control.value
        self.page.update()

    def build(self):
        self.title = Text(
            value="app theme".title(),
            theme_style=TextThemeStyle.TITLE_LARGE,
            expand=True,
            text_align=TextAlign.CENTER,
        )
        self.content = Column(
            controls=[
                RadioGroup(
                    value=self.page.theme_mode,
                    content=Column(
                        controls=[
                            *map(
                                lambda enum: Radio(
                                    value=enum[1].value, label=enum[1].value.title()
                                ),
                                ThemeMode._member_map_.items(),
                            )
                        ]
                    ),
                    on_change=self.__theme_mode__,
                )
            ],
            tight=True,  # Flase sets the Column to expand, causing the AlertDialog to expand too
            alignment=MainAxisAlignment.START,
            horizontal_alignment=CrossAxisAlignment.START,
        )
