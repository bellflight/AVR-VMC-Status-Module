from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from pytest_mock.plugin import MockerFixture

from src import config

if TYPE_CHECKING:
    from src.status import StatusModule


@pytest.mark.parametrize(
    "led, color",
    [(0, config.COLOR_BLACK), (1, config.COLOR_AQUA), (2, config.COLOR_PURPLE)],
)
def test_light_up(status_module: StatusModule, led: int, color: int) -> None:
    status_module.light_up(led, color)
    status_module.pixels.__setitem__.assert_called_with(led, color)
    assert status_module.pixels.show.called


@pytest.mark.parametrize(
    "topic, led, color",
    [
        ("avr/vio/resync", *config.STATUS_LOOKUP["avr/vio"]),
        ("avr/pcm/reset", *config.STATUS_LOOKUP["avr/pcm"]),
        ("avr/thermal/reading", *config.STATUS_LOOKUP["avr/thermal"]),
        ("avr/fcm", *config.STATUS_LOOKUP["avr/fcm"]),
        ("avr/apriltags/selected", *config.STATUS_LOOKUP["avr/apriltags"]),
    ],
)
def test_check_status(
    status_module: StatusModule, topic: str, led: int, color: int
) -> None:
    status_module.check_status(topic)
    status_module.pixels.__setitem__.assert_called_with(led, color)
    assert status_module.pixels.show.called


def test_red_status_all(status_module: StatusModule) -> None:
    status_module.red_status_all()

    for led in range(config.NUM_PIXELS):
        status_module.pixels.__setitem__.assert_any_call(led, config.COLOR_RED)

    assert status_module.pixels.show.called


def test_all_off(status_module: StatusModule) -> None:
    status_module.all_off()

    for led in range(config.NUM_PIXELS):
        status_module.pixels.__setitem__.assert_any_call(led, config.COLOR_BLACK)

    assert status_module.pixels.show.called


def test_light_status(mocker: MockerFixture, status_module: StatusModule) -> None:
    # for speed
    mocker.patch("time.sleep")

    status_module.light_status()

    for led in range(config.NUM_PIXELS):
        status_module.pixels.__setitem__.assert_any_call(led, config.COLOR_RED)
        status_module.pixels.__setitem__.assert_any_call(led, config.COLOR_GREEN)
        status_module.pixels.__setitem__.assert_any_call(led, config.COLOR_BLUE)

    assert status_module.pixels.show.call_count == config.NUM_PIXELS * 3
    status_module.pixels.fill.assert_called_with(config.COLOR_BLACK)


@pytest.mark.parametrize(
    "return_value, color", [(b"", config.COLOR_RED), (b"MAXN", config.COLOR_GREEN)]
)
def test_status_check(
    mocker: MockerFixture, status_module: StatusModule, return_value: bytes, color: int
) -> None:
    status_module.initialized = True

    mocker.patch("subprocess.check_output", return_value=return_value)
    status_module.status_check()
    status_module.pixels.__setitem__.assert_called_with(0, color)
    assert status_module.pixels.show.called
