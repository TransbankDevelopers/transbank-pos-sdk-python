class TransbankException(Exception):
    def __int__(self, message="An error has occurred, verify given parameters."):
        self.message = message
        super().__init__(message)

    def __repr__(self):
        return "message: {}".format(self.message)
