# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 09:04:03 2013

@author: danaukes
"""

import popupcad
import sys
from cx_Freeze import setup, Executable
import os
#import glob
import shutil

import importlib

# Remove the existing folders folder
shutil.rmtree("build", ignore_errors=True)
shutil.rmtree("dist", ignore_errors=True)

import idealab_tools.setup_tools as st

#from distutils.core import setup
#
packages = []
packages.append('photobooth')
packages.append('photobooth.simple_window')
packages.append('photobooth.make_pdf')
#packages.append('PyQt5')

import sys
from cx_Freeze import setup, Executable

include_files = []
#include_files.append(('C:/Python27/Lib/site-packages/pyside/QtGui4.dll','QtGui4.dll'))
#include_files.append(('C:/Python27/Lib/site-packages/OpenGL/DLLS/gle32.dll','gle32.dll'))
include_files.append(('photobooth/template.png','template.png'))
include_files.append(('photobooth/template2.png','template2.png'))
#toinclude.append(('C:/Python27/Lib/site-packages/OpenGL/DLLS/glut32.dll','glut32.dll'))
include_files.extend(st.include_entire_directory(st.fix(st.python_installed_directory,'Library/plugins/platforms'),''))
include_files.extend(st.include_entire_directory(st.fix(st.python_installed_directory,'Library/bin'),''))

include_modules = []
#include_modules.append("scipy.integrate.vode")
#include_modules.append("scipy.integrate.lsoda")
#include_modules.append("scipy.sparse.csgraph._validation")
#include_modules.append("OpenGL.platform.win32")
#include_modules.append("matplotlib.backends")
#include_modules.append("atexit")
include_modules.append('numpy.core._methods')
include_modules.append('numpy.lib.format')

import glob, os
explore_dirs = []
#explore_dirs.append('photobooth')
#    'C:/Users/danb0b/Documents/code projects/popupCAD/popupcad/supportfiles/',

shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "DTI Playlist",           # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]playlist.exe",# Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     )
    ]
msi_data = {}
    
#files = []
#for d in explore_dirs:
#    files.extend( glob.glob( os.path.join(d,'*') ) )
    
zipinclude = []
#for f in files:
##    print f
#    toinclude.append( (f, os.path.join('supportfiles',os.path.basename(f) ) ))

build_exe_options = {"include_msvcr":True,"include_files":include_files,"zip_includes": zipinclude,'packages':include_modules}
#build_exe_options = {"include_msvcr":True,"include_files":toinclude,"zip_includes": zipinclude,'packages':["scipy.integrate.vode","scipy.integrate.lsoda","scipy.sparse.csgraph._validation","OpenGL.platform.win32","matplotlib.backends"]}
bdist_msi_options = {
    'upgrade_code': '{66620F3A-DC3A-11E2-B341-002219E9B01E}',
    'add_to_path': False,
#    'initial_target_dir': r'[ProgramFilesFolder]\%s\%s' % (company_name, product_name),
#    'data': msi_data    
    }
    
base = None
if sys.platform == "win32":
    base = "Win32GUI"

    
module = importlib.import_module('tcl')
p = list(module.__path__)[0]
os.environ['TCL_LIBRARY'] = p
os.environ['TK_LIBRARY'] = p

setup(  name = "photobooth",
        version = "0.1",
        description = "photobooth",
        executables = [Executable("photobooth/gui.py", base=base)],
        options={'build_exe': build_exe_options,'bdist_msi': bdist_msi_options}
          )     
          
          