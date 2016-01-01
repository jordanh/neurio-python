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
import pprint
sys.path.append("..")
from datetime import datetime, timedelta

import neurio
import example_keys
sensor_id = "0x0013A20040B65FAD"


# Authenticate
tp = neurio.TokenProvider(key=example_keys.key, secret=example_keys.secret)
nc = neurio.Client(token_provider=tp)

# Calculate 15 minutes ago, format as ISO timestamp:
print "            now = %s" % (
    datetime.utcnow().replace(microsecond=0).isoformat())
fifteen_min_ago = datetime.utcnow() - timedelta(minutes=15)
fifteen_min_ago = fifteen_min_ago.replace(microsecond=0).isoformat()
print "fifteen min ago = %s" % (fifteen_min_ago)

print "Samples:"
samples = nc.get_samples(sensor_id=sensor_id, start=fifteen_min_ago,
            granularity="minutes", frequency=5)
print "samples ="
pprint.pprint(samples)

print "Stats Samples:"
samples = nc.get_samples_stats(sensor_id=sensor_id, start=fifteen_min_ago,
            granularity="minutes", frequency=5)
print "samples ="
pprint.pprint(samples)
