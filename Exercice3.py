
from machine import ADC, I2C, Pin, PWM
from time import sleep_ms, ticks_ms, ticks_diff

capteur = ADC(4)
potentiometre = ADC(26)
led = Pin("LED", Pin.OUT)

buzzer = PWM(Pin(18))
buzzer.freq(1000)
buzzer.duty_u16(0)

i2c = I2C(0, sda=Pin(8), scl=Pin(9), freq=100000)
adresse = 0x3E

def commande(valeur):
    i2c.writeto(adresse, bytes([0x80, valeur]))
    sleep_ms(2)

def texte(message):
    for caractere in message:
        i2c.writeto(adresse, bytes([0x40, ord(caractere)]))
        sleep_ms(1)

# Initialisation LCD
sleep_ms(50)
commande(0x38)
commande(0x39)
commande(0x14)
commande(0x70)
commande(0x56)
commande(0x6C)
sleep_ms(200)
commande(0x38)
commande(0x0C)
commande(0x01)
sleep_ms(5)

dernier_clignotement = ticks_ms()
derniere_mesure = ticks_ms() - 1000

temperature = 0
consigne = 15

while True:
    maintenant = ticks_ms()

    # Lecture des temperatures chaque seconde
    if ticks_diff(maintenant, derniere_mesure) >= 1000:
        valeur = capteur.read_u16()
        tension = valeur * 3.3 / 65535
        temperature = 27 - (tension - 0.706) / 0.001721

        valeur_pot = potentiometre.read_u16()
        consigne = 15 + (valeur_pot / 65535) * 20

        # Affichage LCD
        commande(0x80)
        texte("Set: {:.1f} C     ".format(consigne))

        commande(0xC0)

        if temperature >= consigne + 3:
            texte("ALARM {:.1f} C   ".format(temperature))
        else:
            texte("Ambient: {:.1f} C ".format(temperature))

        print("Set:", round(consigne, 1),
              "| Ambient:", round(temperature, 1))

        derniere_mesure = ticks_ms()

    # Gestion des trois etats
    if temperature >= consigne + 3:
        # Alarme : clignotement rapide et buzzer
        intervalle = 200
        buzzer.duty_u16(32768)

    elif temperature > consigne:
        # Attention : clignotement a 0.5 Hz
        intervalle = 1000
        buzzer.duty_u16(0)

    else:
        # Normal : tout eteint
        intervalle = 0
        led.off()
        buzzer.duty_u16(0)
        dernier_clignotement = maintenant

    if intervalle > 0:
        if ticks_diff(maintenant, dernier_clignotement) >= intervalle:
            led.toggle()
            dernier_clignotement = maintenant

    sleep_ms(10)
