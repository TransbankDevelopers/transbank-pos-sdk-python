responses = {
    'list_ports': {
        'response': [
            ("/dev/cu.Bluetooth-Incoming-Port", "n/a", "123456789"),
            ("/dev/cu.Bluetooth-Incoming-Port2", "mock_device", "123456789"),
            ("COM3", "mock_com_port", "abcd1234")
            ],
        'expected_response': [
            {'port': '/dev/cu.Bluetooth-Incoming-Port', 'description': 'n/a'},
            {'port': '/dev/cu.Bluetooth-Incoming-Port2', 'description': 'mock_device'},
            {'port': 'COM3', 'description': 'mock_com_port'}
            ]
        }
}