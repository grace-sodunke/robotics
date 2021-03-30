from sr.robot import *
import math

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
	collide_detect()

def sleep(t):
	R.sleep(t)

def move(p):
	ml.power = p
	mr.power = p
	
def distance(p):
	return R.ruggeduinos[0].analogue_read(p)

def bump(s):
	return R.ruggeduinos[0].digital_read(s)

def turnL(t):
	ml.power = -50
	mr.power = 50
	sleep(t)
	stop()

def turnR(t):
	ml.power = 50
	mr.power = -50
	sleep(t)
	stop()

def swerve(d = 'r'): # default is swerving to the right
	move(-50)
	sleep(0.2)
	stop()
	t = (1 / 8) * rev #turn for 30 degrees
	if d == 'l':
		turnL(t)
	else:
		turnR(t)
	move(50)
	sleep(0.9)
	stop()
	if d == 'l':
		turnR(t)
	else:
		turnL(t)
	move(50)
	sleep(0.8)
	stop()

def collide_detect():
	t = []
	ts = R.radio.sweep()
	for a in ts:
		t.append(a.target_info.station_code)
	i = 0
	if bump(2) == True:
		if R.zone == 0:
			try: #need to make this bit more efficient
				i = t.index(captured[-1]) #if it's hit a tower, find the tower it's collided with
				move(-50)
				sleep(0.25)
				stop()
				if (tower == "BE" and captured[-1] == "SZ") or captured[-1] == "TS":
					turnR(rev / 4)
				elif t[i].signal_strength > 5.5: 
					turnR(rev / 4) #if it bumps into a tower outside of alcove and not a wall
				else:
					turnL(rev / 4)
				move(50)
				sleep(1.3)
				stop()
			except:
				move(-50)
				sleep(0.25)
				stop()
				if tower == "BE" and captured[-1] == "SZ":
					turnR(rev / 4)
				else:
					turnL(rev / 4)
				move(50)
				sleep(1.3)
				stop()
		else:
			try: #need to make this bit more efficient
				i = t.index(captured[-1]) #if it's hit a tower, find the tower it's collided with
				move(-50)
				sleep(0.25)
				stop()
				if (tower == "BE" and captured[-1] == "VB") or captured[-1] == "SW":
					turnL(rev / 4)
				elif t[i].signal_strength > 5.5: 
					turnL(rev / 4) #if it bumps into a tower outside of alcove and not a wall
				else:
					turnR(rev / 4)
				move(50)
				sleep(1.3)
				stop()
			except:
				move(-50)
				sleep(0.25)
				stop()
				if tower == "BE" and captured[-1] == "VB":
					turnL(rev / 4)
				else:
					turnR(rev / 4)
				move(50)
				sleep(1.3)
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

rev = 2.125
captured = []
tower = ""
def check_wall(b):
	perim = 1.5
	if b >= -1 * math.pi * (5 / 18) and b <= math.pi * (5 / 18):
		return distance(0) < perim or distance(1) < perim
	elif b <= -1 * math.pi * (5 / 18) and b >= -1 * math.pi * (13 / 18):
		return distance(2) < perim
	elif b <= -1 * math.pi * (13 / 18) or b >= math.pi * (13 / 18):
		return distance(4) < perim or distance(5) < perim
	else:
		return distance(3) < perim

def claim_alcove():
	transmitters = get_transmitters()
	if transmitters[0].target_info.station_code == "PN":
		t = (abs(transmitters[0].bearing) / (2 * math.pi)) * rev
		turnL(t)
		while transmitters[0].signal_strength < 5.75:
			move(50)
			transmitters = get_transmitters()
			while transmitters[0].target_info.station_code != "PN":
				transmitters.pop(0)
		stop()
		claim("PN")
		swerve()
		transmitters = get_transmitters()
		while transmitters[0].target_info.station_code != "EY":
			transmitters.pop(0)
		t = (abs(transmitters[0].bearing) / (2 * math.pi)) * rev
		turnL(t)
		while transmitters[0].signal_strength < 5.75:
			move(50)
			transmitters = get_transmitters()
			while transmitters[0].target_info.station_code != "EY":
				transmitters.pop(0)
		stop()
		claim("EY")
		swerve()
		turnR(rev / 30)
		i = 0
		hasTurned = False
		while i < 5.9:
			move(-50)
			sleep(0.1)
			i += 0.1
			print(distance(3))
			if distance(3) < 0.1 and hasTurned == False:
				stop()
				move(50)
				sleep(0.6)
				stop()
				turnR(rev / 20)
				hasTurned = True
		stop()
		turnR(rev * (3/16))
		move(50)
		sleep(1.5)
		stop()
	else:
		transmitters = get_transmitters()
		t = (abs(transmitters[0].bearing) / (2 * math.pi)) * rev
		turnR(t)
		while transmitters[0].signal_strength < 5.75:
			move(50)
			transmitters = get_transmitters()
			while transmitters[0].target_info.station_code != "YL":
				transmitters.pop(0)
		stop()
		claim("YL")
		swerve('l')
		transmitters = get_transmitters()
		while transmitters[0].target_info.station_code != "PO":
			transmitters.pop(0)
		t = (abs(transmitters[0].bearing) / (2 * math.pi)) * rev
		turnR(t)
		while transmitters[0].signal_strength < 5.75:
			move(50)
			transmitters = get_transmitters()
			while transmitters[0].target_info.station_code != "PO":
				transmitters.pop(0)
		stop()
		claim("PO")
		swerve('l')
		turnL(rev / 24)
		i = 0
		hasTurned = False
		while i < 5.9:
			move(-50)
			sleep(0.1)
			i += 0.1
			print(distance(3))
			if distance(2) < 0.1 and hasTurned == False:
				stop()
				move(50)
				sleep(0.75)
				stop()
				turnL(rev / 20)
				hasTurned = True
		stop()
		turnL(rev * (3/16))
		move(50)
		sleep(1.5)
		stop()

