import subprocess
import time
import requests

from config.app_paths import ARIA2_PATH


class Aria2Engine:

    def __init__(self):

        self.aria2_path = ARIA2_PATH
        self.rpc_url = "http://localhost:6800/jsonrpc"

        self.process = None

        self.start_aria2()

    def start_aria2(self):

        self.process = subprocess.Popen(
            [
                self.aria2_path,
                "--enable-rpc=true",
                "--rpc-listen-port=6800",
                "--rpc-listen-all=false",
                "--max-connection-per-server=8",
                "--min-split-size=10M",
                "--file-allocation=none",
                "--log=D:/aria2.log",
                "--log-level=debug"
            ],
            # stdout=subprocess.DEVNULL,
            # stderr=subprocess.DEVNULL
              stdout=subprocess.PIPE,
              stderr=subprocess.PIPE,
              text=True
        )

        for _ in range(30):

            try:
                response = requests.post(
                    self.rpc_url,
                    json={
                        "jsonrpc": "2.0",
                        "id": "nexora",
                        "method": "aria2.getVersion"
                    },
                    timeout=1
                )

                if response.ok:
                    print("aria2 RPC connected")
                    return

            except requests.RequestException:
                pass

            time.sleep(0.5)

        raise RuntimeError(
            "aria2 RPC server failed to start."
        )

    def _request(self, method, params=None):

        payload = {
            "jsonrpc": "2.0",
            "id": "nexora",
            "method": method,
            "params": params or []
        }

        response = requests.post(
            self.rpc_url,
            json=payload
        )

        
        # print(response.status_code)
        # print(response.text)

              
        response.raise_for_status()

        data = response.json()

        # print("ARIA2 RESPONSE:", data)

        return data.get("result")
    
    def add_download(self, url, options=None):
        print("Adding download:", url)
        print("Options:", options)

        params = [[url]]

        if options:
                params.append(options)

        result = self._request(
            "aria2.addUri",
            params
        )

        print("GID:", result)

        return result

    def get_status(self,gid):

        return self._request(
        "aria2.tellStatus",
            gid
    )

    def pause(self,gid:str):

        return self._request(
            "aria2.pause",
            [gid]
        )

    def resume(self,gid:str):

        return self._request(
            "aria2.unpause",
            [gid]
        )

    def remove(self, gid:str):

        return self._request(
            "aria2.remove",
            [gid]
        ) 