class RelayError(Exception):
    """Generic base class representing one particular type of Relay errors."""

    CODE = 'oops'
    MESSAGE = 'Something went wrong.'
    TYPE = 'fatal'

    def __init__(self, reason=None):
        message = self.MESSAGE
        if reason:
            message += f' {reason}.'

        super().__init__(message)

        self.message = message

    def json(self):
        return {
            'code': self.CODE,
            'message': self.message,
            'type': self.TYPE,
        }


class InvalidPayloadReceivedError(RelayError):
    CODE = 'invalid payload received'
    MESSAGE = 'Invalid JSON payload received.'


class AuthenticationRequiredError(RelayError):
    CODE = 'authentication required'
    MESSAGE = 'Authentication required.'


class SSLCertificateVerificationFailedError(RelayError):
    CODE = 'ssl certificate verification failed'
    MESSAGE = 'Unable to verify SSL certificate:'
