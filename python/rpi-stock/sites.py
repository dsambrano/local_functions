#!/usr/bin/env python3

COMPANIES = [
    "microcenter",
    "adafruit",
    "chicago",
    "pishop",
    "cana",
]

SCRAPPERS = ["https://rpilocator.com/?country=US"]

BASE_URL = {
    "microcenter": "https://www.microcenter.com/product/",
    "adafruit": "https://www.adafruit.com/product/",
    "chicago": "https://chicagodist.com/products/",
    "pishop": "https://www.pishop.us/product/",
    "cana": "https://www.canakit.com/",
}

PRODUCTS = {
    "pi 3": {
        "microcenter": "460968/raspberry-pi-3-model-b",
        "adafruit": "3055",
    },
    "pi 4 1GB": {
        "adafruit": "4295",
        "chicago": "craspberry-pi-4-model-b-1gb",
        "pishop": "raspberry-pi-4-model-b-1gb/",
        "cana": "raspberry-pi-4.html",
    },
    "pi 4 2GB": {
        "microcenter": "621439/raspberry-pi-4-model-b-2gb-ddr4",
        "adafruit": "4292",
        "chicago": "craspberry-pi-4-model-b-2gb",
        "pishop": "raspberry-pi-4-model-b-2gb/",
        "cana": "raspberry-pi-4-2gb.html",
    },
    "pi 4 4GB": {
        "adafruit": "4296",
        "chicago": "craspberry-pi-4-model-b-4gb",
        "pishop": "raspberry-pi-4-model-b-4gb/",
        "cana": "raspberry-pi-4-4gb.html",
    },
    "pi Zero": {
        "microcenter": "643085/pizero2w",
        "adafruit": "3400",
    },
    "pi Zero WH": {
        "adafruit": "3708",
    },
    "pi Zero 2W": {
        "microcenter": "643085/pizero2w",
        "adafruit": "3708",
    },
    "pico W": {
        "microcenter": "650108/raspberry-pi-pico-w",
        "adafruit": "5526",
    },
    "pico H": {
        "microcenter": "650107/raspberry-pi-pico-h-raspberry-pi-pico-with-headers-pre-installed",
        "adafruit": "5525",
    },
    "pico WH": {
        "adafruit": "5544",
    },
    "4 Channel Relay Sheild": {"microcenter":"643966/inland-rpi-4-channel-relay-5v-shield-for-raspberry-pi-ce-certification"},
}

