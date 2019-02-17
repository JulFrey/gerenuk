# python version 3.6
# using pyaudio and aubio
# https://github.com/aubio/aubio/tree/master/python/demos

import cv2
import os
import numpy as np
import bpm_extract as bpm
#import aubio as ab
import wave
import time
import pyaudio


#I used this example: https://www.swharden.com/wp/2016-07-19-realtime-audio-visualization-in-python/

# specify song and image folder
image_folder = 'images'
slice_folder = 'slices'
#soundfile =  'cube.mp3'
slice_length = 3
song_length = 2*60+38
s_rate = 44100
chunk = (s_rate * slice_length)
disco = True
music = False
output_file="slices/test.wav"

#video_name = 'video.avi'

# list image files
images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
images = np.sort(images)
# number of images
n_images = len(images)
# read images to list
ims = list()
for i in images:
    img = cv2.imread(os.path.join(image_folder, i))
    img = cv2.resize(img, (1366,768), interpolation=cv2.INTER_CUBIC)
    ims.append(img)

#img = cv2.resize(img, (1366,768), interpolation=cv2.INTER_CUBIC)
window_name = 'frame'
# define printsize
#frame = cv2.imread(os.path.join(image_folder, images[0]))
#height, width, layers = frame.shape
cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

### we exclude the whole section changing to incomming sounds
# slice song to 5s long wav-segments for the adaption of the gerenuk
#ab.slice_source_at_stamps(soundfile, list(np.arange(1, song_length,slice_length)*s_rate), samplerate=s_rate, output_dir = 'slices')

# get a list of the segments
#slices = [slice for slice in os.listdir('slices') if slice.endswith(".wav")]



# start musik
#os.system("start E:\\Gerenuk\\" + soundfile)
if music:
    p=pyaudio.PyAudio() # start the PyAudio class
    stream=p.open(format=pyaudio.paInt16,channels=2,rate=s_rate,input=True,
                  frames_per_buffer=chunk) #uses default input device



t_cor = 0
# for every slice we adapt the speed
#for s in slices:
EXIT = False
i = 0

while not EXIT:
    #start_time = time.time()


    # add folder to filename
    #s = os.path.join(slice_folder, s)
    bps = 2.7
    if music:
        s = np.fromstring(stream.read(chunk),dtype=np.int16)
        open(output_file, 'w').close()
        outfile = wave.open(output_file, mode='wb')
        outfile.setparams((2, 2, s_rate, 0, 'NONE', 'not compressed'))
        outfile.writeframes(s.tostring())
        outfile.close()
        bps = bpm.get_file_bpm(output_file) / 60
        if bps < 1:
            bps = 2.0   
    #bps = bpm.get_file_bpm(output_file) / 60
    # set image rate
    d = int((1 / (n_images * bps) * 1000))# - t_cor)
    
    #p.play()
    #os.system("start E:\\Gerenuk\\" + s)
    #end_time = time.time()
    #t_cor = (end_time - start_time) * 1000 / n_images
    #if i > 1:
        #d = int(d - t_cor)
    
    #print(str(i)+ ': ' +str(bps) + "BPM " )
    # print the images in a loop
    for t in np.arange(1 , slice_length * bps):
        i += 1
        for img in ims:             
            #video.write(cv2.imread(os.path.join(image_folder, image)))
            if disco:
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                h, s, v = cv2.split(hsv)
                h += i * 18 # 4
                #s += value # 5
                #v += value # 6
                img = cv2.cvtColor(cv2.merge((h, s, v)), cv2.COLOR_HSV2BGR)
                #final_hsv = cv2.merge((h, s, v))
                #img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
            cv2.imshow('frame',img)
            #wait command between the images
            key = cv2.waitKey(d)
            if key == 27:
                print('Pressed Esc')
                EXIT = True
                break
    

# close the stream gracefully
stream.stop_stream()
stream.close()
p.terminate()

# clear window
cv2.destroyAllWindows()

#clear slice files
#for s in slices:   
#    os.remove(os.path.join(slice_folder, s))


#video.release()
