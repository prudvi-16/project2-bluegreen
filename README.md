# Automated Blue-Green Deployment on AWS EC2 using Docker + Jenkins

## Project Overview

This project demonstrates an automated Blue-Green deployment strategy on AWS EC2 using Docker, Jenkins, GitHub, Linux, and NGINX.

The deployment pipeline builds a new Docker image, deploys it to the GREEN environment, performs a health check, and switches production traffic only after the new version is verified as healthy.

If the health check fails, Jenkins stops the pipeline and NGINX continues routing traffic to the currently active BLUE environment.

---

## Architecture

```text
                    GitHub
                       |
                       v
                    Jenkins
                       |
                 Docker Build
                       |
                       v
              +-------------------+
              |      AWS EC2      |
              |                   |
Internet ---> |   NGINX :80       |
              |      |            |
              |  +---+---+        |
              |  |       |        |
              |  v       v        |
              | BLUE    GREEN      |
              | :8081   :8082      |
              | v1.0.0  v1.1.0    |
              +-------------------+

Technology Stack
AWS EC2
Amazon Linux
Git
GitHub
Docker
Jenkins
NGINX
Python Flask
Application Endpoints
Application
/

Example response:

Blue-Green Demo Application - Version 1.1.0 - GREEN
Health Check
/health

Healthy response:

HTTP 200
OK
Blue-Green Environments

BLUE:

Port: 8081
Version: 1.0.0
Container: blue-app

GREEN:

Port: 8082
Version: 1.1.0
Container: green-app

NGINX listens on:

Port 80

and routes production traffic to the active environment.

Jenkins Pipeline

The Jenkins pipeline performs the following stages:

Git Checkout
     |
     v
Build Docker Image
     |
     v
Deploy GREEN
     |
     v
Health Check
     |
     v
Switch NGINX Traffic
     |
     v
Production Verification
Health Check Strategy

Jenkins validates the new GREEN environment before switching traffic.

The pipeline retries the health endpoint several times:

GREEN /health
     |
     +--> PASS
     |      |
     |      v
     |   Switch Traffic
     |
     +--> FAIL
            |
            v
       Pipeline Failure
            |
            v
     Existing production
        remains active
Failed Deployment Protection

A deliberately unhealthy version was tested.

The GREEN application returned:

HTTP 500
Health Check Failed

Jenkins output:

Stage "Switch Traffic" skipped due to earlier failure(s)
Finished: FAILURE

NGINX remained:

proxy_pass http://blue;

Production continued serving:

Version 1.0.0

This confirmed that an unhealthy deployment cannot automatically receive production traffic.

Successful Deployment

After restoring the healthy application version, Jenkins successfully completed:

Build Docker Image       SUCCESS
Deploy GREEN             SUCCESS
Health Check             SUCCESS
Switch Traffic           SUCCESS
Production Verification  SUCCESS

Final output:

Blue-Green deployment completed successfully.
Finished: SUCCESS

Production traffic was switched to GREEN.

Rollback

Traffic can be manually rolled back using:

sudo /usr/local/bin/bluegreen-switch blue

Switch back to GREEN:

sudo /usr/local/bin/bluegreen-switch green

The script validates NGINX configuration before reloading it.

Verification Commands

Check production:

curl http://localhost/

Check production health:

curl http://localhost/health

Check BLUE:

curl http://localhost:8081/

Check GREEN:

curl http://localhost:8082/

Check containers:

docker ps

Check NGINX target:

sudo grep proxy_pass /etc/nginx/conf.d/bluegreen.conf
Final Deployment State
BLUE
Version: 1.0.0
Port: 8081
Status: Standby


GREEN
Version: 1.1.0
Port: 8082
Status: LIVE


NGINX
Port: 80
Traffic Target: GREEN
Key Learning Outcomes

This project demonstrates:

Blue-Green deployment strategy
CI/CD automation with Jenkins
Docker image creation and container deployment
NGINX reverse proxy and traffic switching
Application health checks
Failed deployment protection
Manual rollback
Linux service and permission management
GitHub integration using SSH
Deployment troubleshooting on AWS EC2
Project Result

The completed CI/CD workflow is:

Developer
    |
    v
GitHub
    |
    v
Jenkins
    |
    v
Docker Build
    |
    v
Deploy GREEN
    |
    v
Health Check
   / \
FAIL PASS
 |     |
STOP   v
 |   NGINX Switch
 |     |
 v     v
BLUE  GREEN
LIVE  LIVE
