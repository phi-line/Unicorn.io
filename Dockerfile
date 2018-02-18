FROM python:3.6.4

WORKDIR /
# Copy the current directory contents into the container at /app
ADD . /

RUN pip3 install pipenv
RUN pipenv install
RUN pipenv shell
EXPOSE 5000

ENV NAME unicorn

CMD ["python", "crunchbase.py"]
CMD ["python", "api.py"]