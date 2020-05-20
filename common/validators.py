'''
    This class allows for a smoother argument validation for endpoint
    versions within the request url.  Additional classes could be added
    here as needed.
    Author: Donovan Torgerson
    Email: Donovan@Torgersonlabs.com
'''

# built-in imports
import json

# external imports
from flask import abort
from werkzeug.routing import BaseConverter
from werkzeug.utils import validate_arguments
from uuid import UUID


class VersionConverter(BaseConverter):

    def __init__(self, map, *valid_versions):
        BaseConverter.__init__(self, map)
        self.valid_versions = valid_versions

    def to_python(self, value):
        try:
            assert value in self.valid_versions
            return value
        except AssertionError:
            # TODO: use error dict calling module.
            error = {'version': 'Invalid version.'}
            abort(400, json.dumps(error))

