#!/usr/bin/env python
"""
Copyright 2015, 2016 Jordan Husney <jordan.husney@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys
sys.path.append(".")
sys.path.append("..")

import neurio
import test_keys

import unittest
from datetime import datetime, timedelta

class AppliancesTest(unittest.TestCase):
    def setUp(self):
        self.tp = neurio.TokenProvider(key=test_keys.key,
                                       secret=test_keys.secret)
        self.nc = neurio.Client(token_provider=self.tp)

    def test_get_appliances(self):
        apps = self.nc.get_appliances(location_id=test_keys.location_id)
        self.assertIsInstance(apps, list)
        self.assertGreater(len(apps), 0, "no appliance information received")

    def test_get_appliance(self):
        apps = self.nc.get_appliances(location_id=test_keys.location_id)
        self.assertIsInstance(apps, list)
        self.assertGreater(len(apps), 0, "no appliance information received")
        try:
            stringtype = basestring
        except NameError:
            stringtype = str
        self.assertIsInstance(apps[0]["id"], stringtype)
        app = self.nc.get_appliance(apps[0]["id"])
        self.assertIsInstance(app, dict)
        self.assertEqual(apps[0]["id"], app["id"])

    def test_get_appliance_event_by_location(self):
        pass

    def test_get_appliance_event_after_time(self):
        pass

    def test_get_appliance_event_by_appliance(self):
        pass

    def test_get_appliance_stats_by_location(self):
        pass

    def test_get_appliance_stats_by_appliance(self):
        pass

if __name__ == '__main__':
    unittest.main()
