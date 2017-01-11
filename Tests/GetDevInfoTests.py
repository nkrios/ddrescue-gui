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
import wx
import os
import plistlib

#Set up resource path and determine OS.
if "wxGTK" in wx.PlatformInfo:
    #Set the resource path to /usr/share/ddrescue-gui/
    RescourcePath = '/usr/share/ddrescue-gui'
    Linux = True

    #Check if we're running on Parted Magic.
    if os.uname()[1] == "PartedMagic":
        PartedMagic = True

    else:
        PartedMagic = False

elif "wxMac" in wx.PlatformInfo:
    try:
        #Set the resource path from an environment variable, as mac .apps can be found in various places.
        RescourcePath = os.environ['RESOURCEPATH']

    except KeyError:
        #Use '.' as the rescource path instead as a fallback.
        RescourcePath = "."

    Linux = False
    PartedMagic = False

#Classes for test cases.
class Node1:
    def GetCopy(self):
        return self

    class vendor:
        string = "FakeVendor"

    class product:
        string = "FakeProduct"

    class capacity:
        string = 100000000000

class Node2:
    def GetCopy(self):
        return self

    class vendor:
        string = "FakeVendor2"

    class product:
        string = "FakeProduct2"

    class size:
        string = 10000000000000000000

class BadNode1:
    def GetCopy(self):
        return self

    class vendor:
        notstring = ""

    class product:
        notstring = ""

class BadNode2:
    def GetCopy(self):
        return self

    class vendor:
        notstring = ""

    class product:
        notstring = ""

    class capacity:
        #Too long, causes IndexError.
        string = 1000000000000000000000000000000000000000000000000

class BadNode3:
    def GetCopy(self):
        return self

    class vendor:
        notstring = ""

    class product:
        notstring = ""

    class size:
        string = "fghjk"

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
    DiskInfo["/dev/disk0"]["Partitions"] = ["/dev/disk0s1", "/dev/disk0s2", "/dev/disk0s3"]

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

    #Fictional /dev/disk0s3
    DiskInfo["/dev/disk0s3"] = {}
    DiskInfo["/dev/disk0s3"]["Product"] = "Host Device: FakeDisk"
    DiskInfo["/dev/disk0s3"]["Vendor"] = "FakeOS v3"
    DiskInfo["/dev/disk0s3"]["Name"] = "/dev/disk0s3"
    DiskInfo["/dev/disk0s3"]["Description"] = "FAT Volume"
    DiskInfo["/dev/disk0s3"]["RawCapacity"] = "564313"
    DiskInfo["/dev/disk0s3"]["HostDevice"] = "/dev/disk0"
    DiskInfo["/dev/disk0s3"]["Capacity"] = "24.5GB"
    DiskInfo["/dev/disk0s3"]["Type"] = "Partition"
    DiskInfo["/dev/disk0s3"]["Partitions"] = []

    return DiskInfo

def ReturnFakeDiskutilListPlist():
    return """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>AllDisks</key>
	<array>
		<string>disk0</string>
		<string>disk0s1</string>
		<string>disk0s2</string>
		<string>disk0s3</string>
	</array>
	<key>AllDisksAndPartitions</key>
	<array>
		<dict>
			<key>Content</key>
			<string>GUID_partition_scheme</string>
			<key>DeviceIdentifier</key>
			<string>disk0</string>
			<key>Partitions</key>
			<array>
				<dict>
					<key>Content</key>
					<string>EFI</string>
					<key>DeviceIdentifier</key>
					<string>disk0s1</string>
					<key>DiskUUID</key>
					<string>A0C85363-E33F-4708-9B6A-68BD0AA062C1</string>
					<key>Size</key>
					<integer>209715200</integer>
					<key>VolumeName</key>
					<string>EFI</string>
					<key>VolumeUUID</key>
					<string>85D67001-D93E-3687-A1C2-79D677F0C2E0</string>
				</dict>
				<dict>
					<key>Content</key>
					<string>Apple_HFS</string>
					<key>DeviceIdentifier</key>
					<string>disk0s2</string>
					<key>DiskUUID</key>
					<string>72914C17-6469-457F-B2F0-26BE5BD03843</string>
					<key>MountPoint</key>
					<string>/</string>
					<key>Size</key>
					<integer>42089095168</integer>
					<key>VolumeName</key>
					<string>OSX</string>
					<key>VolumeUUID</key>
					<string>AC723754-135E-39BE-8A81-C91228501E9B</string>
				</dict>
				<dict>
					<key>Content</key>
					<string>Apple_Boot</string>
					<key>DeviceIdentifier</key>
					<string>disk0s3</string>
					<key>DiskUUID</key>
					<string>353F6CFF-8E9C-4480-BC8B-D6357E15299E</string>
					<key>Size</key>
					<integer>650002432</integer>
					<key>VolumeName</key>
					<string>Recovery HD</string>
					<key>VolumeUUID</key>
					<string>F1573C36-EC30-3501-8E0A-E3A424585875</string>
				</dict>
			</array>
			<key>Size</key>
			<integer>42948853248</integer>
		</dict>
	</array>
	<key>VolumesFromDisks</key>
	<array>
		<string>OSX</string>
	</array>
	<key>WholeDisks</key>
	<array>
		<string>disk0</string>
	</array>
</dict>
</plist>"""

