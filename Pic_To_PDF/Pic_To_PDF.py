from PIL import Image
import os
import shutil
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), './Head_Files'))
import Head_Files.Head_Pic_To_PDF as PDF

# PDF.Merge_Images_To_PDF("Input/Dir", "./output.pdf", order = 'n' or 'i')
# PDF.Batch_Folder_To_PDF("Input/Dir", "Output/Dir", order)
# PDF.Pack_Subfolders_To_ZIP(InDir_path, OutDir_path)
# PDF.Process_One_File(InDir_Path, name, order)

name = ""
version = 1
subname = ""
InDir_path = f"/mnt/a/Downloads/666/Manga/{name}"
OutDir_path = f"/mnt/a/Downloads/666/Manga/{name}"


if version == 1:
     PDF.Process_One_File(InDir_path, name, "i")
    
elif version == 2:
    PDF.Batch_Folder_To_PDF(f"{InDir_path}/图片版", f"{OutDir_path}/PDF版", "i")
    PDF.Pack_Subfolders_To_ZIP(f"{InDir_path}/图片版", f"{OutDir_path}/压缩包版")

elif version == 3:
    PDF.Merge_Images_To_PDF(f"{InDir_path}/图片版/{subname}", f"{OutDir_path}/PDF版/{subname}.pdf", "i")