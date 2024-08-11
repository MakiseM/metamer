## Scripts Overview

This repository includes several scripts for generating and analyzing images, as well as comparing image similarity. Below is an overview of each script and its purpose:

- **Image Generation:**
  - `samplescripts/make_gaze_metamer.py`: This script is used for generating images (gaze metamers). Specific parameters for image generation can be adjusted in `poolstatmetamer/metamerstatistics.py`.

- **Image Comparison and Analysis:**
  - `samplescripts/image_quality_metrics_analysis.py`: This script performs analysis of image quality metrics to compare differences between images.
  - `samplescripts/image_similarity_comparator.py`: This script is designed to compare the similarity between different images.

- **Image Comparison Front-End:**
  - `samplescripts/metameric_image_comparator.py`: This script provides a front-end interface for image comparison. 
  - `samplescripts/metameric_image_selector.py`: This is another front-end script that allows users to select images for comparison.

### Database Integration

The image comparison scripts (`metameric_image_comparator.py` and `metameric_image_selector.py`) can be used in conjunction with a database. You can download the database file from the following link:

- [Database Connection](https://drive.google.com/file/d/1rU_QYxwCEX2B2bMB9zkrSNHTP0321RvZ/view?usp=sharing)

## Citation

This project is based on the work described in the following paper and codebase:

- **Paper:** Brown et al., "Efficient Dataflow Modeling of Peripheral Encoding in the Human Visual System." You can access the paper [here](https://dl.acm.org/doi/10.1145/3564605).
- **Codebase:** The implementation is inspired by the code from the repository [PooledStatisticsMetamers](https://github.com/ProgramofComputerGraphics/PooledStatisticsMetamers) 

If you use this project in your research, please consider citing the original paper and code.