def ReturnFakeDiskutilInfoBadDisk0Plist():
    return """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Bootable</key>
	<false/>
	<key>CanBeMadeBootable</key>
	<false/>
	<key>CanBeMadeBootableRequiresDestroy</key>
	<false/>
	<key>Content</key>
	<string>GUID_partition_scheme</string>
	<key>DeviceBlockSize</key>
	<integer>512</integer>
	<key>DeviceIdentifier</key>
	<string>disk0</string>
	<key>DeviceNode</key>
	<string>/dev/disk0</string>
	<key>DeviceTreePath</key>
	<string>IODeviceTree:/PCI0@1e0000/pci8086,2829@1F,2/PRT0@0/PMP@0</string>
	<key>Ejectable</key>
	<false/>
	<key>EjectableMediaAutomaticUnderSoftwareControl</key>
	<false/>
	<key>EjectableOnly</key>
	<false/>
	<key>FreeSpace</key>
	<integer>0</integer>
	<key>GlobalPermissionsEnabled</key>
	<false/>
	<key>IOKitSize</key>
	<integer>42948853248</integer>
	<key>IORegistryEntryName</key>
	<string>VBOX HARDDISK Media</string>
	<key>LowLevelFormatSupported</key>
	<false/>
	<key>MediaType</key>
	<string>Generic</string>
	<key>MountPoint</key>
	<string></string>
	<key>OS9DriversInstalled</key>
	<false/>
	<key>ParentWholeDisk</key>
	<string>disk0</string>
	<key>RAIDMaster</key>
	<false/>
	<key>RAIDSlice</key>
	<false/>
	<key>Removable</key>
	<false/>
	<key>RemovableMedia</key>
	<false/>
	<key>RemovableMediaOrExternalDevice</key>
	<false/>
	<key>SMARTStatus</key>
	<string>Not Supported</string>
	<key>Size</key>
	<integer>42948853248</integer>
	<key>SupportsGlobalPermissionsDisable</key>
	<false/>
	<key>SystemImage</key>
	<false/>
	<key>VirtualOrPhysical</key>
	<string>Physical</string>
	<key>VolumeName</key>
	<string></string>
	<key>VolumeSize</key>
	<integer>0</integer>
	<key>WholeDisk</key>
	<true/>
	<key>Writable</key>
	<true/>
	<key>WritableMedia</key>
	<true/>
	<key>WritableVolume</key>
	<false/>
</dict>
</plist>"""

