#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
left_motor_a = Motor(Ports.PORT21, GearSetting.RATIO_18_1, False)
left_motor_b = Motor(Ports.PORT4, GearSetting.RATIO_18_1, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
right_motor_b = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain_inertial = Inertial(Ports.PORT9)
drivetrain = SmartDrive(left_drive_smart, right_drive_smart, drivetrain_inertial, 319.19, 320, 40, MM, 1)
BELT = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
Loader = Motor(Ports.PORT20, GearSetting.RATIO_18_1, True)
Mogo = DigitalOut(brain.three_wire_port.a)
controller_1 = Controller(PRIMARY)
Colour = Optical(Ports.PORT8)
Arm = DigitalOut(brain.three_wire_port.b)
Wallstake_motor_a = Motor(Ports.PORT18, GearSetting.RATIO_18_1, False)
Wallstake_motor_b = Motor(Ports.PORT19, GearSetting.RATIO_18_1, True)
Wallstake = MotorGroup(Wallstake_motor_a, Wallstake_motor_b)
holder = DigitalOut(brain.three_wire_port.c)
distance_11 = Distance(Ports.PORT11)
Tipper = DigitalOut(brain.three_wire_port.d)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()

vexcode_initial_drivetrain_calibration_completed = False
def calibrate_drivetrain():
    # Calibrate the Drivetrain Inertial
    global vexcode_initial_drivetrain_calibration_completed
    sleep(200, MSEC)
    brain.screen.print("Calibrating")
    brain.screen.next_row()
    brain.screen.print("Inertial")
    drivetrain_inertial.calibrate()
    while drivetrain_inertial.is_calibrating():
        sleep(25, MSEC)
    vexcode_initial_drivetrain_calibration_completed = True
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)


# Calibrate the Drivetrain
calibrate_drivetrain()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")



# define variables used for controlling motors based on controller inputs
drivetrain_l_needs_to_be_stopped_controller_1 = False
drivetrain_r_needs_to_be_stopped_controller_1 = False

# define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
    global drivetrain_l_needs_to_be_stopped_controller_1, drivetrain_r_needs_to_be_stopped_controller_1, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:
            # stop the motors if the brain is calibrating
            if drivetrain_inertial.is_calibrating():
                left_drive_smart.stop()
                right_drive_smart.stop()
                while drivetrain_inertial.is_calibrating():
                    sleep(25, MSEC)
            
            # calculate the drivetrain motor velocities from the controller joystick axies
            # left = axis3
            # right = axis2
            drivetrain_left_side_speed = controller_1.axis3.position()
            drivetrain_right_side_speed = controller_1.axis2.position()
            
            # check if the value is inside of the deadband range
            if drivetrain_left_side_speed < 5 and drivetrain_left_side_speed > -5:
                # check if the left motor has already been stopped
                if drivetrain_l_needs_to_be_stopped_controller_1:
                    # stop the left drive motor
                    left_drive_smart.stop()
                    # tell the code that the left motor has been stopped
                    drivetrain_l_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the left motor next
                # time the input is in the deadband range
                drivetrain_l_needs_to_be_stopped_controller_1 = True
            # check if the value is inside of the deadband range
            if drivetrain_right_side_speed < 5 and drivetrain_right_side_speed > -5:
                # check if the right motor has already been stopped
                if drivetrain_r_needs_to_be_stopped_controller_1:
                    # stop the right drive motor
                    right_drive_smart.stop()
                    # tell the code that the right motor has been stopped
                    drivetrain_r_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the right motor next
                # time the input is in the deadband range
                drivetrain_r_needs_to_be_stopped_controller_1 = True
            
            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_l_needs_to_be_stopped_controller_1:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_r_needs_to_be_stopped_controller_1:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)
        # wait before repeating the process
        wait(20, MSEC)

# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)

#endregion VEXcode Generated Robot Configuration

remote_control_code_enabled = True
vexcode_brain_precision = 0
vexcode_console_precision = 0
vexcode_controller_1_precision = 0
wast = 0
holderExtended = False
armExtended = False
tipperExtended = False

def when_started1():
    global wast, remote_control_code_enabled, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    Mogo.set(False)
    drivetrain.set_drive_velocity(100, PERCENT)
    drivetrain.set_turn_velocity(100, PERCENT)
    BELT.set_velocity(100, PERCENT)
    Loader.set_velocity(100, PERCENT)
    BELT.set_max_torque(100, PERCENT)
    Loader.set_max_torque(100, PERCENT)
    Colour.gesture_disable()
    Wallstake.set_velocity(20, PERCENT)
    Wallstake.set_max_torque(100, PERCENT)
    Wallstake.set_position(0, DEGREES)
    holder.set(False)
    Wallstake.set_stopping(BRAKE)

def onevent_controller_1buttonL1_pressed_0():
    global wast, remote_control_code_enabled, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    BELT.spin(FORWARD)
    Loader.spin(FORWARD)

def onevent_controller_1buttonR1_pressed_0():
    global wast, remote_control_code_enabled, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    Mogo.set(True)

