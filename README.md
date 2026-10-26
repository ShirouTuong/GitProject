# BÁO CÁO BÀI KIỂM TRA CUỐI KỲ: TRIỂN KHAI VÀ QUẢN TRỊ HỆ THỐNG PHẦN MỀM

## THÔNG TIN SINH VIÊN & ĐỀ TÀI
- **Họ và tên:** Trịnh Ngọc Tường
- **Mã số sinh viên (MSSV):** DTC245200211
- **Số thứ tự (STT):** 54
- **Đề tài số 14:** **Hệ thống Quản lý Dự án (Project Management)**
- **Lớp:** CNTTK23E
- **Giảng viên phụ trách:** Bộ môn Triển khai và quản trị hệ thống phần mềm
- **Đơn vị đào tạo:** Khoa Công nghệ Thông tin - Trường Đại học Công nghệ Thông tin và Truyền thông Thái Nguyên (ICTU)
- **Năm thực hiện:** 2026

---

## 1. TỔNG QUAN KIẾN TRÚC HỆ THỐNG

Hệ thống được thiết kế và triển khai hoàn toàn theo kiến trúc Microservices container hóa với **Docker** và **Docker Compose**, tích hợp đầy đủ các tiêu chuẩn bảo mật Hardening và hệ sinh thái Giám sát & Quản lý Log tập trung:

```
[ Internet / Client Browser ]
             │
             │ HTTP (Port 80) -> Chuyển hướng 301 HTTPS
             ▼
     ┌────────────────────────────────────────────────────────┐
     │           Nginx Reverse Proxy & SSL Gateway            │
     │                 (Port 80 / 443 HTTPS)                  │
     │      Security Headers: X-Frame, X-Content, X-XSS       │
     └───────────────────────────┬────────────────────────────┘
                                 │ frontend_net (Bridge)
                                 ▼
     ┌────────────────────────────────────────────────────────┐
     │        Ứng dụng Web: Quản lý Dự án (Node.js)           │
     │         Non-root User (appuser UID 1001) - Port 3000   │
     │         Endpoints: REST APIs, /metrics, Log Errors     │
     └─────────────┬───────────────────────────┬──────────────┘
                   │                           │
  backend_net      │                           │ monitoring_net
  (Internal)       │                           │
                   ▼                           ▼
┌───────────────────────────────┐  ┌─────────────────────────────────────┐
│  Cơ sở dữ liệu PostgreSQL 15 │  │        HỆ THỐNG QUAN SÁT VÀ LOG     │
│  (Port 5432 - Cô lập nội bộ)  │  │  • Prometheus (Port 9090 - Metrics) │
│  + Adminer UI (Port 8080)     │  │  • Grafana (Port 3001 - Dashboards) │
└───────────────────────────────┘  │  • Loki (Port 3100 - Lưu trữ Log)   │
                                   │  • Promtail (Đọc Docker Container)  │
                                   │  • cAdvisor (Port 8085 - Resource)  │
                                   └─────────────────────────────────────┘
```

---

## 2. BẢNG TỔNG HỢP DỊCH VỤ VÀ CỔNG TRUY CẬP

| STT | Dịch Vụ | Tên Container | Cổng Host | Cổng Container | Mô Tả & Chức Năng |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **1** | **Nginx Gateway** | `pm-nginx` | **80, 443** | 80, 443 | Reverse proxy chính, định tuyến SSL tự ký, Security Headers |
| **2** | **Web Application** | `pm-webapp` | *Nội bộ* | 3000 | Hệ thống Quản lý Dự án (REST APIs, Kanban, `/metrics`) |
| **3** | **PostgreSQL** | `pm-database` | *Cô lập* | 5432 | Hệ quản trị CSDL, phân tách mạng `backend_net` |
| **4** | **Adminer** | `pm-adminer` | **8080** | 8080 | Giao diện Web quản trị CSDL trực quan |
| **5** | **Prometheus** | `pm-prometheus` | **9090** | 9090 | Thu thập và lưu trữ số liệu metrics hệ thống |
| **6** | **Grafana** | `pm-grafana` | **3001** | 3000 | Trực quan hóa Metrics & Log Explorer qua Dashboard |
| **7** | **Grafana Loki** | `pm-loki` | **3100** | 3100 | Engine tập trung hóa và tra cứu log bằng LogQL |
| **8** | **Promtail** | `pm-promtail` | *Nội bộ* | 9080 | Daemon thu thập log từ Docker containers đẩy về Loki |
| **9** | **cAdvisor** | `pm-cadvisor` | **8085** | 8080 | Giám sát CPU, Ram, Network I/O của toàn bộ Containers |

