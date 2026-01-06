from connectors.core.connector import ConnectorError, get_logger
import requests
import ipaddress
import re

logger = get_logger('crowdsec')

# Default URLs (fallback if not configured)
DEFAULT_SERVICE_BASE_URL = "https://admin.api.crowdsec.net/v1"
DEFAULT_CTI_BASE_URL = "https://cti.api.crowdsec.net/v2"


class CrowdSecClient:
    def __init__(self, config):
        # Extract API keys with proper field names
        self.service_api_key = config.get('service_api_key')
        self.cti_api_key = config.get('cti_api_key')

        # Extract base URLs from config or use defaults
        self.service_base_url = config.get('service_api_base_url', DEFAULT_SERVICE_BASE_URL)
        self.cti_base_url = config.get('cti_base_url', DEFAULT_CTI_BASE_URL)

        # Extract SSL verification setting (default to True for security)
        self.verify_ssl = config.get('verify_ssl')

        # CTI API key is always required
        if not self.cti_api_key:
            raise ConnectorError("CTI API key is required for connector operations")

    def _validate_ip_address(self, ip_address):
        """Validate IP address format (IPv4 or IPv6)"""
        try:
            ipaddress.ip_address(ip_address.strip())
            return True
        except ValueError:
            return False

    def _requires_service_api(self, operation_name):
        """Check if operation requires Service API key"""
        service_operations = [
            'list_blocklists', 'create_blocklist', 'get_blocklist', 'delete_blocklist',
            'update_blocklist','add_ips_to_blocklist', 'delete_ips_from_blocklist',
            'bulk_overwrite_blocklist_ips', 'get_blocklist_ips', 'list_allowlists', 'create_allowlist',
            'get_allowlist_items', 'add_items_to_allowlist', 'get_specific_allowlist_item',
            'update_allowlist', 'delete_allowlist_item',
            'delete_allowlist', 'list_integrations', 'create_integration',
            'get_integration', 'update_integration', 'delete_integration'
        ]
        return operation_name in service_operations

    def _check_service_api_key(self, operation_name):
        """Validate Service API key is available for operations that need it"""
        if self._requires_service_api(operation_name) and not self.service_api_key:
            raise ConnectorError(f"Service API key is required for {operation_name} operation")

    def make_request(self, method, url, headers=None, params=None, data=None, operation_name=None):
        """Make HTTP request with proper error handling"""
        try:
            # Check Service API key if needed
            if operation_name:
                self._check_service_api_key(operation_name)

            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=data,
                verify=self.verify_ssl
            )

            # Handle different HTTP status codes
            if response.status_code in [200, 201]:
                try:
                    return response.json() if response.text else {}
                except ValueError:
                    # If response is not JSON, return text
                    return {"message": response.text}
            elif response.status_code == 204:
                return {"status": "success", "message": "Operation completed successfully"}
            elif response.status_code == 202:
                return {"status": "accepted", "message": "Request accepted, processing in background"}
            elif response.status_code == 400:
                error_msg = self._extract_error_message(response)
                raise ConnectorError(f"Bad Request: {error_msg}")
            elif response.status_code == 401:
                raise ConnectorError("Authentication failed - check API key")
            elif response.status_code == 403:
                raise ConnectorError("Access forbidden - insufficient permissions")
            elif response.status_code == 404:
                raise ConnectorError("Resource not found")
            elif response.status_code == 429:
                raise ConnectorError("Rate limit exceeded - please try again later")
            elif response.status_code >= 500:
                raise ConnectorError(f"Server error: {response.status_code}")
            else:
                error_msg = self._extract_error_message(response)
                logger.error(f"Request failed | Status: {response.status_code} | Response: {response.text}")
                raise ConnectorError(f"API call failed: {response.status_code} - {error_msg}")

        except requests.exceptions.Timeout:
            raise ConnectorError("Request timeout - API did not respond within 30 seconds")
        except requests.exceptions.ConnectionError:
            raise ConnectorError("Connection error - unable to reach API endpoint")
        except requests.exceptions.SSLError:
            raise ConnectorError("SSL verification failed - check SSL configuration")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request Exception: {e}")
            raise ConnectorError(f"Request failed: {str(e)}")

    def _extract_error_message(self, response):
        """Extract error message from response safely"""
        try:
            error_data = response.json()
            if not error_data:
                return response.text or 'Unknown error'

            # Follow official error schema: check 'message' first, then 'errors' for details
            message = error_data.get('message', 'Unknown error')
            errors = error_data.get('errors')

            if errors:
                return f"{message} - {errors}"
            return message

        except ValueError:
            # Response is not JSON
            return response.text or 'Unknown error'


