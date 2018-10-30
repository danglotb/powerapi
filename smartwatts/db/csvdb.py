"""
Module csv which allow to handle CSV db
"""

import csv

from smartwatts.db.base_db import BaseDB, MissConfigParamError
from smartwatts.model import HWPCReport
import smartwatts.utils as utils


class CsvDB(BaseDB):
    """
    CsvDB class
    !!! BAD PERFORMANCE (load in memory) !!!
    """

    def __init__(self, config):
        self.config = config

        """ Check if config contain the necessary fields """
        for needed in ['files']:
            if needed not in self.config:
                raise MissConfigParamError

        """
        Dict with:
            keys: (timestamp, sensor, target)
            values: HWPCReport
        """
        self.database = {}

        """ Get all .csv filename """
        for path_file in self.config['files']:
            with open(path_file) as csv_file:
                csv_reader = csv.reader(csv_file)
                filename = path_file.split('/')[-1]

                """ Check if the extension is good """
                fieldname = csv_reader.__next__()
                for row in csv_reader:
                    timestamp = utils.timestamp_to_datetime(int(row[0]))
                    key = (timestamp, row[1], row[2])

                    """ If Report doesn't exist, create it """
                    if key not in self.database:
                        hwpc_report = HWPCReport(timestamp)
                        self.database[key] = hwpc_report

                    """
                    Feed him with dict with fieldnames as
                    keys and row as values.
                    """
                    self.database[key].feed_from_csv(
                        {fieldname[i]: row[i]
                         for i in range(len(fieldname))},
                        filename)

    def get_last_hwpc_report(self):
        """ Get the last hwpc report in the base """
        # Find last timestamp in core
        last_timestamp = utils.timestamp_to_datetime(0)
        last_sensor = ""
        last_target = ""
        for timestamp, sensor, target in self.database:
            if last_timestamp < timestamp:
                last_timestamp = timestamp
                last_sensor = sensor
                last_target = target

        return self.database[(last_timestamp, last_sensor, last_target)]
