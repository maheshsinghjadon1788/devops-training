pipeline {
    agent any

    environment {
        APP_NAME = "my-app"
        DOCKER_REGISTRY = "registry.example.com"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
	stage('Build') {
            steps {
                script {
                    sh 'mvn clean install -DskipTests'
                }
            }
        }

        stage('Test') {
            when {
                not { branch 'main' }
            }
	steps {
                script {
                    sh 'mvn test'
                }
            }
        }

        stage('Static Code Analysis') {
            steps {
                sh 'mvn sonar:sonar'
            }
        }
	stage('Docker Build & Push') {
            when {
                branch 'main'
            }
            steps {
                script {
                    sh "docker build -t $DOCKER_REGISTRY/$APP_NAME:${env.BUILD_NUMBER} ."
                    sh "docker push $DOCKER_REGISTRY/$APP_NAME:${env.BUILD_NUMBER}"
                }
            }
	stage('Deploy to Staging') {
            when {
                branch 'release/*'
            }
            steps {
                script {
                    sh './scripts/deploy-staging.sh'
                }
            }
        }
    }

	post {
        always {
            echo "Cleaning workspace..."
            cleanWs()
        }
    }
}
