from flet import (
    AlertDialog,
    BoxShape,
    Container,
    ControlEvent,
    Dropdown,
    Icon,
    Page,
    Ref,
    ResponsiveRow,
    Text,
    TextAlign,
    TextThemeStyle,
    UserControl,
    colors,
    icons,
)

from utils import Preference


class MaterialYouCustomizationDialog(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.preference = Preference(page)
        self.page = page
        self.dropdown = Ref[Dropdown]()
        self._color_clickable = Ref[ResponsiveRow]()
        self._active_container = Ref[Container]()
        self.dialog = AlertDialog(
            title=Text(
                value="material accent".title(),
                theme_style=TextThemeStyle.TITLE_LARGE,
                expand=True,
                text_align=TextAlign.CENTER,
            ),
            content=ResponsiveRow(
                ref=self._color_clickable,
                controls=[
                    *map(lambda color: self.button(color), Preference.__COLORS__)
                ],
            ),
        )

    def __on_click__(self, event: ControlEvent):
        # remove icon from current accent
        self._active_container.current.content = None
        self._active_container.current.update()

        # iterate over all color containers
        # updating only the clicked color container
        for index, container in enumerate(self._color_clickable.current.controls):
            if container.key == event.control.key:
                self._color_clickable.current.controls[index] = Container(
                    ref=self._active_container,
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
        self.preference.update(k="accent", v=event.control.bgcolor)
        self._color_clickable.current.update()
        self.page.update()

    def button(self, color: str) -> Container:
        return Container(
            key=color,
            ref=(
                self._active_container
                if self.page.theme.color_scheme_seed.casefold() == color.casefold()
                else None
            ),
            content=(
                Icon(
                    name=icons.DONE,
                    color=colors.ON_PRIMARY,
                )
                if self.page.theme.color_scheme_seed.casefold() == color.casefold()
                else None
            ),
            bgcolor=color,
            width=24 * 2,
            height=24 * 2,
            col=2,
            shape=BoxShape.CIRCLE,
            on_click=lambda event: self.__on_click__(event=event),
            expand=False,
            shadow=None,
            ink=False,
            tooltip=color.title(),
        )

    def open(self):
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def build(self):
        return self.dialog
