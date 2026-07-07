#!/usr/bin/env python3
from colorsys import hsv_to_rgb
from datetime import datetime
from random import random
from time import sleep

from rpi_ws281x import Adafruit_NeoPixel, Color

LED_COUNT = 64
LED_PIN = 18  # must be PWM-capable
FADE_STEPS = 20  # one fade takes FADE_STEPS * 0.5s

panel = Adafruit_NeoPixel(LED_COUNT, LED_PIN, 800000, 10, False, 50)
panel.begin()

words = {
  'mfive': [16, 17, 18, 19],
  'mten': [1, 3, 4],
  'quarter': [8, 9, 10, 11, 12, 13, 14],
  'twenty': [1, 2, 3, 4, 5, 6],
  'half': [20, 21, 22, 23],
  'past': [25, 26, 27, 28],
  'to': [28, 29],
  'one': [57, 60, 63],
  'two': [48, 49, 57],
  'three': [43, 44, 45, 46, 47],
  'four': [56, 57, 58, 59],
  'five': [32, 33, 34, 35],
  'six': [40, 41, 42],
  'seven': [40, 52, 53, 54, 55],
  'eight': [35, 36, 37, 38, 39],
  'nine': [60, 61, 62, 63],
  'ten': [39, 47, 55],
  'eleven': [50, 51, 52, 53, 54, 55],
  'twelve': [48, 49, 50, 51, 53, 54]
}

hour_words = ['twelve', 'one', 'two', 'three', 'four', 'five', 'six',
              'seven', 'eight', 'nine', 'ten', 'eleven']

# Indexed per 5-minute slot: (minute + 2) // 5 % 12
minute_words = [
  [],
  ['mfive', 'past'],
  ['mten', 'past'],
  ['quarter', 'past'],
  ['twenty', 'past'],
  ['twenty', 'mfive', 'past'],
  ['half', 'past'],
  ['twenty', 'mfive', 'to'],
  ['twenty', 'to'],
  ['quarter', 'to'],
  ['mten', 'to'],
  ['mfive', 'to'],
]

def clear():
  for i in range(panel.numPixels()):
    panel.setPixelColor(i, Color(0, 0, 0))

def set_word(word, color):
  for pixel in words[word]:
    panel.setPixelColor(pixel, color)

def random_color():
  # Random hue at full saturation, so the words never fade to near-black
  r, g, b = hsv_to_rgb(random(), 1, 1)
  return Color(int(r * 255), int(g * 255), int(b * 255))

def gradient(start_color, end_color, steps):
  colors = []
  for i in range(steps):
    t = i / (steps - 1)
    r = int((start_color >> 16 & 0xFF) + ((end_color >> 16 & 0xFF) - (start_color >> 16 & 0xFF)) * t)
    g = int((start_color >> 8 & 0xFF) + ((end_color >> 8 & 0xFF) - (start_color >> 8 & 0xFF)) * t)
    b = int((start_color & 0xFF) + ((end_color & 0xFF) - (start_color & 0xFF)) * t)
    colors.append(Color(r, g, b))
  return colors

def show_time(color):
  now = datetime.now()
  hour, minute = now.hour, now.minute

  clear()

  for word in minute_words[(minute + 2) // 5 % 12]:
    set_word(word, color)

  if minute > 32:
    hour += 1
  set_word(hour_words[hour % 12], color)

  panel.show()

try:
  color = random_color()
  while True:
    target = random_color()
    for step in gradient(color, target, FADE_STEPS):
      show_time(step)
      sleep(0.5)
    color = target
except KeyboardInterrupt:
  pass
finally:
  clear()
  panel.show()
