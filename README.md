# Online Shopping Final Project

This is the final project for the Online Shopping application. It uses Docker to manage and deploy the application.

## Hướng dẫn sử dụng

### Yêu cầu
- Docker
- Docker Compose

### Cài đặt và khởi động dự án

1. **Xây dựng Docker image:**
    ```sh
    docker-compose build
    ```

2. **Chạy lệnh migrate:**
    ```sh
    docker-compose run web python manage.py migrate
    ```

3. **Import sản phẩm:**
    ```sh
    docker-compose run web python manage.py import_products
    ```

4. **Khởi động dịch vụ:**
    ```sh
    docker-compose up
    ```
5. **Truy cập địa chỉ:**
    ```sh
    http://127.0.0.1:8000/  or localhost:8000
    ```

### Tài khoản Admin

- Email: manager@example.com
- Mật khẩu: managerpass1234

## Đóng góp

1. Fork this repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Create a new Pull Request

## Giấy phép

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
