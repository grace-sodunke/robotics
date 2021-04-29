# Modules and robot Object Initialisation ------------------------------------------------------------------------------
from sr.robot import Robot
import math

pi = math.pi


class OlavianRobot(Robot):
    """
    Subclass of Robot, allowing for improved readability and standardised code in SOG-2.
    """

    def __init__(self):
        super().__init__()
        # Peripherals Setup --------------------------------------------------------------------------------------------
        self.leftMotor = self.motors[0].m0
        self.rightMotor = self.motors[0].m1
        self.leftMotor.power = 0
        self.rightMotor.power = 0
        self.controlBoard = self.ruggeduinos[0]
        self.forward = True
        self.reverse = False
        self.right = True
        self.left = False
        self.smooth_brake = True
        self.smooth_turn = True
        self.owned = True
        self.not_owned = False
        self.on = True
        self.off = False
        self.wait = True
        # Bump Sensor Pins ---------------------------------------------------------------------------------------------
        self.front_bumper = 2
        self.rear_bumper = 3
        # LED Pins -----------------------------------------------------------------------------------------------------
        self.red = (4, 7)
        self.green = (5, 8)
        self.blue = (6, 9)
        # Ultrasonic Sensors Pins --------------------------------------------------------------------------------------
        self.front_left_sensor = 0
        self.front_right_sensor = 1
        self.left_sensor = 2
        self.right_sensor = 3
        self.back_left_sensor = 4
        self.back_right_sensor = 5
        # Additional Constants -----------------------------------------------------------------------------------------
        self.next_tower = None
        self.captured = []
        self.rev_const = 2
        self.dont_brake = False

        print("\nOlavian Robot - Successfully Booted")
        '''
        # ! ---------------------------------------------- DO NOT REMOVE --------------------------------------------- !
        # Control Board (Ruggeduino) Pin Initialisation
        controlBoard.pin_mode(frontBumper, INPUT) # Front Bumper Switch
        controlBoard.pin_mode(rearBumper, INPUT) # Rear Bumper Switch
        controlBoard.pin_mode(rightRed, OUTPUT) # Right Red LED
        controlBoard.pin_mode(rightGreen, OUTPUT) # Right Green LED
        controlBoard.pin_mode(rightBlue, OUTPUT) # Right Blue LED
        controlBoard.pin_mode(leftRed, OUTPUT) # Left Red LED
        controlBoard.pin_mode(leftGreen, OUTPUT) # Left Green LED
        controlBoard.pin_mode(leftBlue, OUTPUT) # Left Blue LED
        '''

    # Movement Methods -------------------------------------------------------------------------------------------------

    def move(self, direction, time, power=100):
        """
        Move robot in a specified direction for a set period of time at a default power of 100.
        :param direction: (bool) True: Robot moves forward, False: Robot moves back.
        :param time: (int) Number of seconds.
        :param power: (int) Power of motors, controlled using PWM.
        :return: None
        """
        power = abs(power)
        multiplier = -1
        if direction:
            multiplier = 1
        self.leftMotor.power = self.rightMotor.power = power * multiplier
        self.sleep(time)

    def brake(self, time=1.0, is_smooth=False):
        """
        Procedure to stop the robot moving for a specified length of time.
        :param time: (float) Number of seconds.
        :param is_smooth: (bool) Whether smooth braking is enabled/disabled, default disabled.
        :return: None
        """
        self.leftMotor.use_brake = self.rightMotor.use_brake = not is_smooth
        self.leftMotor.power = self.rightMotor.power = 0
        self.sleep(time)

    def turn(self, direction, degrees, power=50, brake_after=True, smooth=False):
        """
        Procedure to turn the robot through a specific amount of degrees
        """
        radians = degrees*math.pi/180
        d = abs((self.heading() - radians)) / (2 * math.pi)
        time = d * self.rev_const
        if direction:  # Turning right
            self.leftMotor.power = power
            self.rightMotor.power = -1*power
        else:  # Turning left
            self.leftMotor.power = -1*power
            self.rightMotor.power = power
        if brake_after:
            self.sleep(time)
            self.brake(0.25, smooth)
        else:
            self.sleep(time)

    def turnR(self, t, lm_power=50, rm_power=-50):
        self.leftMotor.power = lm_power
        self.rightMotor.power = rm_power
        self.sleep(t)
        self.brake(0.25)

    def turnL(self, t, lm_power=-50, rm_power=50):
        self.leftMotor.power = lm_power
        self.rightMotor.power = rm_power
        self.sleep(t)
        self.brake(0.25)

    def turn_until(self, compass_bearing):
        pass

    def is_in_zone(self):
        signal = self._find_signal()
        print(f"Signal is: {signal}")
        return signal > 37

    def avoid_collision(self):
        """
        :return: None
        """
        if self.is_bumped(self.front_bumper):
            self.move(self.reverse, 1.5)
        if self.is_bumped(self.rear_bumper):
            self.move(self.forward, 1.5)
            self.turn(self.right, 1)

    def avoid_obstacles(self):
        """
        :return: None
        """
        '''
        print("Obstacle detected: Moving away")
        dist = 1.7
        if not self.is_in_zone():
            while self._is_near(self.front_left_sensor, dist) and self._is_near(self.front_right_sensor, dist):
                 self.move(self.reverse, 0.2)
                 self.turn(self.left, 10)
                 self.move(self.forward, 0.2)
        '''
        '''
            while self._is_near(self.back_left_sensor, dist) and self._is_near(self.back_right_sensor, dist):
                 self.move(self.forward, 0.2)
                 self.turn(self.right, 10)
                 self.move(self.reverse, 0.2)
        '''
        if self._is_near(self.right_sensor):
            self.turn(self.left, 90)
        if self._is_near(self.left_sensor):
            self.turn(self.right, 90)

    # Sensing and Control Methods --------------------------------------------------------------------------------------

    def is_bumped(self, bumper):
        """
        :param bumper: (int) Bump sensor pin on controlBoard
        :return: None
        """
        return self.controlBoard.digital_read(bumper)

    def _is_near(self, sensor, dist=21):
        """
        :param sensor: sensor pin
        :param dist: (int) distance in mm to check for
        :return: (bool) whether its within that range
        """
        return self.get_dist_from(sensor) < dist

    def is_movement_viable(self, dist=21):
        """
        :param dist: (int) distance in cm to check for
        :return: (bool) Whether robot can move in the given direction
        """
        return not(self._is_near(self.front_left_sensor, dist) or self._is_near(self.front_right_sensor, dist))

    def get_dist_from(self, sensor):
        """
        :param sensor (int) Sensor pin number on controlBoard.
        :return: (int) Distance in mm from sensor.
        """
        return self.controlBoard.analogue_read(sensor)

    def set_next_tower(self, tower_code):
        self.next_tower = tower_code

    def find_nearest(self, owned=False):
        """
        :param owned: (bool) When false, captured transmitters will not be counted when finding the nearest tower.
        :return: (view object) Nearest transmitter.
        """
        transmitters = self.radio.sweep()
        if not owned:
            for transmitter in transmitters:
                # print([transmitter.target_info.station_code for transmitter in transmitters])
                if transmitter.target_info.owned_by == self.zone or transmitter.target_info.locked:
                    transmitters.remove(transmitter)
                    '''
                    if transmitter.target_info.station_code in self.to_explore:
                        self.to_explore.remove(transmitter.target_info.station_code)
                    print("Removing transmitter: " + transmitter.target_info.station_code)
                    '''
        signal_strengths = []
        for transmitter in transmitters:
            if transmitter.target_info.station_code in self.to_explore:
                signal_strengths.append(transmitter.signal_strength)
        try:
            max_signal_strength = max(signal_strengths)
            for transmitter in transmitters:
                if transmitter.signal_strength == max_signal_strength:
                    print("Going to " + transmitter.target_info.station_code)
                    return transmitter
        except ValueError:
            # self.move_away_if_near()
            self.move(self.forward, 1)
            self.find_nearest(owned)

    def _find_angle(self):
        """
        :return: (float) Angle in degrees required to turn through to face the nearest transmitter.
        """
        tower_code = self.next_tower
        transmitter = self.find_specific(tower_code)
        return transmitter.bearing * (180 / 3.14)

    def find_specific(self, name):
        if name is None:
            print("Tower code is none")
        transmitters = self.radio.sweep()
        for transmitter in transmitters:
            if transmitter.target_info.station_code == name:
                return transmitter
        print(f"Could not find tower {name}")

    def _find_signal(self):
        """
        :param: (string) Tower Code to get signal strength from
        :return: (float) Signal strength from the nearest transmitter or transmitter specified
        """
        tower_code = self.next_tower
        if tower_code is None:
            print("Tower code is none")
        transmitter = self.find_specific(tower_code)
        print(transmitter.signal_strength)
        return transmitter.signal_strength

    def find_name(self):
        """
        :return: (string) 2-letter station code of nearest tower regardless of whether captured or not
        """
        transmitter = self.find_nearest(self.owned)
        return transmitter.target_info.station_code

    def is_in_radius(self):
        """
        :return: (bool) 
        """
        return self._find_signal() > 4.2

    def heading(self):
        return self.compass.get_heading()

    # Output Methods ---------------------------------------------------------------------------------------------------

    def led(self, colour, state, wait=False, side=None):
        """
        :param colour: (tuple) Pins of both LEDs of required colour.
        :param state: (bool) On or Off.
        :param side: (bool) True for Right, False for Left.
        :param wait: (bool) True to wait 0.5 seconds extra.
        :return: None
        """
        right_pin = colour[0]
        left_pin = colour[1]
        if wait:
            self.sleep(0.5)
        if side is not None:
            if side:
                self.controlBoard.digital_write(right_pin, state)
            else:
                self.controlBoard.digital_write(left_pin, state)
        else:
            self.controlBoard.digital_write(right_pin, state)
            self.sleep(0.5)
            self.controlBoard.digital_write(left_pin, state)

    def display_transmitter_info(self):
        """
        Display all the information from a radio sweep to the console.
        :return: None
        """
        transmitters = self.radio.sweep()
        print(f'Found {len(transmitters)} transmitter(s):')
        for transmitter in transmitters:
            print(f'''  Transmitter {transmitter.target_info.station_code}
        Bearing: {transmitter.bearing * (180 / 3.14)}
        Signal strength:{transmitter.signal_strength}
        Owned by: {transmitter.target_info.owned_by} ''')

    def claim(self, tower):
        self.radio.claim_territory()
        self.captured.append(tower)

    def halt(self):
        """
        Shut the robot down completely / Reset.
        :return: None
        """
        self.brake()
        print("Switching off...")
        self.led(self.red, self.off, self.wait)
        self.led(self.green, self.off, self.wait)
        self.led(self.blue, self.off, self.wait)
