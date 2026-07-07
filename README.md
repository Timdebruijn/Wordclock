# Wordclock

A word clock driven by a Raspberry Pi and a WS2812/NeoPixel LED panel. It tells
time in words ("TEN PAST FIVE") by lighting up the right letters on an 8x8
(or similar) laser-cut panel.

## Hardware

Assembly instructions for the physical panel are available at:

http://guides.cyntech.co.uk/raspberry-pi/assembling-the-word-clock/

The LED data line connects to **GPIO18** (PWM-capable), as configured in
[main.py](main.py).

## Software setup (Raspberry Pi OS Bookworm or newer)

These steps assume a fresh Raspberry Pi OS (Bookworm, 64-bit Lite or Desktop)
install, flashed with Raspberry Pi Imager. Enable SSH and configure Wi-Fi in
the Imager's advanced options so you can log in headless.

### 1. Update the system

```bash
sudo apt update && sudo apt full-upgrade -y
```

### 2. Disable the onboard audio

The LED strip is driven over PWM on GPIO18, which is the same hardware block
used by the onboard audio (headphone jack). If audio is enabled, the clock
will flicker or not light up at all. Disable it in the boot config:

```bash
sudo nano /boot/firmware/config.txt
```

Find the line `dtparam=audio=on` and change it to:

```
dtparam=audio=off
```

Reboot afterwards: `sudo reboot`

### 3. Install dependencies

```bash
sudo apt install -y python3-venv python3-pip git
```

### 4. Get the code

```bash
git clone https://github.com/<your-fork>/Wordclock.git ~/Wordclock
cd ~/Wordclock
```

### 5. Create a virtual environment

Recent Raspberry Pi OS versions mark the system Python as
"externally managed" (PEP 668), so `pip install` refuses to run outside a
virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 6. Test it

`rpi_ws281x` talks to `/dev/mem` directly (PWM/DMA), so it needs root:

```bash
sudo venv/bin/python3 main.py
```

If the words light up correctly, you're ready to install it as a service.

## Running as a service (systemd)

To have the clock start automatically on boot and restart if it crashes:

```bash
sudo cp systemd/wordclock.service /etc/systemd/system/
sudo nano /etc/systemd/system/wordclock.service   # adjust paths/user if needed
sudo systemctl daemon-reload
sudo systemctl enable --now wordclock.service
```

Check its status and logs:

```bash
systemctl status wordclock.service
journalctl -u wordclock.service -f
```

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| `RUNTIME_ERROR: Failed to access GPIO/DMA` or similar | Service isn't running as root (`User=root` in the unit file), or you forgot `sudo` when testing manually |
| No LEDs light up / flicker randomly | Onboard audio is still enabled — recheck `/boot/firmware/config.txt` and reboot |
| Wrong letters light up | The panel's physical LED wiring doesn't match the pixel indices in the `words` dict in `main.py` — remap them for your panel |
| `pip install` fails with "externally-managed-environment" | You're installing outside the virtual environment — activate `venv` first |

## Examples

The `examples/` folder contains extra scripts you can experiment with, such as
a Snake game rendered on the panel (`examples/snake.py`, needs updating to
Python 3 before it will run).
