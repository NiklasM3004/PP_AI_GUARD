import requests
import base64
import jwt
import logging

logger = logging.getLogger(__name__)

def exchange_code_for_user_data(auth_code, config):
    """
    Tauscht den Auth-Code gegen die sub (ID) und Email bei Cognito ein.
    """
    token_url = f"{config['cognito_domain']}/oauth2/token"
    
    # Payload für den Token-Endpunkt
    payload = {
        "grant_type": "authorization_code",
        "client_id": config['client_id'],
        "code": auth_code,
        "redirect_uri": config['redirect_uri'],
    }
    
    # Basic Auth Header mit Client ID und Secret
    auth_string = f"{config['client_id']}:{config['client_secret']}"
    encoded_auth = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_auth}"
    }

    try:
        response = requests.post(token_url, headers=headers, data=payload)
        response.raise_for_status()
        tokens = response.json()

        # ID-Token decodieren, um 'sub' (tenant_id) zu erhalten
        id_token = tokens.get("id_token")
        decoded_claims = jwt.decode(id_token, options={"verify_signature": False})
        
        return {
            "tenant_id": decoded_claims.get("sub"),
            "email": decoded_claims.get("email")
        }
    except Exception as e:
        logger.error(f"Fehler beim Cognito-Exchange: {e}")
        raise e