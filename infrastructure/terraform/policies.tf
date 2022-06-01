################ Policies ################

# Create the Lambda IAM policy
data "aws_iam_policy_document" "policy_lambda_iam" {
  statement {
    sid     = ""
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

# Create the S3 IAM role
data "aws_iam_policy_document" "policy_s3" {
  statement {
    sid       = ""
    effect    = "Allow"
    resources = ["*"]

    actions = [
      "s3:*",
      "ses:*",
    ]
  }
}