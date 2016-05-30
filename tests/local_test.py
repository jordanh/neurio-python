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
import json

class UserInfoTest(unittest.TestCase):
    def setUp(self):
        self.tp = neurio.TokenProvider(key=test_keys.key,
                                       secret=test_keys.secret)
        self.nc = neurio.Client(token_provider=self.tp)

    def test_local_current_sample(self):
        user_info = self.nc.get_user_information()
        ips = [
          sensor['ipAddress']
          for sublist in [
            location['sensors'] for location in user_info['locations']
          ]
          for sensor in sublist if sensor['sensorType'] == 'neurio'
        ]
        self.assertGreater(len(ips), 0)
        sample = self.nc.get_local_current_sample(ips[0])
        self.assertGreater(len(sample['timestamp']), 0)

    def test_local_current_sample_ip_arg(self):
      bad_ip1 = "hostname.domain"
      with self.assertRaises(ValueError):
        self.nc.get_local_current_sample(bad_ip1)
      bad_ip2 = "255.256.257.258"
      with self.assertRaises(ValueError):
        self.nc.get_local_current_sample(bad_ip2)


if __name__ == '__main__':
    unittest.main()
