## About the connector

CrowdSec Cyber Threat Intelligence & Service APIs provide a unified, real-time threat intelligence and automation
platform that enables organizations to detect, enrich, and respond to cyber threats at scale.
<p>This document provides information about the CrowdSec Cyber Threat Intelligence Connector, which facilitates automated interactions, with a CrowdSec Cyber Threat Intelligence server using FortiSOAR&trade; playbooks. Add the CrowdSec Cyber Threat Intelligence Connector as a step in FortiSOAR&trade; playbooks and perform automated operations with CrowdSec Cyber Threat Intelligence.</p>

### Version information

Connector Version: 1.0.0

Authored By: SpryIQ.co

Contributor: amey-spryiq

Certified: No

## Installing the connector

Use the **Connector Store** to install the connector. For the detailed procedure to install a connector, click <a href="https://docs.fortinet.com/document/fortisoar/0.0.0/installing-a-connector/1/installing-a-connector" target="_top">here</a>.

You can also use the following `yum` command to install connectors from an SSH session:

```
sudo yum install cyops-connector-crowdsec-cyber-threat-intelligence
```

## Prerequisites to configuring the connector

- You must have the URL of CrowdSec Cyber Threat Intelligence server to which you will connect and perform automated
operations and credentials to access that server.
- The FortiSOAR&trade; server should have outbound connectivity to port 443 on the CrowdSec Cyber Threat Intelligence
server.

## Minimum Permissions Required

- N/A

## Configuring the connector

