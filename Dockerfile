FROM python:3.7-stretch
RUN python3 -m pip install --user pipenv
ENV PATH="/root/.local/bin:${PATH}"
WORKDIR /app
COPY . .
RUN pipenv install
EXPOSE 1234/tcp
CMD [ "pipenv", "run", "python", "main.py" ]
