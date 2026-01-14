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

<p>Use the <strong>Connector Store</strong> to install the connector. For the detailed procedure to install a connector, click <a href="https://docs.fortinet.com/document/fortisoar/0.0.0/installing-a-connector/1/installing-a-connector" target="_top">here</a>.<br>You can also use the following <code>yum</code> user to install connectors from an SSH session:</p>

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

<p>In FortiSOAR&trade;, on the Connectors page, click the <strong>CrowdSec Cyber Threat Intelligence</strong> connector row (if you are in the <strong>Grid</strong> view on the Connectors page) and in the <strong>Configurations&nbsp;</strong> tab enter the required configuration details:&nbsp;</p>
<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>CTI Base URL<br></td><td>Specify the base endpoint for the CrowdSec Cyber Threat Intelligence (CTI) API. All CTI requests (IP reputation, enrichment, behaviors) are sent to this URL.<br>
<tr><td>CTI API Key<br></td><td>Specify the API key used to authenticate requests to the CrowdSec CTI API. This key identifies your organization and grants access to threat intelligence data.<br>
<tr><td>Service API Base URL<br></td><td>Specify the base endpoint for the CrowdSec Service (Admin) API. Used for managing services such as blocklists, decisions, or organization-level operations.<br>
<tr><td>Service API Key<br></td><td>Specify the API key used to authenticate requests to the CrowdSec Service (Admin) API. Grants permission to manage resources such as blocklists and decisions.<br>
<tr><td>Verify SSL<br></td><td>Specifies whether the SSL certificate for the server is to be verified or not. <br/>By default, this option is set as True.<br></td></tr>
</tbody></table>

## Actions supported by the connector

