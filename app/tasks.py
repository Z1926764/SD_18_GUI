# CELERY TASK PREREQUSITES
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# GENERAL PREREQUSITES
import datetime
import time
from collections import deque

# ADC PREREQUSITES
import board
import busio
import adafruit_ads1x15.ads1115 as ADC
from adafruit_ads1x15.analog_in import AnalogIn as AnalogRead

# GPIO REREQUSITES
from gpiozero import PWMLED, Button
#from gpiozero.pins.lgpio import LGPIOFactory

# CONSTANTS
voltagePressureRelation = 300/5

# BUTTONS AND PWM
#fact = LGPIOFactory()


interruptPin = 21
servoControlPin = 16
pressureSwitchReadPin = 12

#servo = PWMLED(servoControlPin, pin_factory=fact)
#interruptButton = Button(interruptPin, pull_up=True, pin_factory=fact)
#switchState = Button(pressureSwitchReadPin, pull_up=True, pin_factory=fact)

servo = PWMLED(servoControlPin)
interruptButton = Button(interruptPin, pull_up=True)
switchState = Button(pressureSwitchReadPin, pull_up=True)



def InterruptCalled():
    from .models import GlobalValues

    data = GlobalValues.objects.all().values()

    interruptStatus = not(data.values()[0]['InterruptStatus'])

    dataOut = GlobalValues.objects.all()[0]
    
    dataOut.InterruptStatus = interruptStatus

    dataOut.save()

interruptButton.when_pressed = InterruptCalled

# ADC
i2c = busio.I2C(board.SCL, board.SDA)
adc = ADC.ADS1115(i2c)
adc.gain = 2/3
supP = AnalogRead(adc, ADC.P0)
conP = AnalogRead(adc, ADC.P1)


# THIS TASK PERFORMS ALL NECESSARY IO SEQUENTIALLY
# AS FAST AS POSSIBLE
@shared_task()
def IO(self, *args):
    
    # IMPORT BOTH DATABASES
    from .models import PressurePoint
    from .models import GlobalValues

    variables = GlobalValues.objects.all().values()

    now = datetime.datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

    pSwitchState = switchState.is_pressed
    currentSupPressure = supP.voltage * voltagePressureRelation
    currentConPressure = conP.voltage * voltagePressureRelation

    entry = PressurePoint(time=date_time, Spressure=currentSupPressure, Cpressure=currentConPressure, switchState=pSwitchState)
    entry.save()

    servo.value = variables.values()[0]['DutyCycle']

    variables.currentSPressure = currentSupPressure
    variables.currentCPressure = currentConPressure
    variables.save()

kp = 1 
kd = 1
ki = 1

error = deque([0.0] * 5, maxlen=5)

# THIS TASK RUNS THE PID CONTROLLER AND DETERMINES THE DUTY CYCLE
@shared_task()
def control_pressure(self, *args):
    from .models import GlobalValues
    
    variables = GlobalValues.objects.all().values()
    setpoint = variables.values()[0]['setPoint']
    currentPressure = variables.values()[0]['currentCPressure']
    global error

    val = float(setpoint - currentPressure)
    error.append(val)
    gain = (kp*error[4]) + (kd*(error[4]-error[3])/2) + (ki*sum(error))
    dutyCycle = max(min(int(gain),100),0)

    variables.dutyCycle = dutyCycle
    variables.save()

