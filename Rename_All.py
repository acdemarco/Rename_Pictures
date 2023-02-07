import os, sys, time
from stat import *
from PIL import Image
from datetime import datetime
from PIL.ExifTags import TAGS
import exifread

file_num = 2  # this is the start number for the new names
"""
# THIS PROGRAM RUNS FROM CMD LINE <Starting path> <file extension> 
# if program in cur directory:  c:\python walktree_directory.py c:/temp jpeg
"""


# def get_date_taken(path):
#     return Image.open(path)._getexif()[36867]


def walktree(top, ext, callback):
    """
    recursively descend the directory tree rooted at top,
    calling the callback function for each regular file
    """

    global file_num
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
            callback(pathname, f, file_num, top, ext)
        else:
            # Unknown file type, print a message
            print('Skipping %s' % pathname)


def visitfile(file, f, fnum, folder, fileext):
    print('visiting', file, f, fnum, folder, fileext)
    has_info = 0
    img_open = 0
    try:
        print("Before image open")
        with Image.open(file) as img:
            # img = Image.open(file)
            d = img.getexif()
            print(d)
            img_open = 1
        for key, value in d.items():
            if key == 306:
                date_taken = value
                img_time = datetime.strptime(date_taken, '%Y:%m:%d %H:%M:%S')
                str_time = str(datetime.strftime(img_time, '%Y_%m_%d'))
                if str_time is not None:
                    has_info = 1
        print(str_time, type(str_time))
        print("before image close 1")
        # img.close()
 #   except UnboundLocalError as U_error:
 #       print(U_error)
 #       if img is not None:
 #           img.close()
    except:
        print("Image does not contain information.")
        # if img_open == 0:
            # img.close()

    tmp = time.strptime((time.ctime(os.path.getmtime(file))))  # the modification date
    if has_info == 1:
        os.rename(file, folder + "/" + fileext + "_" + str_time + "_" + str(fnum) + "." + fileext)
        print("new file: ", folder + "/" + fileext + "_" + str_time + "_" + str(fnum) + "." + fileext)
    else:
        os.rename(file, folder + "/" + fileext + "_" + str(tmp[0]) + str(tmp[1]) + "_" + str(fnum) + "." + fileext)
        print("new file: ", folder + "/" + fileext + "_" + str(tmp[0]) + str(tmp[1]) + "_" + str(fnum) + "." + fileext)


if __name__ == '__main__':
    walktree(sys.argv[1], sys.argv[2], visitfile)