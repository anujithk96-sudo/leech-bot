FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# yt-dlp എപ്പോഴും ലേറ്റസ്റ്റ് വേർഷൻ ആയിരിക്കാൻ ഇത് സഹായിക്കും
RUN pip install --no-cache-dir --upgrade yt-dlp

COPY . .

CMD ["python", "bot.py"]
