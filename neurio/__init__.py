"""
The MIT License

Copyright (c) 2007-2010 Leah Culver, Joe Stump, Mark Paschal, Vic Fryzel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import base64
import urllib
import urlparse
import requests

import _version

__version__ = _version.__version__

class TokenProvider(object):

  __key = None
  __secret = None
  __token = None

  def __init__(self, key, secret):
    self.__key = key
    self.__secret = secret

    if self.__key is None or self.__secret is None:
            raise ValueError("Key and secret must be set.")

  def getToken(self):
    if self.__token is not None:
      return self.__token

    url = "https://api-staging.neur.io/v1/oauth2/token"
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
    self.__token = token_provider.getToken()

  def __gen_headers(self):
    headers = {
      "Authorization": " ".join(["Bearer", self.__token])
    }

    return headers

  def __append_url_params(self, url, params):
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urllib.urlencode(query)

    return urlparse.urlunparse(url_parts)

  def getLiveSamples(self, sensor_id, last=None):
    url = "https://api-staging.neur.io/v1/samples/live"

    headers = self.__gen_headers()
    headers["Content-Type"] = "application/json"

    params = { "sensorId": sensor_id }
    if last:
      params["last"] = last
    url = self.__append_url_params(url, params)

    r = requests.get(url, headers=headers)
    return r.json()


  def getLastLiveSamples(self, sensor_id):
    url = "https://api-staging.neur.io/v1/samples/live/last"

    headers = self.__gen_headers()
    headers["Content-Type"] = "application/json"

    params = { "sensorId": sensor_id }
    url = self.__append_url_params(url, params)

    r = requests.get(url, headers=headers)
    return r.json()

  def getSamples(self, sensor_id, start, granularity, end=None,
                  frequency=None, perPage=None, page=None
                  full=False):
    url = "https://api-staging.neur.io/v1/samples"
    if full:
      url = "https://api-staging.neur.io/v1/samples/full"

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
    if perPage:
      params["perPage"] = perPage
    if page:
      params["page"] = page
    url = self.__append_url_params(url, params)

    r = requests.get(url, headers=headers)
    return r.json()

  def getFullSamples(self, sensor_id, start, granularity, end=None,
                      frequency=None, perPage=None, page=None):
    return getSamples(sensor_id=sensor_id, start=start,
                      granularity=granularity, end=end,
                      frequency=frequency, perPage=perPage,
                      full=True)

  def getStatsSamples(self, sensor_id, start, granularity, end=None,
                  frequency=None, perPage=None, page=None):
    url = "https://api-staging.neur.io/v1/samples/stats"

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
    if perPage:
      params["perPage"] = perPage
    if page:
      params["page"] = page
    url = self.__append_url_params(url, params)

    r = requests.get(url, headers=headers)
    return r.json()
    
