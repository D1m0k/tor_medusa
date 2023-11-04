import os
import time
from signal import SIGINT, SIGKILL

from . import log


class Service:
    def __init__(self, port):
        self.port = port

        for dir in ["lib", "run", "log"]:
            try:
                os.mkdir(f"/var/{dir}/{self.name}")
            except FileExistsError:
                pass
        log.info(f"Starting {self.name} (port {self.port}).")

    def __del__(self):
        log.info(f"Stopping {self.name} (port {self.port}).")
        self.stop()

    @property
    def name(self):
        return type(self).__name__.lower()

    @property
    def pid_file(self):
        return f"/var/run/{self.name}/{self.port}.pid"

    @property
    def pid(self):
        return int(open(self.pid_file, "rt").read().strip())

    @property
    def data_directory(self):
        return f"/var/lib/{self.name}"

    def kill(self, signal):
        try:
            os.kill(self.pid, signal)
            log.info(f"killing {self.pid} with signal {signal}")
        #except FileNotFoundError:
        except Exception as ex:
            log.info(f"{ex}")
            log.error("⛔ Unable to open PID file.")

    def run(self, *args):
        command = " ".join(args)
        log.info(f"Running: {command}.")
        os.system(command)

    def stop(self):
        try:
            self.kill(SIGINT)  # Kill politely.
            time.sleep(3)  # Give it a moment to die graciously.
            self.kill(SIGKILL)  # Kill insistently.
        except FileNotFoundError:
            pass

    def restart(self):
        self.stop()
        self.start()
