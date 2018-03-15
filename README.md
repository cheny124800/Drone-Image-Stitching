Tata Innoverse - Solverhunter
Image Stitching software built Upon python using OpenCV

Requirements

1. Python >= 3.5
2. pip

Set Up 

1. Firstly download the project zip file and extract its contents.
2. Open Command Prompt (with administrative privileges) and navigate to the project folder.
3. Run the following in the Command Prompt (or Terminal on Linux) to install all the required dependencies 
pip install -r requirements.txt

Run the Project

1. Open the command Prompt (or Terminal on Linux) in the Project folder.
2. Place the test dataset images in datasets/images folder
3. Run the following in the Command Prompt (or Terminal)
 python ImageMosaic.py
4. Final Image is saved as finalResult.png inside results folder.

Minimum Specifications
1. 4GB RAM
2. At least 2GB Free Disk Space For storing temporary files

Our Test Bench
1. 4GB RAM with Core i5 3.6 ghz (Desktop) ~ 10 mins
2. 8GB RAM with Core i5 2.6 ghz (Laptop) ~ 20 mins


Note 
1. The software is not compatible with Python 2.
2. All the images must have EXIF data and XMP data with them. (Mostly drone captured images already have these as metadata.)
3. If the software fails to import OpenCV, then please run the project over a virtual environment. Please follow up this link to setup virtualenv.

