#!/usr/bin/env python3

# For GPIO Location and Meaning check out:
## https://www.tomshardware.com/reviews/raspberry-pi-gpio-pinout,6122.html

# For info on the scrip check out this video:
## https://youtu.be/X2YH-XyqyXE

from pathlib import Path
from datetime import datetime
from picamera import PiCamera
import RPi.GPIO as GPIO
import pygame
import re
import time
import subprocess


# CONSTANCES
RELAY_PIN = 37
MOTION_PIN = 35
VIDEO_DIR = Path("videos")
AUDIO = Path("zombie_scream.ogg")

# Initialize GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.setup(MOTION_PIN, GPIO.IN)

# Initialize Camera
## Needs to set up Camera with sudo raspi-config => Interface Options => Legacy camera support
## Can confirm it works with raspistill -o test.png or
## raspivid -o test.h264 -t 10000
## converter requires gpc: `sudo apt install gpac python3-picamera -y`(Usage below)
##  MP4Box -add test.h264 test.mp4
camera = PiCamera()
camera.resolution = (1080, 1020)
camera.framerate = 30
if not VIDEO_DIR.exists():
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)


def set_sound(file: Path) -> pygame.mixer.Sound:
    """TODO: Docstring for set_sound.

    Args:
        file (Path): TODO

    Returns: TODO
    """

    pygame.mixer.init()
    sound = pygame.mixer.Sound(file)
    pygame.mixer.Sound.set_volume(sound, 1)
    return sound


def record(camera: PiCamera, file: Path, sleep: float = 2) -> None:
    """record

    Start Recording and have sleep time for initialization

    Args:
        camera (PiCamera): An instance of a PiCamera
        file (Path): A Path to save the recording to
        sleep (float): Time to sleep to allow initalization

    Return: None
    """

    camera.start_recording(file)
    time.sleep(sleep)


def stop_recording(camera: PiCamera, file: Path) -> None:
    """record

    Start Recording and have sleep time for initialization

    Args:
        camera (PiCamera): An instance of a PiCamera
        file (Path): A Path to saved recording

    Return: None
    """

    camera.stop_recording()
    filename_mp4 = re.sub(r"h264", "mp4", file.as_posix())
    subprocess.run(["MP4Box", "-add", file.as_posix(), filename_mp4])


def activate_relay(pin: int, sleep: float = 0.5) -> None:
    """activate_relay

    Activate the Relay pin for the raspberry pi.

    Args:
        pin (int): Pin Number for the relay board
        sleep (float): Time in Seconds to sleep to allow initialization

    Returns: None, activates the relay switch
    """

    GPIO.output(pin, GPIO.HIGH)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(sleep)  # Allow Time for detection
    GPIO.output(pin, GPIO.HIGH)


def main():
    """TODO: Docstring for main.

    Continuously runs and checks motion sensor.
    If activate it will record, play a sound, activate relay, and convert the video recording.

    Returns: None
    """

    audio = set_sound(AUDIO)
    while True:
        motion_detected = GPIO.input(MOTION_PIN)
        if motion_detected:
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"scary_{current_time}.h264"
            file = Path(VIDEO_DIR, filename)
            record(camera, file)
            activate_relay(RELAY_PIN)
            audio.play()
            camera.stop_recording()
        time.sleep(0.5)


if __name__ == "__main__":
    main()