def check_health(config):
    """Health check using CTI API endpoint"""
    try:
        client = CrowdSecClient(config)
        # Use configured CTI base URL
        url = f"{client.cti_base_url}/smoke/1.1.1.1"
        headers = {"x-api-key": client.cti_api_key, "Accept": "application/json"}
        response = client.make_request("GET", url, headers=headers)
        return {
            "status": "success",
            "details": "Successfully connected to CrowdSec CTI API",
            "cti_base_url": client.cti_base_url
        }
    except ConnectorError as e:
        logger.error(f"Health check failed: {e}")
        raise ConnectorError(f"Health check failed: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during health check: {e}")
        raise ConnectorError("Health check failed due to unexpected error")


def get_ip_reputation(config, params):
    """Retrieve threat intelligence information for an IP address"""
    client = CrowdSecClient(config)
    ip_address = params.get("ip_address", "").strip()
    if not ip_address:
        raise ConnectorError("IP address parameter is required")

    # Validate IP address format
    if not client._validate_ip_address(ip_address):
        raise ConnectorError(f"Invalid IP address format: {ip_address}")

    url = f"{client.cti_base_url}/smoke/{ip_address}"
    headers = {"x-api-key": client.cti_api_key, "Accept": "application/json"}
    return client.make_request("GET", url, headers=headers, operation_name="get_ip_reputation")


def search_ip_reputation(config, params):
    """Search for IPs in CrowdSec CTI API using Lucene query filters"""
    client = CrowdSecClient(config)

    query = params.get("query", "").strip()
    if not query:
        raise ConnectorError("Query parameter is required")

    since = params.get("since", "").strip()
    page = params.get("page", 1)
    limit = params.get("limit", 10)

    url = f"{client.cti_base_url}/smoke/search"
    headers = {"x-api-key": client.cti_api_key, "Accept": "application/json"}

    payload = {"query": query, "page": page, "limit": limit}
    if since:
        payload["since"] = since

    return client.make_request(
        "GET", url, headers=headers, params=payload, operation_name="search_ip_reputation")


def batch_get_ip_reputation(config, params):
    """Query batches of IPs in the CrowdSec CTI API"""
    client = CrowdSecClient(config)
    ips_input = params.get("ips", "").strip()
    if not ips_input:
        raise ConnectorError("IPs parameter is required")

    # Process IPs from comma-separated or newline-separated format
    try:
        ips = []
        for ip in re.split(r'[,\n\r]+', ips_input):
            ip = ip.strip()
            if ip:
                ips.append(ip)
        if not ips:
            raise ConnectorError("No valid IP addresses found in input")
    except Exception as e:
        raise ConnectorError(f"Error processing IP addresses: {str(e)}")

    # Validate each IP address
    for ip in ips:
        if not client._validate_ip_address(ip):
            raise ConnectorError(f"Invalid IP address format: {ip}")

    url = f"{client.cti_base_url}/smoke"
    headers = {"x-api-key": client.cti_api_key, "Accept": "application/json"}
    params_dict = {"ips": ",".join(ips)}

    return client.make_request("GET", url, headers=headers, params=params_dict, operation_name="batch_get_ip_reputation")


