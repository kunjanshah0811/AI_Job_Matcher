FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/kunjanshah0811/AI_Job_Matcher.git .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip3 install --no-cache-dir streamlit

# Use $PORT environment variable that Render sets
ENV PORT=8501

EXPOSE $PORT

HEALTHCHECK CMD curl --fail http://localhost:$PORT/_stcore/health

# Use ENTRYPOINT with python -m for more reliable execution
ENTRYPOINT ["sh", "-c", "python -m streamlit run Home.py --server.port=$PORT --server.address=0.0.0.0"]