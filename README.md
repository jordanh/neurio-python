# Neurio Energy Sensor and Appliance Info API Python Library

This is the unofficial Python library for the [Neurio](http://neur.io)
sensor real-time energy and appliance automation library.

Use it to collect realtime energy production and consumption information for
your home. Create smart home integrations and automations.
Run machine learning experiments.

The library currently supports:

 - OAuth 2 authentication (including token request) – `/v1/oauth2`
 - Consumption and production samples (live and historical) – `/v1/samples`
 - Energy consumption statistics rollups – `/v1/samples/stats`

Appliance detection and reporting will be added as soon as that
functionality is supported by the official Neurio platform.


## Installation

The easiest way to install the module is via pip:

    $ sudo pip install neurio

Or, clone the source repository and install it by hand:

    $ git clone https://github.com/jordanh/neurio-python neurio-python
    $ cd neurio-python
    $ sudo python setup.py install


## Getting Started

Module documentation has been added to `neurio/__init.__.py` and is the
canonical source of documentation. There are also a set of simple examples
in `examples/`.

Using the module is simple:

### 1. Request API Access Key from Neurio, Inc.

At the time of writing, this is accomplished by send an e-mail to
[support@neur.io](mailto:support@neurio.io)

### 2. Create Private Key File

Create a file named `my_keys.py` (for example) and populate it with the
`key` and `secret` information you received from Neurio:

```python
key    = "0123456789abcdef012345"
secret = "0123456789abcdef012345"
```

### 3. Write Your Application

Here's an example application that authenticates using the secret
information from `my_keys.py` and fetches the last real-time energy
data received by the Neurio platform:

```python
import neurio
import my_keys

# Setup authentication:
tp = neurio.TokenProvider(key=example_keys.key, secret=example_keys.secret)
# Create client that can authenticate itself:
nc = neurio.Client(token_provider=tp)
# Fetch sample:
sample = nc.get_samples_live_last(sensor_id="0x0013A20040B65FAD")

print "Current power consumption: %d W" % (sample['consumptionPower'])
```

That's it!

## Contributing

Feel free to fork, submit pull requests, or send feedback. I'm excited
to see what the world will create with Neurio.

Issues can be submitted here: https://github.com/jordanh/neurio-python/issues

## Testing

A series of unit tests have been written for this library. To run them,
first create a file `tests/test_keys.py` containing your credentials and
then:

    $ python -m unittest discover -s tests -p '*_test.py' -v

## License

Copyright 2015, Jordan Husney <jordan.husney@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at: http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