def ReturnFakeDiskutilInfoDisk0Plist():
    return """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Bootable</key>
	<false/>
	<key>BusProtocol</key>
	<string>SATA</string>
	<key>CanBeMadeBootable</key>
	<false/>
	<key>CanBeMadeBootableRequiresDestroy</key>
	<false/>
	<key>Content</key>
	<string>GUID_partition_scheme</string>
	<key>DeviceBlockSize</key>
	<integer>512</integer>
	<key>DeviceIdentifier</key>
	<string>disk0</string>
	<key>DeviceNode</key>
	<string>/dev/disk0</string>
	<key>DeviceTreePath</key>
	<string>IODeviceTree:/PCI0@1e0000/pci8086,2829@1F,2/PRT0@0/PMP@0</string>
	<key>Ejectable</key>
	<false/>
	<key>EjectableMediaAutomaticUnderSoftwareControl</key>
	<false/>
	<key>EjectableOnly</key>
	<false/>
	<key>FreeSpace</key>
	<integer>0</integer>
	<key>GlobalPermissionsEnabled</key>
	<false/>
	<key>IOKitSize</key>
	<integer>42948853248</integer>
	<key>IORegistryEntryName</key>
	<string>VBOX HARDDISK Media</string>
	<key>Internal</key>
	<true/>
	<key>LowLevelFormatSupported</key>
	<false/>
	<key>MediaName</key>
	<string>VBOX HARDDISK</string>
	<key>MediaType</key>
	<string>Generic</string>
	<key>MountPoint</key>
	<string></string>
	<key>OS9DriversInstalled</key>
	<false/>
	<key>ParentWholeDisk</key>
	<string>disk0</string>
	<key>RAIDMaster</key>
	<false/>
	<key>RAIDSlice</key>
	<false/>
	<key>Removable</key>
	<false/>
	<key>RemovableMedia</key>
	<false/>
	<key>RemovableMediaOrExternalDevice</key>
	<false/>
	<key>SMARTStatus</key>
	<string>Not Supported</string>
	<key>Size</key>
	<integer>42948853248</integer>
	<key>SolidState</key>
	<false/>
	<key>SupportsGlobalPermissionsDisable</key>
	<false/>
	<key>SystemImage</key>
	<false/>
	<key>TotalSize</key>
	<integer>42948853248</integer>
	<key>VirtualOrPhysical</key>
	<string>Physical</string>
	<key>VolumeName</key>
	<string></string>
	<key>VolumeSize</key>
	<integer>0</integer>
	<key>WholeDisk</key>
	<true/>
	<key>Writable</key>
	<true/>
	<key>WritableMedia</key>
	<true/>
	<key>WritableVolume</key>
	<false/>
</dict>
</plist>"""

def ReturnFakeDiskutilInfoDisk0s1Plist():
    return """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Bootable</key>
	<false/>
	<key>BusProtocol</key>
	<string>SATA</string>
	<key>CanBeMadeBootable</key>
	<false/>
	<key>CanBeMadeBootableRequiresDestroy</key>
	<false/>
	<key>Content</key>
	<string>EFI</string>
	<key>DeviceBlockSize</key>
	<integer>512</integer>
	<key>DeviceIdentifier</key>
	<string>disk0s1</string>
	<key>DeviceNode</key>
	<string>/dev/disk0s1</string>
	<key>DeviceTreePath</key>
	<string>IODeviceTree:/PCI0@1e0000/pci8086,2829@1F,2/PRT0@0/PMP@0</string>
	<key>DiskUUID</key>
	<string>A0C85363-E33F-4708-9B6A-68BD0AA062C1</string>
	<key>Ejectable</key>
	<false/>
	<key>EjectableMediaAutomaticUnderSoftwareControl</key>
	<false/>
	<key>EjectableOnly</key>
	<false/>
	<key>FreeSpace</key>
	<integer>0</integer>
	<key>GlobalPermissionsEnabled</key>
	<false/>
	<key>IOKitSize</key>
	<integer>209715200</integer>
	<key>IORegistryEntryName</key>
	<string>EFI System Partition</string>
	<key>Internal</key>
	<true/>
	<key>MediaName</key>
	<string></string>
	<key>MediaType</key>
	<string>Generic</string>
	<key>MountPoint</key>
	<string></string>
	<key>ParentWholeDisk</key>
	<string>disk0</string>
	<key>RAIDMaster</key>
	<false/>
	<key>RAIDSlice</key>
	<false/>
	<key>Removable</key>
	<false/>
	<key>RemovableMedia</key>
	<false/>
	<key>RemovableMediaOrExternalDevice</key>
	<false/>
	<key>SMARTStatus</key>
	<string>Not Supported</string>
	<key>Size</key>
	<integer>209715200</integer>
	<key>SolidState</key>
	<false/>
	<key>SupportsGlobalPermissionsDisable</key>
	<false/>
	<key>SystemImage</key>
	<false/>
	<key>TotalSize</key>
	<integer>209715200</integer>
	<key>VolumeName</key>
	<string>EFI</string>
	<key>VolumeSize</key>
	<integer>0</integer>
	<key>VolumeUUID</key>
	<string>85D67001-D93E-3687-A1C2-79D677F0C2E0</string>
	<key>WholeDisk</key>
	<false/>
	<key>Writable</key>
	<true/>
	<key>WritableMedia</key>
	<true/>
	<key>WritableVolume</key>
	<false/>
</dict>
</plist>"""

