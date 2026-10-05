from machine import Pin, PWM, ADC
from time import sleep_ms

pot = ADC(Pin(26))
buzzer = PWM(Pin(18))

DO = 262
RE = 294
MI = 330
FA = 349
SOL = 392
LA = 440
SI = 494
DO2 = 523

melodie = [
    (MI, 300),
    (SOL, 300),
    (LA, 500),
    (SOL, 300),
    (MI, 300),
    (RE, 300),
    (DO, 500),

    (RE, 300),
    (MI, 300),
    (SOL, 500),
    (LA, 300),
    (SOL, 300),
    (MI, 500),

    (SOL, 300),
    (LA, 300),
    (DO2, 500),
    (SI, 300),
    (LA, 300),
    (SOL, 600)
]

while True:
    for note, duree in melodie:
        buzzer.freq(note)

        temps = 0

        while temps < duree:
            valeurPot = pot.read_u16()
            volume = valeurPot // 4

            buzzer.duty_u16(volume)

            sleep_ms(20)
            temps += 20

        buzzer.duty_u16(0)
        sleep_ms(50)