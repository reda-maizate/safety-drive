FROM public.ecr.aws/lambda/python:3.8-arm64

RUN yum update -y && yum install mesa-libGL -y

COPY src/lambda_function.py ${LAMBDA_TASK_ROOT}
COPY requirements.txt .

RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
CMD ["lambda_function.lambda_handler"]