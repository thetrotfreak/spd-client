from flet import (
    FilePicker,
    FilePickerFileType,
    FilePickerResultEvent,
    FilePickerUploadEvent,
    FilePickerUploadFile,
    UserControl,
    Row,
    Page,
    Ref,
    TextField,
    IconButton,
    Icon,
    icons,
    Text,
    MainAxisAlignment,
    CrossAxisAlignment,
    CircleAvatar,
    Column,
    colors,
    border,
    ControlEvent,
    border_radius,
    Image,
    ImageFit,
    ListView,
    InputBorder,
    Container,
    BoxShape,
    BorderRadius,
)

from utils.preferences import Preference


class Message:
    def __init__(self, user: str, text: str | None = None, image: str | None = None):
        self.user = user if user is not None else "Guest"
        self.text = text
        self.image = image

    def avatar(self):
        return Preference.__COLORS__[hash(self.user) % len(Preference.__COLORS__)]


class ChatWindowControl(UserControl):
    """
    A scrollable list of chat messages
    """

    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.control = Ref[ListView]()
        self.page.pubsub.subscribe(lambda message: self.__subscribe__(message=message))

    def __subscribe__(self, message: Message):
        self.control.current.controls.append(
            MessageControl(page=self.page, message=message)
        )
        self.control.current.update()
        # self.page.update()

    def build(self):
        return ListView(
            ref=self.control,
            expand=True,
            auto_scroll=True,
            spacing=8,
            padding=16,
        )


class MessageControl(UserControl):
    """
    Formatted messages
    """

    def __init__(self, page: Page, message: Message):
        super().__init__()
        self.page = page
        self.message = message

    def build(self):
        return Row(
            controls=[
                CircleAvatar(
                    content=Text(
                        value=self.message.user[0].capitalize(),
                        color=colors.ON_PRIMARY,
                    ),
                    bgcolor=self.message.avatar(),
                ),
                Column(
                    controls=[
                        Text(
                            value=self.message.user,
                            weight="bold",
                        ),
                        Text(value=self.message.text),
                    ],
                    tight=True,
                    spacing=5,
                ),
            ],
            vertical_alignment=CrossAxisAlignment.START,
        )


class ChatBoxControl(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.text = Ref[TextField]()
        self.file = Ref[FilePicker]()
        self.page.overlay.append(
            FilePicker(
                ref=self.file,
                on_result=lambda event: self.__on_result__(event=event),
            )
        )
        self.page.update()

    def __nullify_whitespace_text__(self) -> None:
        """
        Cut extra spaces and check if the text should be sent or not
        """
        self.text.current.value = self.text.current.value.strip()
        self.text.current.update()

    def __on_result__(self, event: FilePickerResultEvent):
        if event.files is not None:
            self.page.pubsub.send_all(
                Message(
                    user=self.page.session.get("user"),
                    text=self.text.current.value,
                )
            )
            self.page.update()

    def __on_submit__(self, event: ControlEvent):
        self.__nullify_whitespace_text__()
        if event.control.value:
            self.page.pubsub.send_all(
                Message(
                    user=self.page.session.get("user"),
                    text=event.control.value,
                )
            )
            event.control.value = None
            event.control.focus()
            self.page.update()

    def __on_click__(self, event: ControlEvent):
        self.__nullify_whitespace_text__()
        if self.text.current.value:
            self.page.pubsub.send_all(
                Message(
                    user=self.page.session.get("user"),
                    text=self.text.current.value,
                )
            )
            self.text.current.value = None
            self.text.current.focus()
            self.text.current.update()
            self.page.update()

    def build(self):
        return Row(
            controls=[
                Container(
                    content=IconButton(
                        icon=icons.IMAGE,
                        tooltip="Upload flowchart",
                        on_click=lambda _: self.file.current.pick_files(
                            file_type=FilePickerFileType.IMAGE,
                        ),
                    ),
                    bgcolor=colors.OUTLINE_VARIANT,
                ),
                TextField(
                    ref=self.text,
                    hint_text="Type a message",
                    autofocus=True,
                    shift_enter=True,
                    filled=True,
                    expand=True,
                    multiline=True,
                    on_submit=lambda event: self.__on_submit__(event=event),
                    border=InputBorder.NONE,
                    dense=True,
                ),
                Container(
                    content=IconButton(
                        icon=icons.SEND,
                        tooltip="Send message",
                        on_click=lambda _: self.__on_click__(event=_),
                    ),
                    bgcolor=colors.OUTLINE_VARIANT,
                ),
            ],
            expand=True,
        )
