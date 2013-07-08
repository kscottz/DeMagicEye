from SimpleCV import Image, Display, Color
import numpy as np
img = Image('shark.png')
img = img.scale(0.5)
# roughly the number of tiles in an image

# roughly how far we scan horizontally
window = 100 #int(img.width/repeats)
repeats = np.floor(img.width/window)
print "window: {0}".format(window)
# how big of a signal we convolve 
samplesz = window / 10
print "sample: {0}".format(samplesz)
dmap = np.zeros([img.width-window,img.height])

# we'll do this with iteration first to test
# proof of concept.
print (img.width,img.height)
npgImg = img.getGrayNumpy()
for vidx in range(1,img.height-1):
    print "row {0}".format(vidx)
    for hidx in range(0,img.width-window):
        #get our sample
        #currentWndw = np.floor(hidx/float(window))
        #if( currentWndw == repeats-1 ):
        #    break
        sample = npgImg[hidx:hidx+samplesz,vidx]
        vals = []
        #step = int((((currentWndw+1)*window)))
        for sidx in range(samplesz,window-samplesz):
            tester0 = npgImg[hidx+sidx:hidx+sidx+samplesz,vidx-1]
            tester1 = npgImg[hidx+sidx:hidx+sidx+samplesz,vidx]
            tester2 = npgImg[hidx+sidx:hidx+sidx+samplesz,vidx+1]
            v0 = np.abs(np.sum(sample-tester0))
            v1 = np.abs(np.sum(sample-tester1))
            v2 = np.abs(np.sum(sample-tester2))
            vals.append(np.min([v0,v1,v2]))
        best = np.where(np.array(vals)==np.min(vals))[0]
        # offset is the hidx of the current window
        offset = 0 #hidx - (currentWndw*window)
        dmap[hidx][vidx] = np.abs(best[0]-offset)
        #print dmap
print dmap                     
result = Image(dmap)
result.save('output.png')
            