def get_malevolent_ips(config, params):
    """Retrieve a list of malevolent IP addresses from CrowdSec CTI, filtering by date of modification"""
    client = CrowdSecClient(config)

    # Extract optional parameters with defaults
    page = params.get("page", 1)
    limit = params.get("limit", 50)
    since = params.get("since", "").strip()

    # Validate page and limit parameters
    try:
        page = int(page) if page else 1
        limit = int(limit) if limit else 50
    except (ValueError, TypeError):
        raise ConnectorError("Page and limit parameters must be valid numbers")

    if page < 1:
        raise ConnectorError("Page number must be greater than 0")
    if limit < 1 or limit > 1000:
        raise ConnectorError("Limit must be between 1 and 1000")

    url = f"{client.cti_base_url}/fire"
    headers = {"x-api-key": client.cti_api_key, "Accept": "application/json"}

    # Build query parameters
    query_params = {"page": page, "limit": limit}
    if since:
        query_params["since"] = since

    return client.make_request("GET", url, headers=headers, params=query_params, operation_name="get_malevolent_ips")


def list_blocklists(config, params):
    """Retrieve a list of all blocklists"""
    client = CrowdSecClient(config)
    url = f"{client.service_base_url}/blocklists"
    headers = {"x-api-key": client.service_api_key, "Accept": "application/json"}
    return client.make_request("GET", url, headers=headers, operation_name="list_blocklists")


def create_blocklist(config, params):
    """Create a new custom blocklist"""
    client = CrowdSecClient(config)
    name = params.get("name", "").strip()
    if not name:
        raise ConnectorError("Blocklist name is required")

    url = f"{client.service_base_url}/blocklists"
    headers = {"x-api-key": client.service_api_key, "Accept": "application/json"}
    data = {
        "name": name,
        "description": params.get("description", "").strip()
    }
    return client.make_request("POST", url, headers=headers, data=data, operation_name="create_blocklist")


def update_blocklist(config, params):
    """Update an existing blocklist with new properties"""
    client = CrowdSecClient(config)
    blocklist_id = params.get("blocklist_id", "").strip()
    if not blocklist_id:
        raise ConnectorError("Blocklist ID is required")

    # All fields are required for this operation based on API spec
    required_fields = ["label", "description", "references", "tags", "from_cti_query", "since"]
    data = {}
    for field in required_fields:
        value = params.get(field, "").strip()
        if not value:
            raise ConnectorError(f"{field} is required")
        if field == "references":
            # Split references by newlines and validate URLs
            refs = [ref.strip() for ref in value.split('\n') if ref.strip()]
            data["references"] = refs
        elif field == "tags":
            # Split tags by comma
            tags = [tag.strip() for tag in value.split(',') if tag.strip()]
            data["tags"] = tags
        else:
            data[field] = value

    url = f"{client.service_base_url}/blocklists/{blocklist_id}"
    headers = {"x-api-key": client.service_api_key, "Accept": "application/json", "Content-Type": "application/json"}
    return client.make_request("PATCH", url, headers=headers, data=data, operation_name="update_blocklist")


def add_ips_to_blocklist(config, params):
    """Add IP addresses to a specific blocklist"""
    client = CrowdSecClient(config)
    blocklist_id = params.get("blocklist_id", "").strip()
    if not blocklist_id:
        raise ConnectorError("Blocklist ID is required")

    ips_input = params.get("ips", "").strip()
    if not ips_input:
        raise ConnectorError("IP addresses parameter is required")

    expiration = params.get("expiration", "").strip()
    if not expiration:
        raise ConnectorError("Expiration date is required")

    # Process IPs from comma-separated or newline-separated format
    try:
        # Split by comma, newline, or both and clean up whitespace
        ips = []
        for ip in re.split(r'[,\n\r]+', ips_input):
            ip = ip.strip()
            if ip:
                ips.append(ip)
        if not ips:
            raise ConnectorError("No valid IP addresses found in input")
    except Exception as e:
        raise ConnectorError(f"Error processing IP addresses: {str(e)}")

    # Validate each IP address
    for ip in ips:
        if not client._validate_ip_address(ip):
            raise ConnectorError(f"Invalid IP address format: {ip}")

    url = f"{client.service_base_url}/blocklists/{blocklist_id}/ips"
    headers = {"x-api-key": client.service_api_key, "Accept": "application/json", "Content-Type": "application/json"}

    # API expects JSON array format
    data = {
        "ips": ips,
        "expiration": expiration
    }
    result = client.make_request(
        "POST", url, headers=headers, data=data, operation_name="add_ips_to_blocklist"
    )

    # Handle 201 status code
    if not result:
        result = {"status": "created", "message": f"Successfully added {len(ips)} IP(s) to blocklist"}
    return result


