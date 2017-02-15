#!/usr/bin/python
import json, RPi.GPIO as GPIO
from datetime import datetime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

with open("/home/pi/ServidorAutomacaoPi/cron.log","a") as d:
	d.write(str(datetime.now())+" - Controle!\n")

tempoexecuta = datetime.now().time()

with open("/home/pi/ServidorAutomacaoPi/cron.json","r") as j:
	json = json.load(j)

	# for indice in json:
	# 	print json[indice]['ligar']
	
	for indice in json:
		tempDesliga = str(json[indice]['desligar'])
		tempLiga = str(json[indice]['ligar'])

		# print tempDesliga
		# print tempLiga

		if tempDesliga:
			
			pinoretorno = int(json[indice]['pinoretorno'])
			GPIO.setup(pinoretorno, GPIO.IN, pull_up_down = GPIO.PUD_UP)
			if GPIO.input(pinoretorno) == 1:
				horaCron = int(tempDesliga.split(':', 1)[0])
				minutoCron = int(tempDesliga.split(':', 1)[1])
				minutoTolerancia = int(minutoCron) + 1

				tempocron = tempoexecuta.replace(hour = horaCron, minute = minutoCron, second = 0, microsecond = 0)
				tempotolerancia = tempoexecuta.replace(hour = horaCron, minute = minutoTolerancia, second = 0, microsecond = 0)

				# print tempocron
				# print tempotolerancia
				# print tempoexecuta

				if tempoexecuta >= tempocron and tempoexecuta < tempotolerancia:
					pinoacende = int(json[indice]['pinoacende'])
					GPIO.setup(pinoacende, GPIO.OUT)
					statuspinoacende = GPIO.input(pinoacende)
					GPIO.setup(pinoacende, GPIO.OUT)
					GPIO.output(pinoacende, not statuspinoacende)
					with open("/home/pi/ServidorAutomacaoPi/cron.log","a") as d:
						d.write(str(datetime.now())+" - Desligou!\n")


		if tempLiga:

			pinoretorno = int(json[indice]['pinoretorno'])
			GPIO.setup(pinoretorno, GPIO.IN, pull_up_down = GPIO.PUD_UP)
			if GPIO.input(pinoretorno) == 0:
				horaCron = int(tempLiga.split(':', 1)[0])
				minutoCron = int(tempLiga.split(':', 1)[1])
				minutoTolerancia = int(minutoCron) + 1

				tempocron = tempoexecuta.replace(hour = horaCron, minute = minutoCron, second = 0, microsecond = 0)
				tempotolerancia = tempoexecuta.replace(hour = horaCron, minute = minutoTolerancia, second = 0, microsecond = 0)

				# print tempocron
				# print tempotolerancia
				# print tempoexecuta

				if tempoexecuta >= tempocron and tempoexecuta < tempotolerancia:
					pinoacende = int(json[indice]['pinoacende'])
					GPIO.setup(pinoacende, GPIO.OUT)
					statuspinoacende = GPIO.input(pinoacende)
					GPIO.output(pinoacende, not statuspinoacende)
					with open("/home/pi/ServidorAutomacaoPi/cron.log","a") as d:
						d.write(str(datetime.now())+" - Ligou!\n")