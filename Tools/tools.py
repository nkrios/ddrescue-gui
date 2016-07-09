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

    def IsMounted(self, Partition, MountPoint=None):
        """Checks if the given partition is mounted.
        Partition is the given partition to check.
        If MountPoint is specified, check if the partition is mounted there, rather than just if it's mounted.
        Return boolean True/False.
        """
        if MountPoint == None:
            logger.debug("Tools: Main().IsMounted(): Checking if "+Partition+" is mounted...")
            MountInfo = self.StartProcess("mount", ReturnOutput=True)[1]

            Mounted = False

            for Line in MountInfo.split("\n"):
                if len(Line) != 0:
                    if Line.split()[0] == Partition:
                        Mounted = True

        else:
            #Check where it's mounted to.
            logger.debug("Tools: Main().IsMounted(): Checking if "+Partition+" is mounted at "+MountPoint+"...")

            Mounted = False

            if self.GetMountPointOf(Partition) == MountPoint:
                Mounted = True

        if Mounted:
            logger.debug("Tools: Main().IsMounted(): It is. Returning True...")
            return True

        else:
            logger.debug("Tools: Main().IsMounted(): It isn't. Returning False...")
            return False

    def GetMountPointOf(self, Partition):
        """Returns the mountpoint of the given partition, if any.
        Otherwise, return None"""
        logger.info("Tools: Main().GetMountPointOf(): Trying to get mount point of partition "+Partition+"...")

        MountInfo = self.StartProcess("mount", ReturnOutput=True)[1]
        MountPoint = None

        for Line in MountInfo.split("\n"):
            SplitLine = Line.split()

            if len(SplitLine) != 0:
                if Partition == SplitLine[0]:
                    MountPoint = SplitLine[2]

        if MountPoint != None:
            logger.info("Tools: Main().GetMountPointOf(): Found it! MountPoint is "+MountPoint+"...")

        else:
            logger.info("Tools: Main().GetMountPointOf(): Didn't find it...")

        return MountPoint

    def MountPartition(self, Partition, MountPoint, Options=""):
        """Mounts the given partition.
        Partition is the partition to mount.
        MountPoint is where you want to mount the partition.
        Options is non-mandatory and contains whatever options you want to pass to the mount command.
        The default value for Options is an empty string.
        """
        if Options != "":
            logger.info("Tools: Main().MountPartition(): Preparing to mount "+Partition+" at "+MountPoint+" with extra options "+Options+"...")

        else:
            logger.info("Tools: Main().MountPartition(): Preparing to mount "+Partition+" at "+MountPoint+" with no extra options...")
            
        MountInfo = self.StartProcess("mount", ReturnOutput=True)[1]

        #There is a partition mounted here. Check if our partition is already mounted in the right place.
        if MountPoint == self.GetMountPointOf(Partition):
            #The correct partition is already mounted here.
            logger.debug("Tools: Main().MountPartition(): Partition: "+Partition+" was already mounted at: "+MountPoint+". Continuing...")
            return 0

        elif MountPoint in MountInfo:
            #Something else is in the way. Unmount that partition, and continue.
            logger.warning("Tools: Main().MountPartition(): Unmounting filesystem in the way at "+MountPoint+"...")
            Retval = self.Unmount(MountPoint)

            if Retval != 0:
                logger.error("Tools: Main().MountPartition(): Couldn't unmount "+MountPoint+", preventing the mounting of "+Partition+"! Skipping mount attempt.")
                return False

        #Create the dir if needed.
        if os.path.isdir(MountPoint) == False:
            os.makedirs(MountPoint)
    
        #Mount the device to the mount point.
        Retval = self.StartProcess("mount "+Options+" "+Partition+" "+MountPoint)

        if Retval == 0:
            logger.debug("Tools: Main().MountPartition(): Successfully mounted partition!")

        else:
            logger.warning("Tools: Main().MountPartition(): Failed to mount partition!")

        return Retval

    def UnmountDisk(self, Disk):
        """Unmount the given disk"""
        logger.debug("Tools: Main().UnmountDisk(): Checking if "+Disk+" is mounted...")

        #Check if it is mounted.
        MountPoint = self.GetMountPointOf(Disk)

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
