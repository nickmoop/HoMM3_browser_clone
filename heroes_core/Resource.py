"""
Basic class which implement resource loading and store in memory
"""

import glob
import json

from HoMM3_browser_clone.settings import BASE_DIR


RESOURCE_DIR = '{}/resources'.format(BASE_DIR)


class Resource(object):
    """
    Basic class for implement resources methods realisation
    """

    # name of parameter to sort resources for
    sorting_parameter_name = str()

    def __init__(self, attributes=None):
        """
        basic init

        :param attributes: class attributes as dict
            using when instance loading from file
        :type attributes: dict
        """

        # base attributes
        # update sorting parameter (when redefined in child class)
        self.sorting_parameter_name = self.sorting_parameter_name
        self.name = str()

        # resource defining by using prepared dict of attributes
        # probably resource loding from file
        if attributes:
            for key, value in attributes.items():
                self.__dict__[key] = value

    def load(self, file_path):
        """
        Loading one resource from one json file

        :param file_path: path to json file with resource description
        :type file_path: str
        """
        with open(file_path, 'r') as resource_file:
            data = json.load(resource_file)

        self.__init__(attributes=data)

    @classmethod
    def load_resources(cls):
        """
        Load all resources from .../resources/resource_name/... folder
        returns loaded resources dict with key as resource.key (property)

        :return: return all loaded resources
        :rtype: dict
        """
        resources = dict()
        resources_folder_path = '{}/{}/*/*'.format(
            RESOURCE_DIR, cls.__name__)

        for file_name in glob.glob(resources_folder_path):
            resource = cls()
            resource.load(file_name)
            resources[resource.key] = resource

        return resources

    @property
    def key(self):
        """
        Generate resource key for direct access
        to avoid loop if searching in all resources

        :return: resource key
        """
        return '{}_{}'.format(
            getattr(self, self.sorting_parameter_name), self.name)
