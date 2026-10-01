from PyQt6.QtCore import QObject, pyqtSignal, QThread

from config.app_paths import DOWNLOAD_DIR
from core.storage.storage_manager import StorageManager
from core.database.repositories.base_repository import BaseRepository
from core.database.repositories.download_repository import DownloadRepository
from core.aria2_engine.aria2_engine import Aria2Engine
from core.downloads.download_worker import DownloadWorker

class DownloadManager(QObject):

    progress_changed = pyqtSignal(dict)
    download_completed = pyqtSignal(dict)
    download_error = pyqtSignal(dict) 


    def __init__(
            self,
            db_manager
            ):
        super().__init__()

        self.db_manager = db_manager
        self.storage_manager = StorageManager()
        self.default_download_path = DOWNLOAD_DIR
        self.download_repo = DownloadRepository(
            db_manager
        )
        self.aria2_engine = Aria2Engine()

        self.workers = {}

        
    def start_download(self, data):

        url = data.get("url")
        url_type = data.get("url_type","direct")

        file_name = data.get("file_name") or data.get("filename")
        title = data.get("title")

        save_path = data.get("save_path")
        file_size = data.get("size") or 0
        # print(file_name)
        # print(save_path)
        if not save_path:
            print("not save_path")
            save_path = self.default_download_path

        storage_result = self.storage_manager.check_storage(
                save_path, 
                file_size
            )
        # print(storage_result)
        if not storage_result["success"]:
            return {
                "success": False,
                "error": storage_result["error"]
            }
        # print(file_name)

        # Go repo -> Go Database
        download_id = self.download_repo.create(
            url = url,
            url_type = url_type,
            title = title,
            file_name = file_name,
            destination_path = save_path
        )
        # print(file_name)
        # Repair data aria2 engine
        options = {
            "dir": str(save_path),
            "out": file_name
        }

        gid = self.aria2_engine.add_download(
            url,
            options
        )

        print(gid)
        self.download_repo.update_aria2_gid(
            download_id,
            gid
        )

        # 4. Worker ဖန်တီးမယ်
        worker = DownloadWorker(
            self.aria2_engine,
            gid,
            download_id
        )

        # Creare Thread ဖန်တီးမယ်

        thread = QThread()

        # worker -> Thread
    
        worker.moveToThread(thread)
        print("Controller worker to thread")
        # Thread Start

        thread.started.connect(
            worker.start
        )
        print("Controller worker start")
        
        # 5. Worker signals ချိတ်မယ်
        worker.progress_changed.connect(
            self.handle_progress
        )

        worker.download_completed.connect(
            self.handle_completed
        )

        worker.download_error.connect(
            self.handle_error
        )

        worker.finished.connect(
            thread.quit
        )

        worker.finished.connect(
            worker.deleteLater
        )

        thread.finished.connect(
            thread.deleteLater
        )

        # 6. Worker ကို သိမ်းထားမယ်
        self.workers[gid] = {
        "worker": worker,
        "thread": thread
        }

        thread.finished.connect(
            lambda gid=gid: self.cleanup_worker(gid)
        )
        # 7. Monitoring စမယ်
        thread.start()

        return {
            "success": True,
            "download_id": download_id,
            "aria2_gid": gid,
            "error": None
        }

    def handle_progress(self, data):

        download_id = data.get("download_id")

        if download_id is not None:
            self.download_repo.update_progress(
                download_id=download_id,
                download_bytes=data["downloaded_bytes"],
                total_size=data["total_size"],
                progress=data["progress"],
                speed=data["speed"]
            )

        self.progress_changed.emit(data)

    def handle_completed(self, data):
        pass
        # download_id = data.get("download_id")
        # print("handle_completed")

        # if download_id is not None:

        #     self.download_repo.update_status(
        #         download_id,
        #         "completed"
        #     )

        # download = self.download_repo.get_by_id(
        #     download_id
        # )
        # print("Work ID")
        # print(download)
        # if download is None:
        #     return

        # data["file_name"] = download["file_name"]
        # data["destination_path"] = download["destination_path"]

        # self.download_completed.emit(data)

    def handle_error(self, data):
        # print(data.get("error"))
        pass

        # download_id = data.get("download_id")
        
        # if download_id is not None:
        
        #     self.download_repo.update_status(
        #                 download_id,
        #                 "error"
        #             )

        #     self.download_repo.update_error(
        #         download_id,
        #         data.get("error")
        #     )
        

        # self.download_error.emit(data) 

    def cleanup_worker(self, gid):

        worker_data = self.workers.pop(
            gid,
            None
        )

    def pause(self,current_gid):
        self.aria2_engine.pause(current_gid)
        # print("Manager Pause")

    def resume(self,current_gid):
        self.aria2_engine.resume(current_gid)
        # print("Manager Resume")
    
    def remove(self,current_gid):
        self.aria2_engine.remove(current_gid)
        print("Manager Remove")

          
        