def ReturnFakeDiskutilInfoDisk0s2Plist():
    return """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Bootable</key>
	<true/>
	<key>BusProtocol</key>
	<string>SATA</string>
	<key>CanBeMadeBootable</key>
	<false/>
	<key>CanBeMadeBootableRequiresDestroy</key>
	<false/>
	<key>Content</key>
	<string>Apple_HFS</string>
	<key>DeviceBlockSize</key>
	<integer>512</integer>
	<key>DeviceIdentifier</key>
	<string>disk0s2</string>
	<key>DeviceNode</key>
	<string>/dev/disk0s2</string>
	<key>DeviceTreePath</key>
	<string>IODeviceTree:/PCI0@1e0000/pci8086,2829@1F,2/PRT0@0/PMP@0</string>
	<key>DiskUUID</key>
	<string>72914C17-6469-457F-B2F0-26BE5BD03843</string>
	<key>Ejectable</key>
	<false/>
	<key>EjectableMediaAutomaticUnderSoftwareControl</key>
	<false/>
	<key>EjectableOnly</key>
	<false/>
	<key>FilesystemName</key>
	<string>Journaled HFS+</string>
	<key>FilesystemType</key>
	<string>hfs</string>
	<key>FilesystemUserVisibleName</key>
	<string>Mac OS Extended (Journaled)</string>
	<key>FreeSpace</key>
	<integer>18913898496</integer>
	<key>GlobalPermissionsEnabled</key>
	<true/>
	<key>IOKitSize</key>
	<integer>42089095168</integer>
	<key>IORegistryEntryName</key>
	<string>OSX</string>
	<key>Internal</key>
	<true/>
	<key>JournalOffset</key>
	<integer>1310720</integer>
	<key>JournalSize</key>
	<integer>8388608</integer>
	<key>MediaName</key>
	<string></string>
	<key>MediaType</key>
	<string>Generic</string>
	<key>MountPoint</key>
	<string>/</string>
	<key>ParentWholeDisk</key>
	<string>disk0</string>
	<key>RAIDMaster</key>
	<false/>
	<key>RAIDSlice</key>
	<false/>
	<key>RecoveryDeviceIdentifier</key>
	<string>disk0s3</string>
	<key>Removable</key>
	<false/>
	<key>RemovableMedia</key>
	<false/>
	<key>RemovableMediaOrExternalDevice</key>
	<false/>
	<key>SMARTStatus</key>
	<string>Not Supported</string>
	<key>Size</key>
	<integer>42089095168</integer>
	<key>SolidState</key>
	<false/>
	<key>SupportsGlobalPermissionsDisable</key>
	<true/>
	<key>SystemImage</key>
	<false/>
	<key>TotalSize</key>
	<integer>42089095168</integer>
	<key>VolumeAllocationBlockSize</key>
	<integer>4096</integer>
	<key>VolumeName</key>
	<string>OSX</string>
	<key>VolumeSize</key>
	<integer>42089095168</integer>
	<key>VolumeUUID</key>
	<string>AC723754-135E-39BE-8A81-C91228501E9B</string>
	<key>WholeDisk</key>
	<false/>
	<key>Writable</key>
	<true/>
	<key>WritableMedia</key>
	<true/>
	<key>WritableVolume</key>
	<true/>
</dict>
</plist>"""

