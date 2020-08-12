
from machine import Pin
from time import sleep_us


class Stepper:
    """Class for stepper motor driven by Easy Driver."""

    def __init__(self, step_pin, stepsPerPump, steps_per_rev, mlPerStep , dir_pin = -9999):
        """Initialise stepper."""
        self.stp = Pin(step_pin)
        self.stp.init(Pin.OUT)
        
        if dir_pin != -9999:
            self.dir = Pin(dir_pin)
            self.dir.init(Pin.OUT)
            self.dir.value(0)
            self.direction = 0

        self.step_time = 80  # us
        self.steps_per_rev = steps_per_rev
        self.stepsDelta = 0
        
        self.stepsPerPump = stepsPerPump    
        self.mlPerStep = mlPerStep

    def reverse_direction(self):
        if self.direction==1:
            self.dir.value(0)
            self.direction = 0
        else:
            self.dir.value(1)
            self.direction = 1

    def clear_steps(self):
        self.stepsDelta = 0
        
    def pump_standard_pump(self):
        for i in range(abs(self.stepsPerPump)):
            self.stp.value(1)
            sleep_us(self.step_time)
            self.stp.value(0)
            sleep_us(self.step_time)
        self.stepsDelta = (self.stepsPerPump + self.stepsDelta)
    
    def pump(self,steps):
        for i in range(abs(steps)):
            self.stp.value(1)
            sleep_us(self.step_time)
            self.stp.value(0)
            sleep_us(self.step_time)
        self.stepsDelta = (self.stepsPerPump + steps)
    
    def get_pumped_volume(self):
        return self.stepsDelta * self.mlPerStep
    

