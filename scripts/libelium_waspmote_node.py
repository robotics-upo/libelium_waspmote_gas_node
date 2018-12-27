#!/usr/bin/env python
# license removed for brevity
import sys
import rospy
import serial
from libelium_waspmote_gas_node.msg import GasMeasure
import io
from gas_measure_parser import GasMeasureParser

class GasSerial:
  def __init__(self, serial_location):
     self.opened = False
     self.verbose = False
     if rospy.has_param('~verbose'):
       self.verbose = rospy.get_param('~verbose')
     self.parser = GasMeasureParser()
     
     try:
       self.ser = serial.Serial(serial_location, 115200, timeout=1)
       self.io = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser), errors='ignore')
       self.opened = True
       self.pub = rospy.Publisher('gas_info',GasMeasure, queue_size=2)
     except (serial.serialutil.SerialException):
       print 'Could not open the device: ',serial_location
         
    
  def waitMessage(self):
    if (self.opened):
      line = self.io.readline(200)
      
      if self.verbose:
        print line
        
      msg_raw = line
      if len(line) > 5:
        while line[0]!='*':
          line = self.io.readline(200)
          msg_raw+=line
          msg_raw+='\n'
          if self.verbose:
            print line
          if len(line) <1:
            break
        
        
        self.parser.parseMessage(msg_raw)
        for k, v in self.parser.completed_info.items():
          print k,':',v
        msg = self.parser.getMessage()
        if msg!=None:
          self.pub.publish(msg)
      
      
    
  def close(self):
    if self.opened:
      self.ser.close()
    
    

if __name__ == '__main__':
  rospy.init_node('gas_sensor_node')
  if rospy.has_param('~device'):
    serial_loc = rospy.get_param('~device')
  else:
    serial_loc = '/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AI04GXQT-if00-port0'
    
  gs = GasSerial(serial_loc)
  if gs.opened == True:
    while not rospy.is_shutdown():
      gs.waitMessage()
    
  gs.close()
    
    


    
