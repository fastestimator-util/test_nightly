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
                echo $PWD 
                echo $(ls)
                mkdir Dockerhub-cpu 
                cp fastestimator-misc/docker/nightly/Dockerfile.cpu Dockerhub-cpu/
                mv Dockerhub-cpu/Dockerfile.cpu Dockerhub-cpu/Dockerfile
                cd Dockerhub-cpu
                echo $(ls)
            '''
            withDockerRegistry(credentialsId: 'docker_hub_geez', url:'') {
                sh '''' 
                    echo $PWD 
                    docker build .
                '''
            }
        }
    } 
  }
}
