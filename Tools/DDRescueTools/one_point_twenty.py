#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DDRescue Tools for ddrescue v1.20 (or newer) in the Tools Package for DDRescue-GUI Version 1.8
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
Tools for ddrescue v1.20 or newer.
"""

#Do future imports to prepare to support python 3.
#Use unicode strings rather than ASCII strings, as they fix potential problems.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys

from . import decorators

#Make unicode an alias for str in Python 3.
if sys.version_info[0] == 3:
    unicode = str

@decorators.define_versions
def get_time_since_last_read(split_line):
    """Get Time Since Last Read. Works with ddrescue versions: 1.20,1.21,1.22"""
    return split_line[-1]
