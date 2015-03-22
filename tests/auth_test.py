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

class AuthTest(unittest.TestCase):
    sensor_id = "0x0013A20040B65FAD"

    def test_token_provider_init(self):
        tp = neurio.TokenProvider(key=example_keys.key,
                                  secret=example_keys.secret)
        self.assertIsNotNone(tp)

    def test_token_provider_get_token(self):
        tp = neurio.TokenProvider(key=example_keys.key,
                                  secret=example_keys.secret)
        self.assertIsNotNone(tp.get_token(), "unable to fetch token")


if __name__ == '__main__':
    unittest.main()
