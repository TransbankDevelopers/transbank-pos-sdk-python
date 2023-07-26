import serial.tools.list_ports
import serial


class SerialProvider:

    __port = None

    @staticmethod
    def get_ports_list() -> list:
        ports_list = serial.tools.list_ports.comports()
        return ports_list

    def open_port(self, port, baud_rate) -> bool:
        self.__port = serial.Serial(port=port, baudrate=baud_rate)
        return True

    def is_port_open(self) -> bool:
        is_open = self.__port.isOpen()
        return is_open

    def close_port(self) -> None:
        self.__port.close()

    def read_data(self, size: int = 1) -> bytes:
        data = self.__port.read(size)
        return data

    def in_waiting(self):
        in_waiting = self.__port.inWaiting()
        return in_waiting

    def flush_input(self) -> None:
        self.__port.flushInput()

    def flush(self) -> None:
        self.__port.flush()

    def write(self, data):
        self.__port.write(data)
