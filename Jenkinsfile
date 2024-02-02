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
                dir('/tmp/workspace/CloudFlareDNSUpdate') {
                    
                    // Create a virtual environment
                    script {
                        sh 'python3 -m venv venv'
                    }
                    
                    // Activate the virtual environment
                    script {
                        sh 'source venv/bin/activate'
                    }
                    
                    // Install dependencies if needed (example: pip install -r requirements.txt)
                    script {
                        sh 'pip install -r requirements.txt'
                    }

                    // Run the Python script
                    script {
                        sh 'python main.py'
                    }
                }
            }
        }
    }

    post {
        always {
            // Clean up: Deactivate and remove the virtual environment
            script {
                sh 'deactivate || true'  // Deactivate the virtual environment if it's still active
                sh 'rm -rf venv'         // Remove the virtual environment
            }
        }
    }
}