def get_blocklist_ips(config, params):
    client = CrowdSecClient(config)
    blocklist_id = params.get("blocklist_id")
    url = f"{client.service_base_url}/blocklists/{blocklist_id}"
    headers = {"x-api-key": client.service_api_key, "Accept": "application/json"}

    response = client.make_request("GET", url, headers=headers, operation_name="get_blocklist_ips")

    # Extract only IPs
    ips = []
    try:
        stats = response.get("stats", {}).get("content_stats", {}).get("top_ips", [])
        ips = [entry.get("ip") for entry in stats if "ip" in entry]
    except Exception:
        pass

    return {"blocklist_id": blocklist_id, "ips": ips}


def delete_ips_from_blocklist(config, params):
    """Remove specific IP addresses from a blocklist"""
    client = CrowdSecClient(config)
    blocklist_id = params.get("blocklist_id", "").strip()
    if not blocklist_id:
        raise ConnectorError("Blocklist ID is required")

    ips_input = params.get("ips", "").strip()
    if not ips_input:
        raise ConnectorError("IP addresses parameter is required")

    # Process IPs from comma-separated or newline-separated format
    try:
        ips = []
        for ip in re.split(r'[,\n\r]+', ips_input):
            ip = ip.strip()
            if ip:
                ips.append(ip)
        if not ips:
            raise ConnectorError("No valid IP addresses found in input")
    except Exception as e:
        raise ConnectorError(f"Error processing IP addresses: {str(e)}")

    # Validate each IP address
    for ip in ips:
        if not client._validate_ip_address(ip):
            raise ConnectorError(f"Invalid IP address format: {ip}")

    url = f"{client.service_base_url}/blocklists/{blocklist_id}/ips/delete"
    headers = {"x-api-key": client.service_api_key, "Accept": "application/json", "Content-Type": "application/json"}

    data = {"ips": ips}
    result = client.make_request("POST", url, headers=headers, data=data, operation_name="delete_ips_from_blocklist")

    if not result:
        result = {"status": "success", "message": f"Successfully deleted {len(ips)} IP(s) from blocklist"}
    return result


def bulk_overwrite_blocklist_ips(config, params):
    """Replace all IPs in a blocklist with new ones"""
    client = CrowdSecClient(config)
    blocklist_id = params.get("blocklist_id", "").strip()
    if not blocklist_id:
        raise ConnectorError("Blocklist ID is required")

    ips_input = params.get("ips", "").strip()
    if not ips_input:
        raise ConnectorError("IP addresses parameter is required")

    expiration = params.get("expiration", "").strip()
    if not expiration:
        raise ConnectorError("Expiration date is required")

    try:
        ips = []
        for ip in re.split(r'[,\n\r]+', ips_input):
            ip = ip.strip()
            if ip:
                ips.append(ip)
        if not ips:
            raise ConnectorError("No valid IP addresses found in input")
    except Exception as e:
        raise ConnectorError(f"Error processing IP addresses: {str(e)}")

    for ip in ips:
        if not client._validate_ip_address(ip):
            raise ConnectorError(f"Invalid IP address format: {ip}")

    url = f"{client.service_base_url}/blocklists/{blocklist_id}/ips/bulk_overwrite"
    headers = {"x-api-key": client.service_api_key, "Accept": "application/json", "Content-Type": "application/json"}

    data = {
        "ips": ips,
        "expiration": expiration
    }
    result = client.make_request("POST", url, headers=headers, data=data, operation_name="bulk_overwrite_blocklist_ips")

    if not result:
        result = {
            "status": "accepted",
            "message": f"Bulk overwrite request accepted for {len(ips)} IP(s). Processing in background.",
            "accepted": True
        }
    return result


