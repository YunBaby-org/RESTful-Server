FROM python:3.8

# setup user
RUN useradd -ms /bin/bash auth
USER auth

# setup working directory
WORKDIR /home/auth/app

# install dependencies
COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy source files
COPY . .

# executing
CMD [ "python", "./Auth_Server.py" ]
