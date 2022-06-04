init:
	cd terraform/; terraform init; cd ../

up:
	cd terraform/; terraform apply -var-file=terraform.tfvars -auto-approve; cd ../

down:
	cd terraform/; terraform destroy -var-file=terraform.tfvars -auto-approve; cd ../