# 
FROM python:3.9

# 
COPY ./app /code/app

# 
COPY ./requirements.txt /code

# 
WORKDIR /code



# 
RUN pip3 install -r requirements.txt


# 
CMD ["uvicorn", "app.main:app", "--host", "128.0.0.1", "--port", "8088"]
