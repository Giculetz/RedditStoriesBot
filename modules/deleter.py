
import shutil

def delete_temps():
    folder_path='temps'
    shutil.rmtree(folder_path)
    print(f's-a sters tot din folderul {folder_path}')