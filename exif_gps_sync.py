"""
Module for extracting GPS data from MicroLoon CSV files and embedding it into Canon image EXIF metadata.

Dependencies:
    - csv
    - glob
    - os
    - exif
    - datetime

Functions:
    - extract_ul_data(file_path): Extracts GPS data from MicroLoon CSV file.
    - read_exif_timestamp(folder_path): Reads EXIF timestamps from image files.
    - write_exif_gps(file_path, microloon_data, closest_timestamp_index): Writes GPS data to image EXIF metadata.
    - find_closest_timestamp(timestamp, timestamps): Finds the closest timestamp match for an image.
    - decimal_to_dms(decimal): Converts decimal GPS coordinates to degrees, minutes, and seconds.
    - main(): Main function to execute GPS data extraction and embedding process.
"""



import csv
import glob
import os
from exif import Image
from datetime import datetime, timedelta, time

local_to_zulu = 8  # Zulu time to local PDT


def extract_ul_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        data = [[row[0], float(row[1]), float(row[2]), float(row[3])] for row in reader]
    return data


def read_exif_timestamp(folder_path):
    data = []
    jpg_files = glob.glob(os.path.join(folder_path, '*.jpg'))
    for file_path in jpg_files:
        with open(file_path, 'rb') as image_file:
            image = Image(image_file)
            # hours, minutes, seconds = map(int, image.gps_timestamp)
            # time_obj = time(hours, minutes, seconds)
            # data.append((file_path, image.datetime))
            data.append((file_path, image.datetime_original))
    return data


def write_exif_gps(file_path, microloon_data, closest_timestamp_index):
    with open(file_path, 'rb') as image_file:
        image = Image(image_file)
        altitude, latitude, longitude = microloon_data[closest_timestamp_index][1:]

        # Convert decimal to dms
        latitude = decimal_to_dms(abs(latitude))
        longitude = decimal_to_dms(abs(longitude))

        image.gps_altitude = round(altitude, 3)
        image.gps_latitude = latitude
        image.gps_longitude = longitude
    with open(file_path, 'wb') as image_file:
        image_file.write(image.get_file())


def find_closest_timestamp(timestamp, timestamps):
    timestamp = datetime.strptime(timestamp, '%Y:%m:%d %H:%M:%S')
    time_diff = timedelta(hours=local_to_zulu)
    timestamp_zulu = timestamp + time_diff
    timestamps = [datetime.strptime(row, '%Y-%m-%dT%H:%M:%SZ') for row in timestamps]
    key = timestamps.index(min(timestamps, key=lambda x: abs(x - timestamp_zulu)))
    return key


def decimal_to_dms(decimal):
    degrees = int(decimal)
    decimal_minutes = (decimal - degrees) * 60
    minutes = int(decimal_minutes)
    seconds = (decimal_minutes - minutes) * 60
    return degrees, minutes, seconds


def main():
    # File paths
    microloon_file = 'microloon_log.csv'
    photo_path = r'C:\Users\Good Machine\Desktop\Good Machine\Photogrammetry\Photo\FLIR_mod'

    # Read GPS data from CSV files
    microloon_data = extract_ul_data(microloon_file)
    photo_data = read_exif_timestamp(photo_path)
    microloon_timestamp = [row[0] for row in microloon_data]

    # Find closest timestamp match
    for file_path, img_datetime in photo_data:
        closest_timestamp_index = find_closest_timestamp(img_datetime, microloon_timestamp)
        write_exif_gps(file_path, microloon_data, closest_timestamp_index)
        print(file_path)


if __name__ == "__main__":
    main()
