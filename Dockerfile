# start by pulling the python image
FROM python:3.10-buster

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# install npm and node
RUN curl -fsSL https://deb.nodesource.com/setup_lts.x | bash -
RUN apt-get install -y nodejs

# copy every content from the local file to the image
COPY . .

RUN chmod a+x run.sh
CMD ["./run.sh"]