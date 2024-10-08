## Prequisites

* Python 3.8+
* Pytorch 1.5+  (eg, via anaconda)
* ffmpeg (optional, only needed for movie output, might need to also install libx264x if not already included)

## Structure

* poolstatmetamer - Core code for this project.  Includes classes and functions for computing the various image statistics, pooling such statistics, and optimizing images (via gradient descent) to match a desired set of pooled image statistics (typically those of a chosen target image).  
It also includes a variety of utility routines to compute steerable pyramids, manipulate images, and configure the statistics and solution process. 
You can run metamersolver.py to generate a quick unconverged metamer example as a test of the installed code.
* samplescripts - Some sample scripts demonstrating ways to use the psmcode to generate images.  
  * make_ps_metamer.py - Generates Portilla&Simoncelli-style texture synthesis "metamers".  The statistics used try to match those from Portilla&Simoncelli's paper as closely as we can and the entire image is a single pooling region.
  * make_uniform_metamer.py - Generates a metamers with uniform sized pooling regions (ie same shape and size everywhere in the image) which are intended to be viewed in your periphery.  By default it uses our modified statistics from the paper but can be configured to use other statistics and to create parametric sequences with varying parameters such as pooling size, statistics, etc.
  * make_gaze_metamer.py - Generate gaze-centric metamers where the pooling regions increase in size depending on distance from a specified gaze point.  Internally this is accomplished by warping the image to make the pooling regions uniform, generating a uniform metmamer, and then unwarping back to the original image space.
* sampleimages - A few images used by the sample scripts

* 


* image_quality_metrics_analysis.py  for evaluating generated images against original images.

* image_similarity_comparator.py for comparing image similarity