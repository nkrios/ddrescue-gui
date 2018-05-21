#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Authentication Dialog for DDRescue-GUI Version 1.8
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
A simple authentication dialog that is used when elevated privileges are required.
Until version 1.8, this was used to start the GUI, but since that release, privileges
are only escalated when required to improve security.
"""

#This script is python 3 only - the mac version of this program only runs on python 3.
#Import other modules
import time
import subprocess
import os
import sys
import wx
import wx.adv

try:
    #Set the resource path from an environment variable,
    #as mac .apps can be found in various places.
    RESOURCEPATH = os.environ['RESOURCEPATH']

except KeyError:
    #Use '.' as the resource path instead as a fallback.
    RESOURCEPATH = "."

#Begin Authentication Window.
class AuthWindow(wx.Frame): #pylint: disable=too-many-instance-attributes
    """
    The main authentication window
    """
    def __init__(self):
        """Inititalize AuthWindow"""
        wx.Frame.__init__(self, None, title="DDRescue-GUI - Authenticate", size=(600, 400),
                          style=(wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP) ^ (wx.RESIZE_BORDER | wx.MINIMIZE_BOX))

        self.panel = wx.Panel(self)

        self.firstattempt = True

        #Set the frame's icon.
        prog_icon = wx.Icon(RESOURCEPATH+"/images/Logo.png", wx.BITMAP_TYPE_PNG)
        wx.Frame.SetIcon(self, prog_icon)

        self.create_text()
        self.create_buttons()
        self.create_other_widgets()
        self.setup_sizers()
        self.bind_events()

        #Call Layout() on self.panel() to ensure it displays properly.
        self.panel.Layout()

        #Give the password field focus, so the user can start typing immediately.
        self.password_field.SetFocus()
        
        self.on_auth_attempt()

        self.firstattempt = False

    def create_text(self):
        """Create all text for AuthenticationWindow"""
        self.title_text = wx.StaticText(self.panel, -1,
                                        "DDRescue-GUI requires authentication.")
        self.body_text = wx.StaticText(self.panel, -1, "DDRescue-GUI requires authentication "
                                       + "to\nperform privileged actions.")

        self.password_text = wx.StaticText(self.panel, -1, "Password:")

        bold_font = self.title_text.GetFont()
        bold_font.SetWeight(wx.BOLD)
        self.password_text.SetFont(bold_font)

    def create_buttons(self):
        """Create all buttons for AuthenticationWindow"""
        self.cancel_button = wx.Button(self.panel, -1, "Cancel")
        self.auth_button = wx.Button(self.panel, -1, "Authenticate")

    def create_other_widgets(self):
        """Create all other widgets for AuthenticationWindow"""
        #Create the image.
        img = wx.Image(RESOURCEPATH+"/images/Logo.png", wx.BITMAP_TYPE_PNG)
        self.program_logo = wx.StaticBitmap(self.panel, -1, wx.Bitmap(img))

        #Create the password field.
        self.password_field = wx.TextCtrl(self.panel, -1, "",
                                          style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)

        self.password_field.SetBackgroundColour((255, 255, 255))

        #Create the throbber.
        self.busy = wx.adv.Animation(RESOURCEPATH+"/images/Throbber.gif")
        self.green_pulse = wx.adv.Animation(RESOURCEPATH+"/images/GreenPulse.gif")
        self.red_pulse = wx.adv.Animation(RESOURCEPATH+"/images/RedPulse.gif")

        self.throbber = wx.adv.AnimationCtrl(self.panel, -1, self.green_pulse)
        self.throbber.SetInactiveBitmap(wx.Bitmap(RESOURCEPATH+"/images/ThrobberRest.png",
                                                  wx.BITMAP_TYPE_PNG))

        self.throbber.SetClientSize(wx.Size(30, 30))

    def setup_sizers(self):
        """Setup sizers for AuthWindow"""
        #Make the main boxsizer.
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        #Make the top sizer.
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)

        #Make the top text sizer.
        top_text_sizer = wx.BoxSizer(wx.VERTICAL)

        #Add items to the top text sizer.
        top_text_sizer.Add(self.title_text, 0, wx.ALIGN_LEFT|wx.EXPAND)
        top_text_sizer.Add(self.body_text, 0, wx.TOP|wx.ALIGN_LEFT|wx.EXPAND, 10)

        #Add items to the top sizer.
        top_sizer.Add(self.program_logo, 0, wx.LEFT|wx.ALIGN_CENTER, 18)
        top_sizer.Add(top_text_sizer, 1, wx.LEFT|wx.ALIGN_CENTER, 29)

        #Make the password sizer.
        password_sizer = wx.BoxSizer(wx.HORIZONTAL)

        #Add items to the password sizer.
        password_sizer.Add(self.password_text, 0, wx.LEFT|wx.ALIGN_CENTER, 12)
        password_sizer.Add(self.password_field, 1, wx.LEFT|wx.ALIGN_CENTER, 22)
        password_sizer.Add(self.throbber, 0, wx.LEFT|wx.ALIGN_CENTER|wx.FIXED_MINSIZE, 10)

        #Make the button sizer.
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        #Add items to the button sizer.
        button_sizer.Add(self.cancel_button, 0, wx.ALIGN_CENTER|wx.EXPAND)
        button_sizer.Add(self.auth_button, 1, wx.LEFT|wx.ALIGN_CENTER|wx.EXPAND, 10)

        #Add items to the main sizer.
        main_sizer.Add(top_sizer, 0, wx.ALL|wx.ALIGN_CENTER|wx.EXPAND, 10)
        main_sizer.Add(password_sizer, 0, wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER|wx.EXPAND, 10)
        main_sizer.Add(button_sizer, 1, wx.BOTTOM|wx.LEFT|wx.RIGHT|wx.ALIGN_CENTER|wx.EXPAND, 10)

        #Get the sizer set up for the frame.
        self.panel.SetSizer(main_sizer)

        #Call Layout() on self.panel() to ensure it displays properly.
        self.panel.Layout()

        main_sizer.SetSizeHints(self)

    def bind_events(self):
        """Bind all events for AuthenticationWindow"""
        self.Bind(wx.EVT_TEXT_ENTER, self.on_auth_attempt, self.password_field)
        self.Bind(wx.EVT_BUTTON, self.on_auth_attempt, self.auth_button)
        self.Bind(wx.EVT_BUTTON, self.on_exit, self.cancel_button)

    def on_auth_attempt(self, event=None): #pylint: disable=unused-argument
        """
        Check the password is correct,
        then either warn the user or call self.start_ddrescuegui().
        """

        #Disable the auth button (stops you from trying twice in quick succession).
        self.auth_button.Disable()

        #Check the password is right.
        password = self.password_field.GetLineText(0)
        cmd = subprocess.Popen("LC_ALL=C sudo -S echo 'Authentication Succeeded'",
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, shell=True)

        #Send the password to sudo through stdin,
        #to avoid showing the user's password in the system/activity monitor.
        cmd.stdin.write(password.encode()+b"\n")
        cmd.stdin.close()

        self.throbber.SetAnimation(self.busy)
        self.throbber.Play()

        while cmd.poll() is None:
            wx.Yield()
            time.sleep(0.04)

        output = cmd.stdout.read().decode("utf-8")

        if "Authentication Succeeded" in output:
            #Set the password field colour to green and disable the cancel button.
            self.password_field.SetBackgroundColour((192, 255, 192))
            self.cancel_button.Disable()

            #Play the green pulse for one second.
            self.throbber.SetAnimation(self.green_pulse)
            self.throbber.Play()
            wx.CallLater(1000, self.throbber.Stop)
            wx.CallLater(1100, self.start_ddrescuegui, password)

        else:
            #Re-enable auth button.
            self.auth_button.Enable()

            if self.firstattempt:
                return

            #Shake the window
            x_pos, y_pos = self.GetPosition()
            count = 0

            while count <= 6:
                if count % 2 == 0:
                    x_pos -= 10

                else:
                    x_pos += 10

                time.sleep(0.02)
                self.SetPosition((x_pos, y_pos))
                wx.Yield()
                count += 1

            #Set the password field colour to pink, and select its text.
            self.password_field.SetBackgroundColour((255, 192, 192))
            self.password_field.SetSelection(0, -1)
            self.password_field.SetFocus()

            #Play the red pulse for one second.
            self.throbber.SetAnimation(self.red_pulse)
            self.throbber.Play()
            wx.CallLater(1000, self.throbber.Stop)

    def start_ddrescuegui(self, password):
        """Start DDRescue-GUI and exit"""
        cmd = subprocess.Popen("sudo -SH sh -c '"+' '.join(sys.argv[1:])+" 2>&1'",
                               stdin=subprocess.PIPE, stdout=sys.stdout,
                               stderr=subprocess.PIPE, shell=True)

        #Send the password to sudo through stdin,
        #to avoid showing the user's password in the system/activity monitor.
        cmd.stdin.write(password.encode()+b"\n")
        cmd.stdin.close()

        #Overwrite the password with a string of nonsense characters before deleting it,
        #so the password cannot be read from memory when this script closes.
        password = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789!£$%^&*()_+"
        del password

        #Hide the window.
        self.Hide()
        wx.Yield()

        #Get return code.
        global returncode
        returncode = cmd.wait()

        self.on_exit()

    def on_exit(self, event=None): #pylint: disable=unused-argument
        """Close AuthWindow() and exit"""
        self.Destroy()

#End Authentication Window.

if __name__ == "__main__":
    APP = wx.App(False)
    AuthWindow().Show()
    APP.MainLoop()
    sys.exit(returncode)
