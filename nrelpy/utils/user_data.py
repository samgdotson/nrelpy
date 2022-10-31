from distutils.log import warn
from pathlib import Path
import warnings

class User():
    """
    Class that stores user data for NRELPY.

    Attributes
    ----------
    first_name : str
    last_name : str
    reason : str
        Motivation for making an API query.
    email : str
    affiliation : str
    mailing_list : boolean or str
    api_key : str
    """
    def __init__(self,
                first_name=None,
                last_name=None,
                reason=None,
                email=None,
                affiliation=None,
                mailing_list=False,
                api_key=None,
                ) -> None:

        self.first_name = first_name
        self.last_name = last_name
        self.reason = reason
        self.email = email
        self.affiliation = affiliation
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
        data = {'api_key':self.api_key,
                'name':self._replace_space(self.full_name),
                'reason':self._replace_space(self.reason),
                'affiliation':self._replace_space(self.affiliation),
                'email':self.email,
                'mailing_list':str(self.mailing_list).lower()}
        if not all(list(data.values())):
            for k, v in data.items():
                if not v:
                    msg = f"Field: {k} is empty ({v})."
                    print(msg)
            warnings.warn(
                        "Some fields are missing. API queries may be rejected.",
                        UserWarning
                        )
        return data