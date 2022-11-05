FROM python:3.7.3-stretch
EXPOSE 8001

COPY ./src $HOME/src/
COPY ./Makefile $HOME/Makefile

WORKDIR $HOME
RUN make package
RUN make test

WORKDIR $HOME/src/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]