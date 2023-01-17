import serial.tools.list_ports
import serial
import time

from transbank.error.transbank_exception import TransbankException


class Serial:

    DEFAULT_TIMEOUT = 150000
    DEFAULT_BAUDRATE = 115200
    serial_port = None
    ACK = b'\x06'
    STX = '\x02'
    ETX = '\x03'
    timeout = DEFAULT_TIMEOUT

    def list_ports(self):
        serial_ports = serial.tools.list_ports.comports()
        ports = []
        for port, description, hwid in serial_ports:
            ports.append({"port": port, "description": description})
        return ports

    def open_port(self, port, baudrate=DEFAULT_BAUDRATE):
        self.serial_port = serial.Serial(port=port, baudrate=baudrate)
        return self.serial_port.isOpen()

    def close_port(self):
        self.serial_port.close()
        return self.serial_port.isOpen()

    def can_write(self):
        if self.serial_port is None or not self.serial_port.isOpen():
            raise TransbankException("Can't write to port, the port is null or not open")

    def create_command(self, payload: str):
        calculated_lrc = self.lrc(payload+self.ETX)
        full_command = [ord(self.STX)]
        for character in payload:
            full_command.append(ord(character))
        full_command.append(ord(self.ETX))
        full_command.append(ord(calculated_lrc))
        return full_command

    def lrc(self, command: str):
        lrc = 0
        for character in command:
            lrc = lrc ^ ord(character)
        print("Calculated LRC: {}".format(lrc))
        return chr(lrc)

    def check_ack(self):
        self.wait_response()
        response = []
        if self.serial_port.inWaiting() > 0:
            response.append(self.serial_port.read())
            print("bytes in waiting: {}".format(self.serial_port.inWaiting()))
        print("ACK Received")
        return response[0] == self.ACK

    def wait_response(self):
        timer = 0
        while timer < self.timeout:
            if self.serial_port.inWaiting() > 0:
                print("Response received")
                break
            time.sleep(0.2)
            timer += 1
            print("Waiting for response")
        if timer == self.timeout:
            self.serial_port.flushInput()
            raise TransbankException("Read operation Timeout")

    def send_command(self, command, intermediate_messages=False, sales_detail=False, print_on_pos=False, multicode=False):
        self.can_write()
        full_command = self.create_command(command)
        self.serial_port.flush()
        self.serial_port.write(full_command)
        if not self.check_ack():
            raise TransbankException("NACK received, check the message sent to the POS")

        if sales_detail and print_on_pos:
            details_response = []
            response = self.read_response()
            details_response.append(response)
            while self.has_authorization_code(response):
                response = self.read_response()
                details_response.append(response)
            return details_response

        return self.read_response()

    def read_response(self):
        self.wait_response()
        bytes_in_waiting = self.serial_port.inWaiting()
        print("Reading input buffer. Bytes in waiting: {}".format(bytes_in_waiting))
        response = self.serial_port.read(bytes_in_waiting)
        print("Response readed, lenght: {}".format(str(len(response))))
        self.send_ack()
        while response.decode()[-2] != self.ETX:
            self.wait_response()
            bytes_in_waiting = self.serial_port.inWaiting()
            response += self.serial_port.read(bytes_in_waiting)
        return response

    def send_ack(self):
        ack = [ord(self.ACK)]
        print("sending ACK")
        self.serial_port.write(ack)

    def has_authorization_code(self, response: bytes):
        parsed_response = response.decode().replace(self.STX, '').split("|")
        return parsed_response[5] != ""


