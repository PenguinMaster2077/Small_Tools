from PIL import Image
import os
import shutil
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), './Head_Files'))
import Head_Files.Head_Pic_To_PDF as PDF

# PDF.Merge_Images_To_PDF("Input/Dir", "./output.pdf")
# PDF.Batch_Folder_To_PDF("Input/Dir", "Output/Dir")
# PDF.Pack_Subfolders_To_ZIP(InDir_path, OutDir_path)


InDir_path = ""
OutDir_path = ""

# PDF.Merge_Images_To_PDF(InDir_path, OutDir_path)

# PDF.Batch_Folder_To_PDF(InDir_path, OutDir_path)

# PDF.Pack_Subfolders_To_ZIP(InDir_path, OutDir_path)