def ReturnFakeDiskutilInfoDisk0s3Plist():
    return """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Bootable</key>
	<true/>
	<key>BusProtocol</key>
	<string>SATA</string>
	<key>CanBeMadeBootable</key>
	<false/>
	<key>CanBeMadeBootableRequiresDestroy</key>
	<false/>
	<key>Content</key>
	<string>Apple_Boot</string>
	<key>DeviceBlockSize</key>
	<integer>512</integer>
	<key>DeviceIdentifier</key>
	<string>disk0s3</string>
	<key>DeviceNode</key>
	<string>/dev/disk0s3</string>
	<key>DeviceTreePath</key>
	<string>IODeviceTree:/PCI0@1e0000/pci8086,2829@1F,2/PRT0@0/PMP@0</string>
	<key>DiskUUID</key>
	<string>353F6CFF-8E9C-4480-BC8B-D6357E15299E</string>
	<key>Ejectable</key>
	<false/>
	<key>EjectableMediaAutomaticUnderSoftwareControl</key>
	<false/>
	<key>EjectableOnly</key>
	<false/>
	<key>FreeSpace</key>
	<integer>0</integer>
	<key>GlobalPermissionsEnabled</key>
	<false/>
	<key>IOKitSize</key>
	<integer>650002432</integer>
	<key>IORegistryEntryName</key>
	<string>Recovery HD</string>
	<key>Internal</key>
	<true/>
	<key>MediaName</key>
	<string></string>
	<key>MediaType</key>
	<string>Generic</string>
	<key>MountPoint</key>
	<string></string>
	<key>ParentWholeDisk</key>
	<string>disk0</string>
	<key>RAIDMaster</key>
	<false/>
	<key>RAIDSlice</key>
	<false/>
	<key>Removable</key>
	<false/>
	<key>RemovableMedia</key>
	<false/>
	<key>RemovableMediaOrExternalDevice</key>
	<false/>
	<key>SMARTStatus</key>
	<string>Not Supported</string>
	<key>Size</key>
	<integer>650002432</integer>
	<key>SolidState</key>
	<false/>
	<key>SupportsGlobalPermissionsDisable</key>
	<false/>
	<key>SystemImage</key>
	<false/>
	<key>TotalSize</key>
	<integer>650002432</integer>
	<key>VolumeName</key>
	<string>Recovery HD</string>
	<key>VolumeSize</key>
	<integer>0</integer>
	<key>VolumeUUID</key>
	<string>F1573C36-EC30-3501-8E0A-E3A424585875</string>
	<key>WholeDisk</key>
	<false/>
	<key>Writable</key>
	<true/>
	<key>WritableMedia</key>
	<true/>
	<key>WritableVolume</key>
	<false/>
</dict>
</plist>"""

class TestIsPartition(unittest.TestCase):
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

