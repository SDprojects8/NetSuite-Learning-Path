# Technical Specification Document (TSD)
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
This Technical Specification Document (TSD) details the internal design and implementation plan for the "[Project Name]" project. While the Functional Specification Document (FSD) describes *what* the system does from a user's perspective, this TSD describes *how* it will be built from a technical perspective. It provides a blueprint for the developer.

### 1.2. Scope
This document covers the technical architecture, component design, data structures, algorithms, and implementation details required to meet the functional requirements outlined in the FSD. It is intended to be a living document that may be updated as implementation details are refined.

### 1.3. Intended Audience
*   **Project Developer (Self):** The primary guide for building the application.
*   **Technical Reviewers/Mentors:** To provide feedback on the proposed technical approach.
*   **Potential Employers:** To demonstrate the ability to design and document a robust technical solution.

### 1.4. References
| ID | Document/Link | Description |
|----|---|---|
| 1  | `FSD.md` | The Functional Specification Document outlining what the system must do. |
| 2  | `architecture.md` | The high-level system architecture diagram and principles. |

---

## 2. System Architecture & Design

### 2.1. High-Level Architecture
The system follows a modular, service-based architecture. It is composed of three main logical components: a **Polling Service**, a **Transformation Engine**, and a **Connector Service**. The Polling Service queries the source system for new data. This data is passed to the Transformation Engine, which converts it into the format required by the destination system. Finally, the Connector Service sends the transformed data to the destination system's API.

*(A link to a diagram in `05_design/architecture.md` would be placed here).*

### 2.2. Design Principles
*   **Stateless:** The application will not store session information between runs. All necessary state (like the timestamp of the last successful run) will be persisted externally (e.g., in a state file).
*   **Modularity:** Each component (polling, transforming, connecting) will be developed as a separate module with clear interfaces, allowing for easier testing and maintenance.
*   **Idempotency:** The system should be designed so that running the same job multiple times with the same input does not result in duplicate records in the destination system. This will be achieved by using the `externalId` field.
*   **Configurability:** All environment-specific details (endpoints, credentials, schedules) will be managed via external configuration, not hardcoded.

### 2.3. Technology Stack
| Component | Technology/Library | Version | Purpose |
|---|---|---|---|
| Language | Python | 3.9+ | Core application language. |
| API Interaction | `requests`, `requests-oauthlib` | latest | For making HTTP requests to REST/SOAP APIs. |
| Data Handling | `pandas` | latest | For efficient data transformation and cleaning (if needed). |
| Configuration | `python-dotenv` | latest | For managing environment variables from a `.env` file. |
| Scheduling | OS-level cron job / `apscheduler` | latest | For running the integration on a schedule. |
| Logging | `logging` (standard library) | N/A | For structured application logging. |

---

## 3. Component Design

### 3.1. Main Application (`main.py`)
*   **Responsibility:** Orchestrates the overall integration flow.
*   **Logic:**
    1.  Loads configuration.
    2.  Initializes the logging service.
    3.  Retrieves the timestamp of the last successful run from the state file.
    4.  Instantiates and calls the `SalesforcePoller` to get new/updated data.
    5.  If data is returned, passes it to the `DataTransformer`.
    6.  Passes the transformed data to the `NetSuiteConnector`.
    7.  If the entire process is successful, updates the timestamp in the state file.

### 3.2. Salesforce Poller (`salesforce_poller.py`)
*   **Responsibility:** Fetches data from Salesforce.
*   **Class:** `SalesforcePoller`
*   **Methods:**
    *   `__init__(self, config)`: Initializes the client with OAuth credentials.
    *   `get_new_accounts(self, last_run_timestamp)`:
        *   Constructs a SOQL query to select Accounts created since `last_run_timestamp`.
        *   Performs a GET request to the Salesforce REST API.
        *   Handles API pagination if necessary.
        *   Returns a list of account dictionaries.

### 3.3. Data Transformer (`transformer.py`)
*   **Responsibility:** Maps and transforms data from the Salesforce format to the NetSuite format.
*   **Class:** `DataTransformer`
*   **Methods:**
    *   `transform_account_to_customer(self, salesforce_account)`:
        *   Takes a single Salesforce account dictionary as input.
        *   Creates a new dictionary for the NetSuite customer.
        *   Applies the field mappings defined in `FSD.md`, including any hardcoded values (e.g., `subsidiary`).
        *   Returns the NetSuite customer dictionary.

### 3.4. NetSuite Connector (`netsuite_connector.py`)
*   **Responsibility:** Sends data to the NetSuite API.
*   **Class:** `NetSuiteConnector`
*   **Methods:**
    *   `__init__(self, config)`: Initializes the client with NetSuite TBA credentials.
    *   `_generate_tba_header(self)`: Private method to generate the complex OAuth 1.0 signature required for TBA.
    *   `create_customer(self, customer_data)`:
        *   Takes a NetSuite customer dictionary as input.
        *   Performs a `POST` request to the NetSuite REST API (`/record/v1/customer`).
        *   Includes the TBA header.
        *   Checks the HTTP response code. Raises an exception for non-2xx responses.
        *   Returns the response from the NetSuite API.

---

## 4. Error Handling and Logging

### 4.1. Error Handling Strategy
*   **Transient Errors (e.g., network timeout, 5xx API errors):** The application will implement a simple retry mechanism (e.g., retry up to 3 times with exponential backoff) for API calls.
*   **Permanent Errors (e.g., 4xx API errors, data validation failures):** The error will be caught, logged in detail (including the request payload that caused it), and the application will move to the next record. The run will be marked as a partial success.
*   **Configuration Errors (e.g., missing credentials):** The application will fail fast on startup with a critical error message and will not attempt to run.

### 4.2. Logging
*   A `logging.ini` file will configure a rotating file logger.
*   **`INFO`:** High-level status messages (e.g., "Starting run", "Found 10 new accounts", "Run completed successfully").
*   **`DEBUG`:** Detailed information for troubleshooting (e.g., API request/response bodies, data transformations).
*   **`ERROR`:** All caught exceptions and error details.
*   **Log Format:** `[YYYY-MM-DD HH:MM:SS] [LEVEL] [MODULE_NAME] - [MESSAGE]`

---

## 5. Security

### 5.1. Credentials Management
All secrets (API keys, tokens, consumer secrets) will be stored in a `.env` file. This file will be loaded at runtime and will be listed in the `.gitignore` file to prevent it from being committed to version control.

### 5.2. Data Security
All API communication will occur over HTTPS, ensuring data is encrypted in transit. No sensitive data will be stored at rest by the application, other than what is temporarily held in memory during execution.

---

## 6. Deployment
The application will be packaged with a `requirements.txt` file listing all dependencies. It will be deployed to a server or environment where Python is installed. Execution will be managed by a standard cron job configured to run at the required frequency (e.g., every 5 minutes).

A `run.sh` script will be provided to encapsulate the logic for activating the virtual environment and executing the main Python script.
```bash
#!/bin/bash
source venv/bin/activate
python src/main.py
```

---

## 7. Appendix

### 7.1. Revision History
| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | [YYYY-MM-DD] | [Your Name] | Initial draft. |