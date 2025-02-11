FROM pytorch/pytorch:latest
WORKDIR /crawl
COPY . .

# 로케일 설정
ENV LC_ALL ko_KR.UTF-8 
RUN apt-get update && apt-get install -y locales \
    && locale-gen ko_KR.UTF-8

# 필수 패키지 설치
RUN apt-get update && apt-get install -y \
    python3-pip \
    wget \
    curl \
    gnupg \
    vim \
    apt-transport-https \
    ca-certificates \
    unzip \
    --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Google Chrome 설치
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ChromeDriver 설치
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip

# Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt