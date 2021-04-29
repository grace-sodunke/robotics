from sr.robot import *
import math

graph = {
    '0': ['PN', 'BG', 'OX'],
    'TH': ['PN'],
    'FL': ['EY', 'PO'],
    'SF': ['YL'],
    'PN': ['0', 'TH', 'EY'],
    'YT': ['HA'],
    'YL': ['1', 'SF', 'PO'],
    'EY': ['PN', 'FL', 'VB'],
    'PO': ['FL', 'YL', 'SZ'],
    'BG': ['0', 'VB'],
    'HA': ['YT', 'BE'],
    'HV': ['1', 'SZ'],
    'VB': ['OX', 'BG', 'EY', 'BE', 'PL'],
    'SZ': ['BE', 'PO', 'HV', 'BN', 'PL'],
    'BE': ['VB', 'HA', 'SZ'],
    'OX': ['0', 'VB', 'TS'],
    'TS': ['OX'],
    'PL': ['VB', 'SZ'],
    'SW': ['BN'],
    'BN': ['1', 'SZ', 'SW'],
    '1': ['YL', 'HV', 'BN'],
}

R = robot()
ml = R.motors[0].m0  # motor board 0, channel 0
mr = R.motors[0].m1  # motor board 0, channel 1
controlBoard = R.ruggeduinos[0]

def claim(tower):
    R.radio.claim_territory()
    captured.append(tower)


def stop():
    ml.power = 0
    mr.power = 0
    sleep(0.25)


# collide_detect()

def sleep(t):
    R.sleep(t)


def move(p, t):
    ml.power = p
    mr.power = p
    sleep(t)
    stop()


def distance(p):
    return R.ruggeduinos[0].analogue_read(p)


def bump(s):
    return R.ruggeduinos[0].digital_read(s)


def heading():
    return R.compass.get_heading()


def turnL(t, a=-50, b=50):
    ml.power = a
    mr.power = b
    sleep(t)
    stop()


def turnR(t, a=50, b=-50):
    ml.power = a
    mr.power = b
    sleep(t)
    stop()


def get_transmitters():
    targets = []
    transmitters = R.radio.sweep()
    for tx in transmitters:
        if tx.target_info.owned_by != R.zone and tx.signal_strength < 10:
            targets.append(tx)
    print("I found", len(targets), "transmitter(s):")

    for tx in targets:
        print(" - Transmitter {0} Bearing: {1} with a signal strength of {2}".format(
            tx.target_info.station_code,
            tx.bearing,
            tx.signal_strength,
        ))
    return targets


def avoid_collision():
    """
    :return: None
    """
    if is_bumped(front_bumper):
        move(-100, 0.5)
    if is_bumped(rear_bumper):
        move(100, 0.5)


def avoid_obstacles():
    """
    :return: None
    """
    '''
    print("Obstacle detected: Moving away")
    dist = 1.7
    if not R.is_in_zone():
        while R._is_near(R.front_left_sensor, dist) and R._is_near(R.front_right_sensor, dist):
             R.move(R.reverse, 0.2)
             R.turn(R.left, 10)
             R.move(R.forward, 0.2)
    '''
    '''
        while R._is_near(R.back_left_sensor, dist) and R._is_near(R.back_right_sensor, dist):
             R.move(R.forward, 0.2)
             R.turn(R.right, 10)
             R.move(R.reverse, 0.2)
    '''
    if is_near(right_sensor):
        turn(left, 90)
    if is_near(left_sensor):
        turn(right, 90)


def is_bumped(bumper):
    """
    :param bumper: (int) Bump sensor pin on controlBoard
    :return: None
    """
    return controlBoard.digital_read(bumper)


def _is_near(sensor, dist=21):
    """
    :param sensor: sensor pin
    :param dist: (int) distance in mm to check for
    :return: (bool) whether its within that range
    """
    return get_dist_from(sensor) < dist


def is_movement_viable(dist=21):
    """
    :param dist: (int) distance in mm to check for
    :return: (bool) Whether R can move in the given direction
    """
    return not (is_near(front_left_sensor, dist) or is_near(front_right_sensor, dist))


def get_dist_from(sensor):
    """
    :param sensor (int) Sensor pin number on controlBoard.
    :return: (int) Distance in mm from sensor.
    """
    return controlBoard.analogue_read(sensor)


