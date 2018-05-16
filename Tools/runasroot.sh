#!/bin/bash
# -*- coding: utf-8 -*-
# Executes privileged processes when requested for DDRescue-GUI Version 1.8.
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

#Only do anything if DDRescue-GUI is running.

echo $(ps f) > temp

case "$(ps aux | grep -i DDRescue-GUI)" in

    *ython*DDRescue-GUI.py*)

        #Detect whether we are running on macos or linux.
        case "$(uname -s)" in

        Linux)
            #Keep trying to authorise if it fails / is dismissed.
            retval=126

            #126 - Dismissed.
            #127 - Authentication failure.
            while [[ $retval -eq 126 || $retval -eq 127 ]]
            do
                #Send stderr to /dev/null, because otherwise if authentication fails the
                #first time it may mess up output parsing.
                pkexec /usr/share/ddrescue-gui/Tools/runasroot_linux.sh $@ 2> /dev/null
                retval=$?
            done

            exit $retval
            ;;

        Darwin)
            #For development/debugging.
            #Start the authentication dialog I wrote.
            if [[ -z $RESOURCEPATH ]]; then
                RESOURCEPATH=.
            fi

            python3 $RESOURCEPATH/Tools/runasroot_mac.py $@
            exit $?
            ;;

        esac

        ;;

    *DDRescue-GUI.app*)
        #For macos in production. FIXME
        #Start the authentication dialog I wrote.
        if [[ -z $RESOURCEPATH ]]; then
            RESOURCEPATH=.
        fi

        python3 $RESOURCEPATH/Tools/runasroot_mac.py $@
        exit $?
        ;;

esac

exit 1
