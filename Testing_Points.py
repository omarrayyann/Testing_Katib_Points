import pygame
import random
import time
import string
import os
import csv
import copy
import serial
import math

# Electromagnet Setup
force_pin = 18
magnet1Pin = 23
magnet2Pin = 24
pygame.init()
width = 1600
height = 900
# Screen Setup
screen = pygame.display.set_mode((width, height))
# screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
draw_on = False
drowOn = False
last_pos = (0, 0)
color = (0, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
radius = 10

# 192+(1727-192)/3.0
xl = 1050  # (1727-192)/3.0
xs = 125
# 109+(971-109)/5
yl = 700
ys = 100
imgIndex = 0
delim = ' '
lengthOfarr = 0
flag = 1
letterNames = []
# Serial Setup

# gSer=serial.Serial('/dev/ttyACM0','115200')
# time.sleep(3)
# gSer.flush()
# serL.write("r\n")
# serR.write("r\n")
# time.sleep(6.1)


# Variables to change:
distanceBetweenPoints = 20
currentLoadedDistance = 20
hooks = False


font = pygame.font.Font('freesansbold.ttf', 20)


def invKin(x_in, y_in):
    # x_in = 0.024+0.052*(1-(xs+xl-x_in)/xl)
    # y_in = 0.1171+0.047*((ys+yl-y_in)/yl)
    R = math.sqrt(x_in**2+y_in**2)
    k = math.atan(y_in/x_in)
    phi = math.acos(R/0.2)

    thetaL = math.degrees(k+phi)

    x_in = x_in-0.1

    R = math.sqrt(x_in**2+y_in**2)
    k = math.atan(y_in/x_in)
    phi = math.acos(R/0.2)

    thetaR = math.degrees((k-phi))

    return 90.0+thetaR, -90.0+thetaL


def getCoords(xn, yn):
    if xn < xs+xl and xn >= xs:
        xn = (xn-xs)/xl
    else:
        return
    if yn < ys+yl and yn >= ys:
        yn = (yn-ys)/yl
    else:
        return
    fx = 143*xn
    # fy= 0.00017125*yn+0.09431875
    fy = -95*yn
    return fx, fy


def roundline(srf, color, start, end, radius=10):
    dx = end[0]-start[0]
    dy = end[1]-start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int(start[0]+float(i)/distance*dx)
        y = int(start[1]+float(i)/distance*dy)
        pygame.draw.circle(srf, color, (x, y), radius)


d = dict.fromkeys(string.ascii_lowercase, [])
letterImg = []
lettersX = []
lettersY = []

cwd = os.getcwd()
Data_path = cwd+"/letters"
letter_paths = os.listdir(Data_path)
print(letter_paths)

for file_name in letter_paths:
    letterNames.append(file_name[:len(file_name) - 4])
    with open(Data_path+'/'+file_name, 'r') as csvfile:
        coords = csv.reader(csvfile, delimiter=delim)
        # print(coords)    		#header = next(plots)
        x = []
        y = []
        l = []
        for row in coords:
            if len(row) > 1:
                print(row, row[0], row[1])
                x.append(int(xs+50+(0.7*xl)*(float(row[0]))))
                y.append(int(ys+50+(0.8*yl)*(float(row[1]))))
    lettersX.append(x)
    lettersY.append(y)
#
# for key in d:
#	img = pygame.image.load(imageDir+'/'+key+'.png').convert()
#	img = pygame.transform.rotozoom(img,0,4)
#	rectImg = img.get_rect()
#	rectImg.center = (1450, 400)
#	letterImg.append(img)
#	with open(letterDir+key+'.csv','r') as csvfile:
#		coords = csv.reader(csvfile, delimiter=delim)
#		#header = next(plots)
#		x=[]
#		y=[]
#		for row in coords:
#			x.append(int(xs+60+(xl-80)*(1-float(row[0]))))
#			y.append(int(ys+60+(yl-80)*(1-float(row[1]))))
#		lettersX.append(x)
#		lettersY.append(y)


# Remote Work Magnet Visualization
magnet = pygame.image.load('clear.png').convert()
magnet = pygame.transform.scale(magnet, (30, 30))


startMagnetVisualization = False


def magnet_visualizer(x, y):
    newPoint = pygame.draw.circle(screen, (255, 215, 0), (x, y), 10)


plusDistance = pygame.image.load('plus.png').convert()
plusDistance = pygame.transform.scale(plusDistance, (40, 40))
plusDistance = pygame.transform.rotate(plusDistance, 180)
rectPlusDistance = plusDistance.get_rect()
rectPlusDistance.center = (1410, 180)

minusDistance = pygame.image.load('minus.png').convert()
minusDistance = pygame.transform.scale(minusDistance, (40, 40))
minusDistance = pygame.transform.rotate(minusDistance, 180)
rectMinusDistance = minusDistance.get_rect()
rectMinusDistance.center = (1340, 180)

clear = pygame.image.load('clear.png').convert()
clear = pygame.transform.scale(clear, (50, 50))
clear = pygame.transform.rotate(clear, 180)
rectClear = clear.get_rect()
rectClear.center = (50, 120)

load = pygame.image.load('load.png').convert()
load = pygame.transform.scale(load, (50, 50))
load = pygame.transform.rotate(load, 180)
rectLoad = load.get_rect()
rectLoad.center = (50, 180)

closeL = pygame.image.load('exit.png').convert()
closeL = pygame.transform.scale(closeL, (50, 50))
# closeL=pygame.transform.rotate(closeL,180)
rectClose = closeL.get_rect()
rectClose.center = (width-50, 100)

ResetMs = pygame.image.load('exit.png').convert()
ResetMs = pygame.transform.scale(ResetMs, (50, 50))
# closeL=pygame.transform.rotate(closeL,180)
rectResetMs = ResetMs.get_rect()
rectResetMs.center = (width-50, 200)

rectApply = pygame.Rect(1240, 350, 300, 40)
rectStart = pygame.Rect(1240, 400, 300, 40)
rectNextLetter = pygame.Rect(1240, 450, 300, 40)
rectPreviousLetter = pygame.Rect(1240, 500, 300, 40)


x = []
y = []

# gSer.flush()
# print(gSer.readline())
# print(gSer.readline())
# time.sleep(1)
# gSer.write(str.encode('$X\n'))
# #gSer.write(str.encode('M5\n'))
# gSer.write(str.encode('M3 S100\n'))
# gSer.write(str.encode('M3 S500\n'))
# gSer.write(str.encode('$H\n'))

# time.sleep(15)
# gSer.write(str.encode('$X\n'))
# gSer.write(str.encode('M3 S500\n'))
# time.sleep(1)
# gSer.write(str.encode('G10 P1 L20 X0 Y0\n'))
# print(gSer.readline())
# time.sleep(0.1)
# #gSer.write(str.encode('G10 P1 L20 \n'))
# gSer.write(str.encode('G21 X105  Y-65 F4000\n'))
# print(gSer.readline())
# time.sleep(0.1)
# gSer.write(str.encode('G10 P1 L20 X0 Y0\n'))
# print(gSer.readline())
# time.sleep(2)
# gSer.write(str.encode('$X\n'))
# print(gSer.readline())
# gSer.write(str.encode('M3 S1000\n'))
# print(gSer.readline())
# gSer.write(str.encode(' G21 X0 Y-95 F4000\n'))
# print(gSer.readline())
# gSer.write(str.encode('$X\n'))
# gSer.write(str.encode(' G21 X143 Y-95 F4000\n'))
# print(gSer.readline())
# gSer.write(str.encode('$X\n'))
# gSer.write(str.encode(' G21 X0 Y0 F4000\n'))
# print(gSer.readline())
# gSer.write(str.encode('$X\n'))
# gSer.write(str.encode('M3 S1000\n'))
# #gSer.write(str.encode(' G21 X20  Y-20 F4000\n'))
# #gSer.write(str.encode(' \n'))
# time.sleep(2)
# #gSer.write(str.encode('M3 S10\n'))
# #gSer.write(str.encode('G0 X0 Y0\n' ))


def averagePoint(point1, point2):
    x = (point2[0]+point1[0])/2
    y = (point2[1]+point1[1])/2
    return [x, y]


def distance(point1, point2):
    dx = point2[0]-point1[0]
    dy = point2[1]-point1[1]
    return (abs(dy**2 + dx**2))**0.5


def equalDisatantPoints(points, d):
    newPoints = [[points[0][0], points[0][1]]]
    for i in range(len(points)):
        if (distance(newPoints[len(newPoints)-1], points[i]) > d):
            newPoints.append(points[i])
    return newPoints


def alterPoints(letterX, letterY, distanceBetweenPoints):
    print("AAAAAA")
    points = []
    for i in range(len(letterX)):
        newPoint = [letterX[i], letterY[i]]
        points.append(newPoint)

    # Increasing number of points
    resampledData = resample(points, 2)

    # Equdistant points
    edualdistant_points = equalDisatantPoints(
        resampledData, distanceBetweenPoints)

    xPoints = []
    yPoints = []
    for i in range(len(edualdistant_points)):
        xPoints.append(edualdistant_points[i][0])
        yPoints.append(edualdistant_points[i][1])

    return xPoints, yPoints


def resample(points, howMany):
    # v dumb way, there might be a library that does this better
    newPoints = points
    for m in range(howMany):
        tempPoints = newPoints
        newPoints = []
        for i in range(len(tempPoints)):
            if len(newPoints) > 0:
                newPoints.append(averagePoint(
                    tempPoints[i], newPoints[len(newPoints)-1]))
                newPoints.append(tempPoints[i])
            else:
                newPoints.append(tempPoints[i])
    return newPoints


try:
    while True:
        textDistance = font.render(
            'Distance Between Points: ' + str(distanceBetweenPoints), True, (255, 255, 255), (0, 0, 0))

        rectStartDistance = pygame.Rect(1200, 50, 400, 1000)
        pygame.draw.rect(screen, (0, 0, 0), rectStartDistance, 0, 10)

        textFeedRate = font.render(
            'Feed Rate: 23', True, (255, 255, 255), (0, 0, 0))

        textApply = font.render(
            'Apply Changes', True, (0, 0, 0), (255, 255, 255))

        textStart = font.render(
            'Start', True, (0, 0, 0), (255, 255, 255))

        textPrevious = font.render(
            'Previous Letter: ' + letterNames[(imgIndex+15*len(letterNames)-1) % len(letterNames)], True, (0, 0, 0), (255, 255, 255))

        textCurrent = font.render(
            'Current Letter: ' + letterNames[(imgIndex+15*len(letterNames)) % len(letterNames)], True, (255, 255, 255), (0, 0, 0))

        textNext = font.render(
            'Next Letter: ' + letterNames[(imgIndex+1) % len(letter_paths)], True, (0, 0, 0), (255, 255, 255))

        if (currentLoadedDistance != distanceBetweenPoints):
            textApply = font.render(
                'Apply Changes', True, (0, 0, 0), (255, 100, 100))
            pygame.draw.rect(screen, (255, 100, 100), rectApply, 0, 10)
            screen.blit(textApply, (1320, 355))
        else:
            pygame.draw.rect(screen, white, rectApply, 0, 10)
            screen.blit(textApply, (1320, 355))

        rect = pygame.draw.rect(screen, white, (xs, ys, xl, yl), 3, 10)
        pygame.draw.circle(screen, color, (int(xs), int(ys)), radius)
        pygame.draw.circle(screen, blue, (int(xs+xl), int(ys+yl)), radius)
        screen.blit(clear, rectClear)
        screen.blit(load, rectLoad)
        screen.blit(plusDistance, rectPlusDistance)
        screen.blit(minusDistance, rectMinusDistance)
        screen.blit(textDistance, (1240, 100))
        screen.blit(textFeedRate, (1240, 250))
        pygame.draw.rect(screen, white, rectStart, 0, 10)
        screen.blit(textStart, (1367, 406))
        pygame.draw.rect(screen, white, rectNextLetter, 0, 10)
        screen.blit(textNext, (1270, 457))
        pygame.draw.rect(screen, white, rectPreviousLetter, 0, 10)
        screen.blit(textPrevious, (1270, 508))
        screen.blit(textCurrent,  (1270, 559))

        # slider.update()
        # slider.draw(screen)

        # screen.blit(closeL,rectClose)
        # screen.blit(ResetMs,rectResetMs)
        for e in pygame.event.get():

            # e = pygame.event.wait()
            # keys=pygame.key.get_pressed()
            if e.type == pygame.QUIT:
                raise StopIteration
            if (e.type == pygame.KEYDOWN):
                if e.key == pygame.K_q:
                    raise StopIteration
                if e.key == pygame.K_c:
                    screen.fill(black)

            if e.type == pygame.MOUSEBUTTONDOWN and rectClose.collidepoint(e.pos):
                raise StopIteration
# Reset Motors
            if e.type == pygame.MOUSEBUTTONDOWN and rectResetMs.collidepoint(e.pos):
                pygame.draw.rect(screen, white, rectResetMs, 5)
                pygame.display.flip()
                time.sleep(0.05)
                pygame.draw.rect(screen, black, rectResetMs, 5)
                pygame.display.flip()
                # serL.write("r\n")
                time.sleep(3)
                # serR.write("r\n")
                # screen.fill(black)
# Clear check
            if e.type == pygame.MOUSEBUTTONDOWN and rectClear.collidepoint(e.pos):
                pygame.draw.rect(screen, white, rectClear, 5)
                pygame.display.flip()
                pygame.draw.rect(screen, black, rectClear, 5)
                time.sleep(0.05)
                drowOn = False
                screen.fill(black)

# Plus Distance check
            if e.type == pygame.MOUSEBUTTONDOWN and rectPlusDistance.collidepoint(e.pos):
                distanceBetweenPoints += 1
                pygame.display.update()

# Minus Distance check
            if e.type == pygame.MOUSEBUTTONDOWN and rectMinusDistance.collidepoint(e.pos):
                distanceBetweenPoints -= 1
                pygame.display.update()

# Apply check
            if e.type == pygame.MOUSEBUTTONDOWN and rectApply.collidepoint(e.pos):
                pygame.display.flip()
                time.sleep(0.05)

                pygame.draw.rect(screen, white, rectStart, 5)
                pygame.display.flip()
                time.sleep(0.05)
                pygame.draw.rect(screen, black, (xs, ys, xl, yl))
                rect = pygame.draw.rect(screen, white, (xs, ys, xl, yl), 5)

                # changing points
                newLettersX, newLettersY = alterPoints(
                    lettersX[imgIndex], lettersY[imgIndex], distanceBetweenPoints)

                xp = copy.copy(newLettersX)
                yp = copy.copy(newLettersY)
                lengthOfarr = len(xp)
                newPoint = pygame.draw.circle(
                    screen, (200, 0, 0), (xp.pop(0), yp.pop(0)), 10)
                pygame.display.flip()
                drowOn = True
                currentLoadedDistance = distanceBetweenPoints
                # screen.fill(black)

# Next check

            if e.type == pygame.MOUSEBUTTONDOWN and rectNextLetter.collidepoint(e.pos):

                pygame.display.flip()
                imgIndex = (imgIndex+1) % len(letter_paths)
                # screen.blit(letterImg[imgIndex],rectImg)
                pygame.display.flip()
                pygame.draw.rect(screen, black, (xs, ys, xl, yl))
                rect = pygame.draw.rect(screen, white, (xs, ys, xl, yl), 5)

                # changing points
                newLettersX, newLettersY = alterPoints(
                    lettersX[imgIndex], lettersY[imgIndex], distanceBetweenPoints)

                xp = copy.copy(newLettersX)
                yp = copy.copy(newLettersY)
                lengthOfarr = len(xp)
                newPoint = pygame.draw.circle(
                    screen, white, (xp.pop(0), yp.pop(0)), 20)
                flag = 1
                drowOn = False
                drow_on = False
                currentLoadedDistance = distanceBetweenPoints
                # pygame.display.flip()

# Previous check

            if e.type == pygame.MOUSEBUTTONDOWN and rectPreviousLetter.collidepoint(e.pos):

                pygame.display.flip()
                imgIndex = (imgIndex-1) % len(letter_paths)
                # screen.blit(letterImg[imgIndex],rectImg)
                pygame.display.flip()
                pygame.draw.rect(screen, black, (xs, ys, xl, yl))
                rect = pygame.draw.rect(screen, white, (xs, ys, xl, yl), 5)

                # changing points
                newLettersX, newLettersY = alterPoints(
                    lettersX[imgIndex], lettersY[imgIndex], distanceBetweenPoints)

                xp = copy.copy(newLettersX)
                yp = copy.copy(newLettersY)
                lengthOfarr = len(xp)
                newPoint = pygame.draw.circle(
                    screen, white, (xp.pop(0), yp.pop(0)), 20)
                flag = 1
                drowOn = False
                drow_on = False
                currentLoadedDistance = distanceBetweenPoints
                # pygame.display.flip()

# Start check

            if e.type == pygame.MOUSEBUTTONDOWN and rectStart.collidepoint(e.pos):

                # changing points
                newLettersX, newLettersY = alterPoints(
                    lettersX[imgIndex], lettersY[imgIndex], distanceBetweenPoints)

                xp = copy.copy(newLettersX)
                yp = copy.copy(newLettersY)
                lengthOfarr = len(xp)
                newPoint = pygame.draw.circle(
                    screen, (200, 0, 0), (xp.pop(0), yp.pop(0)), 10)
                pygame.display.flip()
                drowOn = True
                currentLoadedDistance = distanceBetweenPoints
                # screen.fill(black)
# Drawing check

            if e.type == pygame.MOUSEBUTTONDOWN and rect.collidepoint(e.pos) and drowOn:
                color = (0, 255, 0)
                # pygame.draw.circle(screen, color, e.pos, radius)
                draw_on = True
                if e.type == pygame.MOUSEBUTTONUP:
                    draw_on = False
            if draw_on and e.type == pygame.MOUSEMOTION and rect.collidepoint(e.pos) and newPoint.collidepoint(e.pos):
                # if draw_on and :
                # pygame.draw.circle(screen, color, e.pos, radius)
                # roundline(screen, color, e.pos, last_pos,  radius)
                # last_pos = e.pos

                if lengthOfarr-1 > 0:
                    flag = 1
                    xp0, yp0 = (xp.pop(0), yp.pop(0))
                    magnet_visualizer(xp0, yp0)
                    pygame.display.update()
                    xc, yc = getCoords(xp0, yp0)
                    print("pixels x %f , y %f", (xp0, yp0))
                    print(xc, yc)
                    # (thL,thR)=invKin(xc,yc)
                    gcodeString = "G21 X" + \
                        "{:.3f}".format(xc)+" Y"+"{:.3f}".format(yc)+" F4000\n"
                    print(gcodeString)
                    # gSer.write(str.encode(gcodeString))
                    # print 'xp: '+str(xp0)+'yp: '+str(yp0)+'xc: '+str(xc)+'yc: '+str(yc)
                    # thL=-90+thL
                    # thR=90+thR
                    # print str(thL)+' '+str(thR)

                    #################SEND GCODE COMMANDS###################################
                   # sting2send=str(thR)+'\n'
                    # serR.write(sting2send)

                    # readlinR = serR.readline()
                    # time.sleep(0.002)

                    # sting2send = str(thL)+'\n'
                    # serL.write(sting2send)

                    time.sleep(0.002)
                    # readlinL = serL.readline()

                    # print readlinL,readlinR
                    newPoint = pygame.draw.circle(screen, blue, (xp0, yp0), 20)
                    lengthOfarr -= 1
                    pygame.display.flip()
                    time.sleep(0.002)
                    # TURN ON MAGNET
                    # GPIO.output(magnet2Pin,GPIO.HIGH)
                    # print("ON")
                    # serR.flushInput()
                    # serL.flushInput()
                    # time.sleep(0.02)

                else:

                    # (thL,thR) = invKin(xin,yin)
                    # print thL,thR
                    # thL = -90+thL
                    # thR = 90+thR
                    gcodeString = "G21 X" + \
                        "0".format(xc)+" Y"+"0".format(yc)+" F4000\n"
                    if(flag == 1):
                        #################SEND GCODE END COMMAND######################
                        # gSer.write(str.encode(gcodeString))
                        # sting2send=str(thR)+'\n'
                        # serR.write(sting2send)
                        # readlinR = serR.readline()
                        # sting2send = str(thL)+'\n'
                        # serL.write(sting2send)
                        # readlinL = serL.readline()

                        # print readlinL,readlinR
                        draw_on = False
                        drawOn = False
                        # REVERSE MAGNET POLARIT

                        flag = 0
                        time.sleep(0.02)
            pygame.display.flip()
except StopIteration:
    pass
string2send = str(0.0)+'\n'
# gSer.write(str.encode('M3 S100\n'))
# gSer.write(str.encode('M3 S800\n'))
# serL.write(string2send)
# serR.write(string2send)
# time.sleep(0.1)
# serL.close()
# gSer.close()
# serR.close()
# Electromagnet cleanup
# GPIO.output(magnet1Pin,GPIO.LOW)
# GPIO.output(magnet2Pin,GPIO.LOW)
# GPIO.output(force_pin,GPIO.LOW)
# GPIO.cleanup()

pygame.quit()
