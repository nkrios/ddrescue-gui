#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# BackendTools tests for DDRescue-GUI Version 1.6.2
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

#Do future imports to prepare to support python 3. Use unicode strings rather than ASCII strings, as they fix potential problems.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

#Import modules
import unittest
import wx
import os
import subprocess
import time

#Import test data and functions.
from . import BackendToolsTestData as Data
from . import BackendToolsTestFunctions as Functions

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

#Set up test functions.
Functions.subprocess = subprocess
Functions.os = os
Functions.time = time
Functions.Linux = Linux

#Set up autocomplete vars.
PotentialDevicePath = ""
PotentialPartitionPath = ""

class TestStartProcess(unittest.TestCase):
    def setUp(self):
        self.Commands = Data.ReturnFakeCommands()

    def tearDown(self):
        del self.Commands

    @unittest.skipUnless(False, "Disabled to speed up development")
    def testStartProcess(self):
        for Command in self.Commands.keys():
            Retval, Output = BackendTools().StartProcess(Command=Command, ReturnOutput=True)
            self.assertEqual(Retval, self.Commands[Command]["Retval"])
            self.assertEqual(Output, self.Commands[Command]["Output"])

class TestCreateUniqueKey(unittest.TestCase):
    def setUp(self):
        self.KeysDict = {}
        self.Filenames = Data.ReturnFakeFilenames()

    def tearDown(self):
        del self.KeysDict
        del self.Filenames

    def testCreateUniqueKey(self):
        for File in self.Filenames:
            Key = BackendTools().CreateUniqueKey(self.KeysDict, File, 15)
            self.assertTrue(Key in self.Filenames[File]["Result"])
            self.KeysDict[Key] = ""

