pipeline {
    agent any
    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['dev', 'qa', 'prod'],
            description: 'Select the environment'
        )
    }
        stages {
            
            stage('Checkout') {
                steps {
                    git url: 'https://github.com/maheshsinghjadon1788/devops-training.git', branch: 'dev'
                }
            }
            stage('Manual Approval for Prod') {
            when {
                expression { return params.ENVIRONMENT == 'prod' }
            }
            steps {
                script {
                    def userInput = input(
                        id: 'ProdApproval', message: 'Approve Production Deployment?', parameters: [
                            [$class: 'TextParameterDefinition', defaultValue: '', description: 'Enter reason for approval', name: 'ApprovalReason']
                        ]
                    )
                    echo "Approval reason: ${userInput}"
                }
            }
        }
        
        stage('Run Environment Specific Steps') {
            steps {
                script {
                    if (params.ENVIRONMENT == 'dev') {
                        echo 'Running DEV deployment steps...'
                        // Add dev-specific commands here
                    } else if (params.ENVIRONMENT == 'qa') {
                        echo 'Running QA deployment steps...'
                        // Add QA-specific commands here
                    }
                    else if (params.ENVIRONMENT == 'prod') {
                        echo 'Running PROD deployment steps...'
                        // Add prod-specific commands here
                    }
                }
            }
        }
    }       
}
