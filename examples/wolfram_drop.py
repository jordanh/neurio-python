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
sys.path.append("..")

import neurio
import example_keys
sensor_id = "0x0013A20040B65FAD"

import requests
databin_id = "abcd_123"

tp = neurio.TokenProvider(key=example_keys.key, secret=example_keys.secret)
nc = neurio.Client(token_provider=tp)

# Get the last 90-seconds of activity:
samples = nc.get_samples_live(sensor_id=sensor_id, last=90)

# Put in 15-second resolution data into the Wolfram data drop:
for sample in samples[::15]:
    print sample
    payload = {}
    for k in ("timestamp", "consumptionPower", "consumptionEnergy"):
        payload[k] = sample[k]
    payload["bin"] = databin_id
    r = requests.get("https://datadrop.wolframcloud.com/api/v1.0/Add", params=payload)
    print r
