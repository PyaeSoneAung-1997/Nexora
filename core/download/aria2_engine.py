import subprocess

from config.app_paths import ARIA2_PATH


class Aria2Engine:

    def __init__(self):

        self.process = None

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

                "--quiet=true"
            ]
        )

        print("aria2 engine started")

    def stop(self):

        if self.process is None:
            return

        self.process.terminate()
        self.process = None

        print("aria2 engine stopped")