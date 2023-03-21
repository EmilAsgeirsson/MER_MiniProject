from time import sleep
from threading import Thread, Lock
from time import time
from serial import Serial
import serial.tools.list_ports as port_list


class Encoder:
    def __init__(self, port: str = "COM9"):
        self.thread: dict = {
            "thread": None,
            "data": list(),
            "run_flag": True,
            "lock": Lock()
        }
        self.port = port

    def check_for_COM():
        ports = list(port_list.comports())
        for port in ports:
            print(f"{port}")
        return ports

    def read_serial(self) -> None:
        with Serial(port=self.port, baudrate=115200, timeout=1) as serial:
            # Clear the read buffer
            serial.flushInput()
            # Wait for system to start
            sleep(2)
            try:
                line: str = serial.readline().decode()[0:-1]
                assert (
                    line == "System ready"), f"Expected 'System ready', got '{line}'"
            except:
                print('Failed to initialize encoder')
                exit(1)

            # Run until kill signal
            while self.thread["run_flag"]:
                # Clear the read buffer
                serial.flushInput()

                # Read from the device
                line: str = serial.readline().decode()

                try:
                    # Split the values in substrings
                    values_str: str = line.split(",")

                    # Create a dict
                    values: dict = {
                        "Time": time(),
                        "A0": float(values_str[0]), # Analog 0
                        "A1": float(values_str[1]), # Analog 1
                        "A2": float(values_str[2])  # Analog 2
                    }

                    with self.thread["lock"]:
                        # Store the data
                        self.thread["data"].append(values)
                except:
                    pass
            print("Thread ended")

    def start_thread(self) -> None:
        # Start the thread
        self.thread["thread"] = Thread(target=self.read_serial)
        self.thread["thread"].start()
        print('Starting Thread')
        sleep(2.5)

    def get_data(self) -> list:
        data: list = list()
        # Get the data and clear the list
        with self.thread["lock"]:
            data = self.thread["data"].copy()
            self.thread["data"].clear()
        # Use the data
        return data

    def end_thread(self) -> None:
        # End the thread
        self.thread["run_flag"] = False
        self.thread["thread"].join()
