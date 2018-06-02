# MIT License
#
# Copyright (c) 2018 Freedge.org
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# =============================================================================

import jsw
import datetime


def get_config(self, version, base_url, project_id, cloud_region, registry_id, device_id, private_key):
    jwt = create_jwt(project_id, private_key, "ES256")
    headers = {
    'authorization': 'Bearer {}'.format(jwt),
    'content-type': 'application/json',
    'cache-control': 'no-cache'}
    basepath = '{}/projects/{}/locations/{}/registries/{}/devices/{}/'
    template = basepath + 'config?local_version={}'
    config_url = template.format(base_url, project_id, cloud_region, registry_id, device_id, version)
    response = requests.get(config_url, headers=headers)
    if (response.status_code != 200):
        print('Error getting config: {}, retrying'.format(response.status_code))
        raise AssertionError('Not OK response: {}'.format(response.status_code))
    return response


def create_jwt(self, project_id, private_key_file, algorithm, expire_in=20):
    """Creates a Json Web Token (JWB) (https://jwt.io) to establish
    a secured connection between two parties.
    
    Args:
      project_id: The cloud project ID this device belongs to
      private_key_file: A path to a file containing either an RSA256 or
              ES256 private key.
      expire_in: duration for the token to be alived
      algorithm: The encryption algorithm to use. Either 'RS256' or 'ES256'

    Returns:
      An MQTT generated from the given project_id and private key, which
      expires in 20 minutes. After 20 minutes, your client will be
      disconnected, and a new JWT will have to be generated.
      
    Raises:
        ValueError: If the private_key_file does not contain a known key.
    """
    current_time =  datetime.datetime.utcnow()
    alive_duration = datetime.timedelta(minutes=expire_in)
    token = {
        'iat': current_time,  # Time when token is generated
        'exp': current_time + alive_duration,  # Duration the token is alive.
        'aud': project_id   # The audience field should always be set to the GCP project id.
    }

    # Read the private key file.
    with open(private_key_file, 'r') as f:
        private_key = f.read()

    return jwt.encode(token, private_key, algorithm=algorithm).decode("utf-8")
