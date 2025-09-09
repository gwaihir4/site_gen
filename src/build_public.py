import os
import shutil

def build_public(source_dir, target_dir = "public", clean_dest = True): # initialize public/ before running function
    if len(source_dir) == 0 or not os.path.exists(source_dir):
        raise Exception ("Wrong source path input")
    if clean_dest and os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir, exist_ok=True)
    if os.path.exists(source_dir): # path exist
        element_list = os.listdir(source_dir)
        # target_element_list = os.listdir(target_dir)
        for element in element_list:
            src = os.path.join(source_dir, element)
            dst = os.path.join(target_dir, element)
            if os.path.isfile(src): # element is file in source dir
                try:
                    shutil.copy(src, dst)
                    print(f"Copying file: {src} -> {dst}")
                except:
                    raise Exception ("file copy failed")
            else: # if element is dir:
                try:
                    os.makedirs(dst, exist_ok=True)
                    print(f"Making directory at : {dst}")
                    build_public(src, dst, False)
                except:
                    raise Exception ("Error handling target and source directory")