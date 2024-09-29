import os, sys, time
from stat import *
from PIL import Image
from datetime import datetime
from PIL.ExifTags import TAGS
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from pymediainfo import MediaInfo
#import exifread
import logging
from pillow_heif import register_heif_opener

register_heif_opener()



logging.basicConfig(filename='Rename_All.log', filemode='w', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level=logging.INFO)
file_num = 0  # this is the start number for the new names

def walktree(top, ext, fileNum, destfolder, callback):
    """
    recursively descend the directory tree rooted at top,
    calling the callback function for each regular file
    """

    global file_num
    file_num = fileNum
    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        file_num = file_num + 1

        if not f.lower().endswith("." + ext.lower()):  # limit files to certain type or condition
            continue

        mode = os.stat(pathname)[ST_MODE]
        if S_ISDIR(mode):
            # It's a directory, recurse into it
            walktree(pathname, ext, callback)
        elif S_ISREG(mode):
            # It's a file, call the callback function
            callback(pathname, f, file_num, top, ext, destfolder)
        else:
            # Unknown file type, print a message
            logging.info('Skipping %s' % pathname)



def get_date_taken(image_path):
    try:
        with Image.open(image_path) as img:
            #if img.has_exif:
            exif_data = img.getexif()
            if exif_data:
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    if tag_name == 'DateTime':
                        return value
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_video_creation_date2(video_path):
        media_info = MediaInfo.parse(video_path)
        # Loop through tracks and print modification date
        for track in media_info.tracks:
            if track.track_type == "General":

                MyDate = track.file_last_modification_date
                dt_obj = datetime.strptime(MyDate, "%Y-%m-%d %H:%M:%S.%f UTC")
                # Format the datetime object to the desired format without milliseconds or UTC
                formatted_timestamp = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
                MyDate_datetime: str = formatted_timestamp
                #date_string = MyDate.split(" ")[3].strip() + ' ' + MyDate.split(" ")[4].strip()
                #print(date_string)
                try:
                    #date_taken = datetime.strptime(MyDate, "%Y-%m-%d %H:%M:%S")
                    date_taken = MyDate_datetime
                    #print(date_taken)
                    return date_taken
                except ValueError:
                    print("Error: Unable to parse creation date.")
                    return None

        print("Creation date not found in metadata.")
        return None

def get_video_creation_date(video_path):
    with createParser(video_path) as parser:
    #parser = createParser(video_path)
        if not parser:
            print("Error: Unable to parse file.")
            return None

        metadata = extractMetadata(parser)
        if not metadata:
           print("Error: Unable to extract metadata.")
           return None

        for line in metadata.exportPlaintext():
            #if "Creation date" in line:
            if "Last modification" in line:
                date_string = line.split(" ")[3].strip() + ' ' + line.split(" ")[4].strip()
                try:
                    date_taken = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
                    return date_taken
                except ValueError:
                    print("Error: Unable to parse creation date.")
                    return None

    print("Creation date not found in metadata.")
    return None


def visitfile(file, f, fnum, folder, fileext, newfolder):
    logging.info('visiting ' + file + f + str(fnum) + folder + fileext)
    has_info = 0
    img_open = 0
    try:
        logging.info("Before image open")
        if fileext == 'mov' or fileext =='MOV' or fileext == 'mp4' or fileext == 'MP4':
            date_taken_result = get_video_creation_date2(file)
            logging.info(f"This is the date taken value:{date_taken_result}")
            #img_time = datetime.strptime(date_taken_result, '%Y-%m-%d %H:%M:%S')
            # Parse the string into a datetime object
            dt_obj = datetime.strptime(date_taken_result, '%Y-%m-%d %H:%M:%S')

            # Format the datetime object to the desired format '%Y_%m_%d'
            str_time = dt_obj.strftime('%Y_%m_%d')
            #str_time = str(datetime.strftime(date_taken_result, '%Y_%m_%d'))
        else:
            date_taken_result = get_date_taken(file)
            logging.info(f"This is the date taken value:{date_taken_result}")
            img_time = datetime.strptime(date_taken_result, '%Y:%m:%d %H:%M:%S')
            str_time = str(datetime.strftime(img_time, '%Y_%m_%d'))

        logging.info(f"This is the date taken value converted:{str_time}")
        if str_time is not None:
            has_info = 1
        #print(datevar)
                
        # with Image.open(file) as img:
        #     # img = Image.open(file)
        #     d = img.getexif()
        #     logging.info(d)
        #     img_open = 1
        # for key, value in d.items():
        #     if key == 306:
        #         date_taken = value
        #         img_time = datetime.strptime(date_taken, '%Y:%m:%d %H:%M:%S')
        #         str_time = str(datetime.strftime(img_time, '%Y_%m_%d'))
        #         if str_time is not None:
        #             has_info = 1
        # logging.info(str_time)
        # logging.info(type(str_time))
        #logging.info("before image close 1")
        # img.close()
 #   except UnboundLocalError as U_error:
 #       print(U_error)
 #       if img is not None:
 #           img.close()
    except:
        logging.info("Image does not contain information.")
        tmp = time.strptime((time.ctime(os.path.getmtime(file))))  # the modification date
        os.rename(file, newfolder + "/" + fileext + "_" + str(tmp[0]) + "_" + str(tmp[1]) + "_" + str(fnum) + "." + fileext)
        logging.info("new file: " + newfolder + "/" + fileext + "_" + str(tmp[0]) + "_" + str(tmp[1]) + "_" + str(fnum) + "." + fileext)
        # if img_open == 0:
            # img.close()


    if has_info == 1:
         os.rename(file, newfolder + "/" + fileext + "_" + str_time + "_" + str(fnum) + "." + fileext)
         logging.info("new file: " + newfolder + "/" + fileext + "_" + str_time + "_" + str(fnum) + "." + fileext)


if __name__ == '__main__':
    walktree(sys.argv[1], sys.argv[2], visitfile)