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
        sh './test/install_dependencies.sh'
      }
    }
    
    stage('Test'){
      steps{
        sh './test_pass.sh'
      }
    }

    stage('Deploy'){
        // steps('pypi'){
        //     // sh ''' 
        //     // . /var/lib/jenkins/workspace/venv/bin/activate
        //     // ./push_pypi.sh
        //     // '''
        // }
        steps('docker'){
            
            sh '''
                git clone https://github.com/fastestimator-util/fastestimator-misc.git fastestimator-misc
                echo $PWD 
                echo $(ls)
                cp fastestimator-misc/docker/nightly/* ./
                echo $(ls)
            '''
        }
    }

  }
}
