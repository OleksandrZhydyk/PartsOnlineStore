FROM python:3.10

RUN apt update

RUN mkdir "PartsOnlineStore"

WORKDIR /PartsOnlineStore

COPY ./src ./src
#COPY ./requirements.txt ./requirements.txt
COPY ./Pipfile ./Pipfile
COPY ./Pipfile.lock ./Pipfile.lock
COPY ./commands ./commands


RUN python -m pip install --upgrade pip
#RUN pip install -r ./requirements.txt
RUN pip install pipenv
RUN pipenv install --system --deploy
RUN chmod +x ./commands/*


CMD ["bash"]