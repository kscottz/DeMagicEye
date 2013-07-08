from SimpleCV import Image, Display, Color
import numpy as np
img = Image('shark.png')
#img = img.scale(0.5)#.blur(window=(7,7))
# roughly the number of tiles in an image

# roughly how far we scan horizontally
window = 2*100 #int(img.width/repeats)
repeats = np.floor(img.width/window)
print "window: {0}".format(window)
# how big of a signal we convolve 
samplesz = window / 10
print "sample: {0}".format(samplesz)
dmap = np.zeros([img.width-window,img.height])
npgImg = img#.getGrayNumpy()
# we'll do this with iteration first to test
# proof of concept.
print (img.width,img.height)
for vidx in range(0,img.height):
    print "row {0}".format(vidx)
    for hidx in range(0,img.width-window):
        sample = npgImg[hidx:hidx+samplesz,vidx]
        vals = []
        for sidx in range((window/2)-samplesz,window-samplesz):
            tester0 = npgImg[hidx+sidx:hidx+sidx+samplesz,vidx]
            v0 = np.sum(np.abs((sample-tester0).getNumpy()))
            vals.append(v0)
        best = np.where(np.array(vals)==np.min(vals))[0]
        # offset is the hidx of the current window       
        dmap[hidx][vidx] = best[0]
        #print dmap
print dmap                     
result = Image(dmap)
result.save('outputRAW.png')
result.equalize().invert().save('outputEqualize.png')            
