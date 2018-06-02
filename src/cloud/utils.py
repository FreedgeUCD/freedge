import jwt
import datetime

def create_jwt(self, project_id, private_key_file, algorithm='ES256', expire_in=60):
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
         # Time when token is generated
        'iat': current_time, 
        # Duration the token is alive.
        'exp': current_time + alive_duration,  
        # The audience field should always be set to the project id.
        'aud': project_id   
    }
    # Read the private key file.
    with open(private_key_file, 'r') as f:
        private_key = f.read()

    return jwt.encode(token, private_key, algorithm=algorithm).decode("utf-8")
