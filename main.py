#!/usr/bin/env python
from rpi_ws281x import Adafruit_NeoPixel, Color
from time import sleep
from datetime import datetime
from random import randint

# Define the LED panel
panel = Adafruit_NeoPixel(64, 18, 800000, 5, False, 50)
panel.begin()

# Define the LED positions for each word
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

# Clear all LEDs
def clear():
  for i in range(panel.numPixels()):
    panel.setPixelColor(i, Color(0, 0, 0))

# Update the LED panel
def update():
  panel.show()

# Set the color of a word
def set_word(word, color):
  for pixel in words[word]:
    panel.setPixelColor(pixel, color)

# Generate a random color
def generate_random_color():
  r = randint(0, 255)
  g = randint(0, 255)
  b = randint(0, 255)
  return Color(r, g, b)

# Calculate the gradient between two colors
def calculate_gradient(start_color, end_color, steps):
  gradient = []
  for i in range(steps):
    r = int((start_color >> 16 & 0xFF) + ((end_color >> 16 & 0xFF) - (start_color >> 16 & 0xFF)) * i / steps)
    g = int((start_color >> 8 & 0xFF) + ((end_color >> 8 & 0xFF) - (start_color >> 8 & 0xFF)) * i / steps)
    b = int((start_color & 0xFF) + ((end_color & 0xFF) - (start_color & 0xFF)) * i / steps)
    gradient.append(Color(r, g, b))
  return gradient

# Main loop
while True:
  # Get the current time
  current_time = datetime.now().time()
  hour, minute, _ = str(current_time).split(":")
  hour = int(hour)
  minute = int(minute)

  # Clear all LEDs
  clear()

  # Generate a random start and end color
  start_color = generate_random_color()
  end_color = generate_random_color()

  # Calculate the gradient between start and end color
  gradient = calculate_gradient(start_color, end_color, 10)

  # Set the words based on the current time
  if 3 <= minute <= 7:
    set_word('mfive', gradient[0])
    set_word('past', gradient[0])
  elif 8 <= minute <= 12:
    set_word('mten', gradient[0])
    set_word('past', gradient[0])
  # ... (rest of the code)

  # Adjust the hour if necessary
  if minute > 32:
    hour += 1

  # Set the hour word
  if hour == 1 or hour == 13:
    set_word('one', gradient[0])
  elif hour == 2 or hour == 14:
    set_word('two', gradient[0])
  # ... (rest of the code)

  # Update the LED panel
  update()
  sleep(0.5)
