<div align="center" style="margin-bottom: 0;">
    <a href="https://labs.openai.com/s/o5V608Wjr4uBH1mDGOL72ucC"><img src="https://zupimages.net/up/22/29/odmu.png" alt="Safety Drive logo generated by DALLE-2" height="400" width="400"/></a>
    <h1 style="margin-top: 0;">Safety Drive</h1>
</div>

4th year AI and Big Data Annual Project made by Réda MAIZATE and Cédric GARVENES.

*The Safety Drive logo was generated by [DALLE-2](https://www.dalle-2.com/). It's still not perfect as we can see lol.*

[[[TOC]]]

## Prerequisites

Step 1 : To run the project, you will need to have:
  - **Docker** -- [install here](https://docs.docker.com/get-docker/),
  - **Terraform** -- [install here](https://learn.hashicorp.com/tutorials/terraform/install-cli),
  - **AWS CLI** -- [install here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html),
  - **AWS account** -- [create here](https://aws.amazon.com/fr/premiumsupport/knowledge-center/create-and-activate-aws-account/),


Step 2 : Create an AWS profile on your computer to facilitate the connection to the AWS account.
```
$ cd ~ # Go to your home directory
$ mkdir .aws # Create a directory called .aws
$ nano .aws/credentials # Create the file .aws/credentials
```
And now you can write your credentials.
```
[profile]
aws_access_key_id = <your_access_key_id>
aws_secret_access_key = <your_secret_access_key>
```


Step 3 : After Docker, Terraform and AWS CLI installed and your AWS Account created, you now need to create a file called `terraform.tfvars` in the directory `infrastructure/terraform` of the project.
You should copy the content of the file `terraform.tfvars.example` to this file and adapt it to your needs.
```
# This file is used to configure the Terraform project.

# General
aws_account_id                  = "" # Your AWS account ID (e.g., 123456789012)
region                          = "" # Your AWS region (e.g., us-east-1)
bucket_name                     = "" # The name of your S3 bucket
profile_name                    = "" # The name of your AWS profil created earlier (e.g., my-profile)
ecr_repository_name             = "" # The name of your ECR repository
lambda_role_name                = "" # The name of your Lambda role
os                              = "" # The name of your operating system (e.g., mac or win)

# Pipeline
function_name_pipeline          = "" # The name of your Lambda function used in the pipeline
lambda_iam_policy_name_pipeline = "" # The name of your IAM policy used in the pipeline

# Web App
function_name_web_app           = "" # The name of your Lambda function used in the web app
api_gateway_name                = "" # The name of your API Gateway
```

Final step : After your `terraform.tfvars` created and filled, launch the Docker Desktop in your computer.

## Usage
**_WARNING_** : If you are in Windows, you need to install the chocolatey package manager (https://chocolatey.org/install) and then run the command `choco install make`.

The next commands are **ONLY** available in the `infrastructure` directory. So make sure to be in the `infrastructure` directory.
```bash
cd infrastructure
```

### Launch the project
Initialize the infrastructure of the project, by running the following command:

```bash
make init
```

To create the infrastructure on AWS, you will need to run the following command:

```bash
make up
```
✅ If everything launched successfully, you can start the next section Installation of the mobile app.

⚠️ Otherwise, please contact us by opening directly an issue on the Issues section of this repository.


### Destroy the project

To destroy the infrastructure on AWS, you will need to run the following command:

```bash
make down
```

## Installing the mobile application (Android)

To install the Safety Drive mobile application, go to `safety-drive/mobile_app/` and copy the `app_safety_drive.apk` file to your smartphone.

Then, run the .apk file

## Infrastructure

<img title="PA-4IABD1" width="1280" height="720" src="https://app.terrastruct.com/diagrams/1985152524" />
------------------------------

*Safety Drive is a school project, please do not use it for commercial purposes.*