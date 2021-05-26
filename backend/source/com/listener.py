import time
from threading import Thread
from queue import Queue

import serial.tools.list_ports
from serial import Serial

from constants import LOGGER
from utils.singleton import Singleton

from .readers import MessageReader


class COMPort(metaclass=Singleton):

    @staticmethod
    def auto_detect(port="CP210") -> str:
        return "COM2"
        com_list = COMPort.list_all()
        com_dict = next(
            (com_dict for com_dict in com_list if port in str(com_dict.values())), None)
        com_port = com_dict["name"] if com_dict else None
        return com_port

    @staticmethod
    def list_all() -> list:
        ports = serial.tools.list_ports.comports()
        port_list = [port.__dict__ for port in sorted(ports)]
        return port_list

    def __init__(self):
        self.__com_port = None
        self.__stop_cond = False
        self.__listener = None
        self.__worker = None
        self.__queue = None
        self.__conn = None

    def __create_connection(self):
        if self.com_port:
            self.__conn = Serial(self.com_port, 38400, timeout=0)

    @property
    def com_port(self) -> str:
        return self.__com_port

    @com_port.setter
    def com_port(self, val: str):
        self.__com_port = val

    def is_alive(self) -> bool:
        return bool(self.__listener and self.__listener.is_alive())

    def stop(self):
        self.__stop_cond = False
        self.__com_port = None

    def start(self):
        if not (self.__listener and self.__listener.is_alive()):
            self.__queue = Queue()
            self.__listener = Thread(
                target=self.__run_listener, name="com-listener-thread", daemon=True)
            self.__listener.start()
            self.__worker = Thread(
                target=self.__run_worker, name="com-worker-thread", daemon=True)
            self.__worker.start()

    def __run_listener(self):
        LOGGER.info("[LISTENER] Launched!")
        self.com_port = COMPort.auto_detect()
        self.__stop_cond = bool(self.com_port)
        self.__create_connection()
        while self.__stop_cond:
            data = self.__conn.readline()
            if len(data):
                data = data.decode("utf-8").strip()
                self.__queue.put(data)
                LOGGER.info(f"[LISTENER] Data: [{data}] recieved!")
            time.sleep(0.5)
        LOGGER.info("[LISTENER] Killed!")
        self.__queue.put("kill")

    def __run_worker(self):
        LOGGER.info("[WORKER] Launched!")
        while (data := self.__queue.get()) != "kill":
            try:
                MessageReader.load(data)
                LOGGER.info(f"[WORKER] [{data}] successfully processed!")
            except Exception as exp:
                LOGGER.error("[WORKER] Data processing operation failed!")
                LOGGER.error(f"[WORKER] {exp}")
        LOGGER.info("[WORKER] Killed\n")
