"""
This is a setup.py script written for DDRescue-GUI v2.0.0
by Hamish McIntyre-Bhatty.

Usage:
    python3 setup.py py2app
"""

from setuptools import setup

APP = ['./DDRescue_GUI.py']

DATA_FILES = ['./LICENSE', './Tests.py', './ddrescue', './Tools', './images', './other']

OPTIONS = {'arch': 'x86_64',
           'argv_emulation': True,
           'no_strip': True,
           'iconfile': './images/Logo.icns',
           'includes': 'wx,wx.animate,wx.lib.stattext,wx.lib.statbmp,threading,getopt,logging,'
                       + 'time,subprocess,re,os,sys,plistlib,BeautifulSoup,traceback,'
                       + 'unittest,getdevinfo',
           'packages': 'Tools,Tests'}

if __name__ == "__main__":
    setup(
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
    )