def onevent_controller_1buttonR2_pressed_0():
    global wast, remote_control_code_enabled, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    Mogo.set(False)

def onevent_controller_1buttonL2_pressed_0():
    global wast, remote_control_code_enabled, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    BELT.spin(REVERSE)
    Loader.spin(REVERSE)


def onevent_controller_1buttonX_pressed_0():
    global armExtended, wast, remote_control_code_enabled, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    if armExtended == True: 
        Arm.set(False)
        armExtended = False
    else:
        Arm.set(True)
        armExtended = True
    

def onevent_controller_1buttonB_pressed_0():
    global holderExtended, wast, remote_control_code_enabled, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    if holderExtended: 
        holder.set(False)
    else:
        holder.set(True)
    holderExtended = not(holderExtended)

def stopBelt():
    BELT.stop()
    
def onevent_controller_1buttonA_pressed_0():
    global wast, remote_control_code_enabled, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    stopBelt()
    wallstakeTo(170)
    wallstakeTo(100) 

def onevent_controller_1buttonY_pressed_0():
    global tipperExtended, wast, remote_control_code_enabled, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    if tipperExtended: 
        Tipper.set(False)
    else:
        Tipper.set(True)
    tipperExtended = not(tipperExtended)

def onevent_controller_1buttonDown_pressed_0():
    global wast, remote_control_code_enabled, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    controller_1.rumble("....")
    wast = 0
    Wallstake.spin_to_position(1, DEGREES)
    BELT.set_velocity(100, PERCENT)
    wait(0.3, SECONDS)
    Wallstake.spin_to_position(0, DEGREES)
    wait(0.4, SECONDS)
    holder.set(True)
    BELT.spin(FORWARD)
    Loader.spin(FORWARD)

def onevent_controller_1buttonL2_released_0():
    global wast, remote_control_code_enabled, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    BELT.stop()
    Loader.stop()

def onevent_controller_1buttonUp_pressed_0():
    global wast, remote_control_code_enabled, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    controller_1.rumble("-.-.")
    Wallstake.spin_to_position(0, DEGREES)
    Wallstake.spin_to_position(0, DEGREES)
    wait(0.4, SECONDS)
    holder.set(True)
    wast = 1
    BELT.set_velocity(50, PERCENT)

def when_started2():#new
    global wast, remote_control_code_enabled, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    Colour.set_light(LedStateType.ON)
    #while True and competition.is_autonomous():
    while True:
        if Colour.color() == Color.BLUE:
            wast = 0
            BELT.set_velocity(100, PERCENT)
            brain.screen.set_fill_color(Color.CYAN)
            wait(0.25, SECONDS)
            while distance_11.object_distance(MM) >= 50:
                wait(5, MSEC)
            BELT.spin_for(FORWARD, 151,DEGREES)
            BELT.spin_for(REVERSE,100,DEGREES)
            BELT.spin(FORWARD)
            brain.screen.set_fill_color(Color.TRANSPARENT)
    Colour.set_light(LedStateType.OFF)

def onevent_Colour_detects_object_0():
    global wast, remote_control_code_enabled, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    if wast == 1:
        Wallstake.set_stopping(HOLD)
        Wallstake.spin_to_position(10, DEGREES)
        while not distance_11.object_distance(MM) < 50:
            wait(5, MSEC)
        BELT.set_position(0, DEGREES)
        BELT.spin_to_position(145, DEGREES)
        wait(0.5, SECONDS)
        BELT.spin_to_position(147, DEGREES)
        wast = 0
        holder.set(False)
        wait(0.5, SECONDS)
        BELT.spin_for(REVERSE, 45, DEGREES)
        wait(0.4, SECONDS)
        BELT.set_velocity(100, PERCENT)
        Loader.stop()

def onevent_controller_1buttonLeft_released_0():
    global wast, remote_control_code_enabled, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    Wallstake.stop()

def onevent_controller_1buttonRight_released_0():
    global wast, remote_control_code_enabled, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    Wallstake.spin(REVERSE)

def onevent_controller_1buttonRight_pressed_0():
    global wast, remote_control_code_enabled, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    Wallstake.spin(REVERSE)
    holder.set(False)

def when_started3():
    global wast, remote_control_code_enabled, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    while True:
        brain.screen.set_cursor(1, 1)
        brain.screen.print(distance_11.object_distance(MM), precision=6 if vexcode_brain_precision is None else vexcode_brain_precision)
        wait(0.1, SECONDS)
        brain.screen.clear_screen()
        wait(5, MSEC)

def onevent_controller_1buttonLeft_pressed_0():
    global wast, remote_control_code_enabled, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    Wallstake.spin(FORWARD)

def when_started4():
    global wast, remote_control_code_enabled, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    while True:
        if Wallstake.position(DEGREES) >= 175:
            Wallstake.stop()
            Wallstake.spin_to_position(175, DEGREES)
        wait(5, MSEC)

def wallstakeTo(val):
    Wallstake.spin_to_position(val,DEGREES)

