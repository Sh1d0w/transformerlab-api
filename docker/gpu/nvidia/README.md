# TransformerLab API Deployment

This repository contains everything you need to deploy the TransformerLab API using Docker with CUDA support. The provided files include:

- **Dockerfile.cuda** – Builds a CUDA-enabled Docker image (Optional - Only build an image if you want to customize it).
- **docker-compose.yml.tpl** – Template for the Docker Compose configuration.
- **deploy.sh** – Shell script for Linux/Mac deployment.
- **deploy.ps1** – PowerShell script for Windows deployment.

Below you will find detailed instructions for setting up and running the deployment on both Linux/Mac and Windows systems, along with prerequisites and troubleshooting tips.

---

## Table of Contents

- [Pre-requisites](#pre-requisites)
- [Installation and Deployment](#installation-and-deployment)
  - [Linux/Mac](#linuxmac)
- [Windows](#windows)
- [Troubleshooting](#troubleshooting)
- [Additional Information](#additional-information)

---

## Pre-requisites

Before you begin, ensure that your system meets the following requirements:

- **Docker**: 
  - Install Docker from [Docker's official website](https://docs.docker.com/get-docker/).

- **Docker Compose**: 
  - Ensure Docker Compose is installed (often included with Docker Desktop or available as a separate package).

- **NVIDIA GPU Drivers & NVIDIA Container Toolkit** (if using GPU support): 
  - Install the appropriate NVIDIA drivers and follow the [NVIDIA Container Toolkit installation guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html).

- **curl**: 
  - Required for fetching the latest version from GitHub.
  - **Linux/Mac**: Install via your package manager (e.g., `sudo apt-get install curl` or `brew install curl` on macOS).
  - **Windows**: The PowerShell script can install it using [winget](https://github.com/microsoft/winget-cli) if it is not present.

- **envsubst** (Linux/Mac only): 
  - Part of the GNU gettext package. Install with:
    `sudo apt-get install gettext`
    or on macOS:
    `brew install gettext && brew link --force gettext`

- **PowerShell** (Windows): 
  - Ensure you are running PowerShell (available by default on Windows 10+).

---

## Installation and Deployment

### Linux/Mac

1. **Clone the Repository:**
  ```bash
    git clone https://github.com/transformerlab/transformerlab-api.git
    cd transformerlab-api/docker/gpu/nvidia
  ```

2. **Prepare the Deployment Script:**
  - Make sure `deploy.sh` is executable:
  ```bash
    chmod +x deploy.sh
  ```

3. **Run the Deployment Script:**
  - Execute the script:
  ```bash
    ./deploy.sh
  ```
  - **What the script does:**
    - Checks for `curl` and installs it if missing.
    - Fetches the latest version tag from the GitHub repository.
    - Removes any leading `v` from the version tag.
    - Uses `envsubst` to substitute the version into `docker-compose.yml.tpl`, generating `docker-compose.yml`.
    - Deploys the container using Docker Compose.

4. **Access the API:**
  - Once deployed, the API is accessible at [http://localhost:8338](http://localhost:8338).

### Windows

1. **Clone the Repository:**
  - Open PowerShell and run:
  ```powershell
    git clone https://github.com/transformerlab/transformerlab-api.git
    cd transformerlab-api
  ```

2. **Run the Deployment Script:**
  - Open PowerShell (as Administrator if necessary).
  - Execute the PowerShell script:
  ```powershell
    .\\deploy.ps1
  ```
  - **What the script does:**
    - Checks if `curl` is installed; if not, it installs `curl` using `winget`.
    - Fetches the latest version tag from the GitHub API.
    - Removes any leading `v` from the version tag.
    - Reads the `docker-compose.yml.tpl` file and substitutes in the version and your HOME path.
    - Generates a `docker-compose.yml` file.
    - Deploys the container using Docker Compose.

3. **Access the API:**
  - Once deployed, open your browser and navigate to [http://localhost:8338](http://localhost:8338).

---

## Troubleshooting

- **Docker Not Running:**
  - Ensure Docker is installed and the Docker daemon is active.
  - On Linux, you might need to start Docker:
    `sudo systemctl start docker`

- **curl Not Found:**
  - **Linux/Mac**: Install with your package manager (e.g., `sudo apt-get install curl` or `brew install curl`).
  - **Windows**: The PowerShell script attempts to install `curl` via `winget`. Alternatively, install curl manually if required.

- **envsubst Command Not Found (Linux/Mac):**
  - Install GNU gettext:
    `sudo apt-get install gettext`
    or on macOS:
    `brew install gettext && brew link --force gettext`

- **GPU Not Detected:**
  - Verify that your system has a supported NVIDIA GPU.
  - Confirm that the NVIDIA drivers and the NVIDIA Container Toolkit are properly installed.

- **Failed to Fetch Latest Version:**
  - Check your internet connection.
  - Ensure GitHub’s API is accessible from your network.
  - As a workaround, manually set the version by exporting the `VERSION` environment variable before running the script.

- **Docker Compose Errors:**
  - Make sure you have a compatible version of Docker Compose.
  - Update Docker Compose if necessary.

- **Permission Issues:**
  - If you encounter permission issues, try running the deployment scripts with elevated privileges (e.g., using `sudo` on Linux/Mac or running PowerShell as Administrator on Windows).

---

## Additional Information

- **Viewing Logs:**
  - To inspect logs for the running container, use:
  ```bash
    docker compose logs transformerlab-api
  ```

- **Stopping the Deployment:**
  - To stop and remove the container, run:
  ```bash
    docker compose down
  ```
  - To delete all volumes and data, run:
  ```bash
    docker compose down -v
  ``` 

- **Customizing Deployment:**
  - You can modify the `Dockerfile.cuda` with custom implmentation and build an image, make sure to update the `docker-compose.yml.tpl` with build context.
  - You can modify the `docker-compose.yml.tpl` file to adjust settings such as port mappings, volume mounts, or resource reservations as needed.

- **Further Assistance:**
  - For additional help or to report issues, please visit the project’s GitHub repository and open an issue on the tracker.

Happy deploying!