The following automated operations can be included in playbooks and you can also use the annotations to access
operations:
<table border=1><thead><tr><th>Function<br></th><th>Description<br></th><th>Annotation and Category<br></th></tr></thead><tbody><tr><td>Get IP Reputation<br></td><td>Retrieve detailed threat intelligence, reputation scoring, and behavioral context for a given IP address using the CrowdSec CTI API.<br></td><td>get_ip_reputation <br/>Investigation<br></td></tr>
<tr><td>Search IP Reputation<br></td><td>Search CrowdSec Cyber Threat Intelligence for IP addresses matching a Lucene query, with optional time filtering and pagination.<br></td><td>search_ip_reputation <br/>Investigation<br></td></tr>
<tr><td>Batch Get IP Reputation<br></td><td>Retrieve threat intelligence and reputation data for multiple IP addresses in a single request using the CrowdSec CTI API.<br></td><td>batch_get_ip_reputation <br/>Investigation<br></td></tr>
<tr><td>Get Fire IPs<br></td><td>Retrieve a paginated list of malevolent IP addresses from the CrowdSec CTI API, with optional filtering based on last modification time.<br></td><td>get_malevolent_ips <br/>Investigation<br></td></tr>
<tr><td>List All Blocklists<br></td><td>Retrieve all blocklists configured in the CrowdSec Service (Admin) API for the authenticated organization.<br></td><td>list_blocklists <br/>Investigation<br></td></tr>
<tr><td>Create New Blocklist<br></td><td>Create a new custom blocklist in the CrowdSec Service (Admin) API for organizing and enforcing threat containment policies.<br></td><td>create_blocklist <br/>Containment<br></td></tr>
<tr><td>Update Blocklist<br></td><td>Update the metadata and CTI-driven configuration of an existing blocklist in the CrowdSec Service (Admin) API.<br></td><td>update_blocklist <br/>Containment<br></td></tr>
<tr><td>Add IPs to Blocklist<br></td><td>Add one or more IP addresses to a specific blocklist in the CrowdSec Service API. If an IP already exists in the blocklist, its expiration date will be updated.<br></td><td>add_ips_to_blocklist <br/>Containment<br></td></tr>
<tr><td>Get Blocklist IPs<br></td><td>Retrieve all IP addresses currently listed in a specific blocklist from the CrowdSec Service API.<br></td><td>get_blocklist_ips <br/>Investigation<br></td></tr>
<tr><td>Delete IPs from Blocklist<br></td><td>Remove one or more IP addresses from a specific blocklist in the CrowdSec Service API.<br></td><td>delete_ips_from_blocklist <br/>Containment<br></td></tr>
<tr><td>Bulk Overwrite Blocklist IPs<br></td><td>Replace all existing IP addresses in a specific blocklist with a new set of IPs. Existing entries will be fully overwritten.<br></td><td>bulk_overwrite_blocklist_ips <br/>Containment<br></td></tr>
<tr><td>Get Specific Blocklist<br></td><td>Retrieve detailed information about a specific blocklist in the CrowdSec Service API by its ID.<br></td><td>get_blocklist <br/>Investigation<br></td></tr>
<tr><td>Delete Blocklist<br></td><td>Permanently delete a specific blocklist in the CrowdSec Service API by its ID. All IPs and metadata in the blocklist will be removed.<br></td><td>delete_blocklist <br/>Containment<br></td></tr>
<tr><td>List All Allowlists<br></td><td>Retrieve a list of all allowlists configured in the CrowdSec Service API.<br></td><td>list_allowlists <br/>Investigation<br></td></tr>
<tr><td>Create New Allowlist<br></td><td>Create a new custom allowlist in the CrowdSec Service API to define IPs that should be explicitly allowed or excluded from automatic blocking.<br></td><td>create_allowlist <br/>Remediation<br></td></tr>
<tr><td>Get Items in Allowlist<br></td><td>Retrieve all IP addresses or entries contained in a specific allowlist from the CrowdSec Service API.<br></td><td>get_allowlist_items <br/>Investigation<br></td></tr>
<tr><td>Add IPs to Allowlist<br></td><td>Add one or more IP addresses to a specific allowlist in the CrowdSec Service API.<br></td><td>add_items_to_allowlist <br/>Remediation<br></td></tr>
<tr><td>Get Specific Allowlist Item<br></td><td>Retrieve detailed information about a specific allowlist item by its ID from the CrowdSec Service API.<br></td><td>get_specific_allowlist_item <br/>Investigation<br></td></tr>
<tr><td>Update Allowlist<br></td><td>Modify the name or description of an existing allowlist in the CrowdSec Service API.<br></td><td>update_allowlist <br/>Remediation<br></td></tr>
<tr><td>Delete Item from Allowlist<br></td><td>Remove a specific item from an existing allowlist in the CrowdSec Service API.<br></td><td>delete_allowlist_item <br/>Remediation<br></td></tr>
<tr><td>Delete Allowlist<br></td><td>Permanently delete a specific allowlist in the CrowdSec Service API by its ID.<br></td><td>delete_allowlist <br/>Remediation<br></td></tr>
<tr><td>List Integrations<br></td><td>Retrieve a list of all integrations available in the CrowdSec Service API.<br></td><td>list_integrations <br/>Investigation<br></td></tr>
<tr><td>Create Integration<br></td><td>Create a new integration with a firewall or remediation system, managed by your organization.<br></td><td>create_integration <br/>Remediation<br></td></tr>
<tr><td>Get Integration<br></td><td>Retrieve the details of a specific integration by its ID, including associated blocklists and configuration.<br></td><td>get_integration <br/>Investigation<br></td></tr>
<tr><td>Update Integration<br></td><td>Update the details of an existing integration, including name, description, output format, and credentials.<br></td><td>update_integration <br/>Remediation<br></td></tr>
<tr><td>Delete Integration<br></td><td>Permanently delete an existing integration by its unique ID from the CrowdSec Service API.<br></td><td>delete_integration <br/>Remediation<br></td></tr>
</tbody></table>

### operation: Get IP Reputation

