pipeline {
    agent {
        label 'ubuntu'
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    checkout scm
                }
            }
        }

        stage('Build and Run') {
            steps {

                dir('/home/david/Desktop/github/Update_DNS_Records_Cloudflare') {
                    script {
                        sh 'source venv/bin/activate'
                    }
                    
                    script {
                        sh 'python3 main.py'
                    }
                }
            }
        }
    }
}