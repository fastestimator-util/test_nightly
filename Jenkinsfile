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
        sh 'sudo chmod +x test_pass.sh'
        sh 'sudo chmod +x test_fail.sh'
        sh './test_pass.sh'
        sh './test_fail.sh'
      }
    }
  }
}
