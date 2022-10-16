FROM python:3.10

RUN apt update

RUN mkdir "PartsOnlineStore"

WORKDIR /PartsOnlineStore

COPY ./src ./src
#COPY ./requirements.txt ./requirements.txt
COPY ./Pipfile ./Pipfile
COPY ./commands/start_server.sh ./commands/start_server.sh
RUN chmod +x ./commands/start_server.sh

RUN python -m pip install --upgrade pip
#RUN pip install -r ./requirements.txt
RUN pip install pipenv
RUN pipenv install
RUN pipenv install --dev

CMD ["bash"]