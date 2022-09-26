from pathlib import Path

class User():
    """
    Class that stores user data for NRELPY.
    """
    def __init__(self,
                first_name=None,
                last_name=None,
                reason=None,
                email=None,
                institution=None,
                mailing_list=False,
                api_key=None,
                ) -> None:

        self.first_name = first_name
        self.last_name = last_name
        self.reason = reason
        self.email = email
        self.institution = institution
        self.mailing_list = mailing_list
        self.api_key = api_key


    def _replace_space(self, string_value):
        string_value = string_value.replace(" ", "+")
        return string_value

    @property
    def full_name(self):
        name = self.first_name + "+" +self.last_name
        name = name.replace(" ", "+")
        return name
    
    @property
    def personal_data(self):
        return