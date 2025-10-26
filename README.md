# NetSuite Learning Path

This repository outlines a structured learning path to become a proficient NetSuite Technical ERP Solutions Architect. The plan is tailored to leverage existing skills in software engineering, DevOps, and enterprise architecture to accelerate the learning process.

## Project Goal

The primary objective is to acquire the necessary skills and knowledge to meet the requirements of a Technical ERP Solutions Architect role, as detailed in the [Job Description](data/external/Job_Description.txt). This involves a deep dive into the SuiteCloud platform, integration patterns, and NetSuite's development lifecycle.

---

## NetSuite Learning Roadmap (3-6 Months)

This roadmap is divided into five distinct phases, designed to build a strong foundation and progressively advance into complex architectural topics.

### Phase 1: Foundation - The Functional & Admin Layers (2-3 Weeks)

Before you can architect, you must understand the user's perspective and the platform's declarative capabilities.

*   **Topics:**
    *   **Core Business Processes:** Understand the end-to-end flows for Order-to-Cash, Procure-to-Pay, and basic accounting (GL, AP, AR).
    *   **NetSuite Navigation:** Get comfortable with the UI, dashboards, and global search.
    *   **SuiteBuilder (Low-Code):** Learn to create custom fields, forms, record types, and subtabs.
    *   **SuiteFlow (No-Code):** Build point-and-click workflows to automate business processes.
*   **Learning Resources:**
    *   Udemy/LinkedIn Learning courses on "NetSuite Essentials" or "NetSuite Administration."
    *   NetSuite's official "SuiteAnswers" portal and help documentation.
*   **Milestone:** Be able to customize records and automate a simple approval process without writing any code.
*   **Certification Goal:** `SuiteFoundation`.

### Phase 2: Core Development - Mastering SuiteScript (3-4 Weeks)

This is the most critical phase, focusing on the core programmatic customization of NetSuite.

*   **Topics:**
    *   **Modern JavaScript (ES6+):** If you're coming from another language, solidify your understanding of functions, objects, Promises, and `async/await`.
    *   **SuiteScript 2.x:** Dive deep into the NetSuite API.
        *   **Script Types:** Master User Event, Client, Scheduled, and Map/Reduce scripts.
        *   **API Modules:** Learn to work with `N/record`, `N/search`, and `N/https` modules.
*   **Learning Resources:**
    *   SuiteScript 2.0/2.1 tutorials and documentation on SuiteAnswers.
    *   Online communities (e.g., NetSuite Professionals Slack).
*   **Milestone:** Write a User Event script to validate data on a sales order before save and a Scheduled Script to process records nightly.

### Phase 3: Integration & Data Management (2-3 Weeks)

Focus on getting data in and out of NetSuite and connecting it with external systems.

*   **Topics:**
    *   **SuiteTalk (APIs):** Understand and use both SOAP and REST APIs for integrations.
    *   **Authentication:** Learn Token-Based Authentication (TBA).
    *   **API Tools:** Use Postman to test and interact with NetSuite APIs.
    *   **Data Migration:** Practice data import/export using CSV imports and API-based scripts.
*   **Learning Resources:**
    *   SuiteTalk API documentation.
    *   Postman tutorials for REST and SOAP requests.
*   **Milestone:** Build a small application (e.g., in Python) that can create and retrieve customer records from NetSuite via the REST API.

### Phase 4: DevOps & Platform Governance (1-2 Weeks)

Apply modern development practices to the NetSuite ecosystem. This is where prior DevOps experience becomes a major advantage.

*   **Topics:**
    *   **SuiteCloud Development Framework (SDF):** Learn to manage NetSuite customizations as code (XML definitions).
    *   **Version Control:** Use Git to manage your SDF projects and SuiteScripts.
    *   **CI/CD:** Set up a basic pipeline (e.g., using GitHub Actions or Azure DevOps) to deploy changes from a Git repository to a NetSuite sandbox.
*   **Learning Resources:**
    *   SDF Documentation on the official NetSuite help portal.
*   **Milestone:** Successfully deploy a custom field and a SuiteScript file from a local Git repository to a NetSuite account using the SDF CLI.

### Phase 5: Advanced Architecture & Portfolio Building (4-8 Weeks)

Combine all learned skills to design and build robust, scalable solutions.

*   **Topics:**
    *   **Solution Design:** Architect end-to-end solutions for complex business requirements.
    *   **Performance Tuning:** Learn best practices for writing efficient searches and scripts.
    *   **Platform Governance:** Define development standards, code review processes, and release management strategies.
    *   **Portfolio Projects:** Build practical, portfolio-ready projects.
*   **Certification Goal:** `SuiteCloud Developer II`.

---

## Portfolio Projects

1.  **Multi-System Integration Hub:** A middleware service (e.g., Python/Flask) that syncs customer and order data between NetSuite, Salesforce, and an HRIS.
2.  **Automated Data Migration Framework:** A Python-based tool using Pandas to clean, transform, and load legacy data into NetSuite via APIs, with robust error handling and logging.
3.  **NetSuite DevOps Toolkit:** A complete CI/CD pipeline in Azure DevOps or GitHub Actions that automates testing and deployment of SDF projects across Development, QA, and Production sandboxes.
4.  **Custom Workflow Engine:** A SuiteScript-based solution that extends SuiteFlow's capabilities, allowing for more complex, state-based approvals and dynamic routing.
5.  **Real-Time Analytics Engine:** An integration that pushes key NetSuite data (e.g., sales, inventory) to a BI tool or data warehouse for real-time dashboarding.