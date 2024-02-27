from gpiozero import PWMLED, Button
from gpiozero.pins.lgpio import LGPIOFactory

# CONSTANTS
voltagePressureRelation = 300/5

# BUTTONS AND PWM
fact = LGPIOFactory()

fact.close()

fact = LGPIOFactory()

interruptPin = 21
servoControlPin = 16
pressureSwitchReadPin = 12

servo = PWMLED(servoControlPin, pin_factory=fact)
interruptButton = Button(interruptPin, pull_up=True, pin_factory=fact)
