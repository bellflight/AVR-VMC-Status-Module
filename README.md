# AVR-VMC-Status-Module

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Build Status Module](https://github.com/bellflight/AVR-VMC-Status-Module/actions/workflows/build.yml/badge.svg)](https://github.com/bellflight/AVR-VMC-Status-Module/actions/workflows/build.yml)

The Status module is responsible for consuming status information from the various
other modules and updating the status LEDs connected to the VMC. This also
communicates some with the host Jetson as well to check if it’s being power-limited.

## Color Schema

| Module   | Message Prefix  | LED | Color  |
|----------|-----------------|-----|--------|
| VIO      | "avr/vio"       | 1   | PURPLE |
| PCM      | "avr/pcm"       | 2   | AQUA   |
| Thermal  | "avr/thermal"   | 3   | BLUE   |
| FCC      | "avr/fcm"       | 4   | ORANGE |
| AprilTag | "avr/apriltags" | 5   | YELLOW |

## Development

It's assumed you have a version of Python installed from
[python.org](https://python.org) that is the same or newer as
defined in the [`Dockerfile`](Dockerfile).

First, install [Poetry](https://python-poetry.org/):

```bash
python -m pip install pipx --upgrade
pipx ensurepath
pipx install poetry
# (Optionally) Add pre-commit plugin
poetry self add poetry-pre-commit-plugin
```

Now, you can clone the repo and install dependencies:

```bash
git clone https://github.com/bellflight/AVR-VMC-Status-Module
cd AVR-VMC-Status-Module
poetry install --sync
poetry run pre-commit install --install-hooks
```

Run

```bash
poetry shell
```

to activate the virtual environment.

### Notes

The `nvpmodel` application and `/etc/nvpmodel.conf` file must both be
bind-mounted into the `/app` directory.

Additionally, this container must be run as
[privileged](https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities)
