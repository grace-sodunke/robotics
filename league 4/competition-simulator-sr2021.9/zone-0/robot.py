from olavian_robot import *
import math

robot = OlavianRobot()

# Constants and Variables Initialisation -------------------------------------------------------------------------------
forward = robot.forward
reverse = robot.reverse
right = robot.right
left = robot.left
smooth = robot.smooth_brake
front = robot.front_bumper
rear = robot.rear_bumper
on = robot.on
off = robot.off
wait = robot.wait
red = robot.red
green = robot.green
blue = robot.blue
owned = robot.owned

rev = robot.rev_const
dont_brake = robot.dont_brake

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


# Additional required procedures/functions -----------------------------------------------------------------------------

def get_transmitters():
    targets = []
    transmitters = robot.radio.sweep()
    for tx in transmitters:
        if tx.target_info.owned_by != robot.zone and tx.signal_strength < 10:
            targets.append(tx)
    print("I found", len(targets), "transmitter(s):")

    for tx in targets:
        print(" - Transmitter {0} Bearing: {1} with a signal strength of {2}".format(
            tx.target_info.station_code,
            tx.bearing,
            tx.signal_strength,
        ))
    return targets


def claim_three_p():
    print(robot.heading())
    a = (2.94 - robot.heading() + 0.05) / (2 * math.pi)
    robot.turnR(a * rev)
    print(robot.heading())
    robot.move(forward, 2.2, 100)
    robot.claim('OX')
    print("Claimed OX")
    robot.move(reverse, 0.35, 70)
    t = robot.radio.sweep()
    if t[0].bearing < -0.5:
        robot.turn(0.75, 10, 80)
    else:
        robot.turnL(0.6, 10, 70)
    robot.move(forward, 1)
    d = abs((robot.heading() - 1.39)) / (2 * math.pi)  # Turning until approx. 80 degrees (ENE)
    if robot.heading() > math.pi * (4 / 9):
        robot.turnL(d * rev)
    else:
        robot.turnR(d * rev)
    robot.move(forward, 1.35)
    t = get_transmitters()  # Only at this point will it detect TS
    while t[0].target_info.station_code != "TS":
        t.pop(0)
    d = abs(t[0].bearing) / (2 * math.pi)
    if t[0].bearing < 0:
        robot.turnL(d * rev)
    else:
        robot.turnR(d * rev)
    while t[0].signal_strength < 5:
        robot.move(forward, 0.1, 90)
        t = get_transmitters()
    robot.brake(0.25)
    robot.claim('TS')
    if t[0].bearing < -0.5:  # After claiming, it might be on the right side of the tower or face southeast.
        robot.move(reverse, 0.75, 100)  # In this case, it should reverse more
    else:
        robot.move(reverse, 0.45, 100)
    print(robot.heading())
    d = (robot.heading() - 0.45) / (2 * math.pi)  # Turning until approx. 40 degrees (NE)
    robot.turnL(d * rev)
    print(robot.heading())
    robot.move(forward, 1.5, 100)
    t = get_transmitters()
    while t[0].target_info.station_code != "VB":
        t.pop(0)
    d = abs(t[0].bearing) / (2 * math.pi)
    if t[0].bearing < 0:
        robot.turnL(d * rev)
    else:
        robot.turnR(d * rev)
    while t[0].signal_strength < 5:
        robot.move(forward, 0.1, 90)
        t = get_transmitters()
        while t[0].target_info.station_code != "VB":
            t.pop(0)
    robot.brake(0.25)
    robot.claim('VB')