---

## 3. TIẾN ĐỘ THỰC HIỆN THEO CÁC BƯỚC ĐỀ THI

### Bước 1 & Bước 2: Triển khai Ứng dụng Web & Cơ sở dữ liệu
- Xây dựng ứng dụng **Quản lý Dự án** với đầy đủ các nghiệp vụ:
  + Quản lý danh mục Dự án (Tên, mô tả, ngày bắt đầu, deadline, tiến độ %, mức độ ưu tiên).
  + Bảng công việc **Kanban Board** 3 trạng thái: *To Do*, *In Progress*, *Done*.
  + Quản lý thành viên nhóm dự án.
- Tự động kết nối cơ sở dữ liệu **PostgreSQL 15** và tự động khởi tạo bảng dữ liệu mẫu (`projects`, `tasks`, `team_members`).
- Tích hợp công cụ **Adminer** trên cổng `8080` để xem và thao tác dữ liệu.

### Bước 3 (Commit 1): Cấu hình Nginx Reverse Proxy & Bảo mật SSL
- Nginx đóng vai trò cổng giao tiếp duy nhất đón nhận request từ bên ngoài:
  + Tự động chuyển hướng toàn bộ truy cập HTTP (`http://localhost:80`) sang HTTPS (`https://localhost:443`).
  + Tích hợp chứng chỉ **SSL tự ký (Self-signed Certificate)** chuẩn RSA 2048-bit.
  + Áp dụng đầy đủ các **Security Headers**:
    * `X-Frame-Options: SAMEORIGIN` (Chống Clickjacking)
    * `X-Content-Type-Options: nosniff` (Chống MIME-sniffing)
    * `X-XSS-Protection: 1; mode=block` (Chống tấn công XSS)
    * `Referrer-Policy: strict-origin-when-cross-origin`
    * `Content-Security-Policy`

### Bước 4 (Commit 2): Tích hợp Prometheus + Grafana Dashboard
- Cấu hình Prometheus định kỳ cào dữ liệu (`scrape_interval: 10s`) từ:
  + Ứng dụng Web thông qua endpoint `/metrics` (`pm_http_requests_total`, `pm_http_request_duration_seconds`, `pm_active_projects_total`, `pm_tasks_total`).
  + `cadvisor`: đo lường CPU, RAM, Network I/O thời gian thực của từng container.
- Tự động nạp cấu hình Datasource và Dashboard mẫu trên **Grafana**:
  + Biểu đồ Tần suất HTTP Requests (QPS).
  + Biểu đồ Tỷ lệ Mã trạng thái HTTP (2xx, 4xx, 5xx).
  + Biểu đồ Độ trễ phản hồi p95 (Latency).
  + Thống kê Dự án và Công việc.

### Bước 5 (Commit 3): Triển khai Quản lý Log tập trung Loki + Promtail
- Promtail giám sát các container logs và Nginx logs, tự động gắn nhãn (`job="nginx"`, `job="webapp"`) và đẩy về Loki server.
- **Xác thực 2 câu truy vấn LogQL tiêu chuẩn theo yêu cầu đề tài:**
  1. **Truy vấn 1:** Lọc log lỗi HTTP 5xx từ Nginx Access Log:
     ```logql
     {job="nginx"} |= "HTTP/1.1" 5"
     ```
  2. **Truy vấn 2:** Tìm kiếm thông điệp Lỗi hoặc Ngoại lệ trong Web App:
     ```logql
     {job="webapp"} |~ "(ERROR|Exception|Failed)"
     ```
- Ứng dụng Web đã tích hợp sẵn 2 nút bấm trên giao diện và endpoint `/api/test/error`, `/api/test/exception` để tạo ngay log lỗi kiểm chứng.

