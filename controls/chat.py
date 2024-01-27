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
    ControlEvent,
    border_radius,
    Image,
    ImageFit,
)

from utils.preferences import Preference


class Message:
    def __init__(self, user: str, text: str = "", image: str | None = None) -> None:
        self.user = user
        self.text = text
        self.image = image

    def avatar(self):
        return Preference.__COLORS__[hash(self.user) % len(Preference.__COLORS__)]


class ChatControl(UserControl):
    def __init__(self, page: Page, message: Message):
        super().__init__()
        self.page = page
        self.message = message
        print(message.image)

    def build(self):
        return Row(
            controls=[
                CircleAvatar(
                    content=Text(
                        value=self.message.user[0].capitalize(),
                        color=self.message.avatar(),
                    )
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


class MessageControl(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.message = Ref[TextField]()
        self.payload = Ref[FilePicker]()
        self.page.overlay.append(
            FilePicker(
                ref=self.payload,
                on_result=lambda event: self.__on_result__(event=event),
            )
        )
        self.page.update()

    def __on_result__(self, event: FilePickerResultEvent):
        if event.files is not None:
            # self.page.session.set(key=event.files.name, value=event.files.path)
            self.page.pubsub.send_all(
                Message(
                    user=self.page.session.get("user"),
                    text="",
                )
            )
            self.page.update()

    def __on_submit__(self, event: ControlEvent):
        if event.control.value:
            self.page.pubsub.send_all(
                Message(self.page.session.get("user"), event.control.value)
            )
            event.control.value = None
            event.control.focus()
            self.page.update()

    def build(self):
        return Row(
            controls=[
                TextField(
                    ref=self.message,
                    hint_text="Type a message...",
                    autofocus=True,
                    shift_enter=True,
                    filled=True,
                    expand=True,
                    multiline=True,
                    on_submit=lambda event: self.__on_submit__(event=event),
                    border_radius=border_radius.all(value=32),
                ),
                IconButton(
                    icon=icons.IMAGE,
                    tooltip="Upload flowchart",
                    on_click=lambda _: self.payload.current.pick_files(
                        file_type=FilePickerFileType.IMAGE,
                    ),
                ),
                IconButton(icon=icons.SEND, tooltip="Send message"),
            ],
            expand=True,
            alignment=MainAxisAlignment.END,
        )
