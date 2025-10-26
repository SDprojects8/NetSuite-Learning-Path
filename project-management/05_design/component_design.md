# Component Design Specification
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
This document provides a detailed design specification for the individual software components that make up the "[Project Name]" project. It is a deep dive into the internal structure and logic of each component, building upon the high-level architecture defined in the Solution Design Document.

### 1.2. Scope
This document covers the design of all major logical components, detailing their responsibilities, public interfaces, internal workings, dependencies, and error handling strategies.

### 1.3. References
| ID | Document/Link | Description |
|----|---|---|
| 1  | `solution_design.md` | The high-level solution design and component overview. |
| 2  | `TSD.md` | The technical specification that this component design helps implement. |

---

## 2. Component Design Principles
The design of all components in this project adheres to the following principles:
*   **Single Responsibility Principle (SRP):** Each component is designed to have one, and only one, reason to change. Its responsibility is narrowly focused and well-defined.
*   **Separation of Concerns:** Components are designed to be loosely coupled. For example, the component that fetches data is separate from the component that transforms it.
*   **Dependency Inversion:** Components depend on abstractions (like interfaces or base classes), not on concrete implementations, where applicable.
*   **Configurability:** Components are designed to be configured externally, avoiding hardcoded values for environment-specific details.

---

## 3. Component Catalog
This table provides a summary of the components designed in this document.

| Component Name | Responsibility | Key Dependencies | Status |
| :--- | :--- | :--- | :--- |
| **Configuration Service** | Loads and provides access to application settings. | `.env` file | Designed |
| **Orchestration Service** | Controls the main application workflow. | All other services | Designed |
| **Source Connector** | Fetches data from the source system (e.g., Salesforce). | Configuration Service, Logger | Designed |
| **Transformation Service** | Transforms data from source to destination format. | Logger | Designed |
| **Destination Connector**| Loads data into the destination system (e.g., NetSuite). | Configuration Service, Logger | Designed |
| **State Manager** | Manages persistent state between application runs. | File System | Designed |
| **Logging Service** | Provides centralized logging. | `logging.ini` | Designed |

---

## 4. Detailed Component Specifications

### 4.1. Component: Source Connector (e.g., `SalesforcePoller.py`)

*   **Responsibility:**
    This component is solely responsible for connecting to the Salesforce API and fetching new or updated Account records based on a given timestamp.

*   **Public Interface (API):**
    ```python
    class SalesforcePoller:
        def __init__(self, config: dict):
            """Initializes the poller with API credentials and endpoints."""
            pass

        def get_new_accounts(self, last_run_timestamp: str) -> list[dict]:
            """
            Fetches all Account records created since the last run.
            Args:
                last_run_timestamp: An ISO 8601 formatted string.
            Returns:
                A list of dictionaries, where each dictionary is a Salesforce Account record.
            """
            pass
    ```

*   **Internal Logic:**
    1.  The `__init__` method will establish an authenticated session with the Salesforce API using OAuth 2.0 credentials provided by the `config` object.
    2.  The `get_new_accounts` method constructs a SOQL (Salesforce Object Query Language) query.
    3.  The query will filter for records where `CreatedDate > last_run_timestamp` and `Type = 'Customer - Direct'`.
    4.  It executes this query against the Salesforce `/query` REST API endpoint.
    5.  It includes logic to handle API pagination if the number of results exceeds the maximum for a single response.
    6.  It returns the list of records or an empty list if none are found.

*   **Dependencies:**
    *   **Configuration Service:** To get Salesforce API credentials and the endpoint URL.
    *   **Logging Service:** To log status, progress, and errors.
    *   **External:** The Salesforce REST API.

*   **Error Handling:**
    *   Will raise a `ConnectionError` for network-related issues.
    *   Will raise a `ValueError` for authentication failures (401/403 status codes).
    *   Will log a detailed error and return an empty list for API errors during the query (e.g., 400 Bad Request).

### 4.2. Component: Transformation Service (e.g., `transformer.py`)

*   **Responsibility:**
    To transform a single record from the Salesforce Account data structure to the NetSuite Customer data structure. This component is stateless and contains no I/O operations.

*   **Public Interface (API):**
    ```python
    class Transformer:
        def transform_account_to_customer(self, account_record: dict) -> dict:
            """
            Maps a Salesforce Account dictionary to a NetSuite Customer dictionary.
            Args:
                account_record: A dictionary representing a Salesforce Account.
            Returns:
                A dictionary formatted for the NetSuite REST API.
            """
            pass
    ```

*   **Internal Logic:**
    1.  The method creates a new empty dictionary for the NetSuite customer.
    2.  It applies the field mappings defined in the `data_model.md`, copying and formatting values from the input `account_record`.
    3.  It includes logic for any required transformations, such as truncating strings to fit the destination field length.
    4.  It adds any hardcoded values, such as the `subsidiary` ID.

*   **Dependencies:**
    *   **Logging Service:** To log any warnings during transformation (e.g., data truncation).

*   **Error Handling:**
    *   Will raise a `KeyError` if a required field is missing in the source `account_record`. This error should be caught by the Orchestrator.

### 4.3. Component: Destination Connector (e.g., `NetSuiteLoader.py`)
*   **Responsibility:**
    This component is responsible for taking a transformed record and loading it into NetSuite via the SuiteTalk REST API.

*   **Public Interface (API):**
    ```python
    class NetSuiteLoader:
        def __init__(self, config: dict):
            """Initializes the loader with NetSuite API credentials."""
            pass
            
        def create_customer(self, customer_record: dict) -> dict:
            """
            Creates a new Customer record in NetSuite.
            Args:
                customer_record: A dictionary formatted for the NetSuite Customer endpoint.
            Returns:
                A dictionary containing the status and ID of the new record.
            """
            pass
    ```

*   **Internal Logic:**
    1.  The `__init__` method prepares the necessary credentials for NetSuite's Token-Based Authentication (TBA).
    2.  The `create_customer` method dynamically generates the OAuth 1.0a signature for the request.
    3.  It performs a `POST` request to the `/record/v1/customer` endpoint with the `customer_record` as the JSON payload.
    4.  It checks the HTTP response status code. A `204 No Content` is considered a success.
    5.  It extracts the new record's internal ID from the `Location` response header.

*   **Dependencies:**
    *   **Configuration Service:** To get NetSuite API credentials, account ID, and endpoint URL.
    *   **Logging Service:** For logging all load attempts and their results.
    *   **External:** The NetSuite SuiteTalk REST API.

*   **Error Handling:**
    *   Will implement a retry mechanism for transient errors (e.g., 5xx status codes, network timeouts).
    *   Will raise a specific `DataValidationError` for `400 Bad Request` responses, including the error message from NetSuite in the exception.
    *   Will raise a `ValueError` for authentication failures.

---

## 5. Revision History
| Version | Date | Author | Changes |
| :--- | :--- | :--- | :--- |
| 1.0 | [YYYY-MM-DD] | [Your Name] | Initial draft of the component designs. |