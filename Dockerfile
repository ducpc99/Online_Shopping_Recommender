FROM python:3.9-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy file requirements.txt vào thư mục làm việc trong container
COPY requirements.txt .

# Cài đặt các dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc musl-dev default-libmysqlclient-dev pkg-config netcat-openbsd locales && \
    echo "vi_VN.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen vi_VN.UTF-8 && \
    update-locale LANG=vi_VN.UTF-8 && \
    pip install -r requirements.txt && \
    apt-get purge -y --auto-remove gcc musl-dev && \
    rm -rf /var/lib/apt/lists/*

# Thiết lập biến môi trường cho locale
ENV LANG vi_VN.UTF-8
ENV LANGUAGE vi_VN:vi
ENV LC_ALL vi_VN.UTF-8

# Copy toàn bộ mã nguồn vào container
COPY . .

# Copy script chờ
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Mở cổng 8000
EXPOSE 8000

# Chạy lệnh khởi động Django
CMD ["/wait-for-it.sh", "db:3306", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]
