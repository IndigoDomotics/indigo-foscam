#! /bin/sh
# If using on Android, replace "/bin/sh" with "/system/bin/sh"
# Feb 23
[ -z "$1" ] && exec $0 h


######## set these options! ########
####################################
# cam username
user=""

# cam password
pass=""

# cam address or ip, with or without port.
# e.g., xxx.xx.xx.xxx:80
ip=""

# location to save snapshot
snapfile=""
####################################
####################################

addy="http://${user}:${pass}@${ip}"

arg=$#
while [ "$arg" -ne "0" ]; do

case "$1" in

50)
wget -q -O - "${addy}/camera_control.cgi?param=3&value=0"
shift; arg=$(($arg - 1));;

60)
wget -q -O - "${addy}/camera_control.cgi?param=3&value=1"
shift; arg=$(($arg - 1));;

alarm)
[ $2 = off ] && wget -q -O - "${addy}/set_alarm.cgi?motion_armed=0"
[ $2 = on ] && wget -q -O - "${addy}/set_alarm.cgi?motion_armed=1"
shift; shift; arg=$(($arg - 2));;

bright)
[ $2 = 1 ] && wget -q -O - "${addy}/camera_control.cgi?param=1&value=16"
[ $2 = 2 ] && wget -q -O - "${addy}/camera_control.cgi?param=1&value=32"
[ $2 = 3 ] && wget -q -O - "${addy}/camera_control.cgi?param=1&value=48"
[ $2 = 4 ] && wget -q -O - "${addy}/camera_control.cgi?param=1&value=64"
[ $2 = 5 ] && wget -q -O - "${addy}/camera_control.cgi?param=1&value=80"
[ $2 = 6 ] && wget -q -O - "${addy}/camera_control.cgi?param=1&value=96"
[ $2 = 7 ] && wget -q -O - "${addy}/camera_control.cgi?param=1&value=112"
[ $2 = 8 ] && wget -q -O - "${addy}/camera_control.cgi?param=1&value=128"
[ $2 = 9 ] && wget -q -O - "${addy}/camera_control.cgi?param=1&value=144"
[ $2 = 10 ] && wget -q -O - "${addy}/camera_control.cgi?param=1&value=160"
[ $2 = 11 ] && wget -q -O - "${addy}/camera_control.cgi?param=1&value=176"
[ $2 = 12 ] && wget -q -O - "${addy}/camera_control.cgi?param=1&value=192"
[ $2 = 13 ] && wget -q -O - "${addy}/camera_control.cgi?param=1&value=208"
[ $2 = 14 ] && wget -q -O - "${addy}/camera_control.cgi?param=1&value=224"
[ $2 = 15 ] && wget -q -O - "${addy}/camera_control.cgi?param=1&value=240"
[ $2 = 16 ] && wget -q -O - "${addy}/camera_control.cgi?param=1&value=255"
shift; shift; arg=$(($arg - 2));;

center)
wget -q -O - "${addy}/decoder_control.cgi?command=25"
shift; arg=$(($arg - 1));;

contrast)
wget -q -O - "${addy}/camera_control.cgi?param=2&value=$2"
shift; shift; arg=$(($arg - 2));;

down)
wget -q -O - "${addy}/decoder_control.cgi?command=2"
shift; arg=$(($arg - 1));;

flip)
wget -q -O - "${addy}/camera_control.cgi?param=5&value=1"
shift; arg=$(($arg - 1));;

go)
[ $2 = 1 ] && wget -q -O - "${addy}/decoder_control.cgi?command=31"
[ $2 = 2 ] && wget -q -O - "${addy}/decoder_control.cgi?command=33"
[ $2 = 3 ] && wget -q -O - "${addy}/decoder_control.cgi?command=35"
[ $2 = 4 ] && wget -q -O - "${addy}/decoder_control.cgi?command=37"
[ $2 = 5 ] && wget -q -O - "${addy}/decoder_control.cgi?command=39"
[ $2 = 6 ] && wget -q -O - "${addy}/decoder_control.cgi?command=41"
[ $2 = 7 ] && wget -q -O - "${addy}/decoder_control.cgi?command=43"
[ $2 = 8 ] && wget -q -O - "${addy}/decoder_control.cgi?command=45"
[ $2 = 9 ] && wget -q -O - "${addy}/decoder_control.cgi?command=47"
[ $2 = 10 ] && wget -q -O - "${addy}/decoder_control.cgi?command=49"
[ $2 = 11 ] && wget -q -O - "${addy}/decoder_control.cgi?command=51"
[ $2 = 12 ] && wget -q -O - "${addy}/decoder_control.cgi?command=53"
[ $2 = 13 ] && wget -q -O - "${addy}/decoder_control.cgi?command=55"
[ $2 = 14 ] && wget -q -O - "${addy}/decoder_control.cgi?command=57"
[ $2 = 15 ] && wget -q -O - "${addy}/decoder_control.cgi?command=59"
[ $2 = 16 ] && wget -q -O - "${addy}/decoder_control.cgi?command=61"
shift; shift; arg=$(($arg - 2));;

horiz)
wget -q -O - "${addy}/decoder_control.cgi?command=28"
shift; arg=$(($arg - 1));;

interval)
wget -q -O - "${addy}/set_alarm.cgi?mail=${2}"
shift; shift; arg=$(($arg - 2));;

