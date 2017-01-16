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

#Import modules
import unittest
import wx
import os

#Import test data.
import BackendToolsTestData as Data

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

class TestStartProcess(unittest.TestCase):
    def setUp(self):
        self.Commands = Data.ReturnFakeCommands()

    def tearDown(self):
        del self.Commands

    def testStartProcess(self):
        for Command in self.Commands.keys():
            Retval, Output = BackendTools().StartProcess(Command=Command, ReturnOutput=True)
            self.assertEqual(Retval, self.Commands[Command]["Retval"])
            self.assertEqual(Output, self.Commands[Command]["Output"])
