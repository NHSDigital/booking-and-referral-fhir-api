FROM public.ecr.aws/lambda/python:3.9

COPY examples ${LAMBDA_TASK_ROOT}/examples/
COPY app.py ${LAMBDA_TASK_ROOT}

#COPY requirements.txt  .
#RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

CMD [ "app.handler" ]
