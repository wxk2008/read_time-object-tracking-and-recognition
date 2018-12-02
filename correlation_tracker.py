"""
@author: Mahmoud I.Zidan
"""

from dlib import correlation_tracker, rectangle
#import dlib

'''Appearance Model'''
class CorrelationTracker:

  count = 0
  def __init__(self,bbox,img):
    self.tracker = correlation_tracker()
    #print("correctionTracker")
    #print(bbox)
    self.tracker.start_track(img,rectangle(long(bbox[0]),long(bbox[1]),long(bbox[2]),long(bbox[3])))
    #self.tracker.start_track(img,rectangle(long(bbox[0]), long(bbox[1]), long(bbox[0]+bbox[2]),long(bbox[1] + bbox[3])))
    self.confidence = 0. # measures how confident the tracker is! (a.k.a. correlation score)

    self.time_since_update = 0
    self.id = CorrelationTracker.count
    CorrelationTracker.count += 1
    self.hits = 0
    self.hit_streak = 0
    self.age = 0

  def predict(self,img):
    self.confidence = self.tracker.update(img)

    self.age += 1
    if (self.time_since_update > 0):
      self.hit_streak = 0
    self.time_since_update += 1

    return self.get_state()

  def update(self,bbox,img):
    self.time_since_update = 0
    self.hits += 1
    self.hit_streak += 1

    '''re-start the tracker with detected positions (it detector was active)'''
    if bbox != []:
      self.tracker.start_track(img, rectangle(long(bbox[0]), long(bbox[1]), long(bbox[2]), long(bbox[3])))
    '''
    Note: another approach is to re-start the tracker only when the correlation score fall below some threshold
    i.e.: if bbox !=[] and self.confidence < 10.
    but this will reduce the algo. ability to track objects through longer periods of occlusions.
    '''

  def get_state(self):
    pos = self.tracker.get_position()
    return [pos.left(), pos.top(),pos.right(),pos.bottom()]
