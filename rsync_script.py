#!/bin/python

import sys
import os
import commands
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

runtime_dir_path = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.append(os.path.abspath(os.path.join(runtime_dir_path, '../lib/python')))

def deviceslist():
    devicecontrollerlist = ["00:1f.2", "00:11.4"]
    satadevices = []
    if devicecontrollerlist == "":
        pass
    else:
	for controller in devicecontrollerlist:
            f = os.popen(("ls -l /dev/disk/by-path/pci-0000:%s* | grep -v part | cut -d'/' -f7") % controller)
            for i in f.readlines():
	        if not i in commands.getoutput("df -h /boot | grep /dev | awk '{print $1}'"):
		    i.strip("\n")
		    satadevices.append(i)
                    
    satadevices = sorted(satadevices)
    if not satadevices:
        print
        print "\033[1;31mThere are no devices attached\033[1;m"
        print
        exit()
    else:
        return satadevices

def ismount(dev):
    devmnt = commands.getoutput("df")
    if dev in devmnt:
        x = "mounted"
        return x
    else:
        x = "not mounted"
        return x

def colors(sd, cru_number):
    x=ismount(sd)
    if x == "not mounted":
        csi = "\x1B["
        reset = csi + "m"
        mntred = (csi + "0;48;5;214m" + x + csi + "0m")
        return "\t/mount/CRU%s\t|\t/dev/%s\t|\t %s\t" % (cru_number, sd, mntred)
    elif x == "mounted":
        csi = "\x1B["
        reset = csi + "m"
        mntgreen = (csi + "0;42m" + x + csi + "0m")
        return "\t/mount/CRU%s\t|\t/dev/%s\t|\t %s\t" % (cru_number, sd, mntgreen)

def mount(cru_number):
    if cru_number in str(range(0, 6)):
        sd = devices[int(cru_number)]
        x = cru_number
	if not os.path.exists("/mount/CRU%s") % x:
	    os.mkdir(("/mount/CRU%s" % x), 777)
	os.system("mount /dev/%s1 /mount/CRU%s 2>>/dev/null" % (sd, x)

def umount(cru_number):
    if cru_number in str(range(0, 6)):
        sd = devices[int(cru_number)]
        y = cru_number
	if os.path.ismount("/mount/CRU%s" % x):
	    os.system("umount /dev/%s1" % sd)

def fix_perm():
    os.system("cd /media && find . -type d -exec chmod -v 777 {} \; && find . -type f -exec chmod -v 777 {} \;")
    
def main():
    devices = deviceslist()
    for sd in devices:
        cru_number = devices.index(sd)
        print
        print colors(sd, cru_number)
    print
    cru_number = input("Insert the CRU number to use: ")
    status=ismount(devices[cru_number])
    if status == "mounted":
	pass
    elif status == "not mounted":
        print "/mount/CRU%s is not mounted. Mounting the drive.. " % cru_number
        mount(cru_number)
    	sd = devices[int(cru_number)]
    	print colors(sd, cru_number)
    if status == "mounted":
        print
        storedir = raw_input("Drag and drop the directory: ")
	storedir = storedir.replace('"', '')
	storedir = storedir.replace("'", "")
        print
	print "Starting copying files from:" 
        print storedir
	print "To:"
	print "/mount/CRU%s" % cru_number
	print
        os.system("cd %s ; rsync -vrP ./ /mount/CRU%s" % storedir, cru_number)
        print
	print "Fixing permissions.."
	fix_perm()
	print
        os.system("ls -lh /mount/CRU%s" % cru_number)
	print
        print "\033[1;32mCopy completed.\033[1;m"
        print
	print "Unmounting CRU%s.." % cru_number
        umount(cru_number)
        exit()
    else:
        print
	print "Error. Use another slot please."

main()
