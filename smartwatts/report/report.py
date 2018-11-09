"""
Module report
"""

from enum import Enum


class Report:
    """ Model base class """

    def __init__(self, hw_id):
        self.hw_id = hw_id
    
    class GroupBy(Enum):
        """ Enum for GroupBy """
        SENSOR = 1
        SOCKET = 2
        CPU = 3

    def get_child_reports(self):
        """ Return all the reports containing in this report"""
        raise NotImplementedError

    def set_child_report(self, key, val):
        """
        set the child report, corresponding to the given key to the given value
        """
        raise NotImplementedError

    def cut_child(self):
        """
        return a copy of the current report without its childs reports
        """
        raise NotImplementedError

    def serialize(self):
        """
        return the JSON format of the report
        """
        raise NotImplementedError

    def deserialize(self, json):
        """
        feed the report with the JSON input
        """
        raise NotImplementedError