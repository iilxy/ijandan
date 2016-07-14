#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Setup script for distributing SIFT as a stand-alone executable

from distutils.core import setup
import glob
import py2exe
import sys

import pkg_resources
# If run without args, build executables, in quiet mode.
if len(sys.argv) == 1:
    sys.argv.append("py2exe")
    #sys.argv.append("-q")
    
class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        # for the versioninfo resources
        self.version = "0.1"
        self.company_name = u"昕睿软件"
        self.copyright = u"昕睿软件"
        self.name = u"SexyGirl"
        
manifest = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1"
manifestVersion="1.0">
<assemblyIdentity
    version="0.64.1.0"
    processorArchitecture="x86"
    name="Controls"
    type="win32"
/>
<description>myProgram</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
"""

RT_MANIFEST = 24

MyApp = Target(
    # used for the versioninfo resource
    description = u"SexyGirl Downloader",

    # what to build
    script = "spynner_test.py",
    #other_resources = [(24,1,manifest)],
    icon_resources = [(1, "lsc.ico")],
    dest_base = "dist")

py2exe_options = {
        "includes": ["sqlite3","sip"], #PyQt程序打包时需要
        "dll_excludes": ["w9xpopen.exe",],
        "excludes" : ["Tkconstants","Tkinter","tcl","doctest","pdb","unittest"],
        "compressed": 1, #压缩文件
        "optimize": 2, #优化级别，默认为0
        #"ascii": 0, #ascii指不自动包含encodings和codecs
        "bundle_files": 3, #指将程序打包成单文件（此时除了exe文件外，还会生成一个zip文件。如果不需要zip文件，还需要设置zipfile = None）。1表示pyd和dll文件会被打包到单文件中，且不能从文件系统中加载python模块；值为2表示pyd和dll文件会被打包到单文件中，但是可以从文件系统中加载python模块
        }
        
data_files=[("",
                   ["lsc.ico","msvcr90.dll"])]

setup(
      name = u'dist',
      version = '1.0',
      #windows = [MyApp], 
	  console = [MyApp],
      #zipfile = None,
      options = {'py2exe': py2exe_options},
      data_files = data_files,
)