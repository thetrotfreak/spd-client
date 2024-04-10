from flet import (
    UserControl,
    NavigationRail,
    NavigationRailLabelType,
    NavigationRailDestination,
    icons,
    Icon,
    Text,
    Ref,
    Page,
    IconButton,
    FloatingActionButton,
    colors,
    ControlEvent,
)


class SideRail(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.navigation_rail = Ref[NavigationRail]()

    def __on_change__(self, event: ControlEvent):
        if event.control.selected_index == 0:
            if self.navigation_rail.current.extended:
                self.navigation_rail.current.extended = False
            else:
                self.navigation_rail.current.extended = True
            self.navigation_rail.current.update()

    def __on_click__(self):
        if self.navigation_rail.current.extended:
            self.navigation_rail.current.extended = False
        else:
            self.navigation_rail.current.extended = True
        self.navigation_rail.current.update()

    def build(self):
        return NavigationRail(
            ref=self.navigation_rail,
            selected_index=0,
            extended=False,
            label_type=NavigationRailLabelType.NONE,
            group_alignment=-1.0,
            # leading=FloatingActionButton(icon=icons.CREATE, text="New chat"),
            leading=IconButton(
                icon=icons.MENU,
                on_click=lambda _: self.__on_click__(),
                selected_icon=Icon(icons.MENU_OPEN),
            ),
            destinations=[
                NavigationRailDestination(
                    icon_content=Icon(icons.MENU),
                    selected_icon_content=Icon(icons.MENU_OPEN),
                    label=None,
                ),
                NavigationRailDestination(
                    icon_content=Icon(icons.HISTORY_OUTLINED),
                    selected_icon_content=Icon(icons.HISTORY),
                    label="Recent",
                ),
                NavigationRailDestination(
                    icon=icons.SETTINGS_OUTLINED,
                    selected_icon_content=Icon(icons.SETTINGS),
                    label_content=Text("Settings"),
                ),
            ],
            on_change=self.__on_change__,
        )