pipeline {
  agent {
    label 'macos' // Ensure Jenkins agent is macOS
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

    stage('Install Dependencies') {
      steps {
        dir("${WORKSPACE}") {
          echo '#### Yarn install start ####'
          sh 'yarn install'
          echo '#### Yarn install finish ####'
        }
      }
    }

    stage('CocoaPods Install') {
      steps {
        dir("${WORKSPACE}/ios") {
          echo '#### pod install start ####'
          sh 'pod install'
          echo '#### pod install done ####'
        }
      }
    }
  }
}
