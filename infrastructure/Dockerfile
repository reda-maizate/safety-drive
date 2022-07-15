FROM public.ecr.aws/lambda/python:3.6.2022.01.11.19
WORKDIR ${LAMBDA_TASK_ROOT}

RUN yum update -y && yum install mesa-libGL -y

COPY src/lambda/pipeline .
COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["lambda_function.lambda_handler"]