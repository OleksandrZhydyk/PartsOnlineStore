FROM python:3.10

RUN apt update

RUN mkdir "PartsOnlineStore"

WORKDIR /PartsOnlineStore

COPY ./src ./src
#COPY ./requirements.txt ./requirements.txt
COPY ./Pipfile ./Pipfile

RUN python -m pip install --upgrade pip
#RUN pip install -r ./requirements.txt
RUN pip install pipenv
RUN pipenv install
RUN pipenv install --dev

#CMD ["python", "src/manage.py", "runserver", "0:8008"]
CMD ["pipenv", "run", "python", "src/manage.py", "runserver", "0:8008"]