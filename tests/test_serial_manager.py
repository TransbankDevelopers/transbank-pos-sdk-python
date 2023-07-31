import unittest
from unittest.mock import Mock
from transbank.utils.serial_manager import Serial
from transbank.error.transbank_exception import TransbankException
from tests.mocks.serial_manager_mock import responses


class TestSerialManager(unittest.TestCase):
    mock_serial_provider = Mock()
    serial = Serial(mock_serial_provider)
    mock_exception = Exception("Mock Exception")

    def test_list_ports(self):
        self.mock_serial_provider.get_ports_list.return_value = responses['list_ports']['response']
        result = self.serial.list_ports()
        self.assertEqual(result, responses['list_ports']['expected_response'])

    def test_list_ports_exception(self):
        self.mock_serial_provider.get_ports_list.side_effect = self.mock_exception
        with self.assertRaises(TransbankException) as context:
            self.serial.list_ports()
        self.assertTrue('Unable to list ports' in str(context.exception))