### Bước 6: Áp dụng các biện pháp Hardening & Đánh giá Bảo mật
1. **Chạy dưới quyền Non-root User:** Dockerfile của ứng dụng sử dụng `USER appuser (UID 1001)`, ngăn chặn tuyệt đối leo thang đặc quyền lên máy chủ host.
2. **Phân tách mạng nội bộ (Network Isolation):**
   - Mạng `backend_net` được cấu hình `internal: true`. Container PostgreSQL không mở port ra máy host, chỉ cho phép container trong mạng nội bộ truy cập.
   - Mạng `frontend_net` dành cho Nginx và WebApp.
   - Mạng `monitoring_net` dành riêng cho cụm Prometheus, Grafana, Loki.
3. **Quản lý Biến môi trường An toàn:**
   - Sử dụng tệp `.env` riêng biệt, không hardcode thông tin nhạy cảm trong mã nguồn.
   - Cung cấp tệp `.env.example` mẫu.
4. **Nginx Hardening:**
   - Ẩn phiên bản máy chủ (`server_tokens off`).
   - Giới hạn kích thước buffer và rate limiting (`limit_req_zone`) chống tấn công DoS / brute-force.

---

## 4. HƯỚNG DẪN CÀI ĐẶT VÀ VẬN HÀNH HỆ THỐNG

### Yêu cầu tiên quyết:
- Máy tính đã cài đặt **Docker** và **Docker Compose** (Docker Desktop trên Windows/macOS hoặc Docker Engine trên Linux).
- Git để quản lý mã nguồn.

### Bước 1: Clone Repository
```bash
git clone https://github.com/ShirouTuong/GitProject.git
cd GitProject
```

### Bước 2: Thiết lập Biến môi trường
```bash
# Sao chép tệp cấu hình mẫu
cp .env.example .env
```

### Bước 3: Khởi chạy toàn bộ Hệ thống
Chỉ với **01 câu lệnh duy nhất**:
```bash
docker compose up -d --build
```

Kiểm tra trạng thái các container:
```bash
docker compose ps
```

### Bước 4: Kiểm tra tự động bằng Script kiểm thử
- **Trên Linux/macOS:**
  ```bash
  chmod +x ./scripts/verify-system.sh
  ./scripts/verify-system.sh
  ```
- **Trên Windows PowerShell:**
  ```powershell
  .\scripts\verify-system.ps1
  ```

---

## 5. ĐỊA CHỈ TRUY CẬP VÀ XÁC THỰC

- **Giao diện Web Quản lý Dự án (Chính):**
  - HTTPS: [https://localhost](https://localhost) (Chấp nhận cảnh báo chứng chỉ tự ký trên trình duyệt)
  - HTTP: [http://localhost](http://localhost) (Tự động chuyển tiếp sang HTTPS)
- **Công cụ Quản trị CSDL Adminer:**
  - URL: [http://localhost:8080](http://localhost:8080)
  - Hệ quản trị: `PostgreSQL` | Máy chủ: `db` | Tên người dùng: `pm_admin` | Mật khẩu: `SecurePass@Tuong2026!DTC245200211` | CSDL: `project_db`
- **Hệ thống Giám sát Prometheus:**
  - URL: [http://localhost:9090](http://localhost:9090)
  - Kiểm tra Targets: `Status` -> `Targets` (Tất cả webapp, cadvisor ở trạng thái `UP`).
- **Bảng điều khiển Grafana:**
  - URL: [http://localhost:3001](http://localhost:3001)
  - Tài khoản mặc định: `admin` / Mật khẩu: `AdminSecure@2026!`
  - Truy cập Dashboard: `Dashboards` -> `Hệ thống Quản lý Dự án - DevOps Dashboard`.
  - Tra cứu Log: Vào mục `Explore`, chọn datasource `Loki` và dán câu truy vấn LogQL để kiểm tra.

---

## 6. LỊCH SỬ COMMITS THEO TIẾN ĐỘ ĐỀ BÀI

- `Commit 1`: Triển khai Ứng dụng Web Quản lý Dự án, Cơ sở dữ liệu PostgreSQL, pgAdmin 4, Adminer và Nginx Reverse Proxy (SSL & Security Headers).
- `Commit 2`: Tích hợp Hệ thống Giám sát Số liệu Prometheus và Bảng điều khiển Grafana Dashboard.
- `Commit 3`: Tích hợp Hệ thống Quản lý Nhật ký Log tập trung Loki + Promtail và xác thực 3 câu truy vấn LogQL.
- `Commit 4`: Áp dụng toàn diện các biện pháp Hardening (Non-root user, Network Isolation, Rate Limiting), hoàn thiện Scripts kiểm thử và Báo cáo.
