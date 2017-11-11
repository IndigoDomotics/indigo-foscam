#! /usr/bin/env python

import httplib, urllib2, smtplib, sys, os
try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

class Plugin(indigo.PluginBase):

	#maps directions to command codes
	directions = {
		'up': 0,
		'down': 2,
		'left': 6,
		'right': 4,
		'stop': 3
	}

	#maps preset id to command codes for set
	presets = {
		'1': { 'set': 30, 'go': 31},
		'2': { 'set': 32, 'go': 33},
		'3': { 'set': 34, 'go': 35},
		'4': { 'set': 36, 'go': 37},
		'5': { 'set': 38, 'go': 39},
		'6': { 'set': 40, 'go': 41},
		'7': { 'set': 42, 'go': 43},
		'8': { 'set': 44, 'go': 45},
		'9': { 'set': 46, 'go': 47},
		'10': { 'set': 48, 'go': 49},
		'11': { 'set': 50, 'go': 51},
		'12': { 'set': 52, 'go': 53},
		'13': { 'set': 54, 'go': 55},
		'14': { 'set': 56, 'go': 57},
		'15': { 'set': 58, 'go': 59},
		'16': { 'set': 60, 'go': 61}
    }

	def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
		indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
		self.debug = True

	def __del__(self):
		indigo.PluginBase.__del__(self)

	def startup(self):
		self.debugLog(u"startup called")

	def shutdown(self):
		self.debugLog(u"shutdown called")

	def xmitToCamera(self, cgiPath, params, dev):

		if cgiPath is None: 
			return self.debugLog("no path defined")

		url = 'http://%s/%s?user=%s&pwd=%s' % (dev.pluginProps['ipaddress'], cgiPath, dev.pluginProps['username'], dev.pluginProps['password'])
		for param in params:
			url = url + '&%s=%s' % (param, params[param])

		self.debugLog(u"url xmitted: "+url)

		return urllib2.urlopen(url)

	# move camera
	def move(self, pluginAction, dev):

		self.debugLog(u"move called")
		if dev is None: 
			return self.debugLog(u"no device defined")

		direction = pluginAction.props['direction']
		if direction is None: 
			return self.debugLog(u"no direction defined")

		self.xmitToCamera("decoder_control.cgi", {'command': str(self.directions[direction])}, dev)

	# stop camera movement
	def stop(self, pluginAction, dev):

		self.debugLog(u"stop called")
		if dev is None: 
			return self.debugLog(u"no device defined")
		self.xmitToCamera("decoder_control.cgi", {'command': str(self.directions['stop'])}, dev)

	# move camera to preset position
	def goToPreset(self, pluginAction, dev):

		self.debugLog(u"goToPreset called")
		if dev is None: 
			return self.debugLog(u"no device defined")

		preset = pluginAction.props['preset']
		if preset is None: 
			return self.debugLog(u"no preset defined")

		self.xmitToCamera("decoder_control.cgi", {'command': str(self.presets[preset]['go'])}, dev)

	# save current camera position to preset id
	def setPreset(self, pluginAction, dev):

		self.debugLog(u"setPreset called")
		if dev is None: 
			return self.debugLog(u"no device defined")

		preset = pluginAction.props['preset']
		if preset is None: 
			return self.debugLog(u"no preset defined")

		self.xmitToCamera("decoder_control.cgi", {'command': str(self.presets[preset]['set'])}, dev)

	# Disable audio and video streams
	def disable(self, pluginAction, dev):

		self.debugLog(u"disable called")
		if dev is None: 
			return self.debugLog(u"no device defined")

		params = {
			'schedule_enable':-1,
			'schedule_sun_0':-1,
			'schedule_sun_1':-1,
			'schedule_sun_2':-1,
			'schedule_mon_0':-1,
			'schedule_mon_1':-1,
			'schedule_mon_2':-1,
			'schedule_tue_0':-1,
			'schedule_tue_1':-1,
			'schedule_tue_2':-1,
			'schedule_wed_0':-1,
			'schedule_wed_1':-1,
			'schedule_wed_2':-1,
			'schedule_thu_0':-1,
			'schedule_thu_1':-1,
			'schedule_thu_2':-1,
			'schedule_fri_0':-1,
			'schedule_fri_1':-1,
			'schedule_fri_2':-1,
			'schedule_sat_0':-1,
			'schedule_sat_1':-1,
			'schedule_sat_2':-1
		}
		self.xmitToCamera("set_forbidden.cgi", params, dev)

	# Enable audio and video streams
	def enable(self, pluginAction, dev):
	
		self.debugLog(u"enable called")
		if dev is None: 
			return self.debugLog(u"no device defined")

		params = {
			'schedule_enable':0,
			'schedule_sun_0':0,
			'schedule_sun_1':0,
			'schedule_sun_2':0,
			'schedule_mon_0':0,
			'schedule_mon_1':0,
			'schedule_mon_2':0,
			'schedule_tue_0':0,
			'schedule_tue_1':0,
			'schedule_tue_2':0,
			'schedule_wed_0':0,
			'schedule_wed_1':0,
			'schedule_wed_2':0,
			'schedule_thu_0':0,
			'schedule_thu_1':0,
			'schedule_thu_2':0,
			'schedule_fri_0':0,
			'schedule_fri_1':0,
			'schedule_fri_2':0,
			'schedule_sat_0':0,
			'schedule_sat_1':0,
			'schedule_sat_2':0
		}

		self.xmitToCamera("set_forbidden.cgi", params, dev)

	#Enable email alerts when motion sensed
	def motionAlarmOn(self, pluginAction, dev):
	
		self.debugLog(u"motionAlarmOn called")
		if dev is None: 
			return self.debugLog(u"no device defined")

		sensitivity = pluginAction.props['sensitivity']
		if sensitivity is None:
			self.debugLog(u"setting default sensitivity of max")
			sensitivity = 0

		params = {
			'motion_armed':1,
			'motion_sensitivity': sensitivity,
			'motion_compensation':1,
			'mail':1
		}

		self.xmitToCamera("set_alarm.cgi", params, dev)

	#Disable email alerts when motion sensed
	def motionAlarmOff(self, pluginAction, dev):
	
		self.debugLog(u"motionAlarmOff called")
		if dev is None: 
			return self.debugLog(u"no device defined")
		self.xmitToCamera("set_alarm.cgi", {'motion_armed':0}, dev)

	#Enable Infrared LEDs
	def irOn(self, pluginAction, dev):
	
		self.debugLog(u"irOn called")
		if dev is None: 
			return self.debugLog(u"no device defined")
		self.xmitToCamera("decoder_control.cgi", {'command':95}, dev)

	#Disable Infrared LEDs
	def irOff(self, pluginAction, dev):
	
		self.debugLog(u"irOff called")
		if dev is None: 
			return self.debugLog(u"no device defined")
		self.xmitToCamera("decoder_control.cgi", {'command':94}, dev)

	def snap(self, pluginAction, dev):
	
		self.debugLog(u"snap called")
		if dev is None: 
			return self.debugLog(u"no device defined")
		resp = self.xmitToCamera('snapshot.cgi', {}, dev)
		snapimg = resp.read()

		# todo: serialize filename, pass to sendViaEmail
		snappath = "/tmp/snap.jpg"
		f = open(snappath, 'w')
		f.write(snapimg)
		f.close()

		self.sendViaEmail(pluginAction, dev)

	def sendViaEmail(self, pluginAction, dev):
		
		# Create the container (outer) email message.
		msg = MIMEMultipart()
		msg['Subject'] = pluginAction.props['subject']
		msg['From'] = self.pluginPrefs['sender']
		msg['To'] = pluginAction.props['recipient']
		msg.preamble = 'cam snap test'

		# Open the files in binary mode.  Let the MIMEImage class automatically
		# guess the specific image type.
		fp = open('/tmp/snap.jpg', 'rb')
		img = MIMEImage(fp.read(), "jpeg")
		fp.close()
		msg.attach(img)

		s = smtplib.SMTP(self.pluginPrefs['smtphost'],int(self.pluginPrefs['smtpport']))
		s.ehlo()
		s.starttls()
		s.ehlo
		s.login(self.pluginPrefs['smtpuser'], self.pluginPrefs['smtppass'])
		s.sendmail(self.pluginPrefs['sender'], pluginAction.props['recipient'], msg.as_string())
		s.quit()
