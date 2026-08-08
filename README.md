# CCR9 Protein Inhibition

## Local Installation

### 1. Download the repository

Download or clone the entire repository.

### 2. Build the Docker containers

From the root directory, where `backend`, `frontend`, and `compose` are located, make sure Docker is running and execute the following command in CMD or PowerShell:

    docker compose build

To speed up the build process, you can add the `--parallel` flag:

    docker compose build --parallel

### 3. Start the application

Run:

    docker compose up

This will start all the required services.

If you make changes to the code, repeat steps 2 and 3.

## Troubleshooting

If you encounter errors, make sure that no other containers or applications are using the following ports:

`3000`, `5001`, `5002`, `5003`, `5004`, and `8000`.

## Accessing the Interface

Once all services are running, the web interface can be accessed at:

**http://localhost:8000**
