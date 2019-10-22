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
                rm -rf ./fastestimator-misc
                git clone https://github.com/fastestimator-util/fastestimator-misc.git fastestimator-misc
            '''
            withDockerRegistry(credentialsId: 'docker_hub_geez', url:'') {
                sh ''' 
                    echo $PWD 
                    docker build - < fastestimator-misc/docker/nightly/Dockerfile.cpu
                    docker push geez0219/fastestimator:test
                '''
            }

        }
    } 
  }
}
