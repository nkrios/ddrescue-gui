#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# GetDevInfo tests for DDRescue-GUI Version 1.6.2
# This file is part of DDRescue-GUI.
# Copyright (C) 2013-2017 Hamish McIntyre-Bhatty
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

#import modules.
import unittest

#Set to avoid errors.
Linux = True

#Functions to return fake DiskInfo dictionary.
def ReturnFakeDiskInfoLinux():
    DiskInfo = {}

    #Fictional /dev/sda.
    DiskInfo["/dev/sda"] = {}
    DiskInfo["/dev/sda"]["Product"] = "FakeDisk"
    DiskInfo["/dev/sda"]["Vendor"] = "ThereIsNone"
    DiskInfo["/dev/sda"]["Name"] = "/dev/sda"
    DiskInfo["/dev/sda"]["Description"] = "Fake Hard Disk Drive"
    DiskInfo["/dev/sda"]["RawCapacity"] = "56483132"
    DiskInfo["/dev/sda"]["HostDevice"] = "N/A"
    DiskInfo["/dev/sda"]["Capacity"] = "200GB"
    DiskInfo["/dev/sda"]["Type"] = "Device"
    DiskInfo["/dev/sda"]["Partitions"] = ["/dev/sda1", "/dev/sda2"]

    #Fictional /dev/sda1
    DiskInfo["/dev/sda1"] = {}
    DiskInfo["/dev/sda1"]["Product"] = "Host Device: FakeDisk"
    DiskInfo["/dev/sda1"]["Vendor"] = "FakeOS v3"
    DiskInfo["/dev/sda1"]["Name"] = "/dev/sda1"
    DiskInfo["/dev/sda1"]["Description"] = "EXT4 Volume"
    DiskInfo["/dev/sda1"]["RawCapacity"] = "5648313"
    DiskInfo["/dev/sda1"]["HostDevice"] = "/dev/sda"
    DiskInfo["/dev/sda1"]["Capacity"] = "20GB"
    DiskInfo["/dev/sda1"]["Type"] = "Partition"
    DiskInfo["/dev/sda1"]["Partitions"] = []

    #Fictional /dev/sda2
    DiskInfo["/dev/sda2"] = {}
    DiskInfo["/dev/sda2"]["Product"] = "Host Device: FakeDisk"
    DiskInfo["/dev/sda2"]["Vendor"] = "FakeOS v3"
    DiskInfo["/dev/sda2"]["Name"] = "/dev/sda2"
    DiskInfo["/dev/sda2"]["Description"] = "EXT3 Volume"
    DiskInfo["/dev/sda2"]["RawCapacity"] = "564313"
    DiskInfo["/dev/sda2"]["HostDevice"] = "/dev/sda"
    DiskInfo["/dev/sda2"]["Capacity"] = "2.5GB"
    DiskInfo["/dev/sda2"]["Type"] = "Partition"
    DiskInfo["/dev/sda2"]["Partitions"] = []

    return DiskInfo

