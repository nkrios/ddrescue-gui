#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Tools Package for DDRescue-GUI Version 1.6
# This file is part of DDRescue-GUI.
# Copyright (C) 2013-2016 Hamish McIntyre-Bhatty
# DDRescue-GUI is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3 or,
# at your option, any later version.
#
# DDRescue-GUI is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DDRescue-GUI.  If not, see <http://www.gnu.org/licenses/>.

#Do future imports to prepare to support python 3. Use unicode strings rather than ASCII strings, as they fix potential problems.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

#Begin Main Class.
class Main():
    def StartProcess(self, Command, ReturnOutput=False):
        """Start a given process, and return output and return value if needed"""
        logger.debug("Tools: Main().StartProcess(): Starting process: "+Command)
        runcmd = subprocess.Popen("LC_ALL=C "+Command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

        while runcmd.poll() == None:
            time.sleep(0.25)

        #Save runcmd.stdout.readlines, and runcmd.returncode, as they tend to reset fairly quickly.
        Output = runcmd.stdout.readlines()
        Retval = int(runcmd.returncode)

        #Log this info in a debug message.
        logger.debug("Tools: Main().StartProcess(): Process: "+Command+": Return Value: "+unicode(Retval)+", Output: \"\n\n"+''.join(Output)+"\"\n")

        if ReturnOutput == False:
            #Return the return code back to whichever function ran this process, so it can handle any errors.
            return Retval
        else:
            #Return the return code, as well as the output.
            return Retval, ''.join(Output)

    def GetDiskMountPoint(self, Device):
        """Find if the given device or file is mounted or not, and return the mount point, or None if it isn't mounted"""
        #Run a command to get filesystem info.
        Retval, Output = self.StartProcess(Command="df", ReturnOutput=True)

        #Read the output and find the info. ('None' will be returned automatically if we don't return anything, for example if the device isn't found in Output)
        for Line in Output.split("\n"):
            try:
                #Grab the device.
                Dev = Line.split()[0]
                if Linux:
                    MountPoint = ' '.join(Line.split()[5:]).replace(' ', '\\ ').replace("x20", " ")

                else:
                    MountPoint = ' '.join(Line.split()[8:]).replace(' ', '\\ ').replace("x20", " ")

            except IndexError:
                #Ignore IndexErrors.
                continue

            else:
                try:
                    #Check if we have the right mountpoint for a device.
                    if Dev == Device and MountPoint[0] == "/":
                        return MountPoint

                    #In case we were given a mountpont, also check if the MountPoint equals the Device.
                    elif MountPoint == Device:
                        return MountPoint

                except: continue

    def MountDisk(self, Disk, MountPoint):
        """Mount the given disk (partition)"""
        #Also, check that it isn't already mounted, and that nothing else is already mounted there.
        CurrentMountPoint = self.GetDiskMountPoint(Disk)

        if CurrentMountPoint != None:
            #Unmount the disk.
            self.UnmountDisk(Disk)

        #Create the mountpoint if needed.
        if os.path.isdir(MountPoint) == False:
            os.makedirs(MountPoint)

        #Mount the disk to the mount point.
        Retval = self.StartProcess(Command="mount "+Disk+" "+MountPoint, ReturnOutput=False)

        #Check it worked.
        if Retval == 0:
            logger.debug("Tools() Main().MountDisk(): Mounting "+Disk+" to "+MountPoint+" Succeeded!")

        else:
            logger.warning("Tools() Main().MountDisk(): Mounting "+Disk+" to "+MountPoint+" Failed! Retval: "+unicode(Retval))

        return Retval

    def UnmountDisk(self, Disk):
        """Unmount the given disk"""
        logger.debug("Tools: Main().UnmountDisk(): Checking if "+Disk+" is mounted...")

        #Check if it is mounted.
        MountPoint = self.GetDiskMountPoint(Disk)

        if MountPoint == None:
            #The disk isn't mounted.
            #Set Retval to 0 and log this.
            Retval = 0
            logger.info("Tools: Main().UnmountDisk(): "+Disk+" was not mounted. Continuing...")

        else:
            #The disk is mounted.
            logger.debug("Tools: Main().UnmountDisk(): Unmounting "+Disk+"...")

            #Unmount it.
            if Linux:
                Retval = self.StartProcess(Command="umount "+Disk, ReturnOutput=False)

            else:
                Retval = self.StartProcess(Command="diskutil umount "+Disk, ReturnOutput=False)

            #Check that this worked okay.
            if Retval != 0:
                #It didn't, for some strange reason.
                logger.warning("Tools: Main().UnmountDisk(): Unmounting "+Disk+": Failed!")

            else:
                logger.info("Tools: Main().UnmountDisk(): Unmounting "+Disk+": Success!")
            
        #Return the return value
        return Retval

#End Main Class.
