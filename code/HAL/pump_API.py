
from machine import Pin
from time import sleep_us


class Stepper:
    """Class for stepper motor driven by Easy Driver."""

    def __init__(self, step_pin, stepsPerPump, dir_pin = -9999):
        """Initialise stepper."""
        self.stp = step_pin

        self.stp.init(Pin.OUT)
        if dir_pin != -9999:
            self.dir.init(Pin.OUT)
            self.dir.init(Pin.OUT)

        self.step_time = 20  # us
        self.steps_per_rev = 1600
        self.stepsDelta = 0
        
        self.stepsPerPump = stepsPerPump    

    def reverse_direction(self):
        if self.dir.value==1:
            self.dir.value=0
        else:
            self.dir.value=1

    def clear_steps(self):
        self.stepsDelta = 0
        
    def pump_standard_pump(self):
        for i in range(abs(self.stepsPerPump)):
            self.stp.value(1)
            sleep_us(self.step_time)
            self.stp.value(0)
            sleep_us(self.step_time)
        self.stepsDelta += self.stepsPerPump
    
    def pump(self,steps):
        for i in range(abs(steps)):
            self.stp.value(1)
            sleep_us(self.step_time)
            self.stp.value(0)
            sleep_us(self.step_time)
        

