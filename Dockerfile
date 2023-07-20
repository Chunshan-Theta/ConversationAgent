# 使用官方的 Python 映像檔作為基底
FROM python:3.9-slim-buster

# 設定工作目錄
WORKDIR /app

# 複製專案檔案到 Docker 容器中
COPY . /app

# 安裝相依套件
RUN pip install --no-cache-dir -r requirement.txt

# 指定執行的命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]