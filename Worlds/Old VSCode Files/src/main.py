#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
L1 = Motor(Ports.PORT1, GearSetting.RATIO_6_1, False)
L2 = Motor(Ports.PORT2, GearSetting.RATIO_6_1, True)
L3 = Motor(Ports.PORT3, GearSetting.RATIO_6_1, False)
R1 = Motor(Ports.PORT4, GearSetting.RATIO_6_1, True)
R2 = Motor(Ports.PORT5, GearSetting.RATIO_6_1, False)
R3 = Motor(Ports.PORT7, GearSetting.RATIO_6_1, True)
Belt = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
MogoClamp = DigitalOut(brain.three_wire_port.a)
controller_1 = Controller(PRIMARY)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration

myVariable = 0
SpeedLeft = 0
SpeedRight = 0

def when_started1():
    global myVariable, SpeedLeft, SpeedRight
    while True:
        SpeedLeft = (controller_1.axis3.position()) / 8.3
        SpeedRight = (controller_1.axis2.position()) / 8.3
        L1.spin(FORWARD, SpeedLeft, VOLT)
        L2.spin(FORWARD, SpeedLeft, VOLT)
        L3.spin(FORWARD, SpeedLeft, VOLT)
        R1.spin(FORWARD, SpeedRight, VOLT)
        R2.spin(FORWARD, SpeedRight, VOLT)
        R3.spin(FORWARD, SpeedRight, VOLT)
        wait(5, MSEC)

def clampMogo():
    MogoClamp.set(True)

def unclampMogo():
    MogoClamp.set(False)

def startBelt():
    Belt.set_velocity(100, PERCENT)

def stopBelt():
    Belt.set_velocity(0, PERCENT)

Thread(when_started1())

controller_1.buttonR1.pressed(clampMogo)
controller_1.buttonR2.pressed(unclampMogo)
controller_1.buttonL1.pressed(startBelt)
controller_1.buttonL2.pressed(stopBelt)


#5th April