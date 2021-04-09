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

R = Robot()
ml = R.motors[0].m0 # motor board 0, channel 0
mr = R.motors[0].m1 # motor board 0, channel 1

def claim(tower):
	R.radio.claim_territory()
	captured.append(tower)

def stop():
	ml.power = 0
	mr.power = 0
	sleep(0.25)
	#collide_detect()

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

def turnL(t, a = -50, b = 50):
	ml.power = a
	mr.power = b
	sleep(t)
	stop()

def turnR(t, a = 50, b = -50):
	ml.power = a
	mr.power = b
	sleep(t)
	stop()

def get_transmitters():
	targets = []
	transmitters = R.radio.sweep()
	for tx in transmitters:
		if tx.target_info.owned_by != R.zone:
			targets.append(tx)
	print("I found", len(targets), "transmitter(s):")

	for tx in targets:
		print(" - Transmitter {0} Bearing: {1} with a signal strength of {2}".format(
			tx.target_info.station_code,
			tx.bearing,
			tx.signal_strength,
		))
	return targets

def claim_three():
	if R.zone == 0:
		turnR(0.46)
		move(70, 3.1)
		claim('OX')
		move(-70, 0.3)
		t = R.radio.sweep()
		if t[0].bearing < -0.5:
			turnL(0.7, 10, 80)
		else:
			turnL(0.6, 10, 70)
		move(70, 1.5)
		if heading() > math.pi * (5/9):
			turnL(0.2)
		else:
			turnL(0.1)
		move(70, 2)
		t = get_transmitters() # Only at this point will it detect TS
		while t[0].target_info.station_code != "TS":
			t.pop(0)
		if t[0].bearing > math.pi * (2/9):
			turnR(0.2)
		else:
			turnR(0.1)
		while t[0].signal_strength < 5:
			ml.power = 70
			mr.power = 70
			t = get_transmitters()
		stop()
		claim('TS')
		if t[0].bearing < -0.5: # After claiming, it might be on the right side of the tower or face southeast. 
			move(-70, 1) # In this case, it should reverse more and curve to the left side
			turnL(0.7, 10, 70)
			move(70, 2.4)
		elif heading() > math.pi * (5/9):
			move(-70, 0.5)
			turnL(0.7, 10, 70)
			move(70, 2.2)
		else:
			move(-70, 0.5)
			turnL(0.6, 10, 70)
			move(70, 2.2)
		claim('VB')
		# Should take about 21.7s to claim first three
		# Still need to test 100000 times and fix everywhere it goes wrong

def wall_block(b):
	perim = 1.5
	if b >= -1 * math.pi * (5 / 18) and b <= math.pi * (5 / 18):
		return distance(0) < perim or distance(1) < perim
	elif b <= -1 * math.pi * (5 / 18) and b >= -1 * math.pi * (13 / 18):
		print("Distance to wall: ", distance(2))
		return distance(2) < perim
	elif b <= -1 * math.pi * (13 / 18) or b >= math.pi * (13 / 18):
		return distance(4) < perim or distance(5) < perim
	else:
		return distance(3) < perim

def get_target():
	towers = get_transmitters()
	print(towers)
	for tower in towers:
		if tower.target_info.station_code in captured: # A tower that the robot previously claimed is now taken
			return tower.target_info.station_code
		else:
			invalid = True
			for item in captured:
				if tower.target_info.station_code in graph[item]:
					invalid = False # A tower can only be claimed if there is a direct link
					break
			if invalid:
				towers.remove(tower)
	print(towers)
	for tower in towers:
		if tower.target_info.station_code != "HA" and wall_block(tower.bearing) == True or tower.target_info.station_code in ("EY", "YT"): # HA is never obstructed by a wall
			towers.remove(tower) # The left distance sensor is not accurate enough to detect that a wall is close after claiming HA
	print(towers)
	closest = towers[0]
	for tower in towers:
		if tower.signal_strength > closest.signal_strength and tower.target_info.station_code not in captured: # It has once tried to reclaim HA?
			closest = tower
	return closest.target_info.station_code

rev = 2.1
captured = []
claim_three()


if R.zone == 0:
	move(-70, 1)
	turnR(0.6, 70, 10)
	move(70, 1)
	next_tower = get_target()
	while True:
		if captured[-1] not in ("VB", "SZ", "PL"):
			move(-70, 0.7)
		print("Target is ", next_tower)
		t = get_transmitters()
		while t[0].target_info.station_code != next_tower:
			t.pop(0)
		d = (abs(t[0].bearing) / (2 * math.pi)) * rev
		if t[0].bearing < 0:
			turnL(d)
		else:
			turnR(d)
		while t[0].signal_strength < 5.5:
			ml.power = 70
			mr.power = 70
			t = get_transmitters()
			while t[0].target_info.station_code != next_tower:
				t.pop(0)
		stop()
		claim(next_tower)
		if captured[-1] == "SZ":
			move(-70, 0.7)
			turnR(rev / 4)
			move(70, 1)
		elif captured[-1] == "PL":
			move(-70, 0.7)
			turnL(rev * (5/12))
			move(70, 1)
		next_tower = get_target()
		
