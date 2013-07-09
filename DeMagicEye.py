from SimpleCV import Image, Display, Color
import numpy as np
import cv2
img = Image('randot_glass.gif')
img = img.scale(0.5)
# roughly the number of tiles in an image

# caclulate the value of a row
# using the integral image
def idxToSum(x1,x2,y,integral):
    # assume x2 > x1
    p3 = integral[y+1,x2+1]
    p2 = integral[y+1,x1-1]
    p1 = integral[y,x2+1]
    p0 = integral[y,x1-1]
    val = p3-p2-p1+p0
    return val
    
def integralWindow(x1,y1,x2,y2, integral):
    p3 = integral[y2,x2]
    p2 = integral[y2,x1]
    p1 = integral[y1,x2]
    p0 = integral[y1,x1]
    val = p3-p2-p1+p0
    return val
    
def findOptimalWindow(img, integral, minSplit=4, maxSplit=16):
    maxWin = img.width / minSplit
    minWin = img.width / maxSplit
    vals = []
    for i in range(minWin,maxWin):
        left = integralWindow(0,0,i,img.height,integral)
        right = integralWindow(0,i,2*i,img.height,integral)
        vals.append(np.abs(left-right)/(i*img.height))
    return np.where(np.array(vals)==np.min(vals))[0][0]
       
integral = cv2.integral(img.getGrayNumpyCv2())
searchWndw = 1.1
window = int(searchWndw*findOptimalWindow(img,integral))
print "window: {0}".format(window)
# how big of a signal we convolve 
samplesz = window / 10
print "sample: {0}".format(samplesz)
dmap = np.zeros([img.width-window,img.height],dtype='int32')
# we'll do this with iteration first to test
# proof of concept.
print (img.width,img.height)
# need to double check these bounds with the integral image
# really wish I could get rid of this iteration
for vidx in range(1,img.height-1): # for each row
    print "row {0}".format(vidx)
    for hidx in range(1,img.width-window-1): #for each pixel in the row
        # get the sum of a horz chunk
        sample = idxToSum(hidx,hidx+samplesz,vidx,integral)
        # try and grok this, go thru a search window, calc the abs diff of sums
        # between or sample and the test window, toss in a list
        vals = [np.abs(sample-idxToSum(hidx+sidx,hidx+sidx+samplesz,vidx,integral)) for sidx in range(int(window*0.5),window-samplesz) ]
        # find the minimum match
        best = np.where(np.array(vals)==np.min(vals))[0]
        # offset is the hidx of the current window       
        dmap[hidx][vidx] = best[-1] # if we get > 1 use the furthest one
# create the raw out
result = Image(dmap)
result.save('outputRAW.png')
# create the cleaned up output
result = result.medianFilter().equalize().invert().blur(window=(5,5))
result.save('outputEqualize.png')
sbs = img.sideBySide(result)
sbs.save('result.png')