def get_blocklist(config, params):
    """Retrieve details of a specific blocklist by ID"""
    client = CrowdSecClient(config)
    blocklist_id = params.get("blocklist_id", "").strip()
    if not blocklist_id:
        raise ConnectorError("Blocklist ID is required")

    url = f"{client.service_base_url}/blocklists/{blocklist_id}"
    headers = {"x-api-key": client.service_api_key, "Accept": "application/json"}
    return client.make_request("GET", url, headers=headers, operation_name="get_blocklist")


def delete_blocklist(config, params):
    """Delete a specific blocklist by ID"""
    client = CrowdSecClient(config)
    blocklist_id = params.get("blocklist_id", "").strip()
    if not blocklist_id:
        raise ConnectorError("Blocklist ID is required")

    url = f"{client.service_base_url}/blocklists/{blocklist_id}"
    headers = {"x-api-key": client.service_api_key, "Accept": "application/json"}
    return client.make_request("DELETE", url, headers=headers, operation_name="delete_blocklist")


def list_allowlists(config, params):
    """Retrieve a list of all allowlists"""
    client = CrowdSecClient(config)
    url = f"{client.service_base_url}/allowlists"
    headers = {"x-api-key": client.service_api_key, "Accept": "application/json"}
    return client.make_request("GET", url, headers=headers, operation_name="list_allowlists")


def create_allowlist(config, params):
    """Create a new custom allowlist"""
    client = CrowdSecClient(config)
    name = params.get("name", "").strip()
    if not name:
        raise ConnectorError("Allowlist name is required")

    url = f"{client.service_base_url}/allowlists"
    headers = {"x-api-key": client.service_api_key, "Accept": "application/json"}
    data = {
        "name": name,
        "description": params.get("description", "").strip()
    }
    return client.make_request("POST", url, headers=headers, data=data, operation_name="create_allowlist")


def get_allowlist_items(config, params):
    """Retrieve all items in a specific allowlist"""
    client = CrowdSecClient(config)
    allowlist_id = params.get("allowlist_id", "").strip()
    if not allowlist_id:
        raise ConnectorError("Allowlist ID is required")

    url = f"{client.service_base_url}/allowlists/{allowlist_id}/items"
    headers = {"x-api-key": client.service_api_key, "Accept": "application/json"}
    return client.make_request("GET", url, headers=headers, operation_name="get_allowlist_items")


def add_items_to_allowlist(config, params):
    """Add IP addresses to a specific allowlist"""
    client = CrowdSecClient(config)
    allowlist_id = params.get("allowlist_id", "").strip()
    if not allowlist_id:
        raise ConnectorError("Allowlist ID is required")

    items_input = params.get("items", "").strip()
    if not items_input:
        raise ConnectorError("Items parameter is required")

    # Process items (support comma-separated or newline-separated)
    items = []
    for item in re.split(r'[,\n\r]+', items_input):
        item = item.strip()
        if item:
            if not client._validate_ip_address(item):
                raise ConnectorError(f"Invalid IP address format: {item}")
            items.append(item)
    if not items:
        raise ConnectorError("No valid IP addresses found in items parameter")

    url = f"{client.service_base_url}/allowlists/{allowlist_id}/items"
    headers = {"x-api-key": client.service_api_key, "Accept": "application/json"}
    data = {
        "items": items,
        "description": params.get("description", "").strip(),
        "expiration": params.get("expiration")
    }
    data = {k: v for k, v in data.items() if v is not None and v != ""}

    response = client.make_request("POST", url, headers=headers, data=data, operation_name="add_items_to_allowlist")

    # Handle empty or unexpected responses
    if not response:
        return {"status": "success", "message": f"Successfully added {len(items)} IP(s) to allowlist {allowlist_id}"}

    return response


