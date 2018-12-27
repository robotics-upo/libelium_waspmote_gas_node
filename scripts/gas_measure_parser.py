#!/usr/bin/env python
# license removed for brevity
import sys
import rospy
from libelium_waspmote_gas_node.msg import GasMeasure

# msg is a list of strings
class GasMeasureParser:
  def __init__(self):
    self.seq = 0
    self.msg = GasMeasure()
    self.msg.head.seq = 0
    self.msg.head.frame_id = 'base_link'
  
  # Gets the info and stores it in completed_info
  def parseMessage(self,str_msg):
    print str_msg
    self.completed_info = {}
    split_msg = str_msg.split()
    for i in range(len(split_msg)-2):
      self.parseInfo(split_msg[i], split_msg[i+1],split_msg[i+2])
    return self.completed_info
      
  # Parses a part of the message into completed info
  def parseInfo(self,msg, msg_1,msg_2):
    if msg=='seconds':
      self.completed_info['time'] = int(msg_1[1:])
    elif msg=='Acceleration':
      if msg_1=='X:':
        self.completed_info['accel_x']=int(msg_2)
      elif msg_1=='Y:':
        self.completed_info['accel_y']=int(msg_2)  
      elif msg_1=='Z:':
        self.completed_info['accel_z']=int(msg_2)
    elif msg=='Battery':
      if msg_1=='Level:':
        self.completed_info['bat_perc']=int(msg_2)
      elif msg_1=='(Volts):':
        self.completed_info['bat_level']=float(msg_2)
    if msg_1=='concentration:':
      if msg=='O2':
        self.completed_info['o2_conc']=float(msg_2)
      elif msg=='H2S':
        self.completed_info['h2s_conc']=float(msg_2)
      elif msg=='CO':
        self.completed_info['co_conc']=float(msg_2)
      elif msg=='CH4':
        self.completed_info['ch4_conc']=float(msg_2)  
    
    if msg_1=='Alarm:':
      if msg=='O2':
        self.completed_info['o2_alarm']=(msg_2=='ON')
      elif msg=='H2S':
        self.completed_info['h2s_alarm']=(msg_2=='ON')
      elif msg=='CO':
        self.completed_info['co_alarm']=(msg_2=='ON')
      elif msg=='CH4':
        self.completed_info['ch4_alarm']=(msg_2=='ON')
    
    if msg=='Temperature:':
      self.completed_info['temperature']=float(msg_1)
    if msg=='RH:':
      self.completed_info['RH']=float(msg_1)
    if msg=='Pressure:':
      self.completed_info['pressure']=float(msg_1)
      
  # Gets the message (ros dependent)
  def getMessage(self):
    self.msg.head.stamp = rospy.get_rostime()
    self.msg.head.seq = self.seq
    try:
      self.msg.time = self.completed_info['time']
      self.msg.bat_level = self.completed_info['bat_level']
      self.msg.bat_perc = self.completed_info['bat_perc']
      self.msg.temperature = self.completed_info['temperature']
      self.msg.RH = self.completed_info['RH']
      self.msg.pressure = self.completed_info['pressure']
      self.msg.O2_conc = self.completed_info['o2_conc']
      self.msg.H2S_conc = self.completed_info['h2s_conc']
      self.msg.CO_conc = self.completed_info['co_conc']
      self.msg.CH4_conc = self.completed_info['ch4_conc']
      self.msg.accel.x = self.completed_info['accel_x']
      self.msg.accel.y = self.completed_info['accel_y']
      self.msg.accel.z = self.completed_info['accel_z']
      
      self.msg.O2_alarm = self.completed_info['o2_alarm']
      self.msg.H2S_alarm = self.completed_info['h2s_alarm']
      self.msg.CO_alarm = self.completed_info['co_alarm']
      self.msg.CH4_alarm = self.completed_info['ch4_alarm']
      
      self.seq = self.seq + 1
      return self.msg
    except KeyError:
      return None
    return None
      