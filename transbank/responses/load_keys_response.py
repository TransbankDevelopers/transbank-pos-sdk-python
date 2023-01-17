from transbank.responses.base_response import BaseResponse


class LoadKeysResponse(BaseResponse):

    def __init__(self, response):
        super().__init__(response)
        self.parsed_response['function_code'] = int(self.split_response[0])
        self.parsed_response['response_code'] = self.split_response[1]
        self.parsed_response['response_message'] = self.response_message
        self.parsed_response['success'] = self.success
        self.parsed_response['commerce_code'] = self.split_response[2]
        self.parsed_response['terminal_id'] = self.split_response[3]

