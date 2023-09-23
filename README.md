# Pulumi Cloud Infrastructure

Welcome to the Pulumi Cloud Infrastructure project. This project uses the Pulumi framework with AWS and is written in Python to provide a comprehensive solution for managing cloud resources.

## Overview

The project is organized into four distinct subprojects:

1. **Compute**
2. **Identity**
3. **Networking**
4. **Storage**

Each subproject represents a different layer of our cloud infrastructure. This segregation ensures a clear separation of concerns and optimizes the management of our resources.

## Project Structure Diagram

![Project Structure](./assets/pulumi.png)

*Note: The above diagram showcases the hierarchical structure and inter-relationship of the various subprojects and their components. It provides a visual representation of how the infrastructure layers interact and depend on each other.*

## State Management

An essential aspect of infrastructure management is the handling of state files. In the case of Pulumi, state files represent the current state of our infrastructure and are critical for operations like updates or deletions. For this project, each subproject will have its dedicated state file.

While Pulumi offers flexibility regarding the location of state storage, for this example, we have chosen to use **Pulumi Cloud** for state storage. This approach provides centralized access and robust security features to manage the infrastructure's state.

## Subcomponents

Each subproject is not just a monolithic block; they contain various subcomponents that handle specific tasks or represent distinct resources. For an in-depth understanding and a breakdown of what each subproject does, please refer to the documentation available inside the respective subproject folders.

## Getting Started

1. **Setup**: Ensure you have Pulumi installed and set up your AWS credentials.
2. **Clone**: Clone this repository to your local machine.
3. **Navigate**: Change directories to the specific subproject you wish to deploy or manage.
4. **Deploy**: Use Pulumi commands like `pulumi up` to deploy the infrastructure.

## Conclusion

This project aims to provide a structured and efficient way to manage cloud infrastructure using Pulumi, AWS, and Python. Should you have any queries or require further information, kindly refer to the documentation inside each subproject or raise an issue.

Thank you for choosing Pulumi Cloud Infrastructure for your cloud management needs.
