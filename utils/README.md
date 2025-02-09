# Utilities Module

## Goal
The `utils` folder contains utility modules and functions that are used throughout the automation project but are not specific to the core business logic.

## Purpose
- **Code Reusability**: Provides a central location for commonly used functions, promoting DRY (Don't Repeat Yourself) principles.
- **Separation of Concerns**: Keeps utility functions separate from the core application logic, enhancing maintainability and clarity.

## Contents
- **logger.py**: Configures the logging system for structured and consistent logging across the project.
- **data_generator.py**: Functions to generate random data for testing purposes, aiding in test case creation.
- **swagger_parser.py**: (Advanced) Parses a Swagger definition and generates test cases or data models based on the API specifications.
- **helpers.py**: Contains other general utility functions that support various operations within the project.

This folder serves as a toolkit for developers, providing essential functions that streamline the automation process and enhance the overall efficiency of the testing framework.