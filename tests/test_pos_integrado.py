import unittest
from unittest.mock import Mock
from transbank import POSIntegrado
from transbank.error.transbank_exception import TransbankException
from tests.mocks.pos_integrado_mock import responses


class TestPosIntegrado(unittest.TestCase):

    ACK = b'\x06'
    mock_serial = None
    pos = None
    mock_exception = Exception("Mock Exception")

    def setUp(self) -> None:
        self.mock_serial = Mock()
        self.pos = POSIntegrado()
        self.pos._serial_provider = self.mock_serial
        self.pos._serial_port = True
        self.mock_serial.is_port_open.return_value = True
        self.mock_serial.flush.return_value = None
        self.mock_serial.write.return_value = None
        self.mock_serial.in_waiting.return_value = 1

    def test_poll(self):
        self.mock_serial.read_data.return_value = self.ACK
        result = self.pos.poll()
        self.assertEqual(True, result)

    def test_poll_exception(self):
        self.mock_serial.read_data.side_effect = self.mock_exception
        with self.assertRaises(TransbankException) as context:
            self.pos.poll()
        self.assertTrue('Unable to send Poll' in str(context.exception))
