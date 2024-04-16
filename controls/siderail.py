from flet import (
    ControlEvent,
    Icon,
    NavigationRail,
    NavigationRailDestination,
    NavigationRailLabelType,
    Text,
    icons,
)


class SideRail(NavigationRail):
    def __init__(self):
        super().__init__()
        self.selected_index = 0
        self.group_alignment = -1.0
        self.extended = False
        self.label_type = NavigationRailLabelType.NONE
        self.on_change = self.__on_change__
        self.destinations = [
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
        ]

    def __on_change__(self, event: ControlEvent):
        if event.control.selected_index == 0:
            if self.extended:
                self.extended = False
            else:
                self.extended = True
            self.update()
