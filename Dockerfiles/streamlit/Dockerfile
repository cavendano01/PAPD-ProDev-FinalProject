FROM python:3.7-slim-buster
EXPOSE 8501
WORKDIR /usr/local/streamlit
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .