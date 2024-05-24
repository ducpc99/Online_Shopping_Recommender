<<<<<<< HEAD
# Sử dụng image python làm base image
FROM python:3.9

# Đặt thư mục làm việc
WORKDIR /app

# Cài đặt các gói cần thiết cho locale
RUN apt-get update && apt-get install -y locales \
    && sed -i '/vi_VN.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen

# Thiết lập biến môi trường locale
=======
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
>>>>>>> f2c1ddf112f9217eb0f9438daa0d3b2537019c71
ENV LANG vi_VN.UTF-8
ENV LANGUAGE vi_VN:vi
ENV LC_ALL vi_VN.UTF-8

<<<<<<< HEAD
# Copy các tệp requirements.txt vào container
COPY requirements.txt /app/

# Cài đặt các dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install mysqlclient
RUN pip install python-slugify

# Copy tất cả các tệp dự án vào container
COPY . /app/

# Thiết lập biến môi trường
ENV PYTHONUNBUFFERED 1

# Chạy lệnh migrate, import sản phẩm và collectstatic khi container khởi động
CMD ["sh", "-c", "python manage.py migrate && python manage.py import_products && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]
=======
# Copy toàn bộ mã nguồn vào container
COPY . .

# Copy script chờ
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Mở cổng 8000
EXPOSE 8000

# Chạy lệnh khởi động Django
CMD ["/wait-for-it.sh", "db:3306", "--", "python", "manage.py", "runserver", "0.0.0.0:8000"]
>>>>>>> f2c1ddf112f9217eb0f9438daa0d3b2537019c71
