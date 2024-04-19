from typing import Any, Callable, Optional

import requests
from flet import (
    AlertDialog,
    ControlEvent,
    FilePicker,
    FilePickerFileType,
    MainAxisAlignment,
    Text,
    TextButton,
)
from flet_core.ref import Ref

from .url import URL, url


class BlobPicker(FilePicker):
    """
    File Picker for JPEG or PDF
    """

    def __init__(
        self,
        on_result=None,
        on_upload=None,
        ref: Ref | None = None,
    ):
        super().__init__(ref=ref)
        self.upload_url = url(URL.UPLOAD)
        self.on_result = on_result
        self.on_upload = on_upload

    def _cancel_on_click(self, event: ControlEvent):
        self.not200dialog.open = False
        self.not200dialog.update()

    def _retry_on_click(self, event: ControlEvent):
        self.not200dialog.open = False
        self.not200dialog.update()
        self.upload()

    def build(self):
        self.not200dialog = AlertDialog(
            title=Text("Upload failed"),
            content=Text("Your last file couldn't be uploaded."),
            actions=[
                TextButton("Retry", on_click=self._retry_on_click),
                TextButton("Cancel", on_click=self._cancel_on_click),
            ],
            actions_alignment=MainAxisAlignment.END,
        )

        self.page.overlay.append(self.not200dialog)

    def pick_files(self):
        self.allow_multiple = False
        self.allowed_extensions = ["pdf", "jpg"]
        self.file_type = FilePickerFileType.CUSTOM

        return super().pick_files(
            file_type=self.file_type,
            allowed_extensions=self.allowed_extensions,
            allow_multiple=self.allow_multiple,
        )

    def upload(
        self,
        ok_callback: Optional[Callable[..., Any]] = None,
        err_callback: Optional[Callable[..., Any]] = None,
        animation_callback: Optional[Callable[..., Any]] = None,
    ):
        if self.result.files is not None:
            blob = {}
            for file in self.result.files:
                blob.update({"file": open(file.path, "rb")})

            if animation_callback is not None:
                animation_callback()

            response = requests.post(url=self.upload_url, files=blob)

            if response.status_code == 200:
                if ok_callback:
                    ok_callback(response.content)
            else:
                self.page.show_dialog(dialog=self.not200dialog)
                if err_callback:
                    err_callback()
