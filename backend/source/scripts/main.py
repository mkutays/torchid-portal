from com.listener import COMPort
import time


def run():

    COMPort().listen()
    time.sleep(20)
    COMPort().stop()
    print("waiting for finish")
    time.sleep(2)
    print(COMPort().is_alive())
    time.sleep(4)
