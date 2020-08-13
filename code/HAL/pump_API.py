import machine as mc
from machine import Pin
import time


class Stepper:
    """Class for stepper motor driven by Easy Driver."""
    rps = 0

    def __init__(self, step_pin, steps_per_rev, rps, mlPerRev , dir_pin = -9999):
        """Initialise stepper."""
        self.stp = Pin(step_pin)
        
        if dir_pin != -9999:
            self.dir = Pin(dir_pin)
            self.dir.init(Pin.OUT)
            self.dir.value(0)
            self.direction = 0

        self.steps_per_rev = steps_per_rev
        self.mlPerRev = mlPerRev
        self.pwm = None
        self.running = False
        
        #pwm is same freq for all pumps, so class member
        Stepper.rps = rps
    
    def set_rps(self,rps):
        """Only use when pump is on!!
        """
        Stepper.rps = rps
        self.pwm.freq(self.rps * self.steps_per_rev)

    def reverse_direction(self):
        if self.direction==1:
            self.dir.value(0)
            self.direction = 0
        else:
            self.dir.value(1)
            self.direction = 1
    
    def start_pump(self):
        freq = self.rps * self.steps_per_rev
        self.pwm = mc.PWM(self.stp, int(freq), 512)
        self.startTime = time.time()
    
    def stop_pump(self):
        self.pwm.deinit()
        
    
    def get_pumped_volume(self):
        if self.running:
            curTime = time.time()
            return (curTime - self.startTime) * self.mlPerRev * self.steps_per_rev * self.rps
        else:
            return 0
    

