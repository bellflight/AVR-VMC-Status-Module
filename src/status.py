import itertools
import signal
import subprocess
import time
from typing import Any

import board
import config
import neopixel_spi as neopixel
import paho.mqtt.client as paho_mqtt
from bell.avr.mqtt.module import MQTTModule
from loguru import logger


class StatusModule(MQTTModule):
    def __init__(self):
        super().__init__()

        self.initialized = False

        self.topic_callbacks = {
            "avr/status/led/pcm": self.light_status,
            "avr/status/led/vio": self.light_status,
            "avr/status/led/apriltags": self.light_status,
            "avr/status/led/fcm": self.light_status,
            "avr/status/led/thermal": self.light_status,
        }

        self.subscribe_to_all_topics = True

        self.spi = board.SPI()
        self.pixels = neopixel.NeoPixel_SPI(
            self.spi,
            config.NUM_PIXELS,
            pixel_order=config.PIXEL_ORDER,
            auto_write=False,
        )

        # set up handling for turning off the lights on docker shutdown
        self.run_status_check = True
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

        self.red_status_all()

    def on_message(
        self, client: paho_mqtt.Client, userdata: Any, msg: paho_mqtt.MQTTMessage
    ) -> None:
        # run this function on every message recieved before processing topic map
        self.check_status(msg.topic)
        super().on_message(client, userdata, msg)

    def set_cpu_status(self) -> None:
        # Initialize power mode status
        cmd = ["/app/nvpmodel", "--verbose", "-f", "/app/nvpmodel.conf", "-m", "0"]
        try:
            subprocess.check_call(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            logger.exception(
                f"Command '{e.cmd}' return with error ({e.returncode}): {e.output}"
            )

    def light_up(self, which_one: int, color: int) -> None:
        """
        Set a specific LED to a color
        """
        self.pixels[which_one] = color
        self.pixels.show()

    def check_status(self, topic: str) -> None:
        for key, value in config.STATUS_LOOKUP.items():
            if topic.startswith(key):
                self.light_up(*value)

    def red_status_all(self) -> None:
        """
        Set all LEDs to red
        """
        for i in range(config.NUM_PIXELS):
            self.pixels[i] = config.RGB_COLORS[0]
        self.pixels.show()

    def all_off(self) -> None:
        """
        Turn off all LEDs
        """
        for i in range(config.NUM_PIXELS):
            self.pixels[i] = config.COLOR_BLACK
        self.pixels.show()

    def light_status(self) -> None:
        for color, i in itertools.product(config.RGB_COLORS, range(config.NUM_PIXELS)):
            self.pixels[i] = color
            self.pixels.show()
            time.sleep(config.DELAY)
            self.pixels.fill(config.COLOR_BLACK)

    def status_check(self) -> None:
        if not self.initialized:
            self.set_cpu_status()
            self.initialized = True

        cmd = ["/app/nvpmodel", "-f", "/app/nvpmodel.conf", "-q"]
        try:
            result = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode(
                "utf-8"
            )
            self.pixels[0] = (
                config.RGB_COLORS[1] if "MAXN" in result else config.RGB_COLORS[0]
            )
            self.pixels.show()
        except subprocess.CalledProcessError as e:
            logger.exception(
                f"Command '{e.cmd}' return with error ({e.returncode}): {e.output}"
            )

    def run(self) -> None:
        self.run_non_blocking()

        while self.run_status_check:
            self.status_check()
            time.sleep(1)
        self.all_off()

    def exit_gracefully(self, *args: Any) -> None:
        self.run_status_check = False


if __name__ == "__main__":
    status = StatusModule()
    status.run()
