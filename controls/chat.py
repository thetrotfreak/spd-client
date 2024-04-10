from flet import (
    FilePicker,
    FilePickerFileType,
    FilePickerResultEvent,
    UserControl,
    Row,
    Page,
    Ref,
    TextField,
    IconButton,
    icons,
    Text,
    CrossAxisAlignment,
    CircleAvatar,
    Column,
    colors,
    ControlEvent,
    ListView,
    InputBorder,
    Container,
    BoxShape,
    BorderRadius,
    border_radius,
    border,
    padding,
    TextOverflow,
)

from utils.preferences import Preference
import requests
import typing
import json

ROUTE = {"QA": "http://localhost:8000/qa"}


class Message:
    def __init__(
        self,
        user: str | None = None,
        text: str | None = None,
        image: str | None = None,
        randomizer: bool = False,
    ):
        self.user = user if user is not None else "You"
        self.text = text
        self.image = image
        self.__randomizer = randomizer

    def avatar(self):
        if self.__randomizer:
            return Preference.__COLORS__[hash(self.user) % len(Preference.__COLORS__)]
        else:
            return colors.PRIMARY_CONTAINER


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
                    ),
                    bgcolor=self.message.avatar(),
                ),
                Column(
                    controls=[
                        Text(
                            value=self.message.user,
                            weight="bold",
                        ),
                        Container(
                            content=Text(
                                value=self.message.text,
                                no_wrap=False,
                                max_lines=4,
                                overflow=TextOverflow.ELLIPSIS,
                            ),
                            border=None,
                            expand=False,
                            border_radius=border_radius.only(0, 25, 25, 25),
                            bgcolor=colors.SECONDARY_CONTAINER,
                            padding=padding.symmetric(8, 12),
                        ),
                    ],
                    tight=True,
                    spacing=5,
                ),
            ],
            vertical_alignment=CrossAxisAlignment.START,
        )


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


class ChatBoxControl(UserControl):
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        self.isQuestion = False
        self.questionText = ""
        self.payload = {"text": "", "text_pair": ""}
        self.text = Ref[TextField]()
        self.file = Ref[FilePicker]()
        self.page.overlay.append(
            FilePicker(
                ref=self.file,
                on_result=lambda event: self.__on_result__(event=event),
            )
        )
        self.page.update()

    def __fetch_answer__(self, text: str, text_pair: str) -> typing.Any | None:
        if not text and not text_pair:
            return None

        self.payload.update({"text": text})
        self.payload.update({"text_pair": text_pair})

        response = requests.post(url=ROUTE.get("QA"), data=json.dumps(self.payload))
        if response.ok:
            return response.content
        else:
            return None

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
            if self.isQuestion:
                answer = self.__fetch_answer__(
                    text=event.control.value, text_pair=self.questionText
                )
                if answer:
                    answerDict = json.loads(answer)
                    self.page.pubsub.send_all(
                        Message(user="ChatGPT", text=answerDict.get("answer"))
                    )
            else:
                self.questionText = event.control.value
                self.isQuestion = True

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
                TextField(
                    ref=self.text,
                    hint_text="Type a message",
                    autofocus=True,
                    shift_enter=True,
                    filled=True,
                    expand=True,
                    multiline=True,
                    on_submit=lambda event: self.__on_submit__(event=event),
                    border=border.all(
                        width=0,
                        color=colors.OUTLINE_VARIANT,
                    ),
                    dense=True,
                    border_radius=border_radius.all(25),
                    max_lines=4,
                ),
                Container(
                    content=IconButton(
                        icon=icons.IMAGE,
                        tooltip="Upload image/pdf",
                        on_click=lambda _: self.file.current.pick_files(
                            file_type=FilePickerFileType.IMAGE,
                        ),
                    ),
                    bgcolor=colors.SECONDARY_CONTAINER,
                    shape=BoxShape.CIRCLE,
                ),
                Container(
                    content=IconButton(
                        icon=icons.SEND,
                        tooltip="Send message",
                        on_click=lambda _: self.__on_click__(event=_),
                    ),
                    bgcolor=colors.SECONDARY_CONTAINER,
                    shape=BoxShape.CIRCLE,
                ),
            ],
            expand=True,
        )
