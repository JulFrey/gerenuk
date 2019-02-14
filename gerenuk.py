import cv2
import os
import numpy as np
import bpm_extract as bpm
#import aubio as ab
import wave
#import time
import pyaudio


#I used this example: https://www.swharden.com/wp/2016-07-19-realtime-audio-visualization-in-python/

# specify song and image folder
image_folder = 'images'
slice_folder = 'slices'
soundfile =  'cube.mp3'
slice_length = 3
song_length = 2*60+38
s_rate = 44100
chunk = (s_rate * slice_length)

#video_name = 'video.avi'

# list image files
images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
# number of images
n_images = len(images)
# read images to list
ims = list()
for i in images:
    ims.append(cv2.imread(os.path.join(image_folder, i)))

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

p=pyaudio.PyAudio() # start the PyAudio class

# start musik
#os.system("start E:\\Gerenuk\\" + soundfile)
stream=p.open(format=pyaudio.paInt16,channels=2,rate=s_rate,input=True,
              frames_per_buffer=chunk) #uses default input device

t_cor = 0
# for every slice we adapt the speed
#for s in slices:
EXIT = False
i = 0
while True:
    #start_time = time.time()


    # add folder to filename
    #s = os.path.join(slice_folder, s)

    
    s = np.fromstring(stream.read(chunk),dtype=np.int16)
    
    output_file="slices/test.wav"
    open(output_file, 'w').close()
    outfile = wave.open(output_file, mode='wb')
    outfile.setparams((2, 2, s_rate, 0, 'NONE', 'not compressed'))
    outfile.writeframes(s.tostring())
    #outfile.writeframes(s.tostring())
    outfile.close()
    # analyze bps
    bps = bpm.get_file_bpm(output_file) / 60
    
    # set image rate
    d = int((1 / (n_images * bps) * 1000))# - t_cor)
    #i += 1
    #p.play()
    #os.system("start E:\\Gerenuk\\" + s)
    #end_time = time.time()
    #t_cor = (start_time - end_time) * 1000 / n_images
    #if i > 1:
        #d = int(d - t_cor)
    
    print(str(bps*60) + "BPM " )
    # print the images in a loop
    for t in np.arange(1 , slice_length * bps):
        if EXIT:
            break
        for img in ims:             
            #video.write(cv2.imread(os.path.join(image_folder, image)))
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