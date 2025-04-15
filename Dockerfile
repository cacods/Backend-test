FROM public.ecr.aws/sam/build-python3.11:latest

# Install jq (for JSON parsing)
RUN yum install -y jq

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x /app/entrypoint.sh

CMD ["/bin/bash", "/app/entrypoint.sh"]