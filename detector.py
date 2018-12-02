"""
@author: Mahmoud I.Zidan
"""
'''
its purpose is to get the ground truth detection positions per frame.
specifically for Oxford TownCentre dataset
(http://www.robots.ox.ac.uk/~lav/Research/Projects/2009bbenfold_headpose/project.html)

Data format:
personNumber, frameNumber, headValid, bodyValid, headLeft, headTop, headRight, headBottom, bodyLeft, bodyTop, bodyRight, bodyBottom

Note: we ignore using/tracking head detection data
'''

import numpy as np

class GroundTruthDetections:

    def __init__(self, fname= '/home/coco/dataset/MOT16/MOT15-01/det/det.txt'):
        self.all_dets = np.loadtxt(fname ,delimiter=',') #load detections
        self._frames = int(self.all_dets[:, 0].max()) #0 to 4500 inclusive
	

    '''as in practical realtime MOT, the detector doesn't run on every single frame'''
    def _do_detection(self, detect_prob = .4):
        return int(np.random.choice(2, 1, p=[1 - detect_prob, detect_prob]))

    '''returns the detected items positions or [] if no detection'''
    def get_detected_items(self,frame):
        

        
        #if self._do_detection() or frame == 0:
            #return self.all_dets[self.all_dets[:, 0] == frame, 2:6]
        #else:
	    #print("space__detection")
            #return []
	dets = self.all_dets[self.all_dets[:,0] == frame, 2:6]
	detections = np.array(dets)
	#print("origianl_dets")
	#print(type(dets))
	#print(dets)
	for i, det in enumerate(dets):
	  #print("orginal_det")
	  #print(det)
	  det[0] = det[0]
	  det[1] = det[1]
	  det[2] = det[0] + det[2]
	  det[3] = det[1] + det[3]
	  #print("after_det")
	  #print(det)
	  detections[i] = det
	#print("after")
        #print(detections)  
	#return self.all_dets[self.all_dets[:,0] == frame, 2:6]
	return detections

    def get_total_frames(self):
        return self._frames