claim_alcove()
if R.zone == 0:
	while True:
		transmitters = get_transmitters()
		if len(transmitters) == 0: 
			move(50)
			sleep(2)
			stop()
			continue # If the list of current targets is empty, it should move forward to a new area
		inWay = True
		while inWay:
			if captured[-1] == "SZ":
				break
			for tx in transmitters:
				inWay = check_wall(tx.bearing)
				if inWay:
					transmitters.remove(tx)
			if len(transmitters) == 0:
				break
		if len(transmitters) == 0:
			move(50)
			sleep(2)
			stop()
			continue
		tower = transmitters[0].target_info.station_code
		t = (abs(transmitters[0].bearing) / (2 * math.pi)) * rev
		if transmitters[0].bearing < 0:
			turnL(t)
		else:
			turnR(t)
		while transmitters[0].signal_strength < 5.75:
			move(50)
			collide_detect()
			transmitters = get_transmitters()
			while transmitters[0].target_info.station_code != tower:
				transmitters.pop(0)
		stop()
		claim(tower)
		if tower == "OX":# If it has just claimed OX, it should not swerve and should just reverse a bit then turn around
			move(-50)
			sleep(0.5)
			stop()
			turnL(rev / 4)
		elif tower == "PO":
			move(-50)
			sleep(0.5)
			stop()
			turnR(rev / 4)
		elif captured[-1] == "SZ" and "BE" not in captured:
			move(-50)
			sleep(0.5)
			stop()
			turnL(rev / 4)
			move(50)
			sleep(0.7)
		elif tower == "BE":
			move(-50)
			sleep(1.3)
			stop()
			turnR(rev * (7/24))
		elif tower == "TS": # It should never go to left even if bearing > 0
			swerve()
		elif transmitters[0].bearing > 0: 
			swerve('l')
		else:
			swerve()
else:
	while True:
		transmitters = get_transmitters()
		if len(transmitters) == 0: 
			move(50)
			sleep(2)
			stop()
			continue # If the list of current targets is empty, it should move forward to a new area
		inWay = True
		while inWay:
			if captured[-1] == "VB":
				break
			for tx in transmitters:
				inWay = check_wall(tx.bearing)
				if inWay:
					transmitters.remove(tx)
			if len(transmitters) == 0:
				break
		if len(transmitters) == 0:
			move(50)
			sleep(2)
			stop()
			continue
		tower = transmitters[0].target_info.station_code
		t = (abs(transmitters[0].bearing) / (2 * math.pi)) * rev
		if transmitters[0].bearing < 0:
			turnL(t)
		else:
			turnR(t)
		while transmitters[0].signal_strength < 5.75:
			move(50)
			collide_detect()
			transmitters = get_transmitters()
			while transmitters[0].target_info.station_code != tower:
				transmitters.pop(0)
		stop()
		claim(tower)
		if tower == "BN":# If it has just claimed OX, it should not swerve and should just reverse a bit then turn around
			move(-50)
			sleep(0.5)
			stop()
			turnR(rev / 4)
		elif tower == "EY":
			move(-50)
			sleep(0.5)
			stop()
			turnL(rev / 4)
		elif captured[-1] == "VB" and "BE" not in captured:
			move(-50)
			sleep(0.5)
			stop()
			turnR(rev / 4)
			move(50)
			sleep(0.7)
		elif tower == "BE":
			move(-50)
			sleep(1.3)
			stop()
			turnL(rev * (7/24))
		elif tower == "SW": # It should never go to right even if bearing < 0
			swerve('l')
		elif transmitters[0].bearing > 0: 
			swerve('l')
		else:
			swerve()



