pipeline {
    agent any

    environment {
        IMAGE = "bluegreen-app"
        VERSION = "1.1.0"
        GREEN_PORT = "8082"
    }

    stages {

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
                    echo "Checking GREEN environment health..."

                    for i in 1 2 3 4 5
                    do
                        if curl -f http://localhost:${GREEN_PORT}/health
                        then
                            echo "GREEN health check passed"
                            exit 0
                        fi

                        echo "GREEN not ready - attempt $i/5"
                        sleep 3
                    done

                    echo "GREEN health check failed"
                    exit 1
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

        stage('Production Verification') {
            steps {
                sh '''
                    echo "Verifying production environment..."

                    curl -f http://localhost/health
                    curl -f http://localhost/

                    echo "Production verification passed"
                '''
            }
        }
    }

    post {

        success {
            echo 'Blue-Green deployment completed successfully.'
        }

        failure {
            echo 'Deployment failed. Traffic was not promoted if failure occurred before the traffic-switch stage.'
        }

    }
}