def get_specific_allowlist_item(config, params):
    """Get an allowlist item by ID"""
    client = CrowdSecClient(config)

    allowlist_id = params.get("allowlist_id", "").strip()
    if not allowlist_id:
        raise ConnectorError("Allowlist ID is required")

    item_id = params.get("item_id", "").strip()
    if not item_id:
        raise ConnectorError("Item ID is required")

    url = f"{client.service_base_url}/allowlists/{allowlist_id}/items/{item_id}"
    headers = {"x-api-key": client.service_api_key, "Accept": "application/json"}

    return client.make_request("GET", url, headers=headers, operation_name="get_specific_allowlist_item")


def update_allowlist(config, params):
    """Update an existing allowlist by ID"""
    client = CrowdSecClient(config)

    allowlist_id = params.get("allowlist_id", "").strip()
    if not allowlist_id:
        raise ConnectorError("Allowlist ID is required")

    # Prepare data
    data = {}
    if params.get("name", "").strip():
        data["name"] = params["name"].strip()
    if params.get("description", "").strip():
        data["description"] = params["description"].strip()

    if not data:
        raise ConnectorError("At least one of 'name' or 'description' must be provided to update the allowlist")

    url = f"{client.service_base_url}/allowlists/{allowlist_id}"
    headers = {"x-api-key": client.service_api_key, "Accept": "application/json"}

    return client.make_request("PATCH", url, headers=headers, data=data, operation_name="update_allowlist")


def delete_allowlist_item(config, params):
    """Delete a specific item from an allowlist"""
    client = CrowdSecClient(config)
    allowlist_id = params.get("allowlist_id", "").strip()
    item_id = params.get("item_id", "").strip()

    if not allowlist_id:
        raise ConnectorError("Allowlist ID is required")
    if not item_id:
        raise ConnectorError("Item ID is required")

    url = f"{client.service_base_url}/allowlists/{allowlist_id}/items/{item_id}"
    headers = {"x-api-key": client.service_api_key, "Accept": "application/json"}
    return client.make_request("DELETE", url, headers=headers, operation_name="delete_allowlist_item")


def delete_allowlist(config, params):
    """Delete an allowlist by ID"""
    client = CrowdSecClient(config)

    allowlist_id = params.get("allowlist_id", "").strip()
    if not allowlist_id:
        raise ConnectorError("Allowlist ID is required")

    # Default force = false
    force = params.get("force", False)
    if isinstance(force, str):
        force = force.lower() in ["true", "1", "yes"]

    url = f"{client.service_base_url}/allowlists/{allowlist_id}"
    headers = {"x-api-key": client.service_api_key, "Accept": "application/json"}
    query_params = {"force": str(force).lower()}

    return client.make_request("DELETE", url, headers=headers, params=query_params, operation_name="delete_allowlist")


def list_integrations(config, params):
    """Retrieve a list of all integrations"""
    client = CrowdSecClient(config)
    url = f"{client.service_base_url}/integrations"
    headers = {"x-api-key": client.service_api_key, "Accept": "application/json"}
    return client.make_request("GET", url, headers=headers, operation_name="list_integrations")


