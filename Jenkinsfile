pipeline{
  agent any
  
  stages {
    stage('Build') {
      steps {
        sh '''
        echo $PWD
        echo $(ls)
        chmod 775 -R .
        '''
      }
    }
    
    stage('Test'){
      steps{
        sh './test_pass.sh'
        sh './test_fail.sh'
      }
    }
  }
}