ir)
[ $2 = on ] && wget -q -O - "${addy}/decoder_control.cgi?command=95"
[ $2 = off ] && wget -q -O - "${addy}/decoder_control.cgi?command=94"
shift; shift; arg=$(($arg - 2));;

led)
wget -q -O - "${addy}/set_misc.cgi?led_mode=$2"
shift; shift; arg=$(($arg - 2));;

left)
wget -q -O - "${addy}/decoder_control.cgi?command=6"
shift; arg=$(($arg - 1));;

mail)
[ $2 = off ] && wget -q -O - "${addy}/set_alarm.cgi?mail=0"
[ $2 = on ] && wget -q -O - "${addy}/set_alarm.cgi?mail=1"
shift; shift; arg=$(($arg - 2));;

mirror)
wget -q -O - "${addy}/camera_control.cgi?param=5&value=2"
shift; arg=$(($arg - 1));;

out)
wget -q -O - "${addy}/camera_control.cgi?param=3&value=2"
shift; arg=$(($arg - 1));;

reboot)
wget -q -O - "${addy}/reboot.cgi"
shift; arg=$(($arg - 1));;

right)
wget -q -O - "${addy}/decoder_control.cgi?command=4"
shift; arg=$(($arg - 1));;

sense)
wget -q -O - "${addy}/set_alarm.cgi?motion_sensitivity=${2}"
shift; shift; arg=$(($arg - 2));;

set)
# sets camera presets 1-16
[ $2 = 1 ] && wget -q -O - "${addy}/decoder_control.cgi?command=30"
[ $2 = 2 ] && wget -q -O - "${addy}/decoder_control.cgi?command=32"
[ $2 = 3 ] && wget -q -O - "${addy}/decoder_control.cgi?command=34"
[ $2 = 4 ] && wget -q -O - "${addy}/decoder_control.cgi?command=36"
[ $2 = 5 ] && wget -q -O - "${addy}/decoder_control.cgi?command=38"
[ $2 = 6 ] && wget -q -O - "${addy}/decoder_control.cgi?command=40"
[ $2 = 7 ] && wget -q -O - "${addy}/decoder_control.cgi?command=42"
[ $2 = 8 ] && wget -q -O - "${addy}/decoder_control.cgi?command=44"
[ $2 = 9 ] && wget -q -O - "${addy}/decoder_control.cgi?command=46"
[ $2 = 10 ] && wget -q -O - "${addy}/decoder_control.cgi?command=48"
[ $2 = 11 ] && wget -q -O - "${addy}/decoder_control.cgi?command=50"
[ $2 = 12 ] && wget -q -O - "${addy}/decoder_control.cgi?command=52"
[ $2 = 13 ] && wget -q -O - "${addy}/decoder_control.cgi?command=54"
[ $2 = 14 ] && wget -q -O - "${addy}/decoder_control.cgi?command=56"
[ $2 = 15 ] && wget -q -O - "${addy}/decoder_control.cgi?command=58"
[ $2 = 16 ] && wget -q -O - "${addy}/decoder_control.cgi?command=60"
shift; shift; arg=$(($arg - 2));;

setup)
wget -q -O - "${addy}/get_params.cgi"
wget -q -O - "${addy}/get_status.cgi"
wget -q -O - "${addy}/get_misc.cgi"
shift; arg=$(($arg - 1));;

gsetup)
wget -q -O - "${addy}/get_params.cgi" | grep -i "$2"
wget -q -O - "${addy}/get_status.cgi" | grep -i "$2"
wget -q -O - "${addy}/get_misc.cgi" | grep -i "$2"
shift; shift; arg=$(($arg - 2));;

sleep|wait|pause|p|s|w)
sleep $2
shift; shift; arg=$(($arg - 2));;

snap)
wget -q -O ${snapfile} "${addy}/snapshot.cgi?"
shift; arg=$(($arg - 1));;

speed)
wget -q -O - "${addy}/set_misc.cgi?ptz_patrol_rate=$2"
shift; shift; arg=$(($arg - 2));;

stop)
wget -q -O - "${addy}/decoder_control.cgi?command=3"
shift; arg=$(($arg - 1));;

up)
wget -q -O - "${addy}/decoder_control.cgi?command=0"
shift; arg=$(($arg - 1));;

vert)
wget -q -O - "${addy}/decoder_control.cgi?command=26"
shift; arg=$(($arg - 1));;

h|-h|help|--help|*)
echo "sleep|wait|pause|p|s|w- requires argument- will pause script for X seconds.
setup- dumps camera setup (as much as 200 lines)
gsetup- dumps setup but allows you to grep it for keyword. usage: cam gsetup (string)
led- requires argument 0-2. 2 is off, 0/1 on or flashing
snap- save snapshot to /sdcard/cam.jpg
speed- the speed the camera moves. 0-?, 0 is fastest, normal is 2-3
ir- turns IR on or off, must specify on or off
up/down/left/right/stop/center- starts movement, must use separate stop command to stop movement
contrast (0-6)- must specify number
bright (0-16)- must specify number 0-16
vert/horiz- start vert or horiz patrol
50/60/out- set 50hz, 60hz outdoor mode
flip/mirror- flip or mirror the image
alarm- specify on or off
mail- specify on or off to send email on motion detect
interval- image upload interval in seconds, 0 for off, 1 to 65535 for on
sense- motion sensitivity 0-4, 0 being most sensitive
reboot- reboots cam
set- set preset 1-16
go- go to preset 1-16"
shift; arg=$(($arg - 1));;

esac
done