def claim_three_p():
    print(heading())
    a = (2.94 - heading() + 0.05) / (2 * math.pi)
    turnR(a * rev)
    print(heading())
    move(100, 1)
    t = get_transmitters()
    while t[0].target_info.station_code != "OX":
        t.pop(0)
    d = abs(t[0].bearing) / (2 * math.pi)
    if t[0].bearing < 0:
        turnL(d * rev)
    else:
        turnR(d * rev)
    while t[0].signal_strength < 5:
        ml.power = 90
        mr.power = 90
        t = get_transmitters()
    stop()
    claim('OX')
    move(-70, 0.45)
    t = R.radio.sweep()
    if t[0].bearing < -0.5:
        turnL(0.75, 10, 80)
    else:
        turnL(0.6, 10, 70)
    move(100, 1)
    d = abs((heading() - 1.39)) / (2 * math.pi)  # Turning until approx. 80 degrees (ENE)
    if heading() > math.pi * (4 / 9):
        turnL(d * rev)
    else:
        turnR(d * rev)
    move(100, 1.35)
    t = get_transmitters()  # Only at this point will it detect TS
    while t[0].target_info.station_code != "TS":
        t.pop(0)
    d = abs(t[0].bearing) / (2 * math.pi)
    if t[0].bearing < 0:
        turnL(d * rev)
    else:
        turnR(d * rev)
    while t[0].signal_strength < 5:
        ml.power = 90
        mr.power = 90
        t = get_transmitters()
    stop()
    claim('TS')
    if t[0].bearing < -0.5:  # After claiming, it might be on the right side of the tower or face southeast. 
        move(-100, 0.75)  # In this case, it should reverse more
    else:
        move(-100, 0.6)
    print(heading())
    d = (heading() - 0.2) / (2 * math.pi)  # Turning until approx. 40 degrees (NE)
    turnL(d * rev)
    print(heading())
    move(100, 1.5)
    t = get_transmitters()
    while t[0].target_info.station_code != "VB":
        t.pop(0)
    d = abs(t[0].bearing) / (2 * math.pi)
    if t[0].bearing < 0:
        turnL(d * rev)
    else:
        turnR(d * rev)
    while t[0].signal_strength < 5:
        ml.power = 90
        mr.power = 90
        t = get_transmitters()
        while t[0].target_info.station_code != "VB":
            t.pop(0)
    stop()
    claim('VB')


def claim_three_y():
    print(heading())
    a = abs((3.34 - heading() - 0.05)) / (2 * math.pi)
    turnL(a * rev)
    print(heading())
    move(100, 1)
    t = get_transmitters()
    while t[0].target_info.station_code != "BN":
        t.pop(0)
    d = abs(t[0].bearing) / (2 * math.pi)
    if t[0].bearing < 0:
        turnL(d * rev)
    else:
        turnR(d * rev)
    while t[0].signal_strength < 5:
        ml.power = 90
        mr.power = 90
        t = get_transmitters()
    stop()
    claim('BN')
    move(-70, 0.45)
    t = R.radio.sweep()
    if t[0].bearing > 0.5:
        turnL(0.6, 80, 10)
    else:
        turnL(0.6, 70, 10)
    move(100, 1)
    d = abs(heading() - 4.9) / (2 * math.pi)  # Turning until approx. 80 degrees (ENE)
    if heading() < math.pi * (14 / 9):
        turnR(d * rev)
    else:
        turnL(d * rev)
    move(100, 1.35)
    t = get_transmitters()  # Only at this point will it detect SW
    while t[0].target_info.station_code != "SW":
        t.pop(0)
    d = abs(t[0].bearing) / (2 * math.pi)
    if t[0].bearing < 0:
        turnL(d * rev)
    else:
        turnR(d * rev)
    while t[0].signal_strength < 5:
        ml.power = 90
        mr.power = 90
        t = get_transmitters()
    stop()
    claim('SW')
    if t[0].bearing > 0.5:  # After claiming, it might be on the left side of the tower or face southwest. 
        move(-100, 0.8)  # In this case, it should reverse more
    else:
        move(-100, 0.5)
    print(heading())
    d = abs(heading() - 6.1) / (2 * math.pi)  # Turning until approx. 340 degrees (NNW)
    turnR(d * rev)
    print(heading())
    move(100, 1.5)
    t = get_transmitters()
    while t[0].target_info.station_code != "SZ":
        t.pop(0)
    d = abs(t[0].bearing) / (2 * math.pi)
    if t[0].bearing < 0:
        turnL(d * rev)
    else:
        turnR(d * rev)
    while t[0].signal_strength < 5:
        ml.power = 90
        mr.power = 90
        t = get_transmitters()
        while t[0].target_info.station_code != "SZ":
            t.pop(0)
    stop()
    claim('SZ')


