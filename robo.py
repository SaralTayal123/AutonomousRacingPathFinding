#Make sure to run from terminal and not VSCode run button since the track directory is relative
import json
import os
import matplotlib.pyplot as plt
import numpy as np

with open('./LVM_ORN3.txt') as file:
    data = json.load(file)
# print(data.keys())

#Visualize the track

inside = np.array(data.get('Inside'))
outside = np.array(data.get('Outside'))
center = np.array(data.get('Centre'))
insideX = inside[:,0]
insideY = inside[:,1]
outsideX = outside[:,0]
outsideY = outside[:,1]
centerX = center[:,0]
centerY = center[:,1]
# print(np.shape(inside))
# print(np.shape(insideX))
# print(np.shape(insideY))
# print(insideX)
# print(insideY)

# plt.plot(insideX, insideY, 'r')
# plt.plot(outsideX, outsideY,'r')
# plt.plot(centerX, centerY,'g')
# # plt.plot(outsideX, outsideY,insideX, insideY,)
# plt.show(block=False)
# plt.show()
# input('press <ENTER> to continue')




def generateMatrix(ins = inside, out = outside, lanes = 10, sensitivity = 50):
    ''' 
    Since we're generating a matrix based on the internal points, we're going to 
    bias it on there. (we can use a simple ternary operator for checking inner lines
    based on array len).
    '''
    #init matrix
    matrix = np.zeros((len(insideX), lanes, 2)) #2 for x,y dim
    tempx = []
    tempy = []
    #main loop
    outerIndex = 0
    for i in range(len(inside)):
        x = ins[i,0]
        y = ins[i,1]
        if i < len(inside)-1:
            slope = (ins[i+1,1] - ins[i-1,1])/(ins[i+1,0] - ins[i-1,0])
        else: #if at end of track, cyclic continuity
            slope = (ins[0,1] - ins[-1,1])/(ins[0,0] - ins[-1,0])

        slopePerpendicular = -1 * (1/slope) #perpendicular = inverse * - 1

        #Following loop finds the intersection point to the outside lane 
        for j in range((-1 * sensitivity)+outerIndex,(sensitivity+outerIndex)):
            #prevent access greater than 1
            if j == len(out[:,0]) - 1:
                j = 0
            x2 = out[j,0]
            y2 = out[j,1]
            slope2 = (out[j+1,1] - out[j,1])/(out[j+1,0] - out[j,0])
            xIntersect = ((-1*slope2*x2) + (y2) - y + (slopePerpendicular * x))/(slopePerpendicular-slope2)
            yIntersect =((xIntersect-out[j,0]) * slope2) + out[j,1] #y = m(x-1)+b

            #can be more elegant
            if ((yIntersect >= out[j,1] and yIntersect <= out[j+1,1]) or (yIntersect <= out[j,1] and yIntersect >= out[j+1,1])):
                if (xIntersect >= out[j,0] and xIntersect <= out[j+1,0]) or (xIntersect <= out[j,0] and xIntersect >= out[j+1,0]):
                    outerIndex = j    
                    # print("j: ",j, "i: ", i, "difference: ", j-i)
                    # print("Range: ",(-1 * sensitivity)+outerIndex,(sensitivity+outerIndex)%len(ins[:,0]))
                    break #break out of for loop
        # tempx.append(xIntersect)
        # tempy.append(yIntersect)
        # if (i+1)%200 == 0:
        #     plt.plot(insideX, insideY, 'r')
        #     # plt.plot(outsideX, outsideY,'r')
        #     # plt.plot(centerX, centerY,'g')
        #     plt.plot([x2,out[j+1,0]],[y2,out[j+1,1]],'y')
        #     plt.plot([xIntersect, x], [yIntersect, y],'g')
        #     plt.plot([x,x+1],[y,y+(1*slopePerpendicular)],'b')
        #     plt.plot([x,x+1],[y,y+(1*slope)],'w')
        #     # plt.plot(outsideX, outsideY,insideX, insideY,)
        #     # plt.show(block=False)
        #     # plt.show()
        #     # input('press <ENTER> to continue')
        #     # break

        #Following loop fills in the matrix
        for z in range(lanes): #use 1 to avoid the edge of the track
            xStep = (xIntersect - x)/(lanes+1) #stepsize
            xVal = ((z+1) * xStep) + x
            yVal = ((xVal-x) * slopePerpendicular) + y
            matrix[i,z,0] = xVal
            matrix[i,z,1] = yVal

    # plt.plot(insideX, insideY, 'r')
    # plt.plot(tempx, tempy, 'y')
    # plt.show(block=False)
    # plt.show()
    # input('press <ENTER> to continue')
    # print(inside[50], tempx[50],tempy[50])
    return matrix

if __name__ == "__main__":
    outsidePoints = generateMatrix()            

    plt.plot(insideX, insideY, 'r')
    # plt.plot(outsideX, outsideY,'b')
    for i in range(10):
        plt.plot(outsidePoints[:,i,0],outsidePoints[:,i,1]) 
    # plt.plot(centerX, centerY,'g')
    plt.show(block=False)
    plt.show()
    # input('press <ENTER> to continue')
    # print(np.shape(outsidePoints))
    # print(outsidePoints[5,1,0], outsidePoints[5,1,1]) 
    print(outsidePoints[50])
    # print(inside[0,0], inside[0,1], outside[0,0], outside[0,1])

        


# #TODO: Generate a way of representing nodes

# class Node:
#     def __init__():
#         self.edges = []
#         self.g = sys.maxint #intmax or some large val
#         self.h #TODO: Init, hueristic to goal
#         self.rhs #TODO: Init
#         self.key
