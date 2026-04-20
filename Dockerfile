FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    ffmpeg \
    espeak-ng \
    espeak-ng-data \
    libespeak-ng1 \
    libespeak-ng-dev \
    festival \
    alsa-utils \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH
ENV PATH="/root/.cargo/bin:/root/.local/bin:$PATH"

COPY . .

RUN uv pip install --system --no-cache -r requirements.txt
RUN uv pip install --system --no-cache streamlit

ENV PORT=8080
EXPOSE $PORT

ENTRYPOINT ["sh", "-c", "uv run python -m streamlit run app.py --server.port=$PORT --server.address=0.0.0.0"]