#### Input parameters

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>IP Address<br></td><td>Specify the IPv4 or IPv6 address to investigate for malicious activity, reputation, and threat context.<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Query<br></td><td>Lucene query used to filter IPs based on CrowdSec CTI fields such as behaviors, classifications, ASN, or location.<br>
</td></tr><tr><td>Since<br></td><td>Restrict results to IPs observed within a given time window.<br>
</td></tr><tr><td>Page<br></td><td>Page number used for paginated results.<br>
</td></tr><tr><td>Limit<br></td><td>Maximum number of IP results returned per page.<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>IP Addresses<br></td><td>Specify the list of IPv4 and/or IPv6 addresses to query in bulk.<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Page<br></td><td>Page number used to paginate through the list of malevolent IPs.<br>
</td></tr><tr><td>Limit<br></td><td>Maximum number of malevolent IP records returned per page.<br>
</td></tr><tr><td>Since<br></td><td>Filter results to include only IPs updated within a specified time window.<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Blocklist Name<br></td><td>Unique name used to identify the blocklist within the CrowdSec organization.<br>
</td></tr><tr><td>Description<br></td><td>Optional explanation of the blocklist’s purpose and usage.<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Blocklist ID<br></td><td>Unique identifier of the blocklist that will be updated.<br>
</td></tr><tr><td>Label<br></td><td>Display label shown for the blocklist in the CrowdSec console and APIs.<br>
</td></tr><tr><td>Description<br></td><td>Detailed explanation of the blocklist’s intent, scope, and usage.<br>
</td></tr><tr><td>References<br></td><td>Supporting references associated with the blocklist.<br>
</td></tr><tr><td>Tags<br></td><td>Tags used to classify and organize the blocklist.<br>
</td></tr><tr><td>CTI Query<br></td><td>Lucene query used to select IPs from CrowdSec CTI when populating the blocklist.<br>
</td></tr><tr><td>Since Period<br></td><td>Relative time window applied to the CTI query to filter IPs by recency.<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Blocklist ID<br></td><td>Unique identifier of the blocklist to which IPs will be added.<br>
</td></tr><tr><td>IP Addresses<br></td><td>IP addresses to add to the blocklist.<br>
</td></tr><tr><td>Expiration Date<br></td><td>Date and time when the IP entry should expire and be automatically removed from the blocklist.<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Blocklist ID<br></td><td>Unique identifier of the blocklist from which to fetch IP addresses.<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Blocklist ID<br></td><td>Unique identifier of the blocklist from which the IPs will be removed.<br>
</td></tr><tr><td>IP Addresses<br></td><td>IP addresses to be removed from the blocklist.<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Blocklist ID<br></td><td>Unique identifier of the blocklist to be overwritten.<br>
</td></tr><tr><td>IP Addresses<br></td><td>New IP addresses that will replace all existing entries in the blocklist.<br>
</td></tr><tr><td>Expiration Date<br></td><td>Date and time when the new IP entries should expire and be automatically removed from the blocklist.<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Blocklist ID<br></td><td>Unique identifier of the blocklist to retrieve.<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Blocklist ID<br></td><td>Specify the unique identifier of the blocklist to be deleted.<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Allowlist Name<br></td><td>Specify the unique name to identify this allowlist.<br>
</td></tr><tr><td>Description<br></td><td>Optional description explaining the purpose of this allowlist.<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Allowlist ID<br></td><td>Specify the unique identifier of the allowlist whose items you want to retrieve.<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Allowlist ID<br></td><td>Specify the unique identifier of the allowlist to which IPs will be added.<br>
</td></tr><tr><td>IP Addresses<br></td><td>Specify the IP addresses to add to the allowlist.<br>
</td></tr><tr><td>Description<br></td><td>Optional description for the added IPs.<br>
</td></tr><tr><td>Expiration Date<br></td><td>Optional expiration date for these allowlist items.<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Allowlist ID<br></td><td>Specify the Unique identifier of the allowlist containing the item.<br>
</td></tr><tr><td>Item ID<br></td><td>Specify the ID of the allowlist item you want to fetch.<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Allowlist ID<br></td><td>Specif the Unique identifier of the allowlist to update.<br>
</td></tr><tr><td>Name<br></td><td>Specify the new name for the allowlist.<br>
</td></tr><tr><td>Description<br></td><td>Specify the new description for the allowlist<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Allowlist ID<br></td><td>Specify the Unique identifier of the allowlist containing the item to delete.<br>
</td></tr><tr><td>Item ID<br></td><td>Specify the Unique identifier of the item to remove from the allowlist.<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Allowlist ID<br></td><td>Specify the Unique identifier of the allowlist you want to delete.<br>
</td></tr><tr><td>Force Delete<br></td><td>Whether to force deletion even if the allowlist has subscribers.<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Name<br></td><td>Specify a unique name for this integration within your organization.<br>
</td></tr><tr><td>Description<br></td><td>Provide a description explaining the purpose of this integration.<br>
</td></tr><tr><td>Entity Type<br></td><td>Specify the type of integration (default: firewall_integration)<br>
</td></tr><tr><td>Output Format<br></td><td>Choose the output format for the integration (default: plain_text)<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Integration ID<br></td><td>Specify the unique ID of the integration you want to retrieve<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Integration ID<br></td><td>Specify the unique ID of the integration you want to update<br>
</td></tr><tr><td>Name<br></td><td>New name for the integration<br>
</td></tr><tr><td>Description<br></td><td>New description for the integration<br>
</td></tr><tr><td>Output Format<br></td><td>Updated output format for the integration (e.g., plain_text)<br>
</td></tr><tr><td>Regenerate Credentials<br></td><td>Set to 'true' to regenerate API credentials for this integration.<br>
</td></tr></tbody></table>

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

<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Integration ID<br></td><td>Specify the unique ID of the integration you want to delete<br>
</td></tr></tbody></table>

#### Output

The output contains the following populated JSON schema:

```
{
  "status": "",
  "message": ""
}
```

## Included playbooks

The `Sample - CrowdSec Cyber Threat Intelligence - 1.0.0` playbook collection comes bundled with the CrowdSec Cyber
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