For the procedure to configure a connector,
click [here](https://docs.fortinet.com/document/fortisoar/0.0.0/configuring-a-connector/1/configuring-a-connector)

### Configuration parameters

In FortiSOAR&trade;, on the Connectors page, click the **CrowdSec Cyber Threat Intelligence** connector row (if you are in the **Grid** view on the Connectors page) and in the **Configurations&nbsp;** tab enter the required configuration details:

| Parameter            | Description                                                                                                                                                     |
|:---------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CTI Base URL         | Specify the base endpoint for the CrowdSec Cyber Threat Intelligence (CTI) API. All CTI requests (IP reputation, enrichment, behaviors) are sent to this URL.   |
| CTI API Key          | Specify the API key used to authenticate requests to the CrowdSec CTI API. This key identifies your organization and grants access to threat intelligence data. |
| Service API Base URL | Specify the base endpoint for the CrowdSec Service (Admin) API. Used for managing services such as blocklists, decisions, or organization-level operations.     |
| Service API Key      | Specify the API key used to authenticate requests to the CrowdSec Service (Admin) API. Grants permission to manage resources such as blocklists and decisions.  |
| Verify SSL           | Specifies whether the SSL certificate for the server is to be verified or not. <br />By default, this option is set as True.                                    |

## Actions supported by the connector

The following automated operations can be included in playbooks and you can also use the annotations to access operations:

| Function                     | Description                                                                                                                                                  | Annotation and Category                         |
|------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------|
| Get IP Reputation            | Retrieves detailed threat intelligence, reputation scoring, and behavioral context for a given IP address using the CrowdSec CTI API.                        | get_ip_reputation <br />Investigation           |
| Search IP Reputation         | Searches CrowdSec Cyber Threat Intelligence for IP addresses matching a Lucene query, with optional time filtering and pagination.                           | search_ip_reputation <br />Investigation        |
| Batch Get IP Reputation      | Retrieves threat intelligence and reputation data for multiple IP addresses in a single request using the CrowdSec CTI API.                                  | batch_get_ip_reputation <br />Investigation     |
| Get Fire IPs                 | Retrieves a paginated list of malevolent IP addresses from the CrowdSec CTI API, with optional filtering based on last modification time.                    | get_malevolent_ips <br />Investigation          |
| List All Blocklists          | Retrieves all blocklists configured in the CrowdSec Service (Admin) API for the authenticated organization.                                                  | list_blocklists <br />Investigation             |
| Create New Blocklist         | Creates a new custom blocklist in the CrowdSec Service (Admin) API for organizing and enforcing threat containment policies.                                 | create_blocklist <br />Containment              |
| Update Blocklist             | Updates the metadata and CTI-driven configuration of an existing blocklist in the CrowdSec Service (Admin) API.                                              | update_blocklist <br />Containment              |
| Add IPs to Blocklist         | Adds one or more IP addresses to a specific blocklist in the CrowdSec Service API. If an IP already exists in the blocklist, the expiration date is updated. | add_ips_to_blocklist <br />Containment          |
| Get Blocklist IPs            | Retrieves all IP addresses currently listed in a specific blocklist from the CrowdSec Service API.                                                           | get_blocklist_ips <br />Investigation           |
| Delete IPs from Blocklist    | Removes one or more IP addresses from a specific blocklist in the CrowdSec Service API.                                                                      | delete_ips_from_blocklist <br />Containment     |
| Bulk Overwrite Blocklist IPs | Replaces all existing IP addresses in a specific blocklist with a new set of IPs. Existing entries will be fully overwritten.                                | bulk_overwrite_blocklist_ips <br />Containment  |
| Get Specific Blocklist       | Retrieves detailed information about a specific blocklist in the CrowdSec Service API by its ID.                                                             | get_blocklist <br />Investigation               |
| Delete Blocklist             | Permanently deletes a specific blocklist in the CrowdSec Service API by its ID. All IPs and metadata in the blocklist will be removed.                       | delete_blocklist <br />Containment              |
| List All Allowlists          | Retrieves a list of all allowlists configured in the CrowdSec Service API.                                                                                   | list_allowlists <br />Investigation             |
| Create New Allowlist         | Creates a new custom allowlist in the CrowdSec Service API to define IPs that should be explicitly allowed or excluded from automatic blocking.              | create_allowlist <br />Remediation              |
| Get Items in Allowlist       | Retrieves all IP addresses or entries contained in a specific allowlist from the CrowdSec Service API.                                                       | get_allowlist_items <br />Investigation         |
| Add IPs to Allowlist         | Adds one or more IP addresses to a specific allowlist in the CrowdSec Service API.                                                                           | add_items_to_allowlist <br />Remediation        |
| Get Specific Allowlist Item  | Retrieves detailed information about a specific allowlist item by its ID from the CrowdSec Service API.                                                      | get_specific_allowlist_item <br />Investigation |
| Update Allowlist             | Modifies the name or description of an existing allowlist in the CrowdSec Service API.                                                                       | update_allowlist <br />Remediation              |
| Delete Item from Allowlist   | Removes a specific item from an existing allowlist in the CrowdSec Service API.                                                                              | delete_allowlist_item <br />Remediation         |
| Delete Allowlist             | Permanently deletes a specific allowlist in the CrowdSec Service API by its ID.                                                                              | delete_allowlist <br />Remediation              |
| List Integrations            | Retrieves a list of all integrations available in the CrowdSec Service API.                                                                                  | list_integrations <br />Investigation           |
| Create Integration           | Creates a new integration with a firewall or remediation system, managed by your organization.                                                               | create_integration <br />Remediation            |
| Get Integration              | Retrieves the details of a specific integration by its ID, including associated blocklists and configuration.                                                | get_integration <br />Investigation             |
| Update Integration           | Updates the details of an existing integration, including name, description, output format, and credentials.                                                 | update_integration <br />Remediation            |
| Delete Integration           | Permanently deletes an existing integration by its unique ID from the CrowdSec Service API.                                                                  | delete_integration <br />Remediation            |

### operation: Get IP Reputation

#### Input parameters

| Parameter  | Description                                                                                             |
|------------|---------------------------------------------------------------------------------------------------------|
| IP Address | Specify the IPv4 or IPv6 address to investigate for malicious activity, reputation, and threat context. |

#### Output

The output contains the following populated JSON schema:

```
{
  "ip": "",
  "reputation": "",
  "ip_range": "",
  "background_noise": "",
  "confidence": "",
  "background_noise_score": "",
  "ip_range_score": "",
  "as_name": "",
  "as_num": "",
  "ip_range_24": "",
  "ip_range_24_reputation": "",
  "ip_range_24_score": "",
  "location": {
    "country": "",
    "city": "",
    "latitude": "",
    "longitude": ""
  },
  "reverse_dns": "",
  "behaviors": [],
  "history": {
    "first_seen": "",
    "last_seen": "",
    "full_age": "",
    "days_age": ""
  },
  "classifications": {
    "false_positives": [],
    "classifications": []
  },
  "attack_details": [],
  "target_countries": {},
  "mitre_techniques": [],
  "cves": [],
  "scores": {
    "overall": {
      "aggressiveness": "",
      "threat": "",
      "trust": "",
      "anomaly": "",
      "total": ""
    },
    "last_day": {
      "aggressiveness": "",
      "threat": "",
      "trust": "",
      "anomaly": "",
      "total": ""
    },
    "last_week": {
      "aggressiveness": "",
      "threat": "",
      "trust": "",
      "anomaly": "",
      "total": ""
    },
    "last_month": {
      "aggressiveness": "",
      "threat": "",
      "trust": "",
      "anomaly": "",
      "total": ""
    }
  },
  "references": []
}
```

### operation: Search IP Reputation

#### Input parameters

| Parameter | Description                                                                                                        |
|-----------|--------------------------------------------------------------------------------------------------------------------|
| Query     | Lucene query used to filter IPs based on CrowdSec CTI fields such as behaviors, classifications, ASN, or location. |
| Since     | Restrict results to IPs observed within a given time window.                                                       |
| Page      | Page number used for paginated results.                                                                            |
| Limit     | Maximum number of IP results returned per page.                                                                    |

#### Output

The output contains the following populated JSON schema:

```
{
  "total": "",
  "not_found": "",
  "items": [
    {
      "ip": "",
      "reputation": "",
      "ip_range": "",
      "ip_range_score": "",
      "ip_range_24": "",
      "ip_range_24_reputation": "",
      "ip_range_24_score": "",
      "as_name": "",
      "as_num": "",
      "background_noise_score": "",
      "background_noise": "",
      "confidence": "",
      "location": {
        "country": "",
        "city": "",
        "latitude": "",
        "longitude": ""
      },
      "reverse_dns": "",
      "behaviors": [],
      "references": [],
      "history": {
        "first_seen": "",
        "last_seen": "",
        "full_age": "",
        "days_age": ""
      },
      "classifications": {
        "false_positives": [],
        "classifications": []
      },
      "mitre_techniques": [],
      "cves": [],
      "attack_details": [],
      "target_countries": {},
      "scores": {
        "overall": {
          "aggressiveness": "",
          "threat": "",
          "trust": "",
          "anomaly": "",
          "total": ""
        },
        "last_day": {
          "aggressiveness": "",
          "threat": "",
          "trust": "",
          "anomaly": "",
          "total": ""
        },
        "last_week": {
          "aggressiveness": "",
          "threat": "",
          "trust": "",
          "anomaly": "",
          "total": ""
        },
        "last_month": {
          "aggressiveness": "",
          "threat": "",
          "trust": "",
          "anomaly": "",
          "total": ""
        }
      }
    }
  ]
}
```

### operation: Batch Get IP Reputation

#### Input parameters

| Parameter    | Description                                                      |
|--------------|------------------------------------------------------------------|
| IP Addresses | Specify the list of IPv4 and/or IPv6 addresses to query in bulk. |

#### Output

The output contains the following populated JSON schema:

```
{
  "total": "",
  "not_found": "",
  "items": [
    {
      "ip": "",
      "reputation": "",
      "ip_range": "",
      "ip_range_score": "",
      "ip_range_24": "",
      "ip_range_24_reputation": "",
      "ip_range_24_score": "",
      "as_name": "",
      "as_num": "",
      "background_noise_score": "",
      "background_noise": "",
      "confidence": "",
      "location": {
        "country": "",
        "city": "",
        "latitude": "",
        "longitude": ""
      },
      "reverse_dns": "",
      "behaviors": [],
      "references": [],
      "history": {
        "first_seen": "",
        "last_seen": "",
        "full_age": "",
        "days_age": ""
      },
      "classifications": {
        "false_positives": [],
        "classifications": []
      },
      "mitre_techniques": [],
      "cves": [],
      "attack_details": [],
      "target_countries": {},
      "scores": {
        "overall": {
          "aggressiveness": "",
          "threat": "",
          "trust": "",
          "anomaly": "",
          "total": ""
        },
        "last_day": {
          "aggressiveness": "",
          "threat": "",
          "trust": "",
          "anomaly": "",
          "total": ""
        },
        "last_week": {
          "aggressiveness": "",
          "threat": "",
          "trust": "",
          "anomaly": "",
          "total": ""
        },
        "last_month": {
          "aggressiveness": "",
          "threat": "",
          "trust": "",
          "anomaly": "",
          "total": ""
        }
      }
    }
  ]
}
```

### operation: Get Fire IPs

#### Input parameters

| Parameter | Description                                                                |
|-----------|----------------------------------------------------------------------------|
| Page      | Page number used to paginate through the list of malevolent IPs.           |
| Limit     | Maximum number of malevolent IP records returned per page.                 |
| Since     | Filter results to include only IPs updated within a specified time window. |

#### Output

The output contains the following populated JSON schema:

```
{
  "_links": {
    "self": "",
    "prev": "",
    "next": "",
    "first": ""
  },
  "items": [
    {
      "ip": "",
      "reputation": "",
      "ip_range": "",
      "ip_range_score": "",
      "ip_range_24": "",
      "ip_range_24_reputation": "",
      "ip_range_24_score": "",
      "as_name": "",
      "as_num": "",
      "background_noise_score": "",
      "background_noise": "",
      "confidence": "",
      "location": {
        "country": "",
        "city": "",
        "latitude": "",
        "longitude": ""
      },
      "reverse_dns": "",
      "behaviors": [],
      "references": [],
      "history": {
        "first_seen": "",
        "last_seen": "",
        "full_age": "",
        "days_age": ""
      },
      "classifications": {
        "false_positives": [],
        "classifications": []
      },
      "mitre_techniques": [],
      "cves": [],
      "attack_details": [],
      "target_countries": {},
      "scores": {
        "overall": {
          "aggressiveness": "",
          "threat": "",
          "trust": "",
          "anomaly": "",
          "total": ""
        },
        "last_day": {
          "aggressiveness": "",
          "threat": "",
          "trust": "",
          "anomaly": "",
          "total": ""
        },
        "last_week": {
          "aggressiveness": "",
          "threat": "",
          "trust": "",
          "anomaly": "",
          "total": ""
        },
        "last_month": {
          "aggressiveness": "",
          "threat": "",
          "trust": "",
          "anomaly": "",
          "total": ""
        }
      },
      "state": "",
      "expiration": ""
    }
  ]
}
```

### operation: List All Blocklists

#### Input parameters

None.

#### Output

The output contains the following populated JSON schema:

```
{
  "items": [],
  "total": "",
  "page": "",
  "size": "",
  "pages": "",
  "links": {}
}
```

### operation: Create New Blocklist

#### Input parameters

| Parameter      | Description                                                                  |
|----------------|------------------------------------------------------------------------------|
| Blocklist Name | Unique name used to identify the blocklist within the CrowdSec organization. |
| Description    | Optional explanation of the blocklist's purpose and usage.                   |

#### Output

The output contains the following populated JSON schema:

```
{
  "id": "",
  "created_at": "",
  "updated_at": "",
  "name": "",
  "label": "",
  "description": "",
  "references": [],
  "is_private": "",
  "tags": [],
  "pricing_tier": "",
  "source": "",
  "stats": {},
  "shared_with": [],
  "organization_id": "",
  "subscribers": [],
  "categories": []
}
```

### operation: Update Blocklist

#### Input parameters

| Parameter    | Description                                                                      |
|--------------|----------------------------------------------------------------------------------|
| Blocklist ID | Unique identifier of the blocklist that will be updated.                         |
| Label        | Display label shown for the blocklist in the CrowdSec console and APIs.          |
| Description  | Detailed explanation of the blocklist's intent, scope, and usage.                |
| References   | Supporting references associated with the blocklist.                             |
| Tags         | Tags used to classify and organize the blocklist.                                |
| CTI Query    | Lucene query used to select IPs from CrowdSec CTI when populating the blocklist. |
| Since Period | Relative time window applied to the CTI query to filter IPs by recency.          |

#### Output

The output contains the following populated JSON schema:

```
{
  "id": "",
  "created_at": "",
  "updated_at": "",
  "name": "",
  "label": "",
  "description": "",
  "references": [],
  "is_private": "",
  "tags": [],
  "pricing_tier": "",
  "source": "",
  "stats": {},
  "from_cti_query": "",
  "since": "",
  "shared_with": [],
  "organization_id": "",
  "subscribers": [],
  "categories": []
}
```

### operation: Add IPs to Blocklist

#### Input parameters

| Parameter       | Description                                                                                    |
|-----------------|------------------------------------------------------------------------------------------------|
| Blocklist ID    | Unique identifier of the blocklist to which IPs will be added.                                 |
| IP Addresses    | IP addresses to add to the blocklist.                                                          |
| Expiration Date | Date and time when the IP entry should expire and be automatically removed from the blocklist. |

#### Output

The output contains the following populated JSON schema:

```
{
  "status": "",
  "message": ""
}
```

### operation: Get Blocklist IPs

#### Input parameters

| Parameter    | Description                                                          |
|--------------|----------------------------------------------------------------------|
| Blocklist ID | Unique identifier of the blocklist from which to fetch IP addresses. |

#### Output

The output contains the following populated JSON schema:

```
{
  "blocklist_id": "",
  "ips": []
}
```

### operation: Delete IPs from Blocklist

#### Input parameters

| Parameter    | Description                                                            |
|--------------|------------------------------------------------------------------------|
| Blocklist ID | Unique identifier of the blocklist from which the IPs will be removed. |
| IP Addresses | IP addresses to be removed from the blocklist.                         |

#### Output

The output contains the following populated JSON schema:

```
{
  "status": "",
  "message": ""
}
```

### operation: Bulk Overwrite Blocklist IPs

#### Input parameters

| Parameter       | Description                                                                                          |
|-----------------|------------------------------------------------------------------------------------------------------|
| Blocklist ID    | Unique identifier of the blocklist to be overwritten.                                                |
| IP Addresses    | New IP addresses that will replace all existing entries in the blocklist.                            |
| Expiration Date | Date and time when the new IP entries should expire and be automatically removed from the blocklist. |

#### Output

The output contains the following populated JSON schema:

```
{
  "status": "",
  "message": "",
  "accepted": ""
}
```

### operation: Get Specific Blocklist

#### Input parameters

| Parameter    | Description                                     |
|--------------|-------------------------------------------------|
| Blocklist ID | Unique identifier of the blocklist to retrieve. |

#### Output

The output contains the following populated JSON schema:

```
{
  "id": "",
  "created_at": "",
  "updated_at": "",
  "name": "",
  "label": "",
  "description": "",
  "references": [],
  "is_private": "",
  "tags": [],
  "pricing_tier": "",
  "source": "",
  "stats": {},
  "shared_with": [],
  "subscribers": [],
  "categories": []
}
```

### operation: Delete Blocklist

#### Input parameters

| Parameter    | Description                                                   |
|--------------|---------------------------------------------------------------|
| Blocklist ID | Specify the unique identifier of the blocklist to be deleted. |

#### Output

The output contains the following populated JSON schema:

```
{
  "status": "",
  "message": ""
}
```

### operation: List All Allowlists

#### Input parameters

None.

#### Output

The output contains the following populated JSON schema:

```
{
  "items": [],
  "total": "",
  "page": "",
  "size": "",
  "pages": "",
  "links": {}
}
```

### operation: Create New Allowlist

#### Input parameters

| Parameter      | Description                                                    |
|----------------|----------------------------------------------------------------|
| Allowlist Name | Specify the unique name to identify this allowlist.            |
| Description    | Optional description explaining the purpose of this allowlist. |

#### Output

The output contains the following populated JSON schema:

```
{
  "id": "",
  "organization_id": "",
  "name": "",
  "description": "",
  "created_at": "",
  "total_items": ""
}
```

### operation: Get Items in Allowlist

#### Input parameters

| Parameter    | Description                                                                      |
|--------------|----------------------------------------------------------------------------------|
| Allowlist ID | Specify the unique identifier of the allowlist whose items you want to retrieve. |

#### Output

The output contains the following populated JSON schema:

```
{
  "items": [],
  "total": "",
  "page": "",
  "size": "",
  "pages": "",
  "links": {}
}
```

### operation: Add IPs to Allowlist

#### Input parameters

| Parameter       | Description                                                                |
|-----------------|----------------------------------------------------------------------------|
| Allowlist ID    | Specify the unique identifier of the allowlist to which IPs will be added. |
| IP Addresses    | Specify the IP addresses to add to the allowlist.                          |
| Description     | Optional description for the added IPs.                                    |
| Expiration Date | Optional expiration date for these allowlist items.                        |

#### Output

The output contains the following populated JSON schema:

```
{
  "status": "",
  "message": ""
}
```

### operation: Get Specific Allowlist Item

#### Input parameters

| Parameter    | Description                                                         |
|--------------|---------------------------------------------------------------------|
| Allowlist ID | Specify the Unique identifier of the allowlist containing the item. |
| Item ID      | Specify the ID of the allowlist item you want to fetch.             |

#### Output

The output contains the following populated JSON schema:

```
{
  "id": "",
  "allowlist_id": "",
  "description": "",
  "scope": "",
  "value": "",
  "created_at": "",
  "updated_at": "",
  "created_by": {
    "source_type": "",
    "identifier": ""
  },
  "updated_by": {
    "source_type": "",
    "identifier": ""
  },
  "expiration": ""
}
```

### operation: Update Allowlist

#### Input parameters

| Parameter    | Description                                              |
|--------------|----------------------------------------------------------|
| Allowlist ID | Specif the Unique identifier of the allowlist to update. |
| Name         | Specify the new name for the allowlist.                  |
| Description  | Specify the new description for the allowlist            |

#### Output

The output contains the following populated JSON schema:

```
{
  "id": "",
  "organization_id": "",
  "name": "",
  "description": "",
  "created_at": "",
  "updated_at": "",
  "from_cti_query": "",
  "since": "",
  "total_items": ",
  "subscribers": []
}
```

### operation: Delete Item from Allowlist

#### Input parameters

| Parameter    | Description                                                                   |
|--------------|-------------------------------------------------------------------------------|
| Allowlist ID | Specify the Unique identifier of the allowlist containing the item to delete. |
| Item ID      | Specify the Unique identifier of the item to remove from the allowlist.       |

#### Output

The output contains the following populated JSON schema:

```
{
  "status": "",
  "message": ""
}
```

### operation: Delete Allowlist

#### Input parameters

| Parameter    | Description                                                        |
|--------------|--------------------------------------------------------------------|
| Allowlist ID | Specify the Unique identifier of the allowlist you want to delete. |
| Force Delete | Whether to force deletion even if the allowlist has subscribers.   |

#### Output

The output contains the following populated JSON schema:

```
{
  "status": "",
  "message": ""
}
```

### operation: List Integrations

#### Input parameters

None.

#### Output

The output contains the following populated JSON schema:

```
{
  "items": [],
  "total": "",
  "page": "",
  "size": "",
  "pages": "",
  "links": {}
}
```

### operation: Create Integration

#### Input parameters

| Parameter     | Description                                                          |
|---------------|----------------------------------------------------------------------|
| Name          | Specify a unique name for this integration within your organization. |
| Description   | Provide a description explaining the purpose of this integration.    |
| Entity Type   | Specify the type of integration (default: firewall\_integration)     |
| Output Format | Choose the output format for the integration (default: plain\_text)  |

#### Output

The output contains the following populated JSON schema:

```
{
  "id": "",
  "name": "",
  "organization_id": "",
  "description": "",
  "created_at": "",
  "updated_at": "",
  "entity_type": "",
  "output_format": "",
  "last_pull": "",
  "blocklists": [
    {
      "id": "",
      "remediation": "",
      "name": "",
      "label": ""
    }
  ],
  "endpoint": "",
  "stats": {
    "count": ""
  },
  "tags": [],
  "credentials": {
    "api_key": ""
  }
}
```

### operation: Get Integration

#### Input parameters

| Parameter      | Description                                                   |
|----------------|---------------------------------------------------------------|
| Integration ID | Specify the unique ID of the integration you want to retrieve |

#### Output

The output contains the following populated JSON schema:

```
{
  "id": "",
  "name": "",
  "organization_id": "",
  "description": "",
  "created_at": "",
  "updated_at": "",
  "entity_type": "",
  "output_format": "",
  "last_pull": "",
  "blocklists": [
    {
      "id": "",
      "remediation": "",
      "name": "",
      "label": ""
    }
  ],
  "endpoint": "",
  "stats": {
    "count": ""
  },
  "tags": []
}
```

### operation: Update Integration

#### Input parameters

| Parameter              | Description                                                       |
|------------------------|-------------------------------------------------------------------|
| Integration ID         | Specify the unique ID of the integration you want to update       |
| Name                   | New name for the integration                                      |
| Description            | New description for the integration                               |
| Output Format          | Updated output format for the integration (e.g., plain\_text)     |
| Regenerate Credentials | Set to 'true' to regenerate API credentials for this integration. |

#### Output

The output contains the following populated JSON schema:

```
{
  "id": "",
  "name": "",
  "organization_id": "",
  "description": "",
  "created_at": "",
  "updated_at": "",
  "entity_type": "",
  "output_format": "",
  "last_pull": "",
  "blocklists": [
    {
      "id": "",
      "remediation": "",
      "name": "",
      "label": ""
    }
  ],
  "endpoint": "",
  "stats": {
    "count": ""
  },
  "tags": [],
  "credentials": {
    "api_key": ""
  }
}
```

### operation: Delete Integration

#### Input parameters

| Parameter      | Description                                                 |
|----------------|-------------------------------------------------------------|
| Integration ID | Specify the unique ID of the integration you want to delete |

#### Output

The output contains the following populated JSON schema:

```
{
  "status": "",
  "message": ""
}
```

## Included playbooks

The *`Sample - CrowdSec Cyber Threat Intelligence - 1.0.0`* playbook collection comes bundled with the CrowdSec Cyber
Threat Intelligence connector. These playbooks contain steps using which you can perform all supported actions. You can
see bundled playbooks in the **Automation** > **Playbooks** section in FortiSOAR&trade; after importing the CrowdSec
Cyber Threat Intelligence connector.

- Add IPs to Allowlist
- Add IPs to Blocklist
- Batch Get IP Reputation
- Bulk Overwrite Blocklist IPs
- Create Integration
- Create New Allowlist
- Create New Blocklist
- Delete Allowlist
- Delete Blocklist
- Delete IPs from Blocklist
- Delete Integration
- Delete Item from Allowlist
- Get Blocklist IPs
- Get Fire IPs
- Get IP Reputation
- Get Integration
- Get Items in Allowlist
- Get Specific Allowlist Item
- Get Specific Blocklist
- List All Allowlists
- List All Blocklists
- List Integrations
- Search IP Reputation
- Update Allowlist
- Update Blocklist
- Update Integration

---
**Note**:

If you are planning to use any of the sample playbooks in your environment, ensure that you clone those
playbooks and move them to a different collection, since the sample playbook collection gets deleted during connector
upgrade and delete.

---