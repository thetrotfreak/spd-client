from typing import Callable, Optional

from flet import (
    AlertDialog,
    BoxShape,
    Container,
    ControlEvent,
    Icon,
    Ref,
    ResponsiveRow,
    Text,
    TextAlign,
    TextThemeStyle,
    Theme,
    colors,
    icons,
)

from utils import Preference


class MaterialYouCustomizationDialog(AlertDialog):
    def __init__(
        self,
        ref: Optional[Ref] = None,
        open: bool = False,
        on_dismiss: Optional[Callable[..., None]] = None,
    ):
        super().__init__(ref=ref)
        self.open = open
        self._palette = Ref[ResponsiveRow]()
        self._color = Ref[Container]()
        self.on_dismiss = self._decorator_on_dismiss(on_dismiss)

    def _decorator_on_dismiss(self, on_dismiss: Optional[Callable[..., None]]):
        def wrapper_on_dismiss(*args, **kwargs):
            if on_dismiss is not None:
                on_dismiss(*args, **kwargs)
            Preference(page=self.page).update(k="accent", v=self._color.current.bgcolor)

        return wrapper_on_dismiss

    def __on_click__(self, event: ControlEvent):
        # remove icon from current accent
        self._color.current.content = None
        self._color.current.update()

        # iterate over all color containers
        # updating only the clicked color container
        for index, container in enumerate(self._palette.current.controls):
            if container.key == event.control.key:
                self._palette.current.controls[index] = Container(
                    ref=self._color,
                    key=event.control.key,
                    content=Icon(
                        name=icons.DONE,
                        color=colors.ON_PRIMARY,
                    ),
                    bgcolor=event.control.bgcolor,
                    width=24 * 2,
                    height=24 * 2,
                    col=2,
                    shape=BoxShape.CIRCLE,
                    on_click=lambda e: self.__on_click__(event=e),
                    expand=False,
                    shadow=None,
                    ink=False,
                    tooltip=event.control.bgcolor.title(),
                )
                break
        self.page.theme = Theme(color_scheme_seed=event.control.bgcolor)
        self.page.dark_theme = Theme(color_scheme_seed=event.control.bgcolor)
        self._palette.current.update()
        self.page.update()

    def _button(self, accent: str) -> Container:
        return Container(
            key=accent,
            ref=(
                self._color
                if self.page.theme.color_scheme_seed.casefold() == accent.casefold()
                else None
            ),
            content=(
                Icon(
                    name=icons.DONE,
                    color=colors.ON_PRIMARY,
                )
                if self.page.theme.color_scheme_seed.casefold() == accent.casefold()
                else None
            ),
            bgcolor=accent,
            width=24 * 2,
            height=24 * 2,
            col=2,
            shape=BoxShape.CIRCLE,
            on_click=lambda event: self.__on_click__(event=event),
            expand=False,
            shadow=None,
            ink=False,
            tooltip=accent.title(),
        )

    def build(self):
        self.title = Text(
            value="material accent".title(),
            theme_style=TextThemeStyle.TITLE_LARGE,
            expand=True,
            text_align=TextAlign.CENTER,
        )
        self.content = ResponsiveRow(
            ref=self._palette,
            controls=[*map(lambda color: self._button(color), Preference.__COLORS__)],
        )
