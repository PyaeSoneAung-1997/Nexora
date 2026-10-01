import os
import shutil

class StorageManager:
    def __init__(self):
        pass

    def get_free_space(self, path):

        usage = shutil.disk_usage(path)

        free_space = usage.free

        return free_space

    def has_enough_space(self, path, required_size):
        
        free_space = self.get_free_space(path)

        return free_space >= required_size
    
    def is_writable(self, path):
        return os.access(path, os.W_OK)

    def check_storage(self, path, required_size):
        # print("========== STORAGE CHECK ==========")
        # print("PATH:", path)
        # print("PATH TYPE:", type(path))
        # print("EXISTS:", os.path.exists(path))
        # print("IS DIRECTORY:", os.path.isdir(path))
        # print("WRITABLE:", self.is_writable(path))
        # print("REQUIRED SIZE:", required_size)
        
        if not self.is_writable(path):
            
            return {
                "success": False,
                "error": "The specified path is not writable."
            }

        if not self.has_enough_space(path, required_size):

            return {
                "success": False,
                "error": "Not enough free space in the specified path."
            }

        return {
            "success": True,
            "error": None
        }
        