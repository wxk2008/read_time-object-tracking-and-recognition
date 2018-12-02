"""
@author: Mahmoud I.Zidan
"""

import numpy as np
import os.path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from skimage import io
import time
import argparse

from sort import Sort
from detector import GroundTruthDetections

def main():
    args = parse_args()
    display = args.display
    #display = False

    use_dlibTracker  = args.use_dlibTracker
    #use_dlibTracker = False
    saver = args.saver

    total_time = 0.0
    total_frames = 0

    # for disp
    if display:
        colours = np.random.rand(32, 3)  # used only for display
        plt.ion()
        fig = plt.figure()


    if not os.path.exists('output'):
        os.makedirs('output')
    out_file = 'output/townCentreOut.top'

    #init detector
    detector = GroundTruthDetections()

    #init tracker
    tracker =  Sort(use_dlib= use_dlibTracker) #create instance of the SORT tracker

    if use_dlibTracker:
        print "Dlib Correlation tracker activated!"
    else:
        print "Kalman tracker activated!"

    with open(out_file, 'w') as f_out:

        frames = detector.get_total_frames()
	#frames = 795

        for frame in range(0, frames):  #frame numbers begin at 0!
            # get detections
            detections = detector.get_detected_items(frame+1)

            total_frames +=1
	    if total_frames < 10:
	      jpg_name = "00000%d.jpg" %(frame+1)
	    elif total_frames < 100:
	      jpg_name = "0000%d.jpg" %(frame+1)
	    elif total_frames < 1000:
	      jpg_name = "000%d.jpg" %(frame+1)
            fn = '/home/coco/dataset/MOT16/MOT15-01/img1/'+ jpg_name # video frames are extracted to 'test/Pictures%d.jpg' with ffmpeg
            img = io.imread(fn)
            if (display):
                ax1 = fig.add_subplot(111, aspect='equal')
                ax1.imshow(img)
                if(use_dlibTracker):
                    plt.title('Dlib Correlation Tracker')
                else:
                    plt.title('Kalman Tracker')

            start_time = time.time()
	    #print("frame")
	    #print(frame+1)
	    #print(detections)
            trackers = tracker.update(detections,img)

            cycle_time = time.time() - start_time
            total_time += cycle_time

            print('frame: %d...took: %3fs'%(frame,cycle_time))
            print("valid trackers")
	    print(len(trackers))
            for d in trackers:
                f_out.write('%d,%d,%d,%d,x,x,x,x,%.3f,%.3f,%.3f,%.3f\n' % (d[4], frame, 1, 1, d[0], d[1], d[2], d[3]))
                if (display):
                    d = d.astype(np.int32)
                    ax1.add_patch(patches.Rectangle((d[0], d[1]), d[2] - d[0], d[3] - d[1], fill=False, lw=3,
                                                    ec=colours[d[4] % 32, :]))
	            print("frame")
		    print(frame+1)
		    print("draw tracker in the output image")
		    print(d[0])
		    print(d[1])
		    print(d[2])
		    print(d[3])

                    ax1.set_adjustable('box-forced')
                    #label
                    ax1.annotate('id = %d' % (d[4]), xy=(d[0], d[1]), xytext=(d[0], d[1]))
                    if detections != []:#detector is active in this frame
                        ax1.annotate(" DETECTOR", xy=(5, 45), xytext=(5, 45))
            #plt.axis("off")
	    #fig.canvas.flush_events()
	    #plt.draw()
	    #fig.tight_layout()
	    #fig.savefig("/home/coco/dataset/results/frameOut/%s"%(save_name), dpi=200)
	    #axl.cla()
            if (display):
                plt.axis('off')
                fig.canvas.flush_events()
                plt.draw()
                fig.tight_layout()
                if(True):
                    fig.savefig("/home/coco/dataset/results/frameOut/%s"%(jpg_name),dpi = 200)
                ax1.cla()


    #print("Total Tracking took: %.3f for %d frames or %.1f FPS"%(total_time,total_frames,total_frames/total_time))

def parse_args():
    """Parse input arguments."""
    parser = argparse.ArgumentParser(description='Experimenting Trackers with SORT')
    parser.add_argument('--NoDisplay', dest='display', help='Disables online display of tracker output (slow)',action='store_false')
    parser.add_argument('--dlib', dest='use_dlibTracker', help='Use dlib correlation tracker instead of kalman tracker',action='store_true')
    parser.add_argument('--save', dest='saver', help='Saves frames with tracking output, not used if --NoDisplay',action='store_true')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main()
