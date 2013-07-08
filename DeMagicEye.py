from SimpleCV import Image, Display, Color
import numpy as np
img = Image('shark.png')
img = img.scale(0.5)
# roughly the number of tiles in an image
repeats = 5
# roughly how far we scan horizontally
window = img.width/repeats
print "window: {0}".format(window)
# how big of a signal we convolve 
samplesz = window / 4
print "sample: {0}".format(samplesz)
dmap = np.zeros([img.width-window,img.height])

# we'll do this with iteration first to test
# proof of concept.
print (img.width,img.height)
npgImg = img.getGrayNumpy()
for vidx in range(0,img.height):
    print "row {0}".format(vidx)
    for hidx in range(0,img.width-window):
        #get our sample
        currentWndw = np.floor(hidx/float(window))
        if( currentWndw >= repeats-1 ):
            continue

        sample = npgImg[hidx:hidx+samplesz,vidx]
        vals = []
        #print "hidx: {0}".format(hidx)
        #print "currentidx {0} / sz: {1}".format(currentWndw,window)
        
        for sidx in range(0,window-samplesz):

            step = int(((currentWndw+1)*window)-(window/2))
            #print "searching: {0}->{1}".format(step+sidx,step+sidx+samplesz)
            tester = npgImg[step+sidx:step+sidx+samplesz,vidx]
            vals.append( np.abs(np.sum(sample-tester)))
        #print vals
        best = np.where(np.array(vals)==np.min(vals))[0]
        # offset is the hidx of the current window
        offset = hidx - (currentWndw*window)
        dmap[hidx][vidx] = np.abs(best[0]-offset)
        #print dmap
print dmap                     
result = Image(dmap)
result.save('output.png')
            
