# import cv2
# import matplotlib.pyplot as plt
#
# # Read FLIR image
# flir_image = cv2.imread(r'C:\Users\Good Machine\Desktop\Good Machine\Photogrammetry\Photo\FLIR_mod\20240126_100610_R.jpg', cv2.IMREAD_UNCHANGED)
#
# # Convert to temperature data (assuming the image contains temperature information)
# # You might need to consult FLIR's documentation for the exact conversion process


import exiftool
import numpy as np

# Specify the path to the FLIR r.jpg file
file_path = 'path/to/your/r.jpg'

# Initialize ExifTool
with exiftool.ExifTool() as et:
    # Read metadata from the FLIR image file
    metadata = et.get_metadata(file_path)

# Extract the raw sensor data
raw_data = metadata['FLIR:RawThermalImage']

# Convert the raw sensor data to a NumPy array
raw_data_array = np.frombuffer(raw_data, dtype=np.uint16)

# Now you can work with raw_data_array as needed


