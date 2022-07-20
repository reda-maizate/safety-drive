# Safety Drive
4th year AI and Big Data Annual Project made by Réda MAIZATE, Cédric GARVENES and Nacim MESSACI.

## Prerequisites

Step 1 : To run the project, you will need to have **Docker**, **Terraform**, **AWS CLI** installed on your computer and **AWS account**.

Step 2 : After Docker, Terraform and AWS CLI installed and your AWS Account created, you now need to create a file called `terraform.tfvars` in the directory `infrastructure/terraform` of the project.
You should copy the content of the file `terraform.tfvars.example` to this file and adapt it to your needs.
```
# This file is used to configure the Terraform project.

# General
aws_account_id                  = "" # Your AWS account ID (e.g., 123456789012)
region                          = "" # Your AWS region (e.g., us-east-1)
bucket_name                     = ""
profile_name                    = ""
ecr_repository_name             = ""
lambda_role_name                = ""
os                              = ""

# Pipeline
function_name_pipeline          = ""
lambda_iam_policy_name_pipeline = ""

# Web App
function_name_web_app           = ""
api_gateway_name                = ""
```

Final step : After your `terraform.tfvars` created and filled, launch the Docker application.

## Usage
**_WARNING_** : If you are in Windows, you need to install the chocolatey package manager (https://chocolatey.org/install) and then run the command `choco install make`.

The next commands are **ONLY** available in the `infrastructure` directory. So make sure to be in the `infrastructure` directory.

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

## Installing the mobile application (Android)

To install the Safety Drive mobile application, go to `\safety_drive_flutter_app_project\build\app\outputs\flutter-apk` and copy the `app-release.apk` file to your smartphone.

Then, run the .apk file
