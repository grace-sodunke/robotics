from sr.robot import *
import math

R = Robot()
ml = R.motors[0].m0 # motor board 0, channel 0
mr = R.motors[0].m1 # motor board 0, channel 1

captured = []

def claim():
	R.radio.claim_territory()

def stop():
	ml.power = 0
	mr.power = 0

def sleep(t):
	R.sleep(t)

def move(p):
	ml.power = p
	mr.power = p
	
def distance(p):
	return R.ruggeduinos[0].analogue_read(p)

def turnL(a = 10, b = 20):
	ml.power = a
	mr.power = b

def turnR():
	ml.power = 20
	mr.power = 10

def get_transmitters():
	transmitters = R.radio.sweep()
	print("YELLOW: I found", len(transmitters), "transmitter(s):")

	for tx in transmitters:
		print(" - Transmitter {0} Bearing: {1} with a signal strength of {2}".format(
			tx.target_info.station_code,
			tx.bearing,
			tx.signal_strength,
		))
	return transmitters

def capture_three(a):
	if a == "P":
		for i in range(3):
			transmitters = get_transmitters()
			while transmitters[0].target_info.station_code in captured:
				transmitters.pop(0)
			while transmitters[0].bearing < -1 * (math.pi / 15):
				turnL()
				sleep(0.1)
				transmitters = get_transmitters()

				while transmitters[0].target_info.station_code in captured:
					transmitters.pop(0)
			stop()

			while transmitters[0].bearing > -1 * math.pi / 2:
				move(30)
				transmitters = get_transmitters()
				while transmitters[0].target_info.station_code in captured:
					transmitters.pop(0)
				if transmitters[0].bearing > -1 * math.pi / 18:
					stop()
					while transmitters[0].bearing > -1 * math.pi / 15:
						turnR()
						sleep(0.1)
						transmitters = get_transmitters()
						while transmitters[0].target_info.station_code in captured:
							transmitters.pop(0)
					stop()
					
			stop()
			claim()
			captured.append(transmitters[0].target_info.station_code)
	else:
		for i in range(3):
			transmitters = get_transmitters()
			nextTarget = False
			while nextTarget == False:
				nextTarget = True
				if transmitters[0].target_info.station_code in captured or transmitters[0].bearing < -0.2:
					transmitters.pop(0)
					nextTarget = False
			name = transmitters[0].target_info.station_code
			#print("TARGET:", name)
			while transmitters[0].bearing > 1 * math.pi / 15:
				turnR()
				#print("Turn R")
				sleep(0.1)
				transmitters = get_transmitters()

				while transmitters[0].target_info.station_code != name:
					transmitters.pop(0)
			stop()

			while transmitters[0].bearing < 1 * math.pi / 2:
				move(30)
				#print("Moving to", name)
				transmitters = get_transmitters()
				while transmitters[0].target_info.station_code != name:
					transmitters.pop(0)
				if transmitters[0].bearing < 1 * math.pi / 18:
					stop()
					while transmitters[0].bearing < 1 * math.pi / 15:
						turnL()
						#print("Turn L")
						sleep(0.1)
						transmitters = get_transmitters()
						while transmitters[0].target_info.station_code != name:
							transmitters.pop(0)
					stop()
			   
			stop()
			claim()
			captured.append(transmitters[0].target_info.station_code)
			print(captured)



captured = []	#List of already captured territories
testing = True

while testing:	#Loops forever
	transmitters = get_transmitters()
	if transmitters[0].bearing < 0:
		capture_three("P")
	else:
		capture_three("Y")

	#go_to_centre() 
	#turn until the last tower claimed is behind you, then move forward into the bottom centre of arena
	startTurning = False
	while startTurning == False:
		#Figures out which territory will be captured next
		transmitters = get_transmitters()
		while transmitters[0].target_info.station_code in captured:
			transmitters.pop(0)
		if transmitters[0].bearing < 0:
			a = -1
			name = transmitters[0].target_info.station_code
			while transmitters[0].bearing < a * (math.pi / 15):
				turnL()
				sleep(0.1)
				transmitters = get_transmitters()
				while transmitters[0].target_info.station_code != name:
					transmitters.pop(0)
			stop()
			while transmitters[0].bearing > a * math.pi / 2:
				move(30)
				transmitters = get_transmitters()
				while transmitters[0].target_info.station_code != name:
					transmitters.pop(0)
				if transmitters[0].bearing > a * math.pi / 18:
					stop()
					while transmitters[0].bearing > a * math.pi / 15:
						turnR()
						sleep(0.1)
						transmitters = get_transmitters()
						while transmitters[0].target_info.station_code != name:
							transmitters.pop(0)
					stop()    
			stop()
			claim()
			captured.append(name)
			#get the robot to move forward a bit after claiming
			#once signal strength is above a threshold it needs to stop and orientate correctly

			#Get the robot to detect collisions. It will reverse and turn clockwise
			#if pink, or will turn anticlockwise if yellow
