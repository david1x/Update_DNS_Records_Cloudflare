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
                    
                    // Ensure execute permissions for the activate script
                    script {
                        sh 'chmod +x venv/bin/activate'
                    }

                    // Activate the virtual environment
                    script {
                        sh 'venv/bin/activate'
                    }
                    
                    // Run the Python script
                    script {
                        sh 'python main.py'
                    }
                }
            }
        }
    }
}