class TestGetVendorProductCapacityDescription(unittest.TestCase):
    def setUp(self):
        if Linux:
            self.Node1 = Node1().GetCopy()
            self.Node2 = Node2().GetCopy()
            self.BadNode1 = BadNode1().GetCopy()
            self.BadNode2 = BadNode2().GetCopy()
            self.BadNode3 = BadNode3().GetCopy()

        else:
            GetDevInfo.getdevinfo.DiskInfo = ReturnFakeDiskInfoMac()
            self.BadPlist0 = plistlib.readPlistFromString(ReturnFakeDiskutilInfoBadDisk0Plist())
            self.Plist0 = plistlib.readPlistFromString(ReturnFakeDiskutilInfoDisk0Plist())
            self.Plist0s1 = plistlib.readPlistFromString(ReturnFakeDiskutilInfoDisk0s1Plist())
            self.Plist0s2 = plistlib.readPlistFromString(ReturnFakeDiskutilInfoDisk0s2Plist())
            self.Plist0s3 = plistlib.readPlistFromString(ReturnFakeDiskutilInfoDisk0s3Plist())

    def tearDown(self):
        if Linux:
            del self.Node1
            del self.Node2
            del self.BadNode1
            del self.BadNode2
            del self.BadNode3

        else:
            del GetDevInfo.getdevinfo.DiskInfo
            del self.BadPlist0
            del self.Plist0
            del self.Plist0s1
            del self.Plist0s2
            del self.Plist0s3

    @unittest.skipUnless(Linux, "Linux-specific test")
    def testGetVendorLinux(self):
        self.assertEqual(DevInfoTools().GetVendor(Node=self.Node1), "FakeVendor")
        self.assertEqual(DevInfoTools().GetVendor(Node=self.Node2), "FakeVendor2")
        self.assertEqual(DevInfoTools().GetVendor(Node=self.BadNode1), "Unknown")

    @unittest.skipUnless(not Linux, "Mac-specific test")
    def testGetVendorMac(self):
        #baddisk0
        GetDevInfo.getdevinfo.Main.Plist = self.BadPlist0
        self.assertEqual(DevInfoTools().GetVendor(Disk="disk0"), "Unknown")

        #disk0
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0
        self.assertEqual(DevInfoTools().GetVendor(Disk="disk0"), "VBOX")

        #disk0s1
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s1
        self.assertEqual(DevInfoTools().GetVendor(Disk="disk0s1"), "ThereIsNone")

        #disk0s2
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s2
        self.assertEqual(DevInfoTools().GetVendor(Disk="disk0s2"), "ThereIsNone")

        #disk0s3
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s3
        self.assertEqual(DevInfoTools().GetVendor(Disk="disk0s3"), "ThereIsNone")

    @unittest.skipUnless(Linux, "Linux-specific test")
    def testGetProductLinux(self):
        self.assertEqual(DevInfoTools().GetProduct(Node=self.Node1), "FakeProduct")
        self.assertEqual(DevInfoTools().GetProduct(Node=self.Node2), "FakeProduct2")
        self.assertEqual(DevInfoTools().GetProduct(Node=self.BadNode1), "Unknown")

    @unittest.skipUnless(not Linux, "Mac-specific test")
    def testGetProductMac(self):
        #baddisk0
        GetDevInfo.getdevinfo.Main.Plist = self.BadPlist0
        self.assertEqual(DevInfoTools().GetProduct(Disk="disk0"), "Unknown")

        #disk0
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0
        self.assertEqual(DevInfoTools().GetProduct(Disk="disk0"), "HARDDISK")

        #disk0s1
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s1
        self.assertEqual(DevInfoTools().GetProduct(Disk="disk0s1"), "FakeDisk")

        #disk0s2
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s2
        self.assertEqual(DevInfoTools().GetProduct(Disk="disk0s2"), "FakeDisk")

        #disk0s3
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s3
        self.assertEqual(DevInfoTools().GetProduct(Disk="disk0s3"), "FakeDisk")

    @unittest.skipUnless(Linux, "Linux-specific test")
    def testGetCapacityLinux(self):
        #1st good node.
        RawCapacity, HumanSize = DevInfoTools().GetCapacity(Node=self.Node1)
        self.assertEqual(RawCapacity, "100000000000")
        self.assertEqual(HumanSize, "100 GB")

        #2nd good node.
        RawCapacity, HumanSize = DevInfoTools().GetCapacity(Node=self.Node2)
        self.assertEqual(RawCapacity, "10000000000000000000")
        self.assertEqual(HumanSize, "10 EB")

        #1st bad node.
        self.assertEqual(DevInfoTools().GetCapacity(Node=self.BadNode1), ("Unknown", "Unknown"))

        #2nd bad node.
        self.assertEqual(DevInfoTools().GetCapacity(Node=self.BadNode2), ("Unknown", "Unknown"))

    @unittest.skipUnless(Linux, "Linux-specific test")
    @unittest.expectedFailure
    def testBadGetCapacityLinux(self):
        #3rd bad node.
        self.assertEqual(DevInfoTools().GetCapacity(Node=self.BadNode3), ("Unknown", "Unknown"))

    @unittest.skipUnless(not Linux, "Mac-specific test")
    def testGetCapacityMac(self):
        #baddisk0
        GetDevInfo.getdevinfo.Main.Plist = self.BadPlist0
        self.assertEqual(DevInfoTools().GetCapacity(), "Unknown")

        #disk0
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0
        self.assertEqual(DevInfoTools().GetCapacity(), "42948853248")

        #disk0s1
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s1
        self.assertEqual(DevInfoTools().GetCapacity(), "209715200")

        #disk0s2
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s2
        self.assertEqual(DevInfoTools().GetCapacity(), "42089095168")

        #disk0s3
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s3
        self.assertEqual(DevInfoTools().GetCapacity(), "650002432")

    @unittest.skipUnless(not Linux, "Mac-specific test")
    def testGetDescriptionMac(self):
        #baddisk0
        GetDevInfo.getdevinfo.Main.Plist = self.BadPlist0
        self.assertEqual(DevInfoTools().GetDescription(), "Unknown")

        #disk0
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0
        self.assertEqual(DevInfoTools().GetDescription(), "42948853248")

        #disk0s1
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s1
        self.assertEqual(DevInfoTools().GetDescription(), "209715200")

        #disk0s2
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s2
        self.assertEqual(DevInfoTools().GetDescription(), "42089095168")

        #disk0s3
        GetDevInfo.getdevinfo.Main.Plist = self.Plist0s3
        self.assertEqual(DevInfoTools().GetDescription(), "650002432")
