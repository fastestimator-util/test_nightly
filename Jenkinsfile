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
        sh 'chmod +x test_pass.sh'
        sh 'chmod +x test_fail.sh'
        sh './test_pass.sh'
        sh './test_fail.sh'
      }
    }
  }
}
