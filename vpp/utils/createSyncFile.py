#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 20:02:32 2022

@author: domi
"""

import numpy as np
import os


def syncFileCreator(TTL2_folder,
                    lfp_tmp_folder,
                    output_sync_txt,
                   saveORIfs =False):
    ''' 
    TTL2_folder : path to folder with TTL events;
    lfp_tmp_folder : path to folder with 'continuous' LFP recording;
    output_sync_txt : where you want to save created timestamp(s) as .txt files
    saveORIfs : whether a timestamp in sampling freq of LFP should be created besides timestamp in seconds (in future steps we need the one in secs)
    '''
    
    timestamps_events=np.load(os.path.join(TTL2_folder,"timestamps.npy"))
    channel_states=np.load(os.path.join(TTL2_folder,"channel_states.npy"))
    
    lfp_tmp_folder=lfp_tmp_folder
    timestamps_lfp=np.load(os.path.join(lfp_tmp_folder,"timestamps.npy"))
    
    #calculation of timestamps of video frames...
    timestamps_video_frames = timestamps_events[channel_states == 1] - timestamps_lfp[0] - 1
    
    #... (deto) in seconds (smapling freq is assumed 2500Hz).. can be an arg
    timestamps_video_frames_sec = [i/2500 for i in timestamps_video_frames]
    print("Video was recorded from second {}.".format(timestamps_video_frames[0]/2500))
    
    #output path : make sure output folder is assigned with "/" in the end of the string
    out4txt = os.path.join(output_sync_txt,
                           os.path.split(output_sync_txt[:-1])[1]) 
    
    #ephys timestamps for video frames in seconds
    out4txt_secs = out4txt +"tmstp_sec.txt"
    #ephys timestamp for frames in sampling freq (2500Hz)    
    out4txt = out4txt + "tmstp.txt"
    
    
    #save array as txt
    if saveORIfs:
        np.savetxt(out4txt, timestamps_video_frames, fmt = "%d") #%d is decimal
    np.savetxt(out4txt_secs, timestamps_video_frames_sec, fmt = "%f")
    # note: it's better to use np.savetxt - writer object will write it in a row..
    # #open writer object
    # file = open(out4txt, "w+")
    # # Saving the array in a text file
    # #content = str(new_array)
    # file.write(str(timestamps_video_frames))
    # #close writer object
    # file.close()

    
# ttl = "path to TTL file"
# lfp = "path LFP file"
# out = "path to destination"
# syncFileCreator(TTL2_folder = ttl,
#                     lfp_tmp_folder = lfp,
#                     output_sync_txt = out)

# if __name__ == '__main__':
#     syncFileCreator()
    
