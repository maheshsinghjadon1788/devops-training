pipeline {
  agent any

  parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['dev', 'qa', 'prod'],
            description: 'Select the environment'
        )
    }

  tools {
        nodejs 'NodeJS 18 with Yarn'  // <-- Name must match what you configured
    }

  environment {
    LANG = 'en_US.UTF-8'
    LC_ALL = 'en_US.UTF-8'
    selectedScheme = 'expodemo'
    archivePath = "${HOME}/Documents/devops/JenkinsiOSArchive/ExpoDemo.xcarchive"
    exportAppPath = "${HOME}/Documents/devops/iOS"
    exportOptionsPath = "${WORKSPACE}/ios/ExportOptions.plist"
    BUILD_LOG_FILE = 'xcodebuild.log'
  }

  stages {
    stage('Initialize') {
      steps {
        echo 'Build ExpoDemo App mobile'
      }
    }

    stage('Chnage To Root Directories') {
      steps {
        dir("${WORKSPACE}") {
          echo '#### Path change to root directory'
        }
      }
    }

    stage('Install Dependencies') {
      steps {
        dir('expo-demo') {
          echo '#### Npm install start ####'
          sh 'npm install'
          echo '#### Npm install finish ####'
        }
      }
    }

    stage('CocoaPods Install') {
      steps {
        dir("${WORKSPACE}/expo-demo/ios") {
          echo '#### pod install start ####'
        // sh '${POD} install'
          sh '''
            $HOME/.rvm/gems/ruby-3.1.3/wrappers/pod install
          '''
          echo '#### pod install done ####'
        }
      }
    }
  }
}
