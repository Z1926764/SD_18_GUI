from celery import shared_task
import datetime
import RPi.GPIO as GPIO
import board
import busio
import adafruit_ads1x15.ads1115 as ADC
from adafruit_ads1x15.analog_in import AnalogIn as AnalogRead
from collections import deque

# The @shared_task decorator turns a function into a Celery task
# This Celery task is running asyncronously and perpetually when 
#   the user executes the command 'python -m celery -A app worker --beat'
#   within the project folder
# View the beat schedule of this task within app/celery.py. Right now,
#   it is set to run every 5 seconds upon execution of the Celery worker
@shared_task()
def get_pressure(self, *args):
    relation = 1 # This defines the voltage to pressure linear relationship
    # import the PressurePoint model and update it every time this task runs
    from .models import PressurePoint
    # Following Example from library 
    # https://github.com/adafruit/Adafruit_CircuitPython_ADS1x15

    i2c = busio.I2C(board.SCL, board.SDA)

    adc = ADC.ads1115

    supP = AnalogRead(adc, ADC.P0)
    conP = AnalogRead(adc, ADC.P1)


    currentPressure = conP.voltage * relation
    print("CURRENT PRESSURE: " + str(currentPressure))

    # get the current date and time
    now = datetime.datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

    # create a new entry within the PressurePoint table
    entry = PressurePoint(time=date_time, pressure=currentPressure)
    entry.save() 

    return currentPressure

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def read_pressure_switch(self, *args):
    switchState = GPIO.input(4)
    return switchState

er = deque([0.0] * 5, maxlen=5)
pwmVal = 0
GPIO.setup(7,GPIO.OUT)
servoValvePwm = GPIO.PWM(7, 1000) # pin num, frequency
servoValvePwm.start(pwmVal) # duty cycle  
# not sure if have to use args pointer and unpack
def control_pressure(self, *args):
    from .models import GlobalValues
    setpoint = GlobalValues.models.get(setPoint)
    currentPressure = GlobalValues.models.get(currentPressure)
    kp = 1 
    kd = 1
    ki = 1
    global er
    global pwm
    er.append((setpoint-currentPressure))
    gain = (kp*er(4)) + (kd*(er(4)-er(3))/2) + (ki*sum(er))
    servoValvePwm.ChangeDutyCycle(max(min(int(pwmval + gain),100),0))
    return 0
