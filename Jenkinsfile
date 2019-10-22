pipeline{
  agent any
  
  stages {
    stage('Build') {
      steps {
        sh '''
        echo $PWD
        chmod 775 -R .
        conda activate nightly
        '''
      }
    }
    
    stage('Test'){
      steps{
        sh './test_pass.sh'
      }
    }

    stage('Deploy'){
        steps('pypi'){
            sh ''' 
            python setup.py sdist bdist_wheel
            twine upload --repository-url https://test.pypi.org/legacy/ dist/*
            '''
        }
    }
  }
}