def wall_block(b):
    perim = 1.5
    if abs(b) <= math.pi * (5 / 18):
        return distance(0) < perim or distance(1) < perim
    elif b <= -1 * math.pi * (5 / 18) and b >= -1 * math.pi * (13 / 18):
        print("Distance to wall: ", distance(2))
        return distance(2) < perim
    elif abs(b) >= (13 / 18):
        return distance(4) < perim or distance(5) < perim
    else:
        return distance(3) < perim


def get_target():
    towers = get_transmitters()
    print(towers)
    for tower in towers:
        if tower.target_info.station_code in captured:  # A tower that the R previously claimed is now taken
            return tower.target_info.station_code
        else:
            invalid = True
            for item in captured:
                if tower.target_info.station_code in graph[item]:
                    invalid = False  # A tower can only be claimed if there is a direct link
                    break
            if invalid:
                towers.remove(tower)
    print(towers)
    for tower in towers:
        if R.zone == 0:
            if (tower.target_info.station_code != "HA" and wall_block(tower.bearing) == True) or (
                    tower.target_info.station_code in ("EY", "YT") and "HV" not in captured):
                if len(towers) > 1:
                    towers.remove(
                        tower)  # The left distance sensor does not detect that a wall is close after claiming HA
        else:
            if (tower.target_info.station_code != "HA" and wall_block(tower.bearing) == True) or (
                    tower.target_info.station_code in ("PO", "YT") and "BG" not in captured):
                if captured[-1] == "SZ" and tower.target_info.station_code in ("HV", "PO"):
                    towers.remove(tower)
                else:
                    if len(towers) > 1:
                        towers.remove(tower)
    print(towers)
    if R.zone == 0:
        if captured[-1] == "SW":
            return "HV"
        elif captured[-1] == "HV":
            return "PO"
        else:
            closest = towers[0]
            for tower in towers:
                if tower.signal_strength > closest.signal_strength and tower.target_info.station_code not in captured:
                    closest = tower
            return closest.target_info.station_code
    else:
        if captured[-1] == "TS":
            return "BG"
        elif captured[-1] == "BG":
            return "EY"
        else:
            closest = towers[0]
            for tower in towers:
                if tower.signal_strength > closest.signal_strength and tower.target_info.station_code not in captured:
                    closest = tower
            return closest.target_info.station_code


rev = 2
captured = []
if R.zone == 0:
    captured.append('0')  # The R must check which towers connect to its starting zone
    claim_three_p()
    move(-100, 0.7)
    turnR(0.6, 70, 10)
    move(100, 0.7)
    next_tower = get_target()
else:
    captured.append('1')
    claim_three_y()
    move(-100, 0.7)
    turnL(0.6, 10, 70)
    move(100, 0.7)
    next_tower = get_target()

