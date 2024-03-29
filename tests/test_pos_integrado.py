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

    def test_load_keys(self):
        self.mock_serial.read_data.side_effect = responses['load_keys']['read_data_response']
        result = self.pos.load_keys()
        self.assertEqual(responses['load_keys']['expected_response'], result)

    def test_load_keys_exception(self):
        self.mock_serial.read_data.side_effect = self.mock_exception
        with self.assertRaises(TransbankException) as context:
            self.pos.load_keys()
        self.assertTrue('Unable to send load Keys' in str(context.exception))

    def test_set_normal_mode(self):
        self.mock_serial.read_data.return_value = self.ACK
        result = self.pos.set_normal_mode()
        self.assertEqual(True, result)

    def test_set_normal_mode_exception(self):
        self.mock_serial.read_data.side_effect = self.mock_exception
        with self.assertRaises(TransbankException) as context:
            self.pos.set_normal_mode()
        self.assertTrue('Unable to send Normal Mode' in str(context.exception))

    def test_normal_sale(self):
        self.mock_serial.read_data.side_effect = responses['sale']['read_data_response']
        result = self.pos.sale(13990, 'ABCD')
        self.assertEqual(responses['sale']['expected_response'], result)

    def test_normal_sale_amount_exception(self):
        with self.assertRaises(TransbankException) as context:
            self.pos.sale(10, 'ABCD')
        self.assertTrue('Amount must be greater' in str(context.exception))

    def test_normal_sale_ticket_exception(self):
        with self.assertRaises(TransbankException) as context:
            self.pos.sale(1990, 'ABCDEFG')
        self.assertTrue('Ticket must have a length' in str(context.exception))

    def test_normal_sale_callback_exception(self):
        with self.assertRaises(TransbankException) as context:
            self.pos.sale(1990, 'ABCD', send_status=True)
        self.assertTrue('A callback function is needed' in str(context.exception))

    def test_last_sale(self):
        self.mock_serial.read_data.side_effect = responses['last_sale']['read_data_response']
        result = self.pos.last_sale()
        self.assertEqual(responses['last_sale']['expected_response'], result)

    def test_last_sale_exception(self):
        self.mock_serial.read_data.side_effect = self.mock_exception
        with self.assertRaises(TransbankException) as context:
            self.pos.last_sale()
        self.assertTrue('Unable to recover last sale' in str(context.exception))

    def test_multicode_last_sale(self):
        self.mock_serial.read_data.side_effect = responses['multicode_last_sale']['read_data_response']
        result = self.pos.multicode_last_sale()
        self.assertEqual(responses['multicode_last_sale']['expected_response'], result)

    def test_multicode_last_sale_exception(self):
        self.mock_serial.read_data.side_effect = self.mock_exception
        with self.assertRaises(TransbankException) as context:
            self.pos.multicode_last_sale()
        self.assertTrue('Unable to recover multicode last sale' in str(context.exception))

    def test_refund(self):
        self.mock_serial.read_data.side_effect = responses['refund']['read_data_response']
        result = self.pos.refund(123)
        self.assertEqual(responses['refund']['expected_response'], result)

    def test_refund_exception(self):
        self.mock_serial.read_data.side_effect = self.mock_exception
        with self.assertRaises(TransbankException) as context:
            self.pos.refund(123)
        self.assertTrue('Unable to make refund' in str(context.exception))

    def test_totals(self):
        self.mock_serial.read_data.side_effect = responses['totals']['read_data_response']
        result = self.pos.totals()
        self.assertEqual(responses['totals']['expected_response'], result)

    def test_totals_exception(self):
        self.mock_serial.read_data.side_effect = self.mock_exception
        with self.assertRaises(TransbankException) as context:
            self.pos.totals()
        self.assertTrue('Unable to get totals' in str(context.exception))

    def test_details(self):
        self.mock_serial.read_data.side_effect = responses['details']['read_data_response']
        result = self.pos.details(True)
        self.assertEqual(responses['details']['expected_response'], result)

    def test_details_exception(self):
        self.mock_serial.read_data.side_effect = self.mock_exception
        with self.assertRaises(TransbankException) as context:
            self.pos.details(True)
        self.assertTrue('Unable to request sale detail' in str(context.exception))

    def test_close(self):
        self.mock_serial.read_data.side_effect = responses['close']['read_data_response']
        result = self.pos.close()
        self.assertEqual(responses['close']['expected_response'], result)

    def test_close_exception(self):
        self.mock_serial.write.side_effect = self.mock_exception
        with self.assertRaises(TransbankException) as context:
            self.pos.close()
        self.assertTrue('Unable to execute close' in str(context.exception))
