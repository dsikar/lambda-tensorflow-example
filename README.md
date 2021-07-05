# lambda-tensorflow-example
Modified from 
```
https://aws.amazon.com/blogs/machine-learning/using-container-images-to-run-tensorflow-models-in-aws-lambda/  
```
Ran all local code on Ubuntu 18.04.

## Working order
1. Create inference model as per
```
https://github.com/CityDataScienceSociety/ComputerVisionWorkshops/tree/main/detect-fire-with-AI
```
2. Create directory structure (cloned from this repo)
```
- lambda-tensorflow-example
-- app.py
-- Dockerfile
-- requirements.txt
```
3. In app.py, edit line adding appropriate bucket and model name
```
result = client_s3.download_file("dsikar.models.bucket",'firemodel.h5', "/tmp/firemodel.h5")
```

4. Configure AWS CLI, create docker image and upload, changing AWS Account ID and region as appropriate
```
$ aws configure (…)

$ docker build -t  lambda-tensorflow-example .

$ aws ecr create-repository --repository-name lambda-tensorflow-example --image-scanning-configuration scanOnPush=true --region eu-west-2

$ docker tag lambda-tensorflow-example:latest  784146270336.dkr.ecr.eu-west-2.amazonaws.com/lambda-tensorflow-example:latest

$ aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin  784146270336.dkr.ecr.eu-west-2.amazonaws.com

$ docker push  784146270336.dkr.ecr.eu-west-2.amazonaws.com/lambda-tensorflow-example:latest

```
5. Register Lambda function and deploy docker image

![image](https://user-images.githubusercontent.com/232522/124463576-fe80a080-dd8a-11eb-9a39-faf82c7b8c8f.png)

![image](https://user-images.githubusercontent.com/232522/124463678-24a64080-dd8b-11eb-84f6-defb26534834.png)

6. Upload Tensorflow model to S3 bucket

![image](https://user-images.githubusercontent.com/232522/124464158-bd3cc080-dd8b-11eb-97e8-c914769b27d7.png)

7. Upload example image to S3 bucket

![image](https://user-images.githubusercontent.com/232522/124464054-9c746b00-dd8b-11eb-9c75-06c92a857523.png)

8. Verify prediction in CloudWatch

![image](https://user-images.githubusercontent.com/232522/124464371-0856d380-dd8c-11eb-85ce-54ce3e630b99.png)


