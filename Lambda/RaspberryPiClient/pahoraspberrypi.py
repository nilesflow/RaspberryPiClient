#!/usr/bin/env python
# -*- coding: utf-8 -*-

# user modules
from pyfw.pahoawsiot import PahoAwsIot

class PahoRaspberryPi(PahoAwsIot, object):
 """
 PahoのWrapper
 Callbackを実装するため
  """
 
 def __init__(self, **kargs):
  super(PahoRaspberryPi, self).__init__(**kargs)
  
  self.on_message = kargs['on_message']

 def _on_message(self, mosq, obj, msg):
  """
  callbackを呼び出し
  """
  self.on_message(msg)