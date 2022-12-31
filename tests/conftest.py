from __future__ import annotations

import sys
from typing import TYPE_CHECKING

import pytest
from pytest_mock.plugin import MockerFixture

if TYPE_CHECKING:
    from src.status import StatusModule


@pytest.fixture
def status_module(mocker: MockerFixture) -> StatusModule:
    # first, mock the board module
    sys.modules["board"] = mocker.MagicMock()

    # patch the send message function
    sys.path.append("src")
    mocker.patch("src.status.StatusModule.send_message")

    # create module object
    from src.status import StatusModule

    module = StatusModule()

    # mock the neopixels module
    mocker.patch.object(module, "pixels")

    return module
