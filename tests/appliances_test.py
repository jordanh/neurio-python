#!/usr/bin/env python
"""
Copyright [2015] [Jordan Husney <jordan.husney@gmail.com>]

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
import example_keys

import unittest
from datetime import datetime, timedelta

class AppliancesTest(unittest.TestCase):
    def setUp(self):
        self.tp = neurio.TokenProvider(key=example_keys.key,
                                       secret=example_keys.secret)
        self.nc = neurio.Client(token_provider=self.tp)

    def test_get_appliances(self):
        apps = self.nc.get_appliances(location_id="Ke_gkbOzSc2zbTW4riCxaA")
        self.assertIsInstance(apps, list)
        self.assertGreater(len(apps), 0, "no appliance information received")


if __name__ == '__main__':
    unittest.main()
