#!/usr/bin/env python27
# encoding: utf-8

import argparse
import os
import sys
import _winreg
import re

VERSION = "1.0"


parser = argparse.ArgumentParser(description='The script takes two packages as arguments --old [OLD PACKAGE] --new [NEW PACKAGE] and compares the file structure and configuration.')
parser.add_argument('--suit', action='store', type=str, required=True, help='This can be bsp or bsa')
parser.add_argument('--old', action='store', type=str, required=True, help='')
parser.add_argument('--new', action='store', type=str, required=True, help='')
parser.add_argument('--out', action='store', type=str, required=True, help='')
args = parser.parse_args()
print(dir(args))
print(args)

def getUninstallString():
    # Registry set-up.
    regRoot = _winreg.HKEY_LOCAL_MACHINE
    regUninstallPath = r'Software\Microsoft\Windows\CurrentVersion\Uninstall'
    regRights = _winreg.KEY_ALL_ACCESS
    regOpen = _winreg.OpenKey
    regClose = _winreg.CloseKey
    uninstallKey = regOpen(regRoot, regUninstallPath, 0, regRights)
    # Find Uninstall Key
    try:
        for x in range(0, _winreg.QueryInfoKey(uninstallKey)[0]):
            regex = r"^{.{1,}}$"
            uninstallSubKeys = _winreg.EnumKey(uninstallKey, x)
            if re.match(regex, uninstallSubKeys):
                subKey = regOpen(regRoot, regUninstallPath + '\\' + uninstallSubKeys, 0, regRights)
                for y in range(0, _winreg.QueryInfoKey(subKey)[1]):
                        name, value, key_type = _winreg.EnumValue(subKey, y)
                        if value == "BroadSign Player":
                            uninstallString = "msiexec.exe /X {0} /qn".format(uninstallSubKeys)
                            break
                regClose(subKey)
        regClose(uninstallKey)
        return uninstallString
    except UnicodeEncodeError:
        pass

def uninstallApp():
    uninstall_String = getUninstallString()
    os.system(uninstall_String)

