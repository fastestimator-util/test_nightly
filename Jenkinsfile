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
                sh '''
                    . /var/lib/jenkins/workspace/venv/bin/activate
                    ./test/test_image_segmentation/test_unet_cub200.sh
                '''
            }
        }

        // stage('Deploy-pypi'){
        //     steps{
        //         sh ''' 
        //             . /var/lib/jenkins/workspace/venv/bin/activate
        //             rm -rf dist/*
        //             FASTESTIMATOR_IS_NIGHTLY=1 python setup.py sdist bdist_wheel 
        //             twine upload --config-file /home/jenkins/.pypirc --repository testpypi dist/*
        //         '''
        //     }
        // }

        // stage('Deploy-docker'){
        //     steps{
        //         sh '''
        //             rm -rf ./fastestimator-misc
        //             git clone https://github.com/fastestimator-util/fastestimator-misc.git fastestimator-misc
        //         '''
        //         withDockerRegistry(credentialsId: 'docker_hub_geez', url:'') {
        //             sh ''' 
        //                 echo $PWD 
        //                 docker build -t geez0219/fastestimator:test - < fastestimator-misc/docker/nightly/Dockerfile.cpu
        //                 docker push geez0219/fastestimator:test
        //             '''
        //         }
        //     }
        // }
    }
}
