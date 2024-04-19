import json
from typing import Any, Optional

import requests
from flet import (
    AlertDialog,
    Animation,
    AnimationCurve,
    ControlEvent,
    CrossAxisAlignment,
    FilePickerResultEvent,
    Icon,
    IconButton,
    ListView,
    MainAxisAlignment,
    Ref,
    Row,
    Text,
    TextField,
    VerticalAlignment,
    border_radius,
    colors,
    icons,
)
from speech_recognition import AudioData, Microphone, Recognizer

from .blob import BlobPicker
from .message import Message, MessageControl
from .timer import TimerControl
from .url import URL, url

ROUTE = {"QA": "http://localhost:8000/qa"}


class ChatWindowControl(ListView):
    """
    A scrollable list of chat messages
    """

    def __init__(self, ref: Optional[Ref] = None):
        super().__init__(ref=ref)
        self.expand = True
        self.auto_scroll = True
        self.spacing = 8
        self.padding = 16

    def __subscribe__(self, message: Message):
        self.controls.append(MessageControl(message=message))
        self.update()

    def build(self):
        self.page.pubsub.subscribe(lambda message: self.__subscribe__(message=message))


class ChatBoxControl(Row):
    def __init__(self):
        super().__init__()
        self.isQuestion = False
        self.isListening = False
        self.isBlob = False
        self._stop_background_thread_listener = lambda wait_for_stop=True: None
        self.questionText = ""
        self.payload = {"text": "", "text_pair": ""}
        self.text = Ref[TextField]()
        self.file = Ref[BlobPicker]()
        self.timer = Ref[TimerControl]()
        self.mic = Ref[IconButton]()
        self._text_hint_text = "enter a prompt".capitalize()
        self._mic_hint_text = "listening...".capitalize()
        self.file_preview_dialog = AlertDialog(
            icon=Icon(icons.INSERT_DRIVE_FILE),
            actions=[
                IconButton(
                    icon=icons.SEND, on_click=lambda _: self.__on_send__(blob=True)
                )
            ],
            actions_alignment=MainAxisAlignment.END,
        )
        self.controls = [
            TextField(
                ref=self.text,
                hint_text=self._text_hint_text,
                dense=True,
                filled=True,
                expand=True,
                adaptive=True,
                autofocus=True,
                max_lines=4,
                multiline=True,
                shift_enter=True,
                on_submit=lambda event: self.__on_submit__(event=event),
                border_width=0,
                border_radius=border_radius.all(25),
                suffix=IconButton(
                    icon=icons.SEND,
                    tooltip="send message".capitalize(),
                    on_click=lambda _: self.__on_send__(event=_),
                ),
                text_vertical_align=VerticalAlignment.CENTER,
            ),
            IconButton(
                icon=icons.UPLOAD_FILE,
                tooltip="Upload image/pdf",
                on_click=lambda _: self.file.current.pick_files(),
            ),
            Row(
                controls=[
                    TimerControl(
                        ref=self.timer,
                        color=colors.PRIMARY,
                        visible=False,
                        timeout=30,
                        callback=self.__on_mic_animation__,
                        effect=self.__reset_timer__,
                    ),
                    IconButton(
                        ref=self.mic,
                        icon=icons.MIC,
                        tooltip="live speech".capitalize(),
                        on_click=self.__on_mic__,
                        animate_opacity=Animation(
                            duration=400,
                            curve=AnimationCurve.EASE_IN_OUT,
                        ),
                    ),
                ],
                alignment=MainAxisAlignment.CENTER,
                vertical_alignment=CrossAxisAlignment.CENTER,
            ),
        ]

    def build(self):
        self.page.overlay.append(
            BlobPicker(
                ref=self.file,
                on_result=lambda event: self.__on_result__(event=event),
            )
        )

    def __fetch_answer__(self, text: str, text_pair: str) -> Any | None:
        if not text and not text_pair:
            return None

        self.payload.update({"text": text})
        self.payload.update({"text_pair": text_pair})

        response = requests.post(url=url(URL.BERT), data=json.dumps(self.payload))
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
            self.file_preview_dialog.content = Row(
                controls=[Text(event.files[0].name)],
                alignment=MainAxisAlignment.CENTER,
            )
            self.page.show_dialog(self.file_preview_dialog)

    def ok_callback(self, resp: bytes):
        """
        On a HTTP 200 response for file upload, update the text with the OCR
        """
        resp_dict: dict = json.loads(resp.decode())
        self.page.pubsub.send_all(
            Message(
                author=self.page.session.get("user"),
                body=resp_dict.get("context"),
            )
        )
        self.isQuestion = True
        self.questionText = resp_dict.get("context")

    def err_callback(self):
        """
        Reset internal file picker selection for failed uploads
        """
        # BUG
        # consider this scenario
        # we upload a file too large and the server denies processing
        # this callback is then invoked, setting internal file selection to None
        # but the BlobPicker lets you retry upload, which will fail
        # as internal file selection must not be empty when calling upload()
        self.file.current.result.files = None
        self.file.current.update()

    def animation_callback(self):
        # self.text.current.animate_opacity = animate_opacity = Animation(
        #     duration=4000,
        #     curve=AnimationCurve.EASE_IN_OUT,
        # )
        # self.text.current.update()
        # self.text.current.opacity = 0 if self.text.current.opacity == 1 else 1
        # self.text.current.update()
        return

    def __on_submit__(self, event: ControlEvent):
        self.__nullify_whitespace_text__()
        if event.control.value:
            self.page.pubsub.send_all(
                Message(
                    author=self.page.session.get("user"),
                    body=event.control.value,
                )
            )
            if self.isQuestion:
                answer = self.__fetch_answer__(
                    text=event.control.value, text_pair=self.questionText
                )
                if answer:
                    answerDict = json.loads(answer)
                    self.page.pubsub.send_all(
                        Message(author="Flet", body=answerDict.get("answer"))
                    )
            else:
                self.questionText = event.control.value
                self.isQuestion = True

            event.control.value = None
            event.control.focus()
            self.page.update()

    def __on_send__(self, event: ControlEvent = None, blob: bool = False):
        """
        Sends either textual prompt or File (image/pdf)

        If both are available, prefers File over text

        File will be considered only for context. Prompts can be either questions or context.
        However, when using prompts, only first prompt will be considered for context.
        """
        if self.file.current.result.files:
            self.file_preview_dialog.open = False
            self.file_preview_dialog.update()
            if self.file.current.result.files:
                self.file.current.upload(
                    ok_callback=self.ok_callback, err_callback=self.err_callback
                )
        else:
            self.__nullify_whitespace_text__()
            if self.text.current.value:
                self.page.pubsub.send_all(
                    Message(
                        author=self.page.session.get("user"),
                        body=self.text.current.value,
                    )
                )
                self.text.current.value = None
                self.text.current.focus()
                self.text.current.update()
                self.page.update()

    def _speech_to_text_callback(self, recognizer: Recognizer, audio: AudioData):
        # this will be called from a non-main thread
        # due to Recognizer().listen_in_background()
        try:
            self.text.current.value += recognizer.recognize_whisper(
                audio_data=audio,
                language="english",
                # translate=True,
            )
        except RuntimeError:
            # RuntimeError: The size of tensor a (6) must match the size of tensor b (3) at non-singleton dimension 3
            # whisper\model.py
            pass
        else:
            self.text.current.update()

    def __reset_timer__(self):
        """
        Wrapper around TimerControl's .reset()

        The TimerControl has to be hidden(=True) once timeout is reached
        without calling .reset()

        The Mic icon's opacity must be set to 1 as preempting the TimerControl()
        could leave the opactiy to either 0 or 1
        """

        self.isListening = False
        self.mic.current.opacity = 1
        self.timer.current.visible = False
        self.text.current.hint_text = self._text_hint_text
        self.text.current.update()
        self.timer.current.reset()
        self.mic.current.update()

    async def __on_mic_animation__(self):
        """
        Animate ease-in-out on the mic icon
        """
        self.mic.current.opacity = 0 if self.mic.current.opacity == 1 else 1
        self.mic.current.update()

    def __on_mic__(self, _: ControlEvent):
        """
        Toggle the TimerControl
        """

        if not self.isListening:
            self.isListening = True

            self.text.current.hint_text = self._mic_hint_text
            self.text.current.update()

            self.timer.current.visible = True
            self.timer.current.start()

            # BUG
            # hallucination problem
            # the problem lies within the model
            # check OpenAI's Whipser GitHub Repository or SpeechRecognition's
            microphone = Microphone()
            recognizer = Recognizer()
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source=source, duration=1)

            self._stop_background_thread_listener = recognizer.listen_in_background(
                source=microphone,
                callback=self._speech_to_text_callback,
                # phrase_time_limit=30,
            )
        else:
            # BUG
            # Wait for this thread :param wait_for_stop is True
            # before using the :param effect of TimerControl
            # to update states of ChatBoxControl
            #
            # This will make sure that the UI does not freeze
            # due to many possible background thread
            # still listening for 1/2 seconds (when :param wait_for_stop is False)
            #
            # Also, since :param effect of TimerControl
            # will be called once only after it is no longer ticking
            # it could introduce more delayed wait
            self._stop_background_thread_listener(wait_for_stop=True)
            self.__reset_timer__()
