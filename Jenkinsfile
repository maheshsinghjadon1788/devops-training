pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning repository...'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Building the project...'
                // Example: compile or build step
                // sh 'javac Main.java'
            }
        }

       stage('Test') {
            steps {
                echo 'Running tests...'
                // Example: sh 'python3 -m unittest tests/'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying the application...'
                // Example: sh 'scp target/app.jar user@server:/deployments/'
            }
        }
    }
}
