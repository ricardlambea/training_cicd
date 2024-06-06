pipeline {
    triggers {
        // Poll SCM every minute
        pollSCM('* * * * *')
    }
    agent { 
        docker {
            image 'python:3.8' 
            // Run as user with id 1000 (jenkins)
            args '-u 1000:1000' 
        }
    }
    stages {
        // Clean workspace for a fresh start
        stage('Clean workspace') {
            steps {
                echo 'Cleaning up workspace'
                sh 'rm -rf .venv' 
            }
        }
        // Build stage to install dependencies
        stage('Build') {
            steps {
                echo "Installing dependencies"
                sh '''
                    python -m venv .venv
                    . .venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }
        // Static Analysis stage to run PyLint and publish report
        stage('Static Analysis') {
            steps {
                echo "Running PyLint"
                sh '''
                    . .venv/bin/activate
                    pylint -d C0301 -f parseable --reports=no main.py transform.py > pylint.log || echo "pylint exited with $?"
                '''
            }
            environment {
                PYLINTHOME = '.pylint.d'
            }
            post {
                always {
                    echo 'Publishing PyLint Report'
                    sh 'cat pylint.log'
                    recordIssues(
                        healthy: 1, 
                        tools: [pyLint(name: 'Python Project', pattern: '**/pylint.log')], 
                        unhealthy: 2
                    )
                }
            }
        }
          // Unit tests stage to run PyTest and publish JUnit report
        stage('Unit tests') {
            steps {
                echo 'Running Unit tests'
                sh  '''
                    . .venv/bin/activate
                    python -m pytest --verbose --junit-xml reports/junit.xml test.py
                '''
            }
            post {
                always {
                    archiveArtifacts 'reports/junit.xml'
                    junit(testResults: 'reports/junit.xml', allowEmptyResults: false)
                }
            }
        }
          // Coverage stage to run coverage and publish Coverage report
        stage('Coverage') {
            steps {
                echo 'Running coverage'
                sh '''
                    . .venv/bin/activate
                    coverage run test.py 
                    coverage report -m
                    coverage xml -o reports/coverage.xml
                '''
            }
            post {
                always {
                    archiveArtifacts 'reports/coverage.xml'
                    cobertura(
                        autoUpdateHealth: false,
                        autoUpdateStability: false,
                        coberturaReportFile: 'reports/coverage.xml',
                        conditionalCoverageTargets: '70, 0, 0',
                        failUnhealthy: false,
                        failUnstable: false,
                        lineCoverageTargets: '80, 0, 0',
                        maxNumberOfBuilds: 0,
                        methodCoverageTargets: '80, 0, 0',
                        onlyStable: false,
                        sourceEncoding: 'ASCII',
                        zoomCoverageChart: false
                    )
                }
            }
        }
    }
}
