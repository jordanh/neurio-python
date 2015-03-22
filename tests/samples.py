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

class SamplesTest(unittest.TestCase):
    def setUp(self):
        self.sensor_id = "0x0013A20040B65FAD"
        self.tp = neurio.TokenProvider(key=example_keys.key,
                                       secret=example_keys.secret)
        self.nc = neurio.Client(token_provider=self.tp)

    def test_get_samples_live(self):
        samples = self.nc.get_samples_live(sensor_id=self.sensor_id)
        self.assertIsInstance(samples, list)
        self.assertGreater(len(samples), 0, "no samples received")
        self.assertIn('consumptionPower', samples[0])
        self.assertIn('consumptionEnergy', samples[0])
        self.assertIn('generationPower', samples[0])
        self.assertIn('generationEnergy', samples[0])
        self.assertIn('timestamp', samples[0])

    def test_get_samples_live_with_last(self):
        one_min_ago = datetime.utcnow() - timedelta(minutes=1)
        one_min_ago = one_min_ago.replace(microsecond=0).isoformat()
        samples = self.nc.get_samples_live(sensor_id=self.sensor_id,
                                           last=one_min_ago)
        self.assertIsInstance(samples, list)
        self.assertGreater(len(samples), 0, "no samples received")
        self.assertAlmostEqual(len(samples), 60, delta=30,
          msg="should have received ~60 samples, instead received %d" % len(samples))


    def test_get_samples_live_last(self):
        sample = self.nc.get_samples_live_last(self.sensor_id)
        self.assertIsInstance(sample, dict)
        self.assertIn('consumptionPower', sample)
        self.assertIn('consumptionEnergy', sample)
        self.assertIn('generationPower', sample)
        self.assertIn('generationEnergy', sample)
        self.assertIn('timestamp', sample)

    def test_get_samples(self):
        fifteen_min_ago = datetime.utcnow() - timedelta(minutes=15)
        fifteen_min_ago = fifteen_min_ago.replace(microsecond=0).isoformat()
        samples = self.nc.get_samples(self.sensor_id, fifteen_min_ago,
                                      "minutes", frequency=5)
        self.assertIsInstance(samples, list)
        self.assertIn('consumptionPower', samples[0])
        self.assertIn('consumptionEnergy', samples[0])
        self.assertIn('generationPower', samples[0])
        self.assertIn('generationEnergy', samples[0])
        self.assertIn('timestamp', samples[0])

    def test_get_samples_error(self):
        fifteen_min_ago = datetime.utcnow() - timedelta(minutes=15)
        fifteen_min_ago = fifteen_min_ago.replace(microsecond=0).isoformat()
        samples = self.nc.get_samples(self.sensor_id, fifteen_min_ago,
                                      "seconds", frequency=5)
        # this should fail, historical sample resolution not available:
        self.assertIsInstance(samples, dict)
        self.assertIn('status', samples)
        self.assertIn('errors', samples)

    def test_get_samples_full(self):
        fifteen_min_ago = datetime.utcnow() - timedelta(minutes=15)
        fifteen_min_ago = fifteen_min_ago.replace(microsecond=0).isoformat()
        samples = self.nc.get_samples(self.sensor_id, fifteen_min_ago,
                                      "minutes", frequency=5, full=True)
        self.assertIsInstance(samples, list)
        self.assertIn('timestamp', samples[0])
        self.assertIn('channelSamples', samples[0])
        self.assertIsInstance(samples[0]['channelSamples'], list)

    def test_get_samples_stats(self):
        fifteen_min_ago = datetime.utcnow() - timedelta(minutes=15)
        fifteen_min_ago = fifteen_min_ago.replace(microsecond=0).isoformat()
        stats = self.nc.get_samples_stats(self.sensor_id, fifteen_min_ago,
                                      "minutes", frequency=5)
        self.assertIsInstance(stats, list)
        self.assertIn('start', stats[0])
        self.assertIn('end', stats[0])
        self.assertIn('consumptionEnergy', stats[0])


if __name__ == '__main__':
    unittest.main()
