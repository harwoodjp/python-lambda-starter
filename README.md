
How to create a (testable, monitorable) Python REST API with Lambda and Docker using [AWS Lambda Powertools](https://awslabs.github.io/aws-lambda-powertools-python/2.5.0/).

### Prerequisites
* Install and configure `aws` CLI
* Execute `bin/aws_ecr_docker_login.sh` to register Docker with ECR
* Ensure the following environmental variables are in your path:

| Variable           | Description                                   |
|--------------------|-----------------------------------------------|
| AWS_ACCOUNT_ID     | Account ID for AWS user                       |
| AWS_FUNCTION_NAME  | Name of your Lambda function                  |
| AWS_REGION         | Region your AWS resources are associated with |
| AWS_REST_API_ID    | API Gateway ID for your REST API              |
| AWS_REST_API_STAGE | Name of stage your API will deploy to         |

### AWS resources
* Preferably use infra-as-code solution like [Terraform](https://registry.terraform.io/providers/hashicorp/aws/latest/docs) or [CloudFormation](https://aws.amazon.com/cloudformation/) to describe/apply application resources
* AWS components:
  * ECR repo for Lambda images
  * Lambda sourced from latest image
  * API Gateway
  	* REST API
  		* Create resource
  		* Configure as proxy resource
  		* Integration type: Lambda Function Proxy
  		* Select Lambda Function


### Commands/workflow
* Build `hello-world`
  * `docker-compose build`
* Run `hello-world`
  * `docker-compose up --build`  
* Tag `hello-world:latest`
  * `docker tag hello-world:latest [ACCOUNT ID].dkr.ecr.us-east-1.amazonaws.com/hello-world:latest`
* Push to ECR
  * `docker push [ACCOUNT ID].dkr.ecr.us-east-1.amazonaws.com/hello-world:latest`
* Refresh Lambda with latest image
	* `aws lambda update-function-code --function-name [LAMBDA NAME/ARN] --image-uri [ACCOUNT ID].dkr.ecr.us-east-1.amazonaws.com/hello-world:latest`
* Deploy API to Stage `prod`
	* `aws apigateway create-deployment --region us-east-1 --rest-api-id [API ID] --stage-name prod`

### Testing
* Unit tests
	* `pytest` for assertions/coverage
	* `docker exec -it hello-world sh -c "pytest test.py"`
* Requests
	* curl: `bin/request_local.sh`
	* Event body: `bin/request_local_body.json`
* Tip: use method injection (S3, Dynamo, MySQL, etc. clients) for easy mocking (`unittest.Mock`)

### Debugging
* Local
	* `pudb` visual debugger (breakpoints, etc.)
		* From e.g. test context:
			* `import pudb; pu.db` or `pu.db`
		* From container:
			* Use this when debugging invocation via Postman, curl, etc. 
			* `from pudb.remote import set_trace; set_trace(term_size=(160, 40), host='0.0.0.0', port=6900)`
			* `telnet 127.0.0.1 6900` 
* Production
	* Run requests against endpoint URL provided by API Gateway Stage

### Monitoring
* Use `aws_lambda_powertools.Logger` for CloudWatch integration
* Tail production logs with `aws logs tail "/aws/lambda/[LAMBDA NAME]" --follow`