<<<<<<< HEAD
def claim_three_y():
    print(robot.heading())
    a = abs((3.34 - robot.heading() - 0.05)) / (2 * math.pi)
    robot.turnL(a * rev)
    print(robot.heading())
    robot.move(forward, 2.2, 100)
    robot.claim('BN')
    robot.move(reverse, 0.4, 70)
    t = robot.radio.sweep()
    if t[0].bearing > 0.5:
        robot.turnL(0.6, 80, 10)
    else:
        robot.turnL(0.6, 70, 10)
    robot.move(forward, 1, 100)
    d = abs(robot.heading() - 4.9) / (2 * math.pi)  # Turning until approx. 80 degrees (ENE)
    if robot.heading() < math.pi * (14 / 9):
        robot.turnR(d * rev)
    else:
        robot.turnL(d * rev)
    robot.move(forward, 1.35, 100)
    t = get_transmitters()  # Only at this point will it detect SW
    while t[0].target_info.station_code != "SW":
        t.pop(0)
    d = abs(t[0].bearing) / (2 * math.pi)
    if t[0].bearing < 0:
        robot.turnL(d * rev)
    else:
        robot.turnR(d * rev)
    while t[0].signal_strength < 5:
        robot.move(forward, 0.1, 90)
        t = get_transmitters()
    robot.brake(0.25)
    robot.claim('SW')
    if t[0].bearing > 0.5:  # After claiming, it might be on the left side of the tower or face southwest.
        robot.move(reverse, 0.8, 100)  # In this case, it should reverse more
    else:
        robot.move(reverse, 0.5, 100)
    print(robot.heading())
    d = abs(robot.heading() - 6) / (2 * math.pi)  # Turning until approx. 340 degrees (NNW)
    robot.turnR(d * rev)
    print(robot.heading())
    robot.move(forward, 1.5, 100)
    t = get_transmitters()
    while t[0].target_info.station_code != "SZ":
        t.pop(0)
    d = abs(t[0].bearing) / (2 * math.pi)
    if t[0].bearing < 0:
        robot.turnL(d * rev)
    else:
        robot.turnR(d * rev)
    while t[0].signal_strength < 5:
        robot.move(forward, 0.1, 90)
        t = get_transmitters()
        while t[0].target_info.station_code != "SZ":
            t.pop(0)
    robot.brake(0.25)
    robot.claim('SZ')
=======
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
	d = abs((heading() - 1.39)) / (2 * math.pi) # Turning until approx. 80 degrees (ENE)
	if heading() > math.pi * (4/9):
		turnL(d * rev)
	else:
		turnR(d * rev)
	move(100, 1.35)
	t = get_transmitters() # Only at this point will it detect TS
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
	if t[0].bearing < -0.5: # After claiming, it might be on the right side of the tower or face southeast. 
		move(-100, 0.75) # In this case, it should reverse more
	else:
		move(-100, 0.6) 
	print(heading())
	d = (heading() - 0.2) / (2 * math.pi) # Turning until approx. 40 degrees (NE)
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
	d = abs(heading() - 4.9) / (2 * math.pi) # Turning until approx. 80 degrees (ENE)
	if heading() < math.pi * (14/9):
		turnR(d * rev)
	else:
		turnL(d * rev)
	move(100, 1.35)
	t = get_transmitters() # Only at this point will it detect SW
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
	if t[0].bearing > 0.5: # After claiming, it might be on the left side of the tower or face southwest. 
		move(-100, 0.8) # In this case, it should reverse more
	else:
		move(-100, 0.5) 
	print(heading())
	d = abs(heading() - 6.1) / (2 * math.pi) # Turning until approx. 340 degrees (NNW)
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
>>>>>>> 4df46e89de08a4fad499a6016dcdc53c7a3f81c7


def wall_block(b):
    perimeter = 1.5
    if abs(b) <= math.pi * (5 / 18):
        return robot.get_dist(0) < perimeter or robot.get_dist(1) < perimeter
    elif -1 * math.pi * (5 / 18) >= b >= -1 * math.pi * (13 / 18):
        print("robot.get_dist to wall: ", robot.get_dist(2))
        return robot.get_dist(2) < perimeter
    elif abs(b) >= (13 / 18):
        return robot.get_dist(4) < perimeter or robot.get_dist(5) < perimeter
    else:
        return robot.get_dist(3) < perimeter


