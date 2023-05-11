FROM python:3.8-slim

WORKDIR /app

RUN git clone https://github.com/MatteoFasulo/HypeAPI .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=127.0.0.1"]