def create_integration(config, params):
    """Create an integration to a firewall or remediation component"""
    client = CrowdSecClient(config)

    name = params.get("name", "").strip()
    if not name:
        raise ConnectorError("Integration name is required")

    description = params.get("description", "").strip()
    entity_type = params.get("entity_type", "").strip()
    output_format = params.get("output_format", "").strip()

    if not entity_type:
        raise ConnectorError("Entity type is required")
    if not output_format:
        raise ConnectorError("Output format is required")

    url = f"{client.service_base_url}/integrations"
    headers = {"x-api-key": client.service_api_key, "Accept": "application/json", "Content-Type": "application/json"}

    data = {
        "name": name,
        "description": description,
        "entity_type": entity_type,
        "output_format": output_format
    }

    return client.make_request("POST", url, headers=headers, data=data, operation_name="create_integration")


def get_integration(config, params):
    """Get an integration by ID"""
    client = CrowdSecClient(config)
    integration_id = params.get("integration_id", "").strip()
    if not integration_id:
        raise ConnectorError("Integration ID is required")

    url = f"{client.service_base_url}/integrations/{integration_id}"
    headers = {"x-api-key": client.service_api_key, "Accept": "application/json"}
    return client.make_request("GET", url, headers=headers, operation_name="get_integration")


def update_integration(config, params):
    """Update the integration details"""
    client = CrowdSecClient(config)
    integration_id = params.get("integration_id", "").strip()
    if not integration_id:
        raise ConnectorError("Integration ID is required")

    # Prepare data - all fields are optional for update
    data = {}
    if params.get("name", "").strip():
        data["name"] = params["name"].strip()
    if params.get("description", "").strip():
        data["description"] = params["description"].strip()
    if params.get("output_format", "").strip():
        data["output_format"] = params["output_format"].strip()

    # Handle regenerate_credentials as boolean
    regenerate_credentials = params.get("regenerate_credentials", False)
    if isinstance(regenerate_credentials, str):
        regenerate_credentials = regenerate_credentials.lower() in ["true", "1", "yes"]
    if regenerate_credentials:
        data["regenerate_credentials"] = True

    if not data:
        raise ConnectorError("At least one field must be provided to update the integration")

    url = f"{client.service_base_url}/integrations/{integration_id}"
    headers = {"x-api-key": client.service_api_key, "Accept": "application/json", "Content-Type": "application/json"}
    return client.make_request("PATCH", url, headers=headers, data=data, operation_name="update_integration")


def delete_integration(config, params):
    """Delete the integration by ID"""
    client = CrowdSecClient(config)
    integration_id = params.get("integration_id", "").strip()
    if not integration_id:
        raise ConnectorError("Integration ID is required")

    url = f"{client.service_base_url}/integrations/{integration_id}"
    headers = {"x-api-key": client.service_api_key, "Accept": "application/json"}
    return client.make_request("DELETE", url, headers=headers, operation_name="delete_integration")


# Operations dictionary mapping operation names to functions
operations = {
    "get_ip_reputation": get_ip_reputation,
    "search_ip_reputation": search_ip_reputation,
    "batch_get_ip_reputation": batch_get_ip_reputation,
    "get_malevolent_ips": get_malevolent_ips,
    "list_blocklists": list_blocklists,
    "create_blocklist": create_blocklist,
    "update_blocklist": update_blocklist,
    "add_ips_to_blocklist": add_ips_to_blocklist,
    "get_blocklist_ips": get_blocklist_ips,
    "delete_ips_from_blocklist": delete_ips_from_blocklist,
    "bulk_overwrite_blocklist_ips": bulk_overwrite_blocklist_ips,
    "get_blocklist": get_blocklist,
    "delete_blocklist": delete_blocklist,
    "list_allowlists": list_allowlists,
    "create_allowlist": create_allowlist,
    "get_allowlist_items": get_allowlist_items,
    "add_items_to_allowlist": add_items_to_allowlist,
    "get_specific_allowlist_item": get_specific_allowlist_item,
    "update_allowlist": update_allowlist,
    "delete_allowlist_item": delete_allowlist_item,
    'delete_allowlist': delete_allowlist,
    "list_integrations": list_integrations,
    "create_integration": create_integration,
    "get_integration": get_integration,
    "update_integration": update_integration,
    "delete_integration": delete_integration
}