def get_target():
    towers = get_transmitters()
    print(towers)
    for tower in towers:
        if tower.target_info.station_code in robot.captured:  # A tower that the robot previously claimed is now taken
            return tower.target_info.station_code
        else:
            invalid = True
            for item in robot.captured:
                if tower.target_info.station_code in graph[item]:
                    invalid = False  # A tower can only be claimed if there is a direct link
                    break
            if invalid:
                towers.remove(tower)
    print(towers)
    for tower in towers:
        if robot.zone == 0:
            if (tower.target_info.station_code != "HA" and wall_block(tower.bearing) is True) or (
                    tower.target_info.station_code in ("EY", "YT") and "HV" not in robot.captured):
                if len(towers) > 1:
                    towers.remove(
                        tower)  # The left robot.get_dist sensor does not detect that a wall is close after claiming HA
        else:
            if (tower.target_info.station_code != "HA" and wall_block(tower.bearing) is True) or (
                    tower.target_info.station_code in ("PO", "YT") and "BG" not in robot.captured):
                if robot.captured[-1] == "SZ" and tower.target_info.station_code in ("HV", "PO"):
                    towers.remove(tower)
                else:
                    if len(towers) > 1:
                        towers.remove(tower)
    print(towers)
    if robot.zone == 0:
        if robot.captured[-1] == "SW":
            return "HV"
        elif robot.captured[-1] == "HV":
            return "PO"
        else:
            closest = towers[0]
            for tower in towers:
                if tower.signal_strength > closest.signal_strength and tower.target_info.station_code not in robot.captured:
                    closest = tower
            return closest.target_info.station_code
    else:
        if robot.captured[-1] == "TS":
            return "BG"
        elif robot.captured[-1] == "BG":
            return "EY"
        else:
            closest = towers[0]
            for tower in towers:
                if tower.signal_strength > closest.signal_strength and tower.target_info.station_code not in robot.captured:
                    closest = tower
            return closest.target_info.station_code

if robot.zone == 0:
    robot.captured.append('0')  # The robot must check which towers connect to its starting zone
    claim_three_p()
    robot.move(reverse, 0.7, 100)
    robot.turnR(0.6, 70, 10)
    robot.move(forward, 0.7, 100)
    robot.next_tower = get_target()
else:
    robot.captured.append('1')
    claim_three_y()
    robot.move(reverse, 0.7, 100)
    robot.turnL(0.6, 10, 70)
    robot.move(forward, 0.7, 100)
    robot.next_tower = get_target()


