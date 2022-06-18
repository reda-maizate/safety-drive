FROM public.ecr.aws/lambda/python:3.8-arm64

RUN yum update -y && yum install mesa-libGL -y

COPY src/ ${LAMBDA_TASK_ROOT}
COPY requirements.txt ./

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

CMD ["lambda_function.lambda_handler"]