terraform {
  required_providers {
    iterative = {
      source = "iterative/iterative"
    }
  }
}

provider "iterative" {}

resource "iterative_task" "example-basic" {
  cloud   = "aws"    # or any of: gcp, az, k8s
  machine = "m"      # medium. Or any of: l, xl, m+k80, xl+v100, ...
  spot    = 0        # auto-price. Default -1 to disable, or >0 for hourly USD limit
  timeout = 24*60*60 # 24h
  image   = "ubuntu"

  storage {
    workdir = "../src"
    output  = "results"
  }
  environment = { TF_CPP_MIN_LOG_LEVEL = "1" }
  script = <<-END
    #!/bin/bash
    sudo apt-get update -q
    sudo apt-get install -yq python3-pip
    pip3 install -r requirements.txt tensorflow-cpu==2.8.0
    python3 train.py --output results-basic/metrics.json
  END
}