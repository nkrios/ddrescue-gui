#!/usr/bin/env python
# -*- coding: utf-8 -*-
# BackendTools test data for DDRescue-GUI Version 1.8
# This file is part of DDRescue-GUI.
# Copyright (C) 2013-2018 Hamish McIntyre-Bhatty
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

"""
This module holds the data used for the backend tools tests.
"""

#Do future imports to prepare to support python 3.
#Use unicode strings rather than ASCII strings, as they fix potential problems.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

#Functions to return test data.
def return_fake_commands():
    """Returns some fake commands to test the start_process function against to make sure it isn't losing output."""

    dictionary = {}
    dictionary["echo 'This is a test of the fire alarm system'"] = {}
    dictionary["echo 'This is a test of the fire alarm system'"]["Output"] = "This is a test of the fire alarm system\n"
    dictionary["echo 'This is a test of the fire alarm system'"]["Retval"] = 0
    dictionary["echo 'This returns 2'; exit 2"] = {}
    dictionary["echo 'This returns 2'; exit 2"]["Output"] = "This returns 2\n"
    dictionary["echo 'This returns 2'; exit 2"]["Retval"] = 2
    dictionary["TIMES=1; while [ $TIMES -lt 6 ]; do echo 'Slow task'; sleep 2; TIMES=$(( $TIMES + 1 )); done"] = {}
    dictionary["TIMES=1; while [ $TIMES -lt 6 ]; do echo 'Slow task'; sleep 2; TIMES=$(( $TIMES + 1 )); done"]["Output"] = "Slow task\n"*5
    dictionary["TIMES=1; while [ $TIMES -lt 6 ]; do echo 'Slow task'; sleep 2; TIMES=$(( $TIMES + 1 )); done"]["Retval"] = 0
    dictionary["TIMES=1; while [ $TIMES -lt 6000 ]; do echo 'Fast Task'; sleep 0.001; TIMES=$(( $TIMES + 1 )); done"] = {}
    dictionary["TIMES=1; while [ $TIMES -lt 6000 ]; do echo 'Fast Task'; sleep 0.001; TIMES=$(( $TIMES + 1 )); done"]["Output"] = "Fast Task\n"*5999
    dictionary["TIMES=1; while [ $TIMES -lt 6000 ]; do echo 'Fast Task'; sleep 0.001; TIMES=$(( $TIMES + 1 )); done"]["Retval"] = 0

    return dictionary

def return_fake_filenames():
    """Returns some fake filenames to test the create_unique_key function against."""

    dictionary = {}
    dictionary["/dev/ewgrhtjerwhd"] = {}
    dictionary["/dev/ewgrhtjerwhd"]["Result"] = "...ev/ewgrhtjerwhd"
    dictionary["/home/hamish/Desktop/img.img"] = {}
    dictionary["/home/hamish/Desktop/img.img"]["Result"] = ["...Desktop/img.img", "...Desktop/img.i~2"]
    dictionary["/dev/sda"] = {}
    dictionary["/dev/sda"]["Result"] = "/dev/sda"
    dictionary["/home/hamish/Desktop/img2.img"] = {}
    dictionary["/home/hamish/Desktop/img2.img"]["Result"] = ["...Desktop/img.img", "...esktop/img2.img", "...Desktop/img.i~2"]

    return dictionary