def setSpeed(val):
    drivetrain.set_drive_velocity(val, PERCENT)
    drivetrain.set_turn_velocity(val, PERCENT)

def onauton_autonomous_0():
    global holder, remote_control_code_enabled, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    
    drivetrain.set_heading(270, DEGREES)
    remote_control_code_enabled = False
    #red left

    setSpeed(30)
    Loader.spin(REVERSE)
    forward(415)
    turnTo(182)
    forward(100)
    wallstakeTo(165)
    holder.set(True)
    backward(100)
    holder.set(False)
    wallstakeTo(180)
    backward(20)
    forward(20)
    wallstakeTo(0)
    holder.set(True)
    setSpeed(70)
    backward(250)
    turnTo(222)
    backward(700)
    backward(300)
    wait(0.1,SECONDS)
    drivetrain.set_drive_velocity(50, PERCENT)
    backward(215)
    drivetrain.set_drive_velocity(100, PERCENT)
    Mogo.set(True)
    turnTo(92)
    intake()
    forward(700)
    wait(1.5,SECONDS)
    backward(100)
    Mogo.set(False)
    forward(100)
    turnTo(150)
    backward(300)



    # holder.set(True)
    # backward(150)
    # drivetrain.set_drive_velocity(80, PERCENT)
    # backward(710)
    # clamp()
    # pause(0.5)
    # intake()
    # pause(0.5)
    # backward(270)
    # intakeReverse()
    # turnTo(270)
    # forward(450)
    # turnTo(340)
    # forward(215)
    # intakeReverse()
    # backward(100)
    # turnTo(95)
    # forward(1000)
    



def ondriver_drivercontrol_0():
    global wast, remote_control_code_enabled, vexcode_brain_precision, vexcode_console_precision, vexcode_controller_1_precision
    remote_control_code_enabled = True
    holder.set(True)
    drivetrain.set_drive_velocity(100,PERCENT)
    drivetrain.set_turn_velocity(100,PERCENT)

def forward(dist):
    drivetrain.drive_for(FORWARD,dist,MM)

def backward(dist):
    drivetrain.drive_for(REVERSE,dist,MM)

def intake():
    BELT.spin(FORWARD)
    Loader.spin(FORWARD)

def intakeReverse():
    BELT.spin(REVERSE)
    pause(0.5)
    BELT.spin(FORWARD)

def clamp():
    Mogo.set(True)

def unclamp():
    Mogo.set(False)

def pause(sec):
    wait(sec,SECONDS)

def turnTo(ang):
    drivetrain.turn_to_heading(ang, DEGREES)

# create a function for handling the starting and stopping of all autonomous tasks
def vexcode_auton_function():
    # Start the autonomous control tasks
    auton_task_0 = Thread( onauton_autonomous_0 )
    # wait for the driver control period to end
    while( competition.is_autonomous() and competition.is_enabled() ):
        # wait 10 milliseconds before checking again
        wait( 10, MSEC )
    # Stop the autonomous control tasks
    auton_task_0.stop()

def vexcode_driver_function():
    # Start the driver control tasks
    driver_control_task_0 = Thread( ondriver_drivercontrol_0 )

    # wait for the driver control period to end
    while( competition.is_driver_control() and competition.is_enabled() ):
        # wait 10 milliseconds before checking again
        wait( 10, MSEC )
    # Stop the driver control tasks
    driver_control_task_0.stop()


# register the competition functions
competition = Competition( vexcode_driver_function, vexcode_auton_function )

# system event handlers
controller_1.buttonL1.pressed(onevent_controller_1buttonL1_pressed_0)
controller_1.buttonR1.pressed(onevent_controller_1buttonR1_pressed_0)
controller_1.buttonR2.pressed(onevent_controller_1buttonR2_pressed_0)
controller_1.buttonL2.pressed(onevent_controller_1buttonL2_pressed_0)
controller_1.buttonX.pressed(onevent_controller_1buttonX_pressed_0)
controller_1.buttonDown.pressed(onevent_controller_1buttonDown_pressed_0)
controller_1.buttonL2.released(onevent_controller_1buttonL2_released_0)
controller_1.buttonA.pressed(onevent_controller_1buttonA_pressed_0)
controller_1.buttonY.pressed(onevent_controller_1buttonY_pressed_0)
controller_1.buttonB.pressed(onevent_controller_1buttonB_pressed_0)
controller_1.buttonUp.pressed(onevent_controller_1buttonUp_pressed_0)
Colour.object_detected(onevent_Colour_detects_object_0)
controller_1.buttonLeft.released(onevent_controller_1buttonLeft_released_0)
controller_1.buttonRight.released(onevent_controller_1buttonRight_released_0)
controller_1.buttonRight.pressed(onevent_controller_1buttonRight_pressed_0)
controller_1.buttonLeft.pressed(onevent_controller_1buttonLeft_pressed_0)
# add 15ms delay to make sure events are registered correctly.
wait(15, MSEC)

ws2 = Thread( when_started2 )
ws3 = Thread( when_started3 )
ws4 = Thread( when_started4 )
when_started1()
