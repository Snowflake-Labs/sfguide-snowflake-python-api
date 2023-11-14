FROM public.ecr.aws/lambda/python:3.11

# Install your dependencies
RUN yum -y install openssl

COPY requirements.txt  .
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
COPY . ${LAMBDA_TASK_ROOT}

CMD ["app.handler"]

