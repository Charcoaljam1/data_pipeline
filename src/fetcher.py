import requests 
import json
import yaml 
import os
from dotenv import load_dotenv
from typing import Dict, Callable, Any

load_dotenv()

api_key = os.environ.get("ALPHA_VANTAGE_API_KEY")

if not api_key:
    print('API key not available')



with open('alpha_vantage.yaml','r') as f:
    config = yaml.safe_load(f)

url = config['api_settings']['base_url']
function = config['api_function_mapping']['time_series_daily']
size = config['api_settings']['default_output_size']
symbols = config['tickers']['second']








def code_200(response: requests.Response)-> dict:
    """Processes the response from the API when the response code is 200"""
    print("STATUS 200: Request successful. Parsing JSON.")
    return response.json()

def code_301(response: requests.Response):
    """Logs and reports permanent URL redirection."""
    print(f"STATUS 301: Resource permanently moved. URL: {response.url} -> {response.headers.get('Location', 'N/A')}")
    # Log this error, send alert, update config if appropriate
    # You might want to raise an exception or return a specific error object here
    return {} # Or raise an exception

def code_302(response: requests.Response):
    """Logs temporary URL redirection."""
    print(f"STATUS 302: Resource temporarily moved. URL: {response.url} -> {response.headers.get('Location', 'N/A')}")
    # Log this warning
    return {}

def code_304(response: requests.Response):
    """Logs temporary URL redirection."""
    print(f"STATUS 302: Resource temporarily moved. URL: {response.url} -> {response.headers.get('Location', 'N/A')}")
    # Log this warning
    return {}

def code_400(response: requests.Response):
    """Logs bad syntax, suggests checking API docs."""
    print(f"STATUS 400: Bad request syntax. Response: {response.text[:200]}...")
    print("Action: Check request parameters and API documentation for changes.")
    # Potentially log full request details for debugging
    return {}

def code_401(response: requests.Response):
    """Logs authentication issues."""
    print(f"STATUS 401: Unauthorized. Check API key/credentials. Response: {response.text[:200]}...")
    # This is critical, might need to halt pipeline or alert immediately
    return {}

def code_404(response: requests.Response):
    """Logs missing resource."""
    print(f"STATUS 404: Resource not found. URL: {response.url}")
    # This might mean a symbol no longer exists, or endpoint changed
    return {}

def code_405(response: requests.Response):
    """Logs incorrect HTTP method."""
    print(f"STATUS 405: Method Not Allowed. Used GET, expected different method. URL: {response.url}")
    print("Action: Reassess HTTP method (e.g., POST vs GET) and try again if appropriate.")
    return {}

def code_429(response: requests.Response):
    """Handles rate limiting with exponential backoff logic."""
    print(f"STATUS 429: Rate limit exceeded. Response: {response.text[:200]}...")
    print("Action: Implementing exponential backoff. Rescheduling might be needed for free tier.")
    # Implement actual backoff logic here, e.g., using a retry library like tenacity
    # For now, we'll just print and return empty, but in production, this is crucial.
    return {}

def code_5xx(response: requests.Response):
    """Generic handler for 5xx server errors."""
    print(f"STATUS {response.status_code}: Server Error. Response: {response.text[:200]}...")
    print("Action: Server might be down or experiencing issues. Retrying or rescheduling.")
    # This is where you might implement retries
    return {}

STATUS_CODE_HANDLERS: Dict[int, Callable[[requests.Response], Dict[str, Any]]] = {
    200: code_200,
    301: code_301,
    302: code_302,
    304: code_304,
    400: code_400,
    401: code_401,
    404: code_404,
    405: code_405,
    429: code_429
}

from test import Data

for symbol in symbols:
    try:
        with open(f'raw_{symbol}.json', 'r') as f:
            data = f.read()
            print(f'{symbol}_data read.')

    except Exception as e:
        print(e)
   
    m=Data.model_validate_json(data)
   # print(dir(m))

# for symbol in symbols:
#     response = requests.get(url=url, 
#                             params={'function': function, 'symbol':symbol, 'apikey':api_key, 'outputsize':size})
        
#     data = response_code_mapping.get(response.status_code)(response)

#     print(response.headers)

#     # print(response.status_code)
#     # print(response.json())

#     try: 
#         with open(f'raw_{symbol}.json', 'w') as f:
#             json.dump(data,f, indent=4)
#             print(f'raw_{symbol}.json created successfully')
#     except Exception as e:
#         print(f'Error writing to file: {e}')