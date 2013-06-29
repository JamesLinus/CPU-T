#!/usr/bin/env python
#-*- coding: ascii -*-

from __future__ import print_function
import os, sys
from blib_util import *

def build_CPUT(compiler_info, compiler_arch, generator_name):
	curdir = os.path.abspath(os.curdir)

	if "vc" == compiler_info.name:
		build_dir = "build/%s-%d_0-%s" % (compiler_info.name, compiler_info.version, compiler_arch)
	else:
		build_dir = "build/%s-%s" % (compiler_info.name, compiler_arch)
	if not os.path.exists(build_dir):
		os.makedirs(build_dir)

	os.chdir(build_dir)

	toolset_name = ""
	if "vc" == compiler_info.name:
		toolset_name = "-T %s" % compiler_info.toolset
	
	additional_options = ""
	if (compiler_arch.find("_app") > 0):
		additional_options += "-D KLAYGE_WITH_WINRT:BOOL=\"TRUE\""

	cmake_cmd = batch_command()
	cmake_cmd.add_command('cmake -G "%s" %s %s %s' % (generator_name, toolset_name, additional_options, "../cmake"))
	cmake_cmd.execute()

	if ("x86_app" == compiler_arch):
		compiler_arch = "x86"
	elif ("arm_app" == compiler_arch):
		compiler_arch = "x86_arm"
	elif ("x64" == compiler_arch):
		compiler_arch = "x86_amd64"

	build_cmd = batch_command()
	if "vc" == compiler_info.name:
		build_cmd.add_command('CALL "%%VS%d0COMNTOOLS%%..\\..\\VC\\vcvarsall.bat" %s' % (compiler_info.version, compiler_arch))
		for config in compiler_info.cfg:
			compiler_info.msvc_add_build_command(build_cmd, "CPU-T", "ALL_BUILD", config)
	elif "mgw" == compiler_info.name:
		build_cmd.add_command('mingw32-make.exe')
	else:
		build_cmd.add_command('make')
	build_cmd.execute()

	os.chdir(curdir)

if __name__ == "__main__":
	if len(sys.argv) > 1:
		compiler = sys.argv[1]
	else:
		compiler = ""
	if len(sys.argv) > 2:
		arch = (sys.argv[2], )
	else:
		arch = ""
	if len(sys.argv) > 3:
		cfg = sys.argv[3]
	else:
		cfg = ""

	ci = compiler_info(compiler, arch, cfg)

	if 0 == len(ci.name):
		print("Wrong configuration\n")
		sys.exit(1)

	print("Building CPU-T...")
	for arch in ci.arch_list:
		build_CPUT(ci, arch[0], arch[1])