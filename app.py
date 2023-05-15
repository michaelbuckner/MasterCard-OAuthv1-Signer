import oauth1.authenticationutils as authenticationutils
from oauth1.oauth import OAuth
from flask import Flask, request, jsonify

app = Flask(__name__)

def generate_oauth_headers(consumer_key, signing_key, keystore_password, uri, http_verb, json_obj):
    """
    Generates OAuth headers for authenticated requests to an API.
    Args:
        consumer_key (str): The consumer key for the API.
        signing_key (str): The path to the private key file used for signing requests.
        keystore_password (str): The password to access the keystore containing the private key.
        uri (str): The URI of the API endpoint.
        http_verb (str): The HTTP verb to use for the request (e.g., 'GET', 'POST', etc.).
        json_obj (dict): The JSON object to include in the request.
    Returns:
        dict: A dictionary containing the authorization header for the request.
    """
    signing_key = authenticationutils.load_signing_key(signing_key, keystore_password)
    authHeader = OAuth.get_authorization_header(uri, http_verb, json_obj, consumer_key, signing_key)  # Pass the JSON object to the method

    headerdict = {'Authorization': authHeader}
    return headerdict

@app.route('/generate_oauth_headers', methods=['POST'])
def generate_headers():
    """
    Generates OAuth headers for authenticated requests to an API using data in a JSON payload.
    Returns:
        dict: A dictionary containing the authorization header for the request.
    """
    data = request.get_json()
    consumer_key = data.get('consumer_key')
    signing_key = data.get('signing_key')
    keystore_password = data.get('keystore_password')
    uri = data.get('uri')
    http_verb = data.get('http_verb')
    json_obj = data.get('json_obj')

    if all(param is not None for param in [consumer_key, signing_key, keystore_password, uri, http_verb, json_obj]):
        headers = generate_oauth_headers(consumer_key, signing_key, keystore_password, uri, http_verb, json_obj)
        return jsonify(headers)
    else:
        return jsonify({"error": "Missing required parameters"}), 400
    
@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "OK"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)