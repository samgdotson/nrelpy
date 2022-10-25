import os
import sys
import argparse

PERSONAL_DATA = {'api_key':None,
                 'name':None,
                 'reason':None,
                 'affiliation':'University+of+Illinois+at+Urbana+Champaign',
                 'email':'sgd2@illinois.edu',
                 'mailing_list':'false'}


class User(object):
    """
    Stores personal user data.
    """
    def __init__(self,
                 api_key=None,
                 name=None,
                 reason=None,
                 affiliation=None,
                 email=None,
                 mailing_list=False) -> None:
        self.api_key = api_key
        self.name = name
        self.reason = reason
        self.affiliation = affiliation
        self.email = email
        self.mailing_list = mailing_list

    

    @property
    def personal_data(self):
        return {'api_key':self.api_key,
                'name':self.name,
                'reason':self.reason,
                'affiliation':self.affiliation,
                'email':self.email,
                'mailing_list':self.mailing_list}


def create_new_user(save_as='json'):
    """
    Creates new user data.
    """
    return

