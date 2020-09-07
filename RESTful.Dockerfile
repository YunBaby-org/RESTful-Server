FROM python:3.8

# setup user
RUN useradd -ms /bin/bash restful
USER restful

# setup working directory
WORKDIR /home/restful/app

# install dependencies
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy source files
COPY . .

# executing
CMD [ "python", "./RESTful_server.py" ]
