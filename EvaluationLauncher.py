#!/usr/bin/python
#! -*- encoding: utf-8 -*-

# Copyright (c) 2014 Pierre MOULON.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
#
# this script is to evaluate the Global SfM pipeline to a known camera trajectory
# Notes:
#  - OpenMVG 0.8 is required
#
# Usage:
#  $ python EvaluationLauncher.py ./Benchmarking_Camera_Calibration_2008 ./Benchmarking_Camera_Calibration_2008_out
#
# 

# Indicate the openMVG binary directory (must be changed)
OPENMVG_SFM_BIN = "/home/user/Documents/Dev_openMVG/openMVG_Build/software/SfM"
# windows example: "C:\Users\Dev_openMVG\openMVG_Build\software\SfM\Release"
OPENMVG_GLOBAL_SFM_BIN = "/home/user/Documents/Dev_openMVG/openMVG_Build/software/globalSfM"
# windows example: "C:\Users\Dev_openMVG\openMVG_Build\software\globalSfM\Release"

import commands
import os
import subprocess
import sys

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

if not (os.path.exists(OPENMVG_SFM_BIN)):
  print("/!\ Please update the OPENMVG_SFM_BIN to the openMVG_Build/software/SfM/ path.")
  sys.exit(1)

if not (os.path.exists(OPENMVG_GLOBAL_SFM_BIN)):
  print("/!\ Please update the OPENMVG_GLOBAL_SFM_BIN to the openMVG_Build/software/globalSfM/ path.")
  sys.exit(1)

if len(sys.argv) < 3:
  print ("/!\ Invalid input")
  print ("Usage %s ./GT_DATASET ./GT_DATASET_out" % sys.argv[0])
  sys.exit(1)

input_eval_dir = sys.argv[1]
output_eval_dir = os.path.join(sys.argv[2], "evaluation_output")

# Run for each dataset of the input eval dir perform
#  . intrinsic setup
#  . compute matches
#  . compute camera motion
#  . perform quality evaluation

for directory in os.listdir(input_eval_dir):

  print directory
  matches_dir = os.path.join(output_eval_dir, directory, "matching")
  
  ensure_dir(matches_dir)

  print (". intrinsic setup")
  command = OPENMVG_SFM_BIN + "/openMVG_main_CreateList"
  command = command + " -i " + input_eval_dir + "/" + directory + "/images/"
  command = command + " -o " + matches_dir
  command = command + " -k \"2759.48;0;1520.69;0;2764.16;1006.81;0;0;1\""
  proc = subprocess.Popen((str(command)), shell=True)
  proc.wait()
      
  print (". compute matches")
  command = OPENMVG_SFM_BIN + "/openMVG_main_computeMatches"
  command = command + " -i " + input_eval_dir + "/" + directory + "/images/"
  command = command + " -o " + matches_dir + " -r .8 -g e"
  proc = subprocess.Popen((str(command)), shell=True)
  proc.wait()
  
  print (". compute camera motion")
  outGlobal_dir = os.path.join(output_eval_dir, directory, "SfM_Global")
  command = OPENMVG_GLOBAL_SFM_BIN + "/openMVG_main_GlobalSfM"
  command = command + " -i " + input_eval_dir + "/" + directory + "/images/"
  command = command + " -m " + matches_dir
  command = command + " -o " + outGlobal_dir
  command = command + " -r 2" # L2 rotation averaging 
  proc = subprocess.Popen((str(command)), shell=True)
  proc.wait()
  
  print (". perform quality evaluation")
  gt_camera_dir = os.path.join(input_eval_dir, directory, "gt_dense_cameras")
  outStatistics_dir = os.path.join(outGlobal_dir, "stats")
  command = OPENMVG_SFM_BIN + "/openMVG_main_evalQuality"
  command = command + " -i " + gt_camera_dir
  command = command + " -c " + os.path.join(outGlobal_dir, "SfM_output")
  command = command + " -o " + outStatistics_dir
  proc = subprocess.Popen((str(command)), shell=True)
  proc.wait()
    
sys.exit(1)

