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

        stage('Deploy') {
            steps {
                sh '''
                echo "🧹 Cleaning up old containers..."
                docker rm -f react-app postgres-db || true
                echo "🚀 Starting new containers..."
                docker compose up -d --build
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
