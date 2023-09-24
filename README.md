# Pulumi Cloud Infrastructure

Welcome to the Pulumi Cloud Infrastructure project. This project uses the Pulumi framework with AWS and is written in Python to provide a comprehensive solution for managing cloud resources.

## Overview

This project serves as a sophisticated blueprint illustrating a multi-layered approach to cloud infrastructure deployment using the Pulumi framework. The project is organized into four distinct subprojects:

1. **Compute**
2. **Identity**
3. **Networking**
4. **Storage**

Each subproject represents a different layer of our cloud infrastructure. This segregation ensures a clear separation of concerns and optimizes the management of our resources.

## Project Structure Diagram

![Project Structure](./assets/pulumi.png)

*Note: The above diagram showcases the hierarchical structure and inter-relationship of the various subprojects and their components. It provides a visual representation of how the infrastructure layers interact and depend on each other.*

## Getting Started

1. **Clone**: Clone this repository to your local machine.

2. **Setup**: Ensure you've set up an account with Pulumi.
   - **Get Your Pulumi Token**: Before running the infrastructure, generate and secure your Pulumi account token.
   - **Installation**: Keep your local machine clean! You dont have to install complete Pulumi SDK. Just use official Pulumi Docker image to run the code:
        
        - Pull Pulumi docker image from Dockerhub
        
        ```
            docker pull pulumi/pulumi-python
        ```

        - In your VisualCode open your terminal, run the following command and mount the volume to docker container:
        
        ```powershell
          docker run -e "PULUMI_ACCESS_TOKEN=pul-794d0ab88c86127e8535a6a72e29b0d578f73f49" -it -v ${PWD}:/pulumi/projects -v ${HOME}/.aws/:/root/.aws/ pulumi/pulumi-python:latest bash
        ```

        ```bash
        docker run -e "PULUMI_ACCESS_TOKEN=<paste_your_token_here>" -it -v "$(pwd)":/pulumi/projects -v "$HOME/.aws/":/root/.aws/ pulumi/pulumi-python:latest bash
        ```

        ```bash
            root@9c8382742b09:/pulumi/projects# ls -l
            total 4
            -rwxrwxrwx 1 root root 3789 Sep 24 11:07 README.md
            drwxrwxrwx 1 root root 4096 Sep 23 19:14 assets
            drwxrwxrwx 1 root root 4096 Sep 23 19:13 aws-python
        ```

        **Note**: Pulumi reads AWS configuration and credentials from default path ~/.aws/ . You can modify how you will pass AWS credentials to Pulumi, but for this purpose I will keep the default one.

3. **Navigate**: Change directories to the specific subproject you wish to deploy or manage.

4. **Deploy**: Use Pulumi commands like `pulumi up -s dev` to deploy the infrastructure.


## State Management

An essential aspect of infrastructure management is the handling of state files. In the case of Pulumi, state files represent the current state of our infrastructure and are critical for operations like updates or deletions. For this project, each subproject will have its dedicated state file.

While Pulumi offers flexibility regarding the location of state storage, for this example, we have chosen to use **Pulumi Cloud** for state storage. This approach provides centralized access and robust security features to manage the infrastructure's state.

## Subcomponents

Each subproject is not just a monolithic block; they contain various subcomponents that handle specific tasks or represent distinct resources. For an in-depth understanding and a breakdown of what each subproject does, please refer to the documentation available inside the respective subproject folders.

## Conclusion

This project aims to provide a structured and efficient way to manage cloud infrastructure using Pulumi, AWS, and Python. Should you have any queries or require further information, kindly refer to the documentation inside each subproject or raise an issue.

Thank you for choosing Pulumi Cloud Infrastructure for your cloud management needs.
