pipeline {
    agent any

    environment {
        IMAGE = "bluegreen-app"
        VERSION = "1.1.0"
        GREEN_PORT = "8082"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build -t ${IMAGE}:${VERSION} ./app
                '''
            }
        }

        stage('Deploy GREEN') {
            steps {
                sh '''
                    docker rm -f green-app || true

                    docker run -d \
                        --name green-app \
                        -p ${GREEN_PORT}:5000 \
                        ${IMAGE}:${VERSION}
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    sleep 3
                    curl -f http://localhost:${GREEN_PORT}/health
                '''
            }
        }

        stage('Switch Traffic') {
            steps {
                sh '''
                    sudo -n /usr/local/bin/bluegreen-switch green
                '''
            }
        }
    }
}
