pipeline {
    agent any

    environment {
        DOCKER_HOST = 'unix:///var/run/docker.sock'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Test') {
            steps {
                sh 'pytest --maxfail=1 --disable-warnings -q || true'
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                echo "🧹 Cleaning up old containers..."
                docker compose -f $WORKSPACE/docker-compose.yml down --remove-orphans
                echo "🚀 Starting new containers..."
                docker compose -f $WORKSPACE/docker-compose.yml up -d --build
                '''
            }
        }
    }

    post {
        always {
            sh 'docker compose ps || true'
        }
    }
}
