from PIL import Image
import os
import shutil

def Convert_Image_To_PDF(image_path, output_pdf_path):
    """
    将一张图片转换为 PDF 文件并保存到指定路径。
    
    参数：
        image_path (str): 图片文件路径（支持 JPG、PNG、WEBP 等）。
        output_pdf_path (str): 输出 PDF 路径。
    """
    try:
        with Image.open(image_path) as img:
            img = img.convert('RGB')
            img.save(output_pdf_path, 'PDF')
        print(f"✔ 成功转换：{image_path} -> {output_pdf_path}")
    except Exception as e:
        print(f"❌ 图片转换失败：{image_path}，错误信息：{e}")
        
def Merge_Images_To_PDF(folder_path, output_pdf_path):
    """
    将一个文件夹内的所有 JPG/JPEG 图片合并成一个 PDF。
    
    参数：
        folder_path (str): 包含图片的文件夹路径。
        output_pdf_path (str): 输出 PDF 文件的完整路径。
    """
    # 支持格式扩展
    supported_exts = ('.jpg', '.jpeg', '.png', '.webp')

    # 获取图片文件
    img_files = sorted([
        f for f in os.listdir(folder_path)
        if f.lower().endswith(supported_exts)
    ])

    if not img_files:
        print(f"⚠ 文件夹为空或无支持图片：{folder_path}")
        return

    img_list = []
    for fname in img_files:
        img_path = os.path.join(folder_path, fname)
        try:
            with Image.open(img_path) as img:
                img_list.append(img.convert('RGB'))
        except Exception as e:
            print(f"❌ 跳过图片：{fname}，错误：{e}")

    if img_list:
        try:
            img_list[0].save(output_pdf_path, save_all=True, append_images=img_list[1:])
            print(f"✔ PDF 已生成：{output_pdf_path}")
        except Exception as e:
            print(f"❌ PDF 生成失败：{output_pdf_path}，错误：{e}")
    else:
        print(f"❌ 所有图片处理失败，未生成 PDF。")
        

def Batch_Folder_To_PDF(parent_folder_path, output_folder_path):
    """
    遍历 parent_folder_path 下所有子文件夹，
    每个子文件夹内图片合并成一个 PDF，保存到 output_folder_path 中。

    参数：
        parent_folder_path (str): 包含多个子文件夹的上层目录。
        output_folder_path (str): PDF 输出目标路径。
    """
    # 确保输出文件夹存在
    os.makedirs(output_folder_path, exist_ok=True)

    # 遍历子文件夹
    for subfolder in sorted(os.listdir(parent_folder_path)):
        subfolder_path = os.path.join(parent_folder_path, subfolder)
        if not os.path.isdir(subfolder_path):
            continue  # 跳过非文件夹

        # 设置输出 PDF 路径
        output_pdf_path = os.path.join(output_folder_path, f"{subfolder}.pdf")
        
        # 调用图像合并函数
        print(f"📂 正在处理子文件夹：{subfolder}")
        Merge_Images_To_PDF(subfolder_path, output_pdf_path)


def Pack_Subfolders_To_ZIP(input_dir, output_dir):
    """
    将 input_dir 下的每一个子文件夹打包成 RAR 文件（仅打包，不压缩），存放到 output_dir。
    :param input_dir: 输入目录
    :param output_dir: 输出目录
    :param rar_executable: rar 可执行文件路径（默认 'rar'，Windows 可改为 'C:/Program Files/WinRAR/rar.exe'）
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    for item in os.listdir(input_dir):
        folder_path = os.path.join(input_dir, item)
        if os.path.isdir(folder_path):
            output_path = os.path.join(output_dir, item)  # 不要加扩展名
            shutil.make_archive(output_path, 'zip', folder_path)
            print(f"已打包: {output_path}.zip")

