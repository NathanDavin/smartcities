
from machine import ADC, Pin
from neopixel import NeoPixel
from time import sleep_ms, ticks_ms, ticks_diff
from random import randint

micro = ADC(26)
led = NeoPixel(Pin(16), 1)

seuil = 13000
seuil_bas = 5000
delai = 500

dernier_battement = ticks_ms()
niveau_moyen = micro.read_u16()
pret = True

while True:
    valeur = micro.read_u16()

    difference = abs(valeur - niveau_moyen)
    niveau_moyen = niveau_moyen * 0.98 + valeur * 0.02

    maintenant = ticks_ms()

    # Reautoriser une detection quand le son redescend
    if difference < seuil_bas:
        pret = True

    # Detection d'un nouveau pic
    if difference > seuil and pret:
        if ticks_diff(maintenant, dernier_battement) >= delai:

            rouge = randint(30, 255)
            vert = randint(30, 255)
            bleu = randint(30, 255)

            led[0] = (rouge, vert, bleu)
            led.write()

            print("Battement detecte :", int(difference))

            dernier_battement = maintenant
            pret = False

    sleep_ms(5)
