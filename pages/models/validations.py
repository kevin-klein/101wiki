class ValidationMessage(object):
    pass

class ValidationInfo(ValidationMessage):

    def message(self):
        return ''

class ValidationError(ValidationMessage):

    def message(self):
        pass
