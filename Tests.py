#!/usr/bin/env python
# -*- coding: utf-8 -*- 
# Unit tests for DDRescue-GUI Version 1.6.2
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

#Import modules.
import unittest
import wx
import subprocess
import re
import logging
import plistlib
import os
import time
from bs4 import BeautifulSoup

#Custom made modules.
import GetDevInfo
import Tools

from GetDevInfo.getdevinfo import Main as DevInfoTools
from Tools.tools import Main as BackendTools

#Import test modules.
import Tests

from Tests import GetDevInfoTests

#Set up the logger (silence all except critical logging messages).
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s: %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.CRITICAL)
logger = logging

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

#Setup custom-made modules (make global variables accessible inside the packages).
GetDevInfo.getdevinfo.subprocess = subprocess
GetDevInfo.getdevinfo.re = re
GetDevInfo.getdevinfo.logger = logger
GetDevInfo.getdevinfo.Linux = Linux
GetDevInfo.getdevinfo.plistlib = plistlib
GetDevInfo.getdevinfo.BeautifulSoup = BeautifulSoup

Tools.tools.wx = wx
Tools.tools.os = os
Tools.tools.subprocess = subprocess
Tools.tools.logger = logger
Tools.tools.logging = logging
Tools.tools.time = time
Tools.tools.Linux = Linux
Tools.tools.RescourcePath = RescourcePath

#Setup test modules.
GetDevInfoTests.DevInfoTools = DevInfoTools
GetDevInfoTests.GetDevInfo = GetDevInfo

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromModule(GetDevInfoTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