class TestSendNotification(unittest.TestCase):
    def setUp(self):
        self.app = wx.App()

    def tearDown(self):
        self.app.Destroy()
        del self.app

    def testSendNotification(self):
        #Tell the user we are about to send a notification.
        dlg = wx.MessageDialog(None, "DDRescue-GUI's BackendTools tests are about to send you a notification to test that notifications are working. You will then be prompted to confirm if they are working or not.", "DDRescue-GUI - Tests", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        
        #Send it.
        BackendTools().SendNotification("Test Message from unit tests.")

        #Ask the user if they got it.
        dlg = wx.MessageDialog(None, "Did you see the notification? Note that on some systems (Macs especially) they can take up to 10 seconds to come through.", "DDRescue-GUI - Tests", wx.YES_NO | wx.ICON_QUESTION)
        Result = dlg.ShowModal()
        dlg.Destroy()

        self.assertEqual(Result, wx.ID_YES)

class TestMacHdiutil(unittest.TestCase):
    def setUp(self):
        self.app = wx.App()

    def tearDown(self):
        self.app.Destroy()
        del self.app

    @unittest.skipUnless(not Linux, "Mac-specific test")
    def testMacRunHdiutil(self):
        #*** Add more tests for when "resource is temporarily unavailable" errors happen ***
        #Get a device path from the user to test against.
        dlg = wx.TextEntryDialog(None, "DDRescue-GUI needs a device name to test against.\nNo data on your device will be modified. Suggested: insert a USB disk and leave it mounted.\nNote: Do not use your device while these test are running, or it may interfere with the tests.", "DDRescue-GUI Tests", PotentialDevicePath, style=wx.OK)
        dlg.ShowModal()
        DevicePath = dlg.GetValue()
        dlg.Destroy()

        #Save it for autocomplete with other dialogs.
        global PotentialDevicePath
        PotentialDevicePath = DevicePath

        self.assertEqual(BackendTools().MacRunHdiutil("info", DevicePath)[0], 0)
        self.assertEqual(BackendTools().MacRunHdiutil("detach "+DevicePath, DevicePath)[0], 0)

class TestIsMounted(unittest.TestCase):
    def setUp(self):
        self.app = wx.App()

        #Get a device path from the user to test against.
        dlg = wx.TextEntryDialog(None, "DDRescue-GUI needs a partition name to test against.\nNo data on your device will be modified. Suggested: insert a USB disk and leave it mounted.\nNote: Do not use your device while these test are running, or it may interfere with the tests.", "DDRescue-GUI Tests", PotentialPartitionPath, style=wx.OK)
        dlg.ShowModal()
        self.Path = dlg.GetValue()
        dlg.Destroy()

        #Save it for autocomplete with other dialogs.
        global PotentialPartitionPath
        PotentialPartitionPath = self.Path

    def tearDown(self):
        #Check if anything is mounted at our temporary mount point.
        if Functions.GetMountPointOf(self.Path):
            Functions.UnmountDisk(self.Path)

        #Remove the mount point.
        if os.path.isdir("/tmp/ddrescueguimtpt"):
            os.rmdir("/tmp/ddrescueguimtpt")

        self.app.Destroy()
        del self.app
        del self.Path

    def testIsMounted1(self):
        #If not mounted, mount it
        if not Functions.IsMounted(self.Path):
            Functions.MountPartition(self.Path, "/tmp/ddrescueguimtpt")

        self.assertTrue(BackendTools().IsMounted(self.Path))

    def testIsMounted2(self):
        #Unmount it.
        Functions.UnmountDisk(self.Path)

        self.assertFalse(BackendTools().IsMounted(self.Path))

class TestGetMountPointOf(unittest.TestCase):
    def setUp(self):
        self.app = wx.App()

        #Get a device path from the user to test against.
        dlg = wx.TextEntryDialog(None, "DDRescue-GUI needs a partition name to test against.\nNo data on your device will be modified. Suggested: insert a USB disk and leave it mounted.\nNote: Do not use your device while these test are running, or it may interfere with the tests.", "DDRescue-GUI Tests", PotentialPartitionPath, style=wx.OK)
        dlg.ShowModal()
        self.Path = dlg.GetValue()
        self.MountPoint = Functions.GetMountPointOf(self.Path)
        dlg.Destroy()

        #Save it for autocomplete with other dialogs.
        global PotentialPartitionPath
        PotentialPartitionPath = self.Path

    def tearDown(self):
        self.app.Destroy()
        del self.app
        del self.Path

    def testGetMountPointOf1(self):
        #Mount disk if not mounted.
        if not Functions.IsMounted(self.Path):
            Functions.MountPartition(self.Path, "/tmp/ddrescueguimtpt")

        #Get mount point and verify.
        self.assertEqual(BackendTools().GetMountPointOf(self.Path), Functions.GetMountPointOf(self.Path))

    def testGetMountPointOf2(self):
        #Unmount disk.
        BackendTools().UnmountDisk(self.Path)

        #Get mount point.
        self.assertIsNone(BackendTools().GetMountPointOf(self.Path))

class TestMountPartition(unittest.TestCase):
    def setUp(self):
        self.app = wx.App()

        #Get a device path from the user to test against.
        dlg = wx.TextEntryDialog(None, "DDRescue-GUI needs a partition name to test against.\nNo data on your device will be modified. Suggested: insert a USB disk and leave it mounted.\nNote: Do not use your device while these test are running, or it may interfere with the tests.", "DDRescue-GUI Tests", PotentialPartitionPath, style=wx.OK)
        dlg.ShowModal()
        self.Path = dlg.GetValue()
        self.MountPoint = Functions.GetMountPointOf(self.Path)
        dlg.Destroy()

        #Save it for autocomplete with other dialogs.
        global PotentialPartitionPath
        PotentialPartitionPath = self.Path

    def tearDown(self):
        self.app.Destroy()
        del self.app
        del self.Path

    def TestMountPartition1(self):
        #Partition should be mounted, so we should pass this without doing anything.
        self.assertEqual(BackendTools().MountPartition(self.Path, self.MountPoint), 0)

    def TestMountPartition2(self):
        #Unmount disk.
        BackendTools().UnmountDisk(self.Path)

        self.assertEqual(BackendTools().MountPartition(self.Path, self.MountPoint), 0)

    def TestMountPartition3(self):
        #*** Test when other device is in the way TODO ***
        self.assertTrue(True)

    def TestMountPartition4(self):
        #*** Test when dir needs to be created TODO ***
        self.assertTrue(True)
