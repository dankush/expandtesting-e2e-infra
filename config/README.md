# Configuration Module

## Goal
The `config` folder serves as a centralized storage and management system for configuration settings across the entire automation project.

## Purpose
- **Configuration Management**: Facilitates easy modification of settings without altering the codebase. This is crucial for adapting to different environments (development, testing, production) and for adjusting parameters dynamically.
- **Separation of Concerns**: Keeps configuration settings distinct from application logic, enhancing maintainability and readability.
- **Reproducibility**: Ensures consistent behavior across various environments by providing a single source of truth for configuration settings.

## Contents
- **config.yaml**: The main configuration file for global settings, including API base URLs, timeouts, database connection strings, feature flags, and other essential parameters.
- **logging.yaml**: Defines the logging configuration, specifying log levels, formats, handlers, and other logging-related settings.

This folder is essential for maintaining a flexible and manageable configuration system, allowing for seamless adjustments and consistent application behavior across different environments.