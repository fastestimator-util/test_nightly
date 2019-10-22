pipeline{
  agent any
  
  stages {
    stage('Build') {
      steps {
        sh '''
        echo $PWD
        chmod 775 -R .
        '''
        sh './test/install_dependencies.sh'
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
            ./push_pypi.sh
            
            '''
        }
    }
  }
}
