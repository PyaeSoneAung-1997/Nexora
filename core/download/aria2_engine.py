import subprocess
import requests
from config.app_paths import ARIA2_PATH


class Aria2Engine:

    def __init__(self):

        self.process = None
        self.rpc_url = ("http://127.0.0.1:6800/jsonrpc")

    def start(self):

        if self.process is not None:
            return

        if not ARIA2_PATH.exists():
            raise FileNotFoundError(
                f"aria2c.exe not found: {ARIA2_PATH}"
            )

        self.process = subprocess.Popen(
            [
                str(ARIA2_PATH),

                "--enable-rpc=true",
                "--rpc-listen-all=false",
                "--rpc-listen-port=6800",
                "--rpc-allow-origin-all=true",

                "--file-allocation=none",

                "--quiet=true"
            ]
        )

        print("aria2 engine started")

    def rpc_call(self,method, params=None):
        if params is None:
            params = []


        payload = {
            "jsonrpc":"2.0",
            "id":"nexora",
            "method":method,
            "params": params
        }

        response = requests.post(
            self.rpc_url,
            json = payload,
            timeout=5
        )

        response.raise_for_status()

        result = response.json()

        if "error" in result:
            raise RuntimeError(
                result["error"]
            )

        return result["result"]

    def get_version(self):
        return self.rpc_call(
            "aria2.getVersion"
        )
    

    def stop(self):

        if self.process is None:
            return
        try:
            self.rpc_call(
                "aria2.shutdown"
            )
        except Exception:
            self.process.terminate()

        self.process = None

        print("aria2 engine stopped")

    def add_download(self, url, download_dir):

        params = [
            [url],
            {
                "dir": download_dir,
                "continue": "true",
                # "max-connection-per-server": "4",
                # "split": "4"
            }
        ]

        gid = self.rpc_call(
            "aria2.addUri",
            params
        )

        print("aria2 GID:", gid)

        return gid

    def get_status(self, gid):

        params = [
            gid
        ]

        return self.rpc_call(
            "aria2.tellStatus",
            params
        )

    def pause(self,gid):
        raise self.rpc_call(
            "aria2.pause",
            [gid]
        )

    def resume(self,gid):
            raise self.rpc_call(
                "aria2.unpause",
                [gid]
            )

    def stop(self,gid):
            raise self.rpc_call(
                "aria2.remove",
                [gid]
            )