while True:
    if robot.zone == 0:
        if robot.captured[-1] not in ("VB", "SZ", "PL", "HV", "SW", "YL", "EY", "FL"):
            robot.move(reverse, 0.49, 100)
    else:
        if robot.captured[-1] not in ("SZ", "VB", "PL", "BG", "TS", "PN", "HA", "PO"):
            robot.move(reverse, 0.49, 100)
    print("Target is ", robot.next_tower)
    t = get_transmitters()
    while t[0].target_info.station_code != robot.next_tower:
        t.pop(0)
        if len(t) == 0:
            robot.next_tower = get_target()
            t = get_transmitters()
    d = (abs(t[0].bearing) / (2 * math.pi)) * rev
    if t[0].bearing < 0:
        robot.turnL(d)
    else:
        robot.turnR(d)
    while t[0].signal_strength < 5:
        robot.move(forward, 0.1)
        t = get_transmitters()
        while t[0].target_info.station_code != robot.next_tower:
            t.pop(0)
    robot.brake(0.25)
    robot.claim(robot.next_tower)

    if robot.zone == 0:
        if robot.captured[-1] == "SZ":
            robot.move(reverse, 0.49)
            robot.turnR(rev / 4)
            robot.move(forward, 0.7)
            if "PL" in robot.captured:  # Get closer to BN
                robot.turnL(rev / 6)
                robot.move(forward, 2.5)
        elif robot.captured[-1] == "PL":
            robot.move(reverse, 0.7)
            if robot.heading() < math.pi:
                robot.move(reverse, 0.3)
                d = (robot.heading() + 0.1) / (2 * math.pi)  # Turning until approx. 0 degrees (N)
                robot.turnL(d * rev)
                robot.move(forward, 0.6)
            elif "SZ" not in robot.captured:
                robot.turnL(rev * (5 / 12))
                robot.move(forward, 0.7)
            if "SZ" in robot.captured:  # Get closer to BN
                d = (robot.heading() - 0.75) / (2 * math.pi)  # Turning until approx. 45 degrees (NE)
                robot.turnL(d * rev)
                robot.move(forward, 0.5)
                robot.turnR(rev / 8)
                robot.move(forward, 1.3)
                robot.turnR(rev / 8)
                robot.move(forward, 1.3)
        elif robot.captured[-1] == "BN":  # Get closer to SW
            robot.move(reverse, 1.5)
        elif robot.captured[-1] == "SW":  # Get closer to HV (The arena walls have fallen)
            if robot.heading() > 4.7:
                robot.move(reverse, 0.5)
                robot.turnR(rev / 3)
                robot.move(forward, 2)
            else:
                robot.move(reverse, 2)
                d = (5.8 - robot.heading()) / (2 * math.pi)  # Turning until approx. 315 degrees (NW)
                robot.turnR(d * rev)
                robot.move(forward, 1.5)
        elif robot.captured[-1] == "HV":  # Manoeuvre to top of arena
            robot.move(reverse, 1)
            robot.turnR(rev / 6)
            robot.move(forward, 1.7)
            robot.turnL(rev / 3)
            robot.move(forward, 1.6)
            d = abs((robot.heading() - 4.7)) / (2 * math.pi)  # Turning until approx. 270 degrees (W)
            robot.turnL(d * rev)
            robot.move(forward, 1)
        elif robot.captured[-1] == "YL":
            robot.move(reverse, 1)
            robot.turnL(rev / 2.5)
            robot.move(forward, 0.7)
        elif robot.captured[-1] == "FL":
            robot.move(reverse, 0.5)
            d = (robot.heading() - 4.7) / (2 * math.pi)  # Turning until approx. 270 degrees (W)
            robot.turnL(d * rev)
            robot.move(forward, 1)
        elif robot.captured[-1] == "EY":
            robot.move(reverse, 0.7)
            robot.turnR(rev / 6)
            robot.move(forward, 1)
    else:
        if robot.captured[-1] == "VB":
            robot.move(reverse, 0.49)
            robot.turnL(rev / 4)
            robot.move(forward, 0.7)
            if "PL" in robot.captured:  # Get closer to OX
                robot.turnR(rev / 6)
                robot.move(forward, 2.5)
        elif robot.captured[-1] == "PL":
            robot.move(reverse, 0.7)
            if robot.heading() > math.pi:
                robot.move(reverse, 0.3)
                d = (robot.heading()) / (2 * math.pi)  # Turning until approx. 0 degrees (N)
                robot.turnR(d * rev)
                robot.move(forward, 0.6)
            elif "VB" not in robot.captured:
                robot.turnR(rev * (5 / 12))
                robot.move(forward, 0.7)
            if "VB" in robot.captured:  # Get closer to OX
                d = abs(robot.heading() - 5.6) / (2 * math.pi)  # Turning until approx. 315 degrees (NW)
                robot.turnR(d * rev)
                robot.move(forward, 0.5)
                robot.turnL(rev / 8)
                robot.move(forward, 1.3)
                robot.turnL(rev / 7)
                robot.move(forward, 1.5)
        elif robot.captured[-1] == "OX":  # Get closer to TS
            robot.move(reverse, 1.5)
        elif robot.captured[-1] == "TS":  # Get closer to BG (The arena walls have fallen)
            if robot.heading() < 1.6:
                robot.move(reverse, 0.5)
                robot.turnL(rev / 3)
                robot.move(forward, 100, 2)
            else:
                robot.move(reverse, 2)
                d = abs(0.5 - robot.heading()) / (2 * math.pi)  # Turning until approx. 30 degrees (NE)
                robot.turnL(d * rev)
                robot.move(forward, 1.5)
        elif robot.captured[-1] == "BG":  # Manoeuvre to top of arena
            robot.move(reverse, 1)
            robot.turnL(rev / 6)
            robot.move(forward, 1.7)
            robot.turnR(rev / 3)
            robot.move(forward, 1.6)
            d = abs((robot.heading() - 1.57)) / (2 * math.pi)  # Turning until approx. 270 degrees (W)
            robot.turnR(d * rev)
            robot.move(forward, 1)
        elif robot.captured[-1] == "PN":
            robot.move(reverse, 1)
            robot.turnR(rev / 2.5)
            robot.move(forward, 0.7)
        elif robot.captured[-1] == "FL":
            robot.move(reverse, 0.5)
            robot.turnR(rev / 4)
            robot.move(forward, 1)
        elif robot.captured[-1] == "HA":
            robot.move(reverse, 0.5)
            robot.turnL(0.4)
            robot.move(forward, 0.4)
        elif robot.captured[-1] == "PO":
            robot.move(reverse, 0.5)
            robot.turnL(rev / 5)
            robot.move(forward, 0.5)
    robot.next_tower = get_target()

robot.halt()
