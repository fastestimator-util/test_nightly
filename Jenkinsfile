pipeline{
  agent any
  
  stages {
    stage('Build') {
      steps {
        sh '''
        echo $PWD
        echo $(ls)
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
