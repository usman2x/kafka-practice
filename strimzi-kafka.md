# Strimzi Reference Guide

## What is Minikube?
Minikube is a lightweight Kubernetes implementation that creates a local Kubernetes cluster for development and testing purposes. It allows developers to run Kubernetes locally on their machines without needing a full-fledged cluster.

## How is `kubectl` related to Minikube?
`kubectl` is the command-line tool used to interact with Kubernetes clusters, including those created by Minikube. When Minikube is installed and started, it can automatically download and configure `kubectl` to work with the local Minikube cluster.

## Installation on macOS (Intel Processor)
To install Minikube on a Mac with an Intel processor, follow these steps:

1. Download the latest Minikube binary:
   ```sh
   curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-darwin-amd64
   ```
2. Install Minikube by moving it to a system-wide binary directory:
   ```sh
   sudo install minikube-darwin-amd64 /usr/local/bin/minikube
   ```

## Starting Minikube
To start Minikube, use the following command:
```sh
minikube start
```
### Important Considerations:
- **Docker Desktop must be running** before executing `minikube start`, otherwise, you may encounter the following error:
  
  ❌ *Exiting due to DRV_DOCKER_NOT_RUNNING: Found docker, but the docker service isn't running. Try restarting the docker service.*

- This command automatically downloads `kubectl` if it's not already installed.

## Expected Output
Upon successfully starting Minikube, you should see output similar to:
```plaintext
✨  Automatically selected the docker driver
📌  Using Docker Desktop driver with root privileges
👍  Starting "minikube" primary control-plane node in "minikube" cluster
🚜  Pulling base image v0.0.46 ...
💾  Downloading Kubernetes v1.32.0 preload ...
🔥  Creating docker container (CPUs=2, Memory=4000MB) ...
🐳  Preparing Kubernetes v1.32.0 on Docker 27.4.1 ...
🔗  Configuring bridge CNI (Container Networking Interface) ...
🔎  Verifying Kubernetes components...
🌟  Enabled addons: storage-provisioner, default-storageclass

❗  /usr/local/bin/kubectl is version 1.30.5, which may have incompatibilities with Kubernetes 1.32.0.
    ▪ Want kubectl v1.32.0? Try 'minikube kubectl -- get pods -A'
🏄  Done! kubectl is now configured to use "minikube" cluster and "default" namespace by default
```

## Verifying `kubectl`
To check if `kubectl` is running correctly and Minikube is functioning as expected, use:
```sh
kubectl get nodes
```
This command should return information about the Minikube node, confirming that the cluster is active.