def ReturnFakeDiskInfoMac():
    DiskInfo = {}

    #Fictional /dev/disk0.
    DiskInfo["/dev/disk0"] = {}
    DiskInfo["/dev/disk0"]["Product"] = "FakeDisk"
    DiskInfo["/dev/disk0"]["Vendor"] = "ThereIsNone"
    DiskInfo["/dev/disk0"]["Name"] = "/dev/disk0"
    DiskInfo["/dev/disk0"]["Description"] = "Fake Hard Disk Drive"
    DiskInfo["/dev/disk0"]["RawCapacity"] = "56483132"
    DiskInfo["/dev/disk0"]["HostDevice"] = "N/A"
    DiskInfo["/dev/disk0"]["Capacity"] = "200GB"
    DiskInfo["/dev/disk0"]["Type"] = "Device"
    DiskInfo["/dev/disk0"]["Partitions"] = ["/dev/disk0s1", "/dev/disk0s2"]

    #Fictional /dev/disk0s1
    DiskInfo["/dev/disk0s1"] = {}
    DiskInfo["/dev/disk0s1"]["Product"] = "Host Device: FakeDisk"
    DiskInfo["/dev/disk0s1"]["Vendor"] = "FakeOS v3"
    DiskInfo["/dev/disk0s1"]["Name"] = "/dev/disk0s1"
    DiskInfo["/dev/disk0s1"]["Description"] = "HFS+ Volume"
    DiskInfo["/dev/disk0s1"]["RawCapacity"] = "5648313"
    DiskInfo["/dev/disk0s1"]["HostDevice"] = "/dev/disk0"
    DiskInfo["/dev/disk0s1"]["Capacity"] = "20GB"
    DiskInfo["/dev/disk0s1"]["Type"] = "Partition"
    DiskInfo["/dev/disk0s1"]["Partitions"] = []

    #Fictional /dev/disk0s2
    DiskInfo["/dev/disk0s2"] = {}
    DiskInfo["/dev/disk0s2"]["Product"] = "Host Device: FakeDisk"
    DiskInfo["/dev/disk0s2"]["Vendor"] = "FakeOS v3"
    DiskInfo["/dev/disk0s2"]["Name"] = "/dev/disk0s2"
    DiskInfo["/dev/disk0s2"]["Description"] = "NTFS Volume"
    DiskInfo["/dev/disk0s2"]["RawCapacity"] = "564313"
    DiskInfo["/dev/disk0s2"]["HostDevice"] = "/dev/disk0"
    DiskInfo["/dev/disk0s2"]["Capacity"] = "2.5GB"
    DiskInfo["/dev/disk0s2"]["Type"] = "Partition"
    DiskInfo["/dev/disk0s2"]["Partitions"] = []

    return DiskInfo

class TestDevInfoIsPartition(unittest.TestCase):
    def setUp(self):
        #Create a fictional DiskInfo distionary for it to test against.
        if Linux:
            GetDevInfo.getdevinfo.DiskInfo = ReturnFakeDiskInfoLinux()

        else:
            GetDevInfo.getdevinfo.DiskInfo = ReturnFakeDiskInfoMac()

    def tearDown(self):
        del GetDevInfo.getdevinfo.DiskInfo

    @unittest.skipUnless(Linux, "Linux-specific test")
    def testIsPartitionLinux(self):
        #Cdrom drives.
        for CDROM in ["/dev/cdrom", "/dev/dvd", "/dev/sr0", "/dev/sr1", "/dev/sr10", "/dev/scd0", "/dev/scd1", "/dev/scd10"]:
            self.assertFalse(DevInfoTools().IsPartition(CDROM))

        #Floppy drives.
        for FLOPPY in ["/dev/fd0", "/dev/fd1", "/dev/fd10"]:
            self.assertFalse(DevInfoTools().IsPartition(FLOPPY))

        #Devices.
        for DEVICE in ["/dev/sda", "/dev/sdb", "/dev/hda", "/dev/hdb"]:
            self.assertFalse(DevInfoTools().IsPartition(DEVICE))

        #Partitions.
        for PARTITION in ["/dev/sda1", "/dev/sda2", "/dev/sda11", "/dev/sda56"]:
            self.assertTrue(DevInfoTools().IsPartition(PARTITION))

    @unittest.skipUnless(not Linux, "Mac-specific test")
    def testIsPartitionMac(self):
        #Devices.
        for DEVICE in ["/dev/disk0", "/dev/disk1", "/dev/disk10"]:
            self.assertFalse(DevInfoTools().IsPartition(DEVICE))

        #Partitions.
        for PARTITION in ["/dev/disk0s2", "/dev/disk0s1", "/dev/disk0s45", "/dev/disk1s5", "/dev/disk1s45"]:
            self.assertTrue(DevInfoTools().IsPartition(PARTITION))
