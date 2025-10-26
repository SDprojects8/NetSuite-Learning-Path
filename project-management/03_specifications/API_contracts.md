# API Contract Specification
# Portfolio Project: [Project Name]

---

## Document Information
**Version:** 1.0  
**Date:** [YYYY-MM-DD]  
**Author:** [Your Name]  
**Status:** [Draft / In Review / Approved]

---

## 1. Introduction

### 1.1. Purpose
This document defines the API contracts for all external web services used or exposed by the "[Project Name]" project. A contract specifies the agreed-upon interface, including endpoints, request/response formats, and authentication methods. This ensures clear communication and stable integration between system components.

### 1.2. Scope
This specification covers the APIs for the following systems:
*   NetSuite (SuiteTalk REST API)
*   Salesforce (REST API)

This document is the source of truth for all API interactions.

---

## 2. General Information

### 2.1. Base URLs
| System | Environment | Base URL |
| :--- | :--- | :--- |
| NetSuite | Production | `https://<ACCOUNT_ID>.suitetalk.api.netsuite.com/services/rest` |
| NetSuite | Sandbox | `https://<ACCOUNT_ID>.sandbox.suitetalk.api.netsuite.com/services/rest` |
| Salesforce | Production/Dev | `https://<MY_DOMAIN>.my.salesforce.com/services/data/vXX.X` |

### 2.2. Authentication
*   **NetSuite:** All requests to the NetSuite API must be authenticated using **Token-Based Authentication (TBA)**, which follows the OAuth 1.0a specification. An `Authorization` header containing the signature must be included in every request.
*   **Salesforce:** All requests to the Salesforce API must be authenticated using **OAuth 2.0**. A valid bearer token must be included in the `Authorization` header (e.g., `Authorization: Bearer <ACCESS_TOKEN>`).

### 2.3. Common Headers
| Header | Value | System | Description |
| :--- | :--- | :--- | :--- |
| `Content-Type` | `application/json` | All | Specifies that the request/response body is in JSON format. |
| `Authorization` | (Varies) | All | Contains the authentication credentials. |

---

## 3. NetSuite SuiteTalk API Contracts

### 3.1. Create Customer Record

*   **Endpoint:** `POST /record/v1/customer`
*   **Description:** Creates a new Customer record in NetSuite.
*   **Authentication:** NetSuite TBA (OAuth 1.0a) required.

#### Request Body
The body must contain a JSON object representing the Customer record.
| Field | Type | Required? | Description |
| :--- | :--- | :--- | :--- |
| `companyName` | `string` | Yes | The name of the customer's company. |
| `subsidiary` | `object` | Yes | An object containing the internal `id` of the subsidiary. |
| `externalId` | `string` | Yes | The unique ID from the source system (e.g., Salesforce `Id`). |
| `phone` | `string` | No | The customer's primary phone number. |
| `url` | `string` | No | The customer's website URL. |

**Example Request Body:**
```json
{
    "companyName": "Test Customer Inc.",
    "subsidiary": {
        "id": "1"
    },
    "externalId": "0015j00000AbCdEf",
    "phone": "555-123-4567",
    "url": "http://www.testcustomer.com"
}
```

#### Success Response
*   **Status Code:** `204 No Content`
*   **Headers:** The `Location` header will contain the URL to the newly created resource.
    *   `Location: https://<ACCOUNT_ID>.suitetalk.api.netsuite.com/services/rest/record/v1/customer/12345`
*   **Response Body:** None.

#### Error Responses
*   **Status Code:** `400 Bad Request`
*   **Description:** The request body is malformed or violates a business rule (e.g., a required field is missing).
*   **Response Body:**
    ```json
    {
        "type": "https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.1",
        "title": "Bad Request",
        "status": 400,
        "o:errorDetails": [
            {
                "detail": "Error while accessing a resource. You must enter a value for Company Name.",
                "o:errorCode": "USER_ERROR"
            }
        ]
    }
    ```

---

## 4. Salesforce REST API Contracts

### 4.1. Query for New Accounts

*   **Endpoint:** `GET /query?q=<SOQL_QUERY>`
*   **Description:** Executes a Salesforce Object Query Language (SOQL) query to retrieve Account records.
*   **Authentication:** Salesforce OAuth 2.0 required.

#### Request Parameters
| Parameter | Type | Required? | Description |
| :--- | :--- | :--- | :--- |
| `q` | `string` | Yes | A URL-encoded SOQL query string. |

**Example SOQL Query:**
```sql
SELECT Id, Name, Phone, Website, Type FROM Account WHERE CreatedDate > 2023-10-27T10:00:00Z AND Type = 'Customer - Direct'
```
*Note: The query string must be URL encoded before being included in the endpoint URL.*

#### Success Response
*   **Status Code:** `200 OK`
*   **Response Body:** A JSON object containing the results of the query.
    ```json
    {
        "totalSize": 1,
        "done": true,
        "records": [
            {
                "attributes": {
                    "type": "Account",
                    "url": "/services/data/v58.0/sobjects/Account/0015j00000AbCdEf"
                },
                "Id": "0015j00000AbCdEf",
                "Name": "Example Corp",
                "Phone": "555-555-5555",
                "Website": "http://www.example.com",
                "Type": "Customer - Direct"
            }
        ]
    }
    ```

#### Error Responses
*   **Status Code:** `400 Bad Request`
*   **Description:** The SOQL query is malformed or invalid.
*   **Response Body:**
    ```json
    [
        {
            "message": "The SOQL is invalid.",
            "errorCode": "MALFORMED_QUERY"
        }
    ]
    ```
*   **Status Code:** `401 Unauthorized`
*   **Description:** The provided OAuth token is invalid or expired.
*   **Response Body:**
    ```json
    [
        {
            "message": "Session expired or invalid",
            "errorCode": "INVALID_SESSION_ID"
        }
    ]
    ```

---

## 5. Revision History
| Version | Date | Author | Changes |
| :--- | :--- | :--- | :--- |
| 1.0 | [YYYY-MM-DD] | [Your Name] | Initial draft of NetSuite and Salesforce API contracts. |
