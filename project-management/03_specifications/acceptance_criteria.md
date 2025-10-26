# Acceptance Criteria
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
This document provides a comprehensive list of acceptance criteria for the "[Project Name]" project. These criteria define the specific, testable conditions that must be met for each feature and for the project as a whole to be considered complete and accepted. This document serves as the basis for all acceptance testing.

### 1.2. Scope
The scope of this document covers the acceptance criteria for all functional and non-functional requirements detailed in the `FSD.md` and `NFR.md`.

### 1.3. References
| ID | Document/Link | Description |
|----|---|---|
| 1  | `FSD.md` | The Functional Specification Document, which contains the user stories and functional requirements. |
| 2  | `NFR.md` | The Non-Functional Requirements document. |

---

## 2. Overall Project Acceptance Criteria

The project will be considered successfully completed and ready for final acceptance when all of the following high-level conditions are met:

1.  **All Functional Criteria Met:** All feature-level acceptance criteria listed in Section 3 have been tested and have passed.
2.  **All Non-Functional Criteria Met:** All non-functional requirements (performance, security, etc.) as detailed in Section 4 have been verified and have passed.
3.  **Portfolio Projects Complete:** All planned portfolio projects are fully functional, documented, and available in a public Git repository.
4.  **Certifications Achieved:** The target certifications (`SuiteFoundation`, `SuiteCloud Developer II`) have been successfully obtained.
5.  **Documentation Finalized:** All project documentation (charter, specifications, design, etc.) is complete, reviewed, and in a finalized state.

---

## 3. Functional Acceptance Criteria

This section details the acceptance criteria for each user story or functional requirement defined in the `FSD.md`.

### 3.1. Feature: Customer Data Synchronization

#### 3.1.1. User Story: F-001 - Create NetSuite Customer from New Salesforce Account
*   **Scenario 1: Successful Creation of a New Customer**
    *   **Given** a new "Account" with `Type` = "Customer - Direct" is created in Salesforce
    *   **When** the integration service runs
    *   **Then** a new "Customer" record should exist in NetSuite
    *   **And** the NetSuite Customer's `externalId` must match the Salesforce Account's `Id`
    *   **And** the NetSuite Customer's `companyName` must match the Salesforce Account's `Name`
    *   **And** a success message is logged containing both the Salesforce ID and the new NetSuite internal ID.

*   **Scenario 2: Account is Not a Customer Type**
    *   **Given** a new "Account" with `Type` = "Prospect" is created in Salesforce
    *   **When** the integration service runs
    *   **Then** no new "Customer" record should be created in NetSuite for this account
    *   **And** a log message should indicate that the record was skipped due to its type.

*   **Scenario 3: NetSuite API Fails on Creation**
    *   **Given** a new valid "Account" is created in Salesforce
    *   **And** the NetSuite API is configured to return a validation error (e.g., a required field is missing from the payload)
    *   **When** the integration service attempts to create the customer
    *   **Then** no new customer record should be created in NetSuite
    *   **And** a detailed error message must be logged, including the Salesforce ID and the error response from NetSuite.

#### 3.1.2. User Story: F-002 - Update NetSuite Customer from Salesforce Account Update
*   **Scenario 1: Successful Update of Customer Phone Number**
    *   **Given** a Salesforce "Account" is linked to a NetSuite "Customer" via `externalId`
    *   **And** the `Phone` number on the Salesforce Account is changed
    *   **When** the integration service runs
    *   **Then** the `phone` field on the corresponding NetSuite Customer record is updated to the new value
    *   **And** a success message is logged.

---

## 4. Non-Functional Acceptance Criteria

This section details the acceptance criteria for the non-functional requirements defined in the `NFR.md`.

| NFR ID  | Requirement Category | Acceptance Criteria | Test Method |
| :--- | :--- | :--- | :--- |
| PERF-01 | Performance | **GIVEN** a test data set of 1,000 new Salesforce Accounts, **WHEN** the integration runs, **THEN** the entire process must complete in under 5 minutes. | Execute a timed test run with a prepared data set. |
| SEC-01  | Security | **GIVEN** the project codebase, **WHEN** the Git repository is scanned, **THEN** no API keys, tokens, or secrets are found in any committed file. | Perform a manual code review and use a secret scanning tool. |
| REL-04  | Reliability | **GIVEN** a batch of 100 synchronized records, **WHEN** a data audit is performed, **THEN** 100% of the mapped fields must match exactly between the source and destination records. | Run a validation script or manually compare a sample set of records. |
| USE-01  | Usability | **GIVEN** the log file from a successful run, **WHEN** an administrator reviews it, **THEN** they must be able to easily identify when the job started, when it ended, and how many records were processed successfully. | Manual review of log files. |

---

## 5. Acceptance Process

1.  **Developer Testing:** The primary developer (self) will conduct tests against all criteria listed in this document in a development environment.
2.  **Peer Review (Optional):** A mentor or peer will review the test results and the final deliverables.
3.  **Demonstration:** A live demonstration of each feature will be performed, showing that it meets the acceptance criteria.
4.  **Final Sign-off:** Once all criteria are met and demonstrated, the project will be formally accepted.

---

## 6. Approval & Sign-off

The undersigned agree that the project has met all the acceptance criteria defined in this document.

| Role | Name | Signature | Date |
| :--- | :--- | :--- | :--- |
| Project Lead / Developer | [Your Name] | | |
| Reviewer / Mentor | [Reviewer Name] | | |

---

## 7. Revision History
| Version | Date | Author | Changes |
| :--- | :--- | :--- | :--- |
| 1.0 | [YYYY-MM-DD] | [Your Name] | Initial draft. |