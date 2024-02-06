from celery import shared_task
import datetime
import RPi.GPIO as GPIO
import board
import busio
import adafruit_ads1x15.ads1115 as ADC
from adafruit_ads1x15.analog_in import AnalogIn as AnalogRead
from collections import deque
import time
import pigpio

# The @shared_task decorator turns a function into a Celery task
# This Celery task is running asyncronously and perpetually when 
#   the user executes the command 'python -m celery -A app worker --beat'
#   within the project folder
# View the beat schedule of this task within app/celery.py. Right now,
#   it is set to run every 5 seconds upon execution of the Celery worker
i2c = busio.I2C(board.SCL, board.SDA)

adc = ADC.ADS1115(i2c)

adc.gain = 2/3

supP = AnalogRead(adc, ADC.P0)
conP = AnalogRead(adc, ADC.P1)

'''
@shared_task()
def structure(self, *args):
    pass
'''

@shared_task()
def get_pressure(self, *args):
    relation = 1 # This defines the voltage to pressure linear relationship
    # import the PressurePoint model and update it every time this task runs
    from .models import PressurePoint
    from .models import GlobalValues
    # Following Example from library 
    # https://github.com/adafruit/Adafruit_CircuitPython_ADS1x1
    currentPressure = conP.voltage * relation

    # get the current date and time
    now = datetime.datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

    var2 = read_pressure_switch(self)

    setPoint = 2.5
    # Clear the GlobalValues model before saving new data
    data = GlobalValues.objects.all()[0]
    data.currentPressure = currentPressure
    data.setPoint = setPoint
    #data.delete()
    #data = GlobalValues(currentPressure = currentPressure, setPoint = setPoint)
    data.save()

    # create a new entry within the PressurePoint table
    entry = PressurePoint(time=date_time, pressure=currentPressure, switchState=var2)
    entry.save() 
    
    return currentPressure

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
@shared_task
def read_pressure_switch(self, *args):
    switchState = GPIO.input(4)
    return switchState

er = deque([0.0] * 5, maxlen=5)
PWM_PIN = 21
pi = pigpio.pi()
pi.set_PWM_frequency(PWM_PIN, 100)  # Initial frequency set to 100 Hz
pi.set_PWM_dutycycle(PWM_PIN, 0)
# not sure if have to use args pointer and unpack
@shared_task()
def control_pressure(self, *args):
    from .models import GlobalValues
    
    variables = GlobalValues.objects.all().values()
    setpoint = variables.values()[0]['setPoint']
    currentPressure = variables.values()[0]['currentPressure']
    kp = 1 
    kd = 1
    ki = 1
    global er
    global pwm
    val = float(setpoint - currentPressure)
    er.append(val)
    gain = (kp*er[4]) + (kd*(er[4]-er[3])/2) + (ki*sum(er))
    gain = max(min(int(gain),100),0)
    print(gain)
    pi.set_PWM_dutycycle(PWM_PIN, gain)
    return 0