FROM python:3.9.7

WORKDIR /COVID


COPY requirements.txt .

RUN pip install -r requirements.txt 


COPY service_account.json .
COPY tool_V3.py .
COPY msgraph.py .


CMD ["python", "tool_V3.py"] 