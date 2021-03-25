import smtplib


class Gmail:

    def __init__(self, username, password):
        username = self.__set_attribute(username)
        password = self.__set_attribute(password)
        self.server = self.login(username, password)

    def __set_attribute(self, attribute):
        if not isinstance(attribute, str):
            warning_phase = "ERROR: '{}' should be a string"
            self.__raise_error(TypeError, warning_phase, attribute)
        elif len(attribute) == 0:
            warning_phase = "ERROR: '{}' shouldn't have length equal zero"
            self.__raise_error(ValueError, warning_phase, attribute)
        else:
            return attribute

    def __raise_error(self, error_function, warning_phase, key_word):
        raise error_function(warning_phase.format(key_word))

    def login(self, username, password):
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(username, password)
        except:
            print('ERROR: Something went wrong during login process')

        return server
