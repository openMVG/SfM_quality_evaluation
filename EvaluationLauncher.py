#!/usr/bin/python
#! -*- encoding: utf-8 -*-

# Copyright (c) 2015 Pierre MOULON.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
#
# this script is to evaluate the Global SfM pipeline to a known camera trajectory
# Notes:
#  - OpenMVG 0.9 is required
#
# Usage:
#  $ python EvaluationLauncher.py OPENMVG_BIN_DIR ./Benchmarking_Camera_Calibration_2008 ./Benchmarking_Camera_Calibration_2008_out
#  i.e:
#  $ python EvaluationLauncher.py /home/user/openMVG_Build/Linux-x86_64-RELEASE ./Benchmarking_Camera_Calibration_2008 ./Benchmarking_Camera_Calibration_2008_out
#
# 

import commands
import os
import subprocess
import sys

def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)

if len(sys.argv) < 4:
  print ("/!\ Invalid input")
  print ("Usage %s OPENMVG_BIN_DIR ./GT_DATASET ./GT_DATASET_out" % sys.argv[0])
  sys.exit(1)

OPENMVG_SFM_BIN = sys.argv[1]
if not (os.path.exists(OPENMVG_SFM_BIN)):
  print("/!\ Please use a valid OPENMVG_SFM_BIN directory.")
  sys.exit(1)

input_eval_dir = sys.argv[2]
output_eval_dir = os.path.join(sys.argv[3], "evaluation_output")

# Run for each dataset of the input eval dir perform
#  . intrinsic setup
#  . compute features
#  . compute matches
#  . compute camera motion
#  . perform quality evaluation regarding ground truth camera trajectory

for directory in os.listdir(input_eval_dir):

  print directory
  matches_dir = os.path.join(output_eval_dir, directory, "matching")

  ensure_dir(matches_dir)

  print (". intrinsic setup")
  command = OPENMVG_SFM_BIN + "/openMVG_main_SfMInit_ImageListing"
  command = command + " -i " + input_eval_dir + "/" + directory + "/images/"
  command = command + " -o " + matches_dir
  command = command + " -k \"2759.48;0;1520.69;0;2764.16;1006.81;0;0;1\""
  command = command + " -c 1" # force pinhole camera
  command = command + " -g 1" # shared intrinsic
  proc = subprocess.Popen((str(command)), shell=True)
  proc.wait()

  print (". compute features")
  command = OPENMVG_SFM_BIN + "/openMVG_main_ComputeFeatures"
  command = command + " -i " + matches_dir + "/sfm_data.json"
  command = command + " -o " + matches_dir
  proc = subprocess.Popen((str(command)), shell=True)
  proc.wait()

  print (". compute matches")
  command = OPENMVG_SFM_BIN + "/openMVG_main_ComputeMatches"
  command = command + " -i " + matches_dir + "/sfm_data.json"
  command = command + " -o " + matches_dir + " -r .8 -g e -n ANNL2 -f 1"
  proc = subprocess.Popen((str(command)), shell=True)
  proc.wait()

  print (". compute camera motion")
  outGlobal_dir = os.path.join(output_eval_dir, directory, "SfM_Global")
  command = OPENMVG_SFM_BIN + "/openMVG_main_GlobalSfM"
  command = command + " -i " + matches_dir + "/sfm_data.json"
  command = command + " -m " + matches_dir
  command = command + " -o " + outGlobal_dir
  command = command + " -f NONE" # Do not refine intrinsics
  proc = subprocess.Popen((str(command)), shell=True)
  proc.wait()

  print (". perform quality evaluation")
  gt_camera_dir = os.path.join(input_eval_dir, directory, "gt_dense_cameras")
  outStatistics_dir = os.path.join(outGlobal_dir, "stats")
  command = OPENMVG_SFM_BIN + "/openMVG_main_evalQuality"
  command = command + " -i " + gt_camera_dir
  command = command + " -c " + outGlobal_dir + "/sfm_data.bin"
  command = command + " -o " + outStatistics_dir
  proc = subprocess.Popen((str(command)), shell=True)
  proc.wait()

sys.exit(1)

