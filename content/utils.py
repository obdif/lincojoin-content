import requests
from rest_framework.exceptions import AuthenticationFailed


AUTH_SERVICE_URL = "https://lincojoin-authentication.onrender.com/api/auth/validate-token/"

def get_user_id_from_auth_service(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise AuthenticationFailed("Authorization header is missing.")

    try:
        token = auth_header.split(" ")[1]
    except IndexError:
        raise AuthenticationFailed("Invalid token format. Expected 'Bearer <token>'.")

    try:
        response = requests.post(AUTH_SERVICE_URL, data={"token": token})
    except requests.exceptions.RequestException as e:
        raise AuthenticationFailed(f"Unable to connect to authentication service: {e}")

    # if response.status_code != 200:
    #     raise AuthenticationFailed("Invalid token. Authentication service rejected the token.")
    
    
    if response.status_code != 200:
        raise AuthenticationFailed(f"Auth Service Error: {response.status_code} - {response.text}")

    
    

    user_data = response.json()
    user_id = user_data.get("id")
    if not user_id:
        raise AuthenticationFailed("Authentication service did not return a valid user ID.")

    return user_id