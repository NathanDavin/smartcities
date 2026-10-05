from machine import Pin
from time import sleep, ticks_ms, ticks_diff

led = Pin("LED", Pin.OUT)
button = Pin(18, Pin.IN)

mode = 0
last_button = 0
last_change = ticks_ms()
led_state = 0

while True:
    current_button = button.value()

    if current_button == 1 and last_button == 0:
        mode += 1

        if mode > 2:
            mode = 0

        print("Mode :", mode)
        sleep(0.2)

    last_button = current_button

    if mode == 0:
        led.off()

    elif mode == 1:
        if ticks_diff(ticks_ms(), last_change) >= 1000:
            led_state = not led_state
            led.value(led_state)
            last_change = ticks_ms()

    elif mode == 2:
        if ticks_diff(ticks_ms(), last_change) >= 250:
            led_state = not led_state
            led.value(led_state)
            last_change = ticks_ms()