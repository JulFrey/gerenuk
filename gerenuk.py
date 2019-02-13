import cv2
import os
import numpy as np
import bpm_extract as bpm
import aubio as ab
import time
#from pygame import mixer


#mixer.init()
# specify song and image folder
image_folder = 'images'
slice_folder = 'slices'
soundfile =  'cube.mp3'
slice_length = 3
song_length = 2*60+38
#video_name = 'video.avi'

# list image files
images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
# number of images
n_images = len(images)
# read images to list
ims = list()
for i in images:
    ims.append(cv2.imread(os.path.join(image_folder, i)))

# define printsize
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

#video = cv2.VideoWriter(video_name, 0, 22, (width,height))
#set delay
#s = bpm.source(soundfile, 512)

# slice song to 5s long wav-segments for the adaption of the gerenuk
ab.slice_source_at_stamps(soundfile, list(np.arange(1, song_length,slice_length)*44100), samplerate=44100, output_dir = 'slices')

# get a list of the segments
slices = [slice for slice in os.listdir('slices') if slice.endswith(".wav")]
#sls = list()
#for s in slices:
#    sls.append(mixer.music.load(os.path.join(slice_folder, s)))

# start musik
os.system("start E:\\Gerenuk\\" + soundfile)

t_cor = 0
# for every slice we adapt the speed
for s in slices:
    start_time = time.time()
    # add folder to filename
    s = os.path.join(slice_folder, s)
    
    # analyze bps
    bps = bpm.get_file_bpm(s) / 60
    
    # set image rate
    d = int((1000 / n_images / bps) - t_cor)
    print(str(bps) + "BPS " + s)
    #p.play()
    #os.system("start E:\\Gerenuk\\" + s)
    end_time = time.time()
    t_cor = (end_time - start_time) * 1000 / n_images

    # print the images in a loop
    for t in np.arange(1 , slice_length * bps):
        for img in ims:
            #video.write(cv2.imread(os.path.join(image_folder, image)))
            cv2.imshow('Frame',img)
            #wait command between the images
            key = cv2.waitKey(d)
            if key == 27:
                print('Pressed Esc')
                break
    

# clear window
cv2.destroyAllWindows()

#clear slice files
for s in slices:   
    os.remove(os.path.join(slice_folder, s))


#video.release()