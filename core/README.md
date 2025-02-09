# Core Module

## Goal
The `core` folder encapsulates the core business logic and reusable components of the automation framework.

## Purpose
- **Code Reusability**: Provides a central location for code that is utilized by multiple parts of the application, such as the API client, data models, and common functions.
- **Abstraction**: Hides the implementation details of complex operations, making the codebase easier to understand and maintain.
- **Testability**: Facilitates the testing of core logic in isolation from the rest of the application, ensuring that the foundational components are reliable.

## Contents
- **api_client.py**: A generic API client for interacting with the self-service application's API, handling requests and responses.
- **data_models.py**: Pydantic models for request and response data structures, providing type validation and ensuring data integrity.
- **exceptions.py**: Custom exception classes for handling specific error conditions within the application, improving error management.
- **utils.py** (or break into smaller files): Contains utility functions that are used across the core components, promoting code reuse and organization.

This folder is essential for maintaining the foundational logic of the automation framework, ensuring that core functionalities are well-structured, reusable, and easy to test.