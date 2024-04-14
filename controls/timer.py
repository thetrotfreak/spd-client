import asyncio
from concurrent.futures import Future
from typing import Any, Callable, Optional

from flet import Page, Text
from flet_core.ref import Ref


class TimerControl(Text):
    """
    A custom control for an async count-up timer
    """

    def __init__(
        self,
        page: Page,
        ref: Optional[Ref] = None,
        timeout: Optional[int] = None,
        color: Optional[str] = None,
        visible: Optional[bool] = None,
        callback: Optional[Callable[..., Any]] = None,
        effect: Optional[Callable[..., Any]] = None,
    ):
        super().__init__(ref=ref, color=color, visible=visible)
        self.page = page
        self._seconds = 0  # seconds counter
        self._frequency = 1  # how frequently we should update, every 1 second
        self._precision = 60  # extract Minute(s) & Second(s)
        self._is_ticking = False  # state of the Timer's Text Value
        self._timeout = timeout  # number of seconds whence to stop, 0 is no timeout
        self._task = (
            None  # task to keep track of _tick launched via self.page.run_task()
        )
        self.callback = callback  # callable during ticking
        self.effect = (
            effect  # callable only once after the timer has timed-out or preempted
        )
        self.reset()

    def _effect_wrapper(self, future: Future[Any]) -> object:
        """
        Internal method will be called after task is completed or cancelled
        """
        if self.effect is not None:
            self.effect()

    def set(self, minutes: int, seconds: int):
        """
        Sets the Timer's Text Value to `minutes:seconds`

        Note this updates the control
        so there is no need for manual update
        """
        self.value = f"{minutes:02d}:{seconds:02d}"
        self.update()

    def reset(self):
        """
        Will always stop the clock and reset it to 0:0
        """
        self._is_ticking = False
        self._seconds = 0
        self.set(0, 0)

    def stop(self):
        """
        Will only ever stop if clock was ever started
        """
        if self._is_ticking:
            self._is_ticking = False

    def start(self):
        """
        Will only ever start if clock ever stopped
        """
        if not self._is_ticking:
            self._is_ticking = True
            if not self._task or self._task.done():
                self._task = self.page.run_task(self._tick)
                self._task.add_done_callback(self._effect_wrapper)

    def toggle(self, should_reset: bool = False):
        """
        Toggle between start() and stop() OR start() and reset()

        toggle() will do either but not both
        If toggle() had started the clock then next toggle() will only stop/reset it
        and vice-versa

        :param should_reset decides whether to call stop() or reset()
        """
        if not self._is_ticking:
            self.start()
        else:
            self.reset() if should_reset else self.stop()

    async def _tick(self):
        """
        Async clock update
        """
        predicate = lambda: (
            self._seconds <= self._timeout and self._is_ticking
            if self._timeout is not None
            else self._is_ticking
        )
        while predicate():
            m, s = divmod(self._seconds, self._precision)
            self.set(minutes=m, seconds=s)
            if self.callback is not None:
                await self.callback()
            await asyncio.sleep(self._frequency)
            self._seconds += 1
