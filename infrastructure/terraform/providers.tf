terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "2.16.0"
    }
    null = {
      source  = "hashicorp/null"
    }
  }
}

provider "aws" {
  region = "us-east-1"
  profile = "redaprofile"
}