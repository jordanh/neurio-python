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

import base64
import urllib
import urlparse
import requests

__version__ = "0.2.7"

class TokenProvider(object):
  __key = None
  __secret = None
  __token = None

  def __init__(self, key, secret):
    """Handles token authentication for Neurio Client.

    Args:
      key (string): your Neurio API key
      secret (string): your Neurio API secret
    """
    self.__key = key
    self.__secret = secret

    if self.__key is None or self.__secret is None:
            raise ValueError("Key and secret must be set.")

  def get_token(self):
    """Performs Neurio API token authentication using provided key and secret.

    Note:
      This method is generally not called by hand; rather it is usually
      called as-needed by a Neurio Client object.

    Returns:
      string: the access token
    """
    if self.__token is not None:
      return self.__token

    url = "https://api.neur.io/v1/oauth2/token"
    credentials = base64.b64encode(":".join([self.__key,self.__secret]))
    headers = {
      "Authorization": " ".join(["Basic", credentials]),
    }
    payload = {
      "grant_type": "client_credentials"
    }

    r = requests.post(url, data=payload, headers=headers)

    self.__token = r.json()["access_token"]

    return self.__token


class Client(object):
  __token = None

  def __init__(self, token_provider):
    """The Neurio API client.

    Args:
      token_provider (TokenProvider): object providing authentication services
    """
    self.__token = token_provider.get_token()

  def __gen_headers(self):
    """Utility method adding authentication token to requests."""
    headers = {
      "Authorization": " ".join(["Bearer", self.__token])
    }

    return headers

  def __append_url_params(self, url, params):
    """Utility method formatting url request parameters."""
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urllib.urlencode(query)

    return urlparse.urlunparse(url_parts)

  def get_samples_live(self, sensor_id, last=None):
    """Get recent samples, one sample per second for up to the last 2 minutes.

    Args:
      sensor_id (string): hexadecimal id of the sensor to query, e.g.
        ``0x0013A20040B65FAD``
      last (string): starting range, as ISO8601 timestamp

    Returns:
      list: dictionary objects containing sample data
    """
    url = "https://api.neur.io/v1/samples/live"

    headers = self.__gen_headers()
    headers["Content-Type"] = "application/json"

    params = { "sensorId": sensor_id }
    if last:
      params["last"] = last
    url = self.__append_url_params(url, params)

    r = requests.get(url, headers=headers)
    return r.json()


  def get_samples_live_last(self, sensor_id):
    """Get the last sample recorded by the sensor.

    Args:
      sensor_id (string): hexadecimal id of the sensor to query, e.g.
        ``0x0013A20040B65FAD``

    Returns:
      list: dictionary objects containing sample data
    """
    url = "https://api.neur.io/v1/samples/live/last"

    headers = self.__gen_headers()
    headers["Content-Type"] = "application/json"

    params = { "sensorId": sensor_id }
    url = self.__append_url_params(url, params)

    r = requests.get(url, headers=headers)
    return r.json()

  def get_samples(self, sensor_id, start, granularity, end=None,
                  frequency=None, per_page=None, page=None,
                  full=False):
    """Get a sensor's samples for a specified time interval.

    Args:
      sensor_id (string): hexadecimal id of the sensor to query, e.g.
                          ``0x0013A20040B65FAD``
      start (string): ISO 8601 start time of sampling; depends on the
        ``granularity`` parameter value, the maximum supported time ranges are:
        1 day for minutes or hours granularities, 1 month for days,
        6 months for weeks, 1 year for months granularity, and 10 years for
        years granularity
      granularity (string): granularity of the sampled data; must be one of
        "minutes", "hours", "days", "weeks", "months", or "years"
      end (string, optional): ISO 8601 stop time for sampling; should be later
        than start time (default: the current time)
      frequency (string, optional): frequency of the sampled data (e.g. with
        granularity set to days, a value of 3 will result in a sample for every
        third day, should be a multiple of 5 when using minutes granularity)
        (default: 1) (example: "1, 5")
      per_page (string, optional): the number of returned results per page
        (min 1, max 500) (default: 10)
      page (string, optional): the page number to return (min 1, max 100000)
        (default: 1)
      full (bool, optional): include additional information per sample
        (default: False)

    Returns:
      list: dictionary objects containing sample data
    """
    url = "https://api.neur.io/v1/samples"
    if full:
      url = "https://api.neur.io/v1/samples/full"

    headers = self.__gen_headers()
    headers["Content-Type"] = "application/json"

    params = {
      "sensorId": sensor_id,
      "start": start,
      "granularity": granularity
    }
    if end:
      params["end"] = end
    if frequency:
      params["frequency"] = frequency
    if per_page:
      params["perPage"] = per_page
    if page:
      params["page"] = page
    url = self.__append_url_params(url, params)

    r = requests.get(url, headers=headers)
    return r.json()

  def get_samples_stats(self, sensor_id, start, granularity, end=None,
                  frequency=None, per_page=None, page=None):
    """Get brief stats for energy consumed in a given time interval.

    Note:
      Note: this endpoint uses the sensor location's time zone when
      generating time intervals for the stats, which is relevant if that time
      zone uses daylight saving time (some days will be 23 or 25 hours long).

    Args:
      sensor_id (string): hexadecimal id of the sensor to query, e.g.
                          ``0x0013A20040B65FAD``
      start (string): ISO 8601 start time of sampling; depends on the
        ``granularity`` parameter value, the maximum supported time ranges are:
        1 day for minutes or hours granularities, 1 month for days,
        6 months for weeks, 1 year for months granularity, and 10 years for
        years granularity
      granularity (string): granularity of the sampled data; must be one of
        "minutes", "hours", "days", "weeks", "months", or "years"
      end (string, optional): ISO 8601 stop time for sampling; should be later
        than start time (default: the current time)
      frequency (string, optional): frequency of the sampled data (e.g. with
        granularity set to days, a value of 3 will result in a sample for every
        third day, should be a multiple of 5 when using minutes granularity)
        (default: 1) (example: "1, 5")
      per_page (string, optional): the number of returned results per page
        (min 1, max 500) (default: 10)
      page (string, optional): the page number to return (min 1, max 100000)
        (default: 1)

    Returns:
      list: dictionary objects containing sample statistics data
    """
    url = "https://api.neur.io/v1/samples/stats"

    headers = self.__gen_headers()
    headers["Content-Type"] = "application/json"

    params = {
      "sensorId": sensor_id,
      "start": start,
      "granularity": granularity
    }
    if end:
      params["end"] = end
    if frequency:
      params["frequency"] = frequency
    if per_page:
      params["perPage"] = per_page
    if page:
      params["page"] = page
    url = self.__append_url_params(url, params)

    r = requests.get(url, headers=headers)
    return r.json()

  def get_appliances(self, location_id):
    """Get the appliances added for a specified location.

    Note:
      This funcitonality is not presently supported.

    Args:
      location_id (string): identifiying string of appliance

    Returns:
      list: dictionary objects containing appliances data
    """
    url = "https://api.neur.io/v1/appliances"

    headers = self.__gen_headers()
    headers["Content-Type"] = "application/json"

    params = {
      "locationId": location_id,
    }
    url = self.__append_url_params(url, params)

    r = requests.get(url, headers=headers)
    return r.json()
