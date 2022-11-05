FROM python:3.7.3-stretch
EXPOSE 8001

WORKDIR $HOME/src
COPY . $HOME/src/
RUN pip3 install -r $HOME/src/requirements.txt

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]