while True:
    if R.zone == 0:
        if captured[-1] not in ("VB", "SZ", "PL", "HV", "SW", "YL", "EY", "FL"):
            move(-100, 0.49)
    else:
        if captured[-1] not in ("SZ", "VB", "PL", "BG", "TS", "PN", "HA", "PO"):
            move(-100, 0.49)

    print("Target is ", next_tower)
    t = get_transmitters()
    while t[0].target_info.station_code != next_tower:
        t.pop(0)
        if len(t) == 0:
            next_tower = get_target()
            t = get_transmitters()
    d = (abs(t[0].bearing) / (2 * math.pi)) * rev
    if t[0].bearing < 0:
        turnL(d)
    else:
        turnR(d)
    while t[0].signal_strength < 5:
        ml.power = 100
        mr.power = 100
        t = get_transmitters()
        while t[0].target_info.station_code != next_tower:
            t.pop(0)
    stop()
    claim(next_tower)

    if R.zone == 0:
        if captured[-1] == "SZ":
            move(-100, 0.49)
            turnR(rev / 4)
            move(100, 0.7)
            if "PL" in captured:  # Get closer to BN
                turnL(rev / 6)
                move(100, 2.5)
        elif captured[-1] == "PL":
            move(-100, 0.7)
            if heading() < math.pi:
                move(-100, 0.3)
                d = (heading() + 0.1) / (2 * math.pi)  # Turning until approx. 0 degrees (N)
                turnL(d * rev)
                move(100, 0.6)
            elif "SZ" not in captured:
                turnL(rev * (5 / 12))
                move(100, 0.7)
            if "SZ" in captured:  # Get closer to BN
                d = (heading() - 0.75) / (2 * math.pi)  # Turning until approx. 45 degrees (NE)
                turnL(d * rev)
                move(100, 0.5)
                turnR(rev / 8)
                move(100, 1.3)
                turnR(rev / 8)
                move(100, 1.3)
        elif captured[-1] == "BN":  # Get closer to SW
            move(-100, 1.5)
        elif captured[-1] == "SW":  # Get closer to HV (The arena walls have fallen)
            if heading() > 4.7:
                move(-100, 0.5)
                turnR(rev / 3)
                move(100, 2)
            else:
                move(-100, 2)
                d = (5.8 - heading()) / (2 * math.pi)  # Turning until approx. 315 degrees (NW)
                turnR(d * rev)
                move(100, 1.5)
        elif captured[-1] == "HV":  # Manoeuvre to top of arena
            move(-100, 1)
            turnR(rev / 6)
            move(100, 1.7)
            turnL(rev / 3)
            move(100, 1.6)
            d = abs((heading() - 4.7)) / (2 * math.pi)  # Turning until approx. 270 degrees (W)
            turnL(d * rev)
            move(100, 1)
        elif captured[-1] == "YL":
            move(-100, 1)
            turnL(rev / 2.5)
            move(100, 0.7)
        elif captured[-1] == "FL":
            move(-100, 0.5)
            d = (heading() - 4.7) / (2 * math.pi)  # Turning until approx. 270 degrees (W)
            turnL(d * rev)
            move(100, 1)
        elif captured[-1] == "EY":
            move(-100, 0.7)
            turnR(rev / 6)
            move(100, 1)
    else:
        if captured[-1] == "VB":
            move(-100, 0.49)
            turnL(rev / 4)
            move(100, 0.7)
            if "PL" in captured:  # Get closer to OX
                turnR(rev / 6)
                move(100, 2.5)
        elif captured[-1] == "PL":
            move(-100, 0.7)
            if heading() > math.pi:
                move(-100, 0.3)
                d = (heading()) / (2 * math.pi)  # Turning until approx. 0 degrees (N)
                turnR(d * rev)
                move(100, 0.6)
            elif "VB" not in captured:
                turnR(rev * (5 / 12))
                move(100, 0.7)
            if "VB" in captured:  # Get closer to OX
                d = abs(heading() - 5.6) / (2 * math.pi)  # Turning until approx. 315 degrees (NW)
                turnR(d * rev)
                move(100, 0.5)
                turnL(rev / 8)
                move(100, 1.3)
                turnL(rev / 7)
                move(100, 1.5)
        elif captured[-1] == "OX":  # Get closer to TS
            move(-100, 1.5)
        elif captured[-1] == "TS":  # Get closer to BG (The arena walls have fallen)
            if heading() < 1.6:
                move(-100, 0.5)
                turnL(rev / 3)
                move(100, 2)
            else:
                move(-100, 2)
                d = abs(0.5 - heading()) / (2 * math.pi)  # Turning until approx. 30 degrees (NE)
                turnL(d * rev)
                move(100, 1.5)
        elif captured[-1] == "BG":  # Manoeuvre to top of arena
            move(-100, 1)
            turnL(rev / 6)
            move(100, 1.7)
            turnR(rev / 3)
            move(100, 1.6)
            d = abs((heading() - 1.57)) / (2 * math.pi)  # Turning until approx. 270 degrees (W)
            turnR(d * rev)
            move(100, 1)
        elif captured[-1] == "PN":
            move(-100, 1)
            turnR(rev / 2.5)
            move(100, 0.7)
        elif captured[-1] == "FL":
            move(-100, 0.5)
            turnR(rev / 4)
            move(100, 1)
        elif captured[-1] == "HA":
            move(-100, 0.5)
            turnL(0.4)
            move(100, 0.4)
        elif captured[-1] == "PO":
            move(-100, 0.5)
            turnL(rev / 5)
            move(100, 0.5)

    next_tower = get_target()
