
=========================================
SfM Camera trajectory quality evaluation
=========================================

Those datasets can be used to evaluate the SfM camera trajectory quality found by
openMVG.

-----------------------------
Usage
-----------------------------

1. Update the OPENMVG_SFM_BIN and OPENMVG_GLOBAL_SFM_BIN directory path in EvaluationLauncher.py
   - Use full path (linux user must use /home/user/...)
   
2. Launch the benchmark evaluation
$ python EvaluationLauncher.py ./GT_DATASET ./GT_DATASET_out

3. Look to results
  - open ExternalCalib_Report.html files in ./GT_DATASET_out

-----------------------------
"dense multi-view stereo"
-----------------------------

  - http://cvlabwww.epfl.ch/data/multiview/
  - C. Strecha, W. von Hansen, L. Van Gool, P. Fua, U. Thoennessen
    "On Benchmarking Camera Calibration and Multi-View Stereo for High Resolution Imagery"
     CVPR 2008.

  Modification:
   * Compress image from png to LosslessJPEG (318.9MB => 261.3MB)
   * rename .png.camera to .jpg.camera
   * Intrinsic camera to use (K matrix):
    2759.48;0;1520.69;
    0;2764.16;1006.81;
    0;0;1

