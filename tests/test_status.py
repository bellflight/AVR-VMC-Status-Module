from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from pytest_mock.plugin import MockerFixture

if TYPE_CHECKING:
    from src.status import StatusModule


@pytest.mark.parametrize("led, color", [(0, 0x000000), (1, 0x00FFFF), (2, 0x6A0DAD)])
def test_light_up(status_module: StatusModule, led: int, color: int) -> None:
    status_module.light_up(led, color)
    status_module.pixels.__setitem__.assert_called_with(led, color)
    assert status_module.pixels.show.called


@pytest.mark.parametrize(
    "topic, led, color",
    [
        ("avr/vio/resync", 1, 0x6A0DAD),
        ("avr/pcm/reset", 2, 0x00FFFF),
        ("avr/thermal/reading", 3, 0x001EE3),
        ("avr/fcm", 4, 0xF5A506),
        ("avr/apriltags/selected", 5, 0xC1E300),
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

    for led in range(12):
        status_module.pixels.__setitem__.assert_any_call(led, 0xFF0000)

    assert status_module.pixels.show.called


def test_all_off(status_module: StatusModule) -> None:
    status_module.all_off()

    for led in range(12):
        status_module.pixels.__setitem__.assert_any_call(led, 0x000000)

    assert status_module.pixels.show.called


def test_light_status(status_module: StatusModule) -> None:
    status_module.light_status(None)

    for led in range(12):
        status_module.pixels.__setitem__.assert_any_call(led, 0xFF0000)
        status_module.pixels.__setitem__.assert_any_call(led, 0x00FF00)
        status_module.pixels.__setitem__.assert_any_call(led, 0x0000FF)

    assert status_module.pixels.show.call_count == 36
    status_module.pixels.fill.assert_called_with(0x000000)


@pytest.mark.parametrize("return_value, color", [(b"", 0xFF0000), (b"MAXN", 0x00FF00)])
def test_status_check(
    mocker: MockerFixture, status_module: StatusModule, return_value: bytes, color: int
) -> None:
    status_module.initialized = True

    mocker.patch("subprocess.check_output", return_value=return_value)
    status_module.status_check()
    status_module.pixels.__setitem__.assert_called_with(0, color)
    assert status_module.pixels.show.called
