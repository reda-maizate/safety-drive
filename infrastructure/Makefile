# Install the lambda's dependencies and put it in the lambda function.
up:
	docker-compose build
	docker-compose --env-file .env up --abort-on-container-exit --exit-code-from create_python_package_dependencies