import time
import random
import logging
from threading import Thread
from queue import Queue

import serial.tools.list_ports

from utils.singleton import Singleton

logger = logging.getLogger(__name__)


class COMPort(metaclass=Singleton):

    @staticmethod
    def auto_detect() -> str:
        com_list = COMPort.list_all()
        com_dict = next(
            (com_dict for com_dict in com_list if "CP2102" in str(com_dict.values())), None)
        com_port = com_dict["name"] if com_dict else None
        return com_port

    @staticmethod
    def list_all() -> list:
        ports = serial.tools.list_ports.comports()
        port_list = [port.__dict__ for port in sorted(ports)]
        return port_list

    def __init__(self):
        self.__com_port = None
        self.__listener = None
        self.__worker = None
        self.__alive = False
        self.__queue = None

    @property
    def com_port(self) -> str:
        return self.__com_port

    @com_port.setter
    def com_port(self, val: str):
        self.__com_port = val

    def is_alive(self) -> bool:
        return bool(self.__listener and self.__listener.is_alive())

    def stop(self):
        self.__alive = False
        self.__com_port = None

    def listen(self):
        if not (self.__listener and self.__listener.is_alive()):
            self.__queue = Queue()
            self.__listener = Thread(
                target=self.__run_listener, name="com-listener-thread", daemon=True)
            self.__listener.start()
            self.__worker = Thread(
                target=self.__run_worker, name="com-worker-thread", daemon=True)
            self.__worker.start()

    def __run_listener(self):
        logger.info("[LISTENER]: Launched!")
        self.com_port = self.com_port if self.com_port else COMPort.auto_detect()
        self.__alive = bool(self.com_port)
        while self.__alive:
            data = random.randint(1, 10)
            time.sleep(data)
            self.__queue.put(f"data-{data}")
            logger.info(f"[LISTENER]: data-{data} recieved!")
        logger.info("[LISTENER]: Killed!")
        self.__queue.put("kill")

    def __run_worker(self):
        while (data := self.__queue.get()) != "kill":
            time.sleep(0.5)
            print(f"WORKER: {data} processed\n")

        print("WORKER: killed\n")
