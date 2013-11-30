#! /usr/bin/env python

import httplib, urllib2, smtplib, sys, os
try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

class Plugin(indigo.PluginBase):

	directions = {
			'up': 0,
			'down': 2,
			'left': 6,
			'right': 4,
			'stop': 3
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

		if path is None:
			self.debugLog("no path defined")

        url = 'http://%s/%s?user=%s&pwd=%s' % (dev.pluginProps['ipaddress'], cgiPath, dev.pluginProps['username'], dev.pluginProps['password'])
        for param in params:
            url = url + '&%s=%s' % (param, params[param])

        self.debugLog(u"url xmitted: ")

        return urllib2.urlopen(url)

	def move(self, pluginAction, dev):

		# move camera
		self.debugLog(u"move called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		direction = pluginAction.props['direction']

		if direction is None:
			self.debugLog(u"no direction defined")
			return

		self.xmitToCamera("/decoder_control.cgi", {'command': str(self.directions[direction])}, dev)
		self.stop(pluginAction, dev)

	def stop(self, pluginAction, dev):

		# stop camera movement
		self.debugLog(u"stop called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		self.xmitToCamera("/decoder_control.cgi", {'command': str(self.directions['stop'])}, dev)

	def disable(self, pluginAction, dev):

		# Disable audio and video streams
		self.debugLog(u"disable called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

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
		self.xmitToCamera("/set_forbidden.cgi", params, dev)

	def enable(self, pluginAction, dev):

		# Enable audio and video streams
		self.debugLog(u"enable called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

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

		self.xmitToCamera("/set_forbidden.cgi", params, dev)

	def motionAlarmOn(self, pluginAction, dev):

		#Enable email alerts when motion sensed
		self.debugLog(u"motionAlarmOn called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

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

		self.xmitToCamera("/set_alarm.cgi", params, dev)

	def motionAlarmOff(self, pluginAction, dev):

		#Disable email alerts when motion sensed
		self.debugLog(u"motionAlarmOff called")

		params = {
			'motion_armed':0
		}

		self.xmitToCamera("/set_alarm.cgi", params, dev)

	def irOn(self, pluginAction, dev):

		#Enable Infrared LEDs
		self.debugLog(u"irOn called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		self.xmitToCamera("/decoder_control.cgi", {'command':95}, dev)

	def irOff(self, pluginAction, dev):

		#Disable Infrared LEDs
		self.debugLog(u"irOff called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		self.xmitToCamera("/decoder_control.cgi", {'command':94}, dev)

	def snap(self, pluginAction, dev):

		self.debugLog(u"snap called")

		if dev is None:
			self.debugLog(u"no device defined")

		username = dev.pluginProps['username']
		password = dev.pluginProps['password']

		path = "/snapshot.cgi?user="+username+"&pwd="+password
		resp = self.xmitToCamera(path, dev)
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
		img = MIMEImage(fp.read())
		fp.close()
		msg.attach(img)

		s = smtplib.SMTP(self.pluginPrefs['smtphost'],int(self.pluginPrefs['smtpport']))
		s.ehlo()
		s.starttls()
		s.ehlo
		s.login(self.pluginPrefs['smtpuser'], self.pluginPrefs['smtppass'])
		s.sendmail(self.pluginPrefs['sender'], pluginAction.props['recipient'], msg.as_string())
		s.quit()
