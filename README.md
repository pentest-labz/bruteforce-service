# Brute-Force Cracker

A Flask-based microservice for controlled web-form brute-force testing. It accepts a target URL, username, and a list of passwords (or falls back to a built-in default list), attempts logins in parallel, and reports any successful credential.

## Table of Contents

- [Features](#features)  
- [Prerequisites](#prerequisites)  
- [Quick Start (Docker)](#quick-start-docker)  
- [Usage](#usage)  
  - [Endpoint](#endpoint)  
  - [Request Body](#request-body)  
  - [Response](#response)  
- [Project Structure](#project-structure)  
- [Kubernetes Deployment](#kubernetes-deployment)  
- [Configuration](#configuration)  
- [Security Considerations](#security-considerations)  
- [License](#license)  

## Features

- Web-form brute-force via HTTP POST  
- Built-in default password list (top 10 common passwords)  
- Custom wordlists via JSON payload  
- Request timeouts to prevent hangs  
- Parallel attempts with configurable thread pool  
- Returns success status, matched password, and total attempts  

## Prerequisites

- Docker  
- (Optional) Python 3.10+ for local development  

## Quick Start (Docker)

```bash
git clone https://github.com/your-org/brute-force-cracker.git
cd brute-force-cracker

# Build the Docker image
docker build -t brute-force-cracker .

# Run the container on port 5002
docker run -d -p 5002:5002 --name cracker brute-force-cracker
