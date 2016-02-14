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

import base64
import requests

try:
  from urllib import urlencode
except ImportError:
  from urllib.parse import urlencode

try:
  from urlparse import urlparse, parse_qsl, urlunparse
except ImportError:
  from urllib.parse import urlparse, parse_qsl, urlunparse

__version__ = "0.3.0"

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
    try:
      credentials = base64.b64encode(":".join([self.__key,self.__secret]))
    except TypeError:
      credentials = base64.b64encode(self.__key.encode('ascii') + ":".encode('ascii') + self.__secret.encode('ascii')).decode("utf-8")
    headers = {
      "Authorization": " ".join(["Basic", credentials]),
    }
    payload = {
      "grant_type": "client_credentials"
    }

    r = requests.post(url, data=payload, headers=headers)

    print(r.json())

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
    url_parts = list(urlparse(url))
    query = dict(parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urlencode(query)

    return urlunparse(url_parts)

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


  def get_appliance(self, appliance_id):
    """Get the information for a specified appliance

    Args:
      appliance_id (string): identifiying string of appliance

    Returns:
      list: dictionary object containing information about the specified appliance
    """
    url = "https://api.neur.io/v1/appliances/%s"%(appliance_id)

    headers = self.__gen_headers()
    headers["Content-Type"] = "application/json"

    r = requests.get(url, headers=headers)
    return r.json()



  def get_user_information(self):
    """Gets the current user information, including sensor ID

    Args:
      None

    Returns:
      dictionary object containing information about the current user
    """
    url = "https://api.neur.io/v1/users/current"

    headers = self.__gen_headers()
    headers["Content-Type"] = "application/json"

    r = requests.get(url, headers=headers)
    return r.json()


  def get_appliance_event_by_location(self, location_id, start, end, per_page=None, page=None, min_power=None):
    """Get appliance events by location Id.

    Args:
      location_id (string): hexadecimal id of the sensor to query, e.g.
                          ``0x0013A20040B65FAD``
      start (string): ISO 8601 start time for getting the events of appliances.
      end (string): ISO 8601 stop time for getting the events of appliances.
        Cannot be larger than 1 day from start time
      min_power (string): The minimum average power (in watts) for filtering.
        Only events with an average power above this value will be returned.
        (default: 400)
      per_page (string, optional): the number of returned results per page
        (min 1, max 500) (default: 10)
      page (string, optional): the page number to return (min 1, max 100000)
        (default: 1)

    Returns:
      list: dictionary objects containing appliance events meeting specified criteria
    """
    url = "https://api.neur.io/v1/appliances/events"

    headers = self.__gen_headers()
    headers["Content-Type"] = "application/json"

    params = {
      "locationId": location_id,
      "start": start,
      "end": end
    }
    if min_power:
      params["minPower"] = min_power
    if per_page:
      params["perPage"] = per_page
    if page:
      params["page"] = page
    url = self.__append_url_params(url, params)

    r = requests.get(url, headers=headers)
    return r.json()

  def get_appliance_event_after_time(self, location_id, since, per_page=None, page=None, min_power=None):
    """Get appliance events by location Id after defined time.

    Args:
      location_id (string): hexadecimal id of the sensor to query, e.g.
                          ``0x0013A20040B65FAD``
      since (string): ISO 8601 start time for getting the events that are created or updated after it.
        Maxiumim value allowed is 1 day from the current time.
      min_power (string): The minimum average power (in watts) for filtering.
        Only events with an average power above this value will be returned.
        (default: 400)
      per_page (string, optional): the number of returned results per page
        (min 1, max 500) (default: 10)
      page (string, optional): the page number to return (min 1, max 100000)
        (default: 1)

    Returns:
      list: dictionary objects containing appliance events meeting specified criteria
    """
    url = "https://api.neur.io/v1/appliances/events"

    headers = self.__gen_headers()
    headers["Content-Type"] = "application/json"

    params = {
      "locationId": location_id,
      "since": since
    }
    if min_power:
      params["minPower"] = min_power
    if per_page:
      params["perPage"] = per_page
    if page:
      params["page"] = page
    url = self.__append_url_params(url, params)

    r = requests.get(url, headers=headers)
    return r.json()

  def get_appliance_event_by_appliance(self, appliance_id, start, end, per_page=None, page=None, min_power=None):
    """Get appliance events by appliance Id.

    Args:
      appliance_id (string): hexadecimal id of the appliance to query, e.g.
                          ``0x0013A20040B65FAD``
      start (string): ISO 8601 start time for getting the events of appliances.
      end (string): ISO 8601 stop time for getting the events of appliances.
        Cannot be larger than 1 day from start time
      min_power (string): The minimum average power (in watts) for filtering.
        Only events with an average power above this value will be returned.
        (default: 400)
      per_page (string, optional): the number of returned results per page
        (min 1, max 500) (default: 10)
      page (string, optional): the page number to return (min 1, max 100000)
        (default: 1)

    Returns:
      list: dictionary objects containing appliance events meeting specified criteria
    """
    url = "https://api.neur.io/v1/appliances/events"

    headers = self.__gen_headers()
    headers["Content-Type"] = "application/json"

    params = {
      "applianceId": appliance_id,
      "start": start,
      "end": end
    }
    if min_power:
      params["minPower"] = min_power
    if per_page:
      params["perPage"] = per_page
    if page:
      params["page"] = page
    url = self.__append_url_params(url, params)

    r = requests.get(url, headers=headers)
    return r.json()

  def get_appliance_stats_by_location(self, location_id, start, end, granularity=None, per_page=None, page=None,
                                      min_power=None):
    """Get appliance usage data for a given location within a given time range.
    Stats are generated by fetching appliance events that match the supplied
    criteria and then aggregating them together based on the granularity
    specified with the request.

    Note:
      This endpoint uses the location's time zone when generating time intervals
      for the stats, which is relevant if that time zone uses daylight saving
      time (some days will be 23 or 25 hours long).

    Args:
      location_id (string): hexadecimal id of the sensor to query, e.g.
                          ``0x0013A20040B65FAD``
      start (string): ISO 8601 start time for getting the events of appliances.
      end (string): ISO 8601 stop time for getting the events of appliances.
        Cannot be larger than 1 month from start time
      granularity (string): granularity of stats. If the granularity is
        'unknown', the stats for the appliances between the start and
        end time is returned.;
        must be one of  "minutes", "hours", "days", "weeks", "months", or "unknown"
        (default: days)
      min_power (string): The minimum average power (in watts) for filtering.
        Only events with an average power above this value will be returned.
        (default: 400)
      per_page (string, optional): the number of returned results per page
        (min 1, max 500) (default: 10)
      page (string, optional): the page number to return (min 1, max 100000)
        (default: 1)

    Returns:
      list: dictionary objects containing appliance events meeting specified criteria
    """
    url = "https://api.neur.io/v1/appliances/stats"

    headers = self.__gen_headers()
    headers["Content-Type"] = "application/json"

    params = {
      "locationId": location_id,
      "start": start,
      "end": end
    }
    if granularity:
      params["granularity"] = granularity
    if min_power:
      params["minPower"] = min_power
    if per_page:
      params["perPage"] = per_page
    if page:
      params["page"] = page
    url = self.__append_url_params(url, params)

    r = requests.get(url, headers=headers)
    return r.json()

  def get_appliance_stats_by_appliance(self, appliance_id, start, end, granularity=None, per_page=None, page=None,
                                      min_power=None):
    """Get appliance usage data for a single appliance within a given time range.
    Stats are generated by fetching appliance events that match the supplied
    criteria and then aggregating them together based on the granularity
    specified with the request.

    Note:
      This endpoint uses the location's time zone when generating time intervals
      for the stats, which is relevant if that time zone uses daylight saving
      time (some days will be 23 or 25 hours long).

    Args:
      appliance_id (string): hexadecimal id of the appliance to query, e.g.
                          ``0x0013A20040B65FAD``
      start (string): ISO 8601 start time for getting the events of appliances.
      end (string): ISO 8601 stop time for getting the events of appliances.
        Cannot be larger than 1 month from start time
      granularity (string): granularity of stats. If the granularity is
        'unknown', the stats for the appliances between the start and
        end time is returned.;
        must be one of  "minutes", "hours", "days", "weeks", "months", or "unknown"
        (default: days)
      min_power (string): The minimum average power (in watts) for filtering.
        Only events with an average power above this value will be returned.
        (default: 400)
      per_page (string, optional): the number of returned results per page
        (min 1, max 500) (default: 10)
      page (string, optional): the page number to return (min 1, max 100000)
        (default: 1)

    Returns:
      list: dictionary objects containing appliance events meeting specified criteria
    """
    url = "https://api.neur.io/v1/appliances/stats"

    headers = self.__gen_headers()
    headers["Content-Type"] = "application/json"

    params = {
      "applianceId": appliance_id,
      "start": start,
      "end": end
    }
    if granularity:
      params["granularity"] = granularity
    if min_power:
      params["minPower"] = min_power
    if per_page:
      params["perPage"] = per_page
    if page:
      params["page"] = page
    url = self.__append_url_params(url, params)

    r = requests.get(url, headers=headers)
    return r.json()
