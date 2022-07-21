terraform {
  required_providers {
    iterative = {
      source = "iterative/iterative"
    }
    aws = {
      source = "hashicorp/aws"
      version = "4.17.1"
    }
  }
}

provider "iterative" {}

provider "aws" {
  profile     = var.profile_name
  max_retries = 1
}

resource "iterative_task" "example-basic" {
  cloud   = "aws"    # or any of: gcp, az, k8s
  machine = "m"      # medium. Or any of: l, xl, m+k80, xl+v100, ...
  spot    = -1      # auto-price. Default -1 to disable, or >0 for hourly USD limit
  timeout = 60*60    # 1h
  image   = "ubuntu"
  region  = var.region

  storage {
    workdir = "../src"
    output  = "results-tpi"
  }
  environment = { TF_CPP_MIN_LOG_LEVEL = "1" }
  script = <<-END
    #!/bin/bash
    sudo apt-get update -q
    sudo apt-get install -yq python3-pip
    pip3 install -r requirements.txt
    python3 train.py
  END
}