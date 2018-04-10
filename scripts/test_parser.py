#!/usr/bin/env python
# license removed for brevity
import sys
from siar_gas_sensor.msg import GasMeasure
from gas_measure_parser import GasMeasureParser

if __name__ == '__main__':
  gmp = GasMeasureParser()
  
  if len(sys.argv)<2:
    print 'Usage: ',sys.argv[0],' <test_file>'
  else:
    file = open(sys.argv[1],'r')
    
    if gmp.parseMessage(file.read())==None:
      print 'Could not parse the message'
      
    else:
      print 'Message file parsed successfully'
      for k, v in gmp.completed_info.items():
        print k,':',v
        
    
