# Safety Drive
4th year AI and Big Data Annual Project made by Réda MAIZATE, Cédric GARVENES and Nacim MESSACI.

## Prerequisites

Step 1 : To run the project, you will need to have **Docker**, **Terraform** installed on your computer and **AWS account**.

Step 2 : After Docker, Terraform installed and your AWS Account created, you now need to create a file called `terraform.tfvars` in the directory `infrastructure/terraform` of the project.
You should copy the content of the file `terraform.tfvars.example` to this file and adapt it to your needs.
```
# This file is used to configure the Terraform project.

aws_account_id         = "" # Your AWS account ID (e.g., 123456789012)
region                 = "" # Your AWS region (e.g., us-east-1)
function_name          = "" # The name of the Lambda function (e.g., my-function)
lambda_role_name       = "" # The name of the Lambda IAM role (e.g., lambda-my-role)
lambda_iam_policy_name = "" # The name of the Lambda IAM policy (e.g., lambda-my-policy)
bucket_name            = "" # The name of the S3 bucket (e.g., my-bucket)
ecr_repository_name    = "" # The name of the ECR repository (e.g., my-repository)
```

Final step : After your `terraform.tfvars` created and filled, launch the Docker application.

## Usage
**_WARNING_** : The next commands after are **ONLY** available in the `infrastructure` directory. So make sure to be in the `infrastructure` directory.

```bash
cd infrastructure
```

To initialize the infrastructure of the project, you will need to run the following command:

```bash
make init
```

To create the infrastructure on AWS, you will need to run the following command:

```bash
make up
```

To destroy the infrastructure on AWS, you will need to run the following command:

```bash
make down
```
