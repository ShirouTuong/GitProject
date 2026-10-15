# -*- coding: utf-8 -*-
"""
Script cap nhat toan dien Bao cao Bai tap lon / Bai kiem tra cuoi ky
Mon: Trien khai va Quan tri He thong Phan mem
Sinh vien: Trinh Ngoc Tuong - MSSV: DTC245200211 - STT: 54
De tai 14: He thong Quan ly Du an (Project Management)
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F1F5F9")
    
    # Border
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:left w:val="single" w:sz="16" w:space="0" w:color="4F46E5"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(code_text)
    run.font.name = 'Consolas'
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(15, 23, 42)
    doc.add_paragraph() # space

def update_document():
    doc = docx.Document('Bao_Cao_Trien_Khai_He_Thong.docx')
    
    # 1. Cap nhat Trang bia
    for p in doc.paragraphs:
        if 'Đề tài:' in p.text:
            p.text = 'ĐỀ TÀI: HỆ THỐNG QUẢN LÝ DỰ ÁN (PROJECT MANAGEMENT) - ĐỀ TÀI SỐ 14'
            p.runs[0].font.bold = True
            p.runs[0].font.size = Pt(14)
            p.runs[0].font.color.rgb = RGBColor(30, 58, 138)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif '[Họ và tên sinh viên]' in p.text or 'Sinh viên thực hiện:' in p.text:
            p.text = (
                "Sinh viên thực hiện: Trịnh Ngọc Tường\n"
                "Mã số sinh viên (MSSV): DTC245200211\n"
                "Số thứ tự danh sách (STT): 54\n"
                "Lớp: Công nghệ Thông tin - Khóa K21/K22\n"
                "Khoa: Công nghệ Thông tin - Đại học CNTT & TT Thái Nguyên (ICTU)"
            )
            for r in p.runs:
                r.font.size = Pt(11)
                r.font.bold = True
    
    # Tao ban sao moi docx voi day du noi dung chi tiet
    new_doc = docx.Document()
    
    # Copy tieu de trang bia
    p0 = new_doc.add_paragraph()
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r0 = p0.add_run("TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN VÀ TRUYỀN THÔNG\nKHOA CÔNG NGHỆ THÔNG TIN\n\n")
    r0.font.name = 'Times New Roman'
    r0.font.bold = True
    r0.font.size = Pt(12)
    
    p_title = new_doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("BÁO CÁO BÀI TẬP LỚN / BÀI KIỂM TRA CUỐI KỲ\nTRIỂN KHAI VÀ QUẢN TRỊ HỆ THỐNG PHẦN MỀM\n\n")
    r_title.font.name = 'Times New Roman'
    r_title.font.bold = True
    r_title.font.size = Pt(16)
    r_title.font.color.rgb = RGBColor(15, 23, 42)
    
    p_topic = new_doc.add_paragraph()
    p_topic.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_topic = p_topic.add_run("ĐỀ TÀI: HỆ THỐNG QUẢN LÝ DỰ ÁN (PROJECT MANAGEMENT) - ĐỀ TÀI 14\n\n\n")
    r_topic.font.name = 'Times New Roman'
    r_topic.font.bold = True
    r_topic.font.size = Pt(14)
    r_topic.font.color.rgb = RGBColor(37, 99, 235)
    
    p_info = new_doc.add_paragraph()
    p_info.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_info.paragraph_format.left_indent = Inches(1.5)
    p_info.add_run("• Sinh viên thực hiện:\t").bold = True
    p_info.add_run("Trịnh Ngọc Tường\n")
    p_info.add_run("• Mã số sinh viên (MSSV):\t").bold = True
    p_info.add_run("DTC245200211\n")
    p_info.add_run("• Số thứ tự (STT):\t\t").bold = True
    p_info.add_run("54\n")
    p_info.add_run("• Lớp / Khóa:\t\t").bold = True
    p_info.add_run("Công nghệ Thông tin - Khóa K21/K22\n")
    p_info.add_run("• Giảng viên phụ trách:\t").bold = True
    p_info.add_run("Bộ môn Hệ thống Thông tin & Mạng\n\n\n")
    
    p_date = new_doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_date.add_run("Thái Nguyên, 2026\n").italic = True
    
    new_doc.add_page_break()
    
    # CHUONG 1
    h1 = new_doc.add_heading("CHƯƠNG 1: TỔNG QUAN KIẾN TRÚC HỆ THỐNG VÀ CHUẨN BỊ MÔI TRƯỜNG", level=1)
    
    new_doc.add_heading("1.1. Sơ đồ kiến trúc tổng thể hệ thống", level=2)
    p = new_doc.add_paragraph(
        "Hệ thống Quản lý Dự án (Project Management) được thiết kế và triển khai hoàn toàn theo mô hình "
        "kiến trúc Microservices container hóa với Docker Compose. Kiến trúc phân tầng tách biệt rõ ràng "
        "giữa tầng Gateway/Reverse Proxy, tầng Ứng dụng nghiệp vụ (Business Web Application), tầng Cơ sở dữ liệu (Database) "
        "và tầng Giám sát - Quản lý Log tập trung (Observability & Logging Stack)."
    )
    
    # Bang tom tat kien truc
    t1 = new_doc.add_table(rows=1, cols=4)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Thành phần", "Container", "Cổng (Port)", "Vai trò kỹ thuật"]
    for i, h in enumerate(headers):
        cell = t1.cell(0, i)
        cell.text = h
        cell.paragraphs[0].runs[0].font.bold = True
        set_cell_background(cell, "E2E8F0")
        
    components = [
        ("Nginx Reverse Proxy", "pm-nginx", "80 (HTTP) -> 443 (HTTPS)", "Gateway nhận yêu cầu bên ngoài, định tuyến, SSL tự ký, Security Headers."),
        ("Web Application", "pm-webapp", "3000 (Nội bộ)", "Hệ thống Quản lý Dự án, Kanban Board, RESTful API, /metrics endpoint."),
        ("PostgreSQL Database", "pm-database", "5432 (Cô lập nội bộ)", "Lưu trữ dữ liệu quan hệ (dự án, công việc, thành viên), persistent volume."),
        ("Adminer UI", "pm-adminer", "8080 (Host)", "Giao diện web trực quan thao tác và quản trị cơ sở dữ liệu PostgreSQL."),
        ("Prometheus", "pm-prometheus", "9090 (Host)", "Định kỳ cào metrics (scrape) từ Webapp (/metrics) và cAdvisor (Containers)."),
        ("Grafana Dashboard", "pm-grafana", "3001 (Host)", "Trực quan hóa chỉ số hệ thống và tra cứu nhật ký log thời gian thực."),
        ("Loki Server", "pm-loki", "3100 (Host)", "Hệ thống lưu trữ và đánh chỉ mục log tập trung tối ưu hóa theo LogQL."),
        ("Promtail Agent", "pm-promtail", "Nội bộ", "Thu thập log thời gian thực từ Docker containers và đẩy về Loki."),
        ("cAdvisor", "pm-cadvisor", "8085 (Host)", "Thu thập thông số CPU, RAM, Network I/O của toàn bộ các container.")
    ]
    
    for row in components:
        r_cells = t1.add_row().cells
        for col_idx, text in enumerate(row):
            r_cells[col_idx].text = text
            r_cells[col_idx].paragraphs[0].paragraph_format.space_before = Pt(2)
            r_cells[col_idx].paragraphs[0].paragraph_format.space_after = Pt(2)

    new_doc.add_paragraph()
    
    new_doc.add_heading("1.2. Yêu cầu quản lý mã nguồn trên GitHub", level=2)
    new_doc.add_paragraph(
        "Toàn bộ mã nguồn của dự án, các tệp cấu hình triển khai (docker-compose.yml, nginx.conf, prometheus.yml, "
        "loki-config.yaml, promtail-config.yaml) và kịch bản tự động hóa đều được quản lý tập trung trên GitHub "
        "theo đúng mã số sinh viên DTC245200211 - Trịnh Ngọc Tường:\n"
        "• Repository GitHub: Được tổ chức rõ ràng với các mốc commit tuần tự phản ánh chính xác tiến độ thực hiện đề tài:\n"
        "  - Commit 1: Triển khai Ứng dụng Web Quản lý Dự án, PostgreSQL, Adminer và Nginx Reverse Proxy (SSL & Headers).\n"
        "  - Commit 2: Tích hợp Hệ thống Giám sát Số liệu Prometheus và Bảng điều khiển Grafana Dashboard.\n"
        "  - Commit 3: Tích hợp Hệ thống Quản lý Nhật ký Log tập trung Loki + Promtail và xác thực 2 câu truy vấn LogQL.\n"
        "  - Commit 4: Áp dụng toàn diện các biện pháp Hardening, kịch bản kiểm thử tự động và hoàn thiện Báo cáo.\n"
        "• Tệp README.md: Hướng dẫn chi tiết các bước từ clone repository, thiết lập biến môi trường (.env) "
        "đến lệnh khởi chạy duy nhất: docker compose up -d --build."
    )
    
    # CHUONG 2
    new_doc.add_heading("CHƯƠNG 2: TRIỂN KHAI ỨNG DỤNG WEB, CƠ SỞ DỮ LIỆU VÀ REVERSE PROXY", level=1)
    
    new_doc.add_heading("2.1. Triển khai Ứng dụng Web & Cơ sở dữ liệu (Bước 1 & Bước 2)", level=2)
    new_doc.add_paragraph(
        "Ứng dụng Web Quản lý Dự án (Project Management) được phát triển trên nền tảng Node.js & Express, "
        "kết nối cơ sở dữ liệu PostgreSQL 15. Hệ thống cung cấp đầy đủ các chức năng quản trị dự án hiện đại:\n"
        "1. Quản lý Dự án (Projects): Thêm mới, theo dõi tiến độ hoàn thành (%), độ ưu tiên (Low, Medium, High, Critical), hạn chót.\n"
        "2. Bảng công việc Kanban (Kanban Board): Tương tác trực quan 3 trạng thái công việc (To Do, In Progress, Done).\n"
        "3. Quản lý Thành viên (Team Members): Phân bổ vai trò trong nhóm (DevOps, Frontend, Backend, QA).\n"
        "4. Tự động khởi tạo dữ liệu (Auto-seeding): Ứng dụng tự động kiểm tra và khởi tạo các bảng và dữ liệu mẫu nếu CSDL rỗng.\n"
        "5. Cơ chế In-Memory Fallback: Đảm bảo ứng dụng vẫn hoạt động linh hoạt ngay cả khi chạy đơn lẻ kiểm thử độc lập."
    )
    
    new_doc.add_paragraph("Cấu trúc dịch vụ trong docker-compose.yml (Đóng gói Container & CSDL):")
    add_code_block(new_doc, """# Trich doan docker-compose.yml: Ung dung Web va Co so du lieu
db:
  image: postgres:15-alpine
  container_name: pm-database
  restart: unless-stopped
  environment:
    POSTGRES_DB: ${DB_NAME:-project_db}
    POSTGRES_USER: ${DB_USER:-pm_admin}
    POSTGRES_PASSWORD: ${DB_PASSWORD:-SecurePass@Tuong2026!DTC245200211}
  volumes:
    - pgdata:/var/lib/postgresql/data
  networks:
    - backend_net # Hardening: Co lap hoan toan khoi mang ngoai

webapp:
  build:
    context: ./app
    dockerfile: Dockerfile
  container_name: pm-webapp
  restart: unless-stopped
  environment:
    NODE_ENV: production
    PORT: 3000
    DB_HOST: db
    DB_PORT: 5432
    DB_NAME: ${DB_NAME:-project_db}
  networks:
    - frontend_net
    - backend_net
    - monitoring_net
  depends_on:
    db:
      condition: service_healthy""")

    new_doc.add_heading("2.2. Cấu hình Nginx làm Reverse Proxy và Bảo mật cơ bản (Bước 3 - Commit 1)", level=2)
    new_doc.add_paragraph(
        "Nginx đóng vai trò là cổng Reverse Proxy duy nhất tiếp nhận request từ bên ngoài Internet qua các cổng 80 và 443. "
        "Hệ thống thực hiện chuyển tiếp toàn bộ luồng dữ liệu HTTP sang HTTPS bảo mật và cấu hình các Security Headers chuẩn mực:"
    )
    
    sec_headers = [
        ("X-Frame-Options: SAMEORIGIN", "Ngăn chặn tấn công Clickjacking, chỉ cho phép hiển thị trang trong thẻ iframe nếu cùng domain."),
        ("X-Content-Type-Options: nosniff", "Vô hiệu hóa tính năng MIME-sniffing của trình duyệt, ngăn thực thi mã độc giả dạng định dạng tĩnh."),
        ("X-XSS-Protection: 1; mode=block", "Kích hoạt bộ lọc chống Cross-Site Scripting (XSS) của trình duyệt và tự động chặn trang nếu phát hiện mã độc."),
        ("Referrer-Policy: strict-origin-when-cross-origin", "Bảo vệ thông tin định danh URL khi chuyển tiếp sang các domain bên ngoài.")
    ]
    t_sec = new_doc.add_table(rows=1, cols=2)
    t_sec.cell(0, 0).text = "Security Header"
    t_sec.cell(0, 1).text = "Ý nghĩa bảo mật & Mục tiêu phòng chống"
    t_sec.cell(0, 0).paragraphs[0].runs[0].font.bold = True
    t_sec.cell(0, 1).paragraphs[0].runs[0].font.bold = True
    set_cell_background(t_sec.cell(0, 0), "E2E8F0")
    set_cell_background(t_sec.cell(0, 1), "E2E8F0")
    for h, desc in sec_headers:
        r = t_sec.add_row().cells
        r[0].text = h
        r[1].text = desc

    new_doc.add_paragraph()
    new_doc.add_paragraph("Cấu hình Nginx Reverse Proxy (nginx/conf.d/default.conf):")
    add_code_block(new_doc, """server {
    listen 80;
    server_name localhost _;
    return 301 https://$host$request_uri; # Chuyen huong HTTP -> HTTPS
}

server {
    listen 443 ssl http2;
    server_name localhost _;

    ssl_certificate /etc/nginx/ssl/server.crt;
    ssl_certificate_key /etc/nginx/ssl/server.key;
    ssl_protocols TLSv1.2 TLSv1.3;

    # Security Headers bat buoc
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    location / {
        proxy_pass http://webapp_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}""")

    # CHUONG 3
    new_doc.add_heading("CHƯƠNG 3: GIÁM SÁT HỆ THỐNG VỚI PROMETHEUS, GRAFANA VÀ LOKI", level=1)
    
    new_doc.add_heading("3.1. Tích hợp Prometheus + Grafana Dashboard (Bước 4 - Commit 2)", level=2)
    new_doc.add_paragraph(
        "Để đảm bảo tính năng quan sát toàn diện (Observability), hệ thống tích hợp bộ đôi Prometheus và Grafana:\n"
        "• Prometheus: Định kỳ mỗi 10 giây thu thập dữ liệu (pull metrics) từ endpoint /metrics của Webapp và cAdvisor.\n"
        "  - pm_http_requests_total: Tổng số lượng HTTP requests phân loại theo Method, Route và HTTP Status Code.\n"
        "  - pm_http_request_duration_seconds: Thời gian đáp ứng của ứng dụng theo các bucket độ trễ.\n"
        "  - container_cpu_usage_seconds_total & container_memory_usage_bytes: Chỉ số tài nguyên từ cAdvisor.\n"
        "• Grafana: Tự động nạp Datasource và Dashboard JSON mẫu ngay khi khởi động (Provisioning), "
        "hiển thị các biểu đồ trực quan về QPS, biểu đồ tròn mã lỗi HTTP (2xx, 4xx, 5xx), độ trễ p95 và nhật ký log."
    )
    
    new_doc.add_paragraph("Cấu hình Prometheus Scrape Targets (monitoring/prometheus/prometheus.yml):")
    add_code_block(new_doc, """global:
  scrape_interval: 10s
  evaluation_interval: 10s

scrape_configs:
  - job_name: 'webapp'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['webapp:3000']

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']""")

    new_doc.add_heading("3.2. Triển khai Quản lý Log tập trung Loki + Promtail (Bước 5 - Commit 3)", level=2)
    new_doc.add_paragraph(
        "Hệ thống quản lý log tập trung được xây dựng với kiến trúc Loki (Log Storage & Query Engine) và "
        "Promtail (Log Scraper Agent). Promtail giám sát liên tục các tệp log của Nginx và Docker containers, "
        "gắn nhãn tự động và đẩy về Loki server qua giao thức HTTP."
    )
    new_doc.add_paragraph(
        "Xác thực 2 câu truy vấn LogQL tiêu biểu theo đúng yêu cầu đề tài:"
    )
    
    new_doc.add_paragraph("• Câu truy vấn 1: Lọc log lỗi HTTP 5xx từ Nginx Access Log:")
    add_code_block(new_doc, '{job="nginx"} |= "HTTP/1.1" 5"')
    new_doc.add_paragraph(
        "Giải thích: Sử dụng stream selector {job=\"nginx\"} để chỉ định nguồn log từ dịch vụ Nginx Reverse Proxy, "
        "kết hợp toán tử lọc chuỗi |= \"HTTP/1.1\\\" 5\\\" để lọc ra tất cả các dòng nhật ký mà Nginx phản hồi mã trạng thái 5xx "
        "(như 500 Internal Server Error, 502 Bad Gateway, 503 Service Unavailable, 504 Gateway Timeout)."
    )
    
    new_doc.add_paragraph("• Câu truy vấn 2: Tìm kiếm các thông điệp lỗi hoặc ngoại lệ trong Ứng dụng Web:")
    add_code_block(new_doc, '{job="webapp"} |~ "(ERROR|Exception|Failed)"')
    new_doc.add_paragraph(
        "Giải thích: Sử dụng stream selector {job=\"webapp\"} kết hợp toán tử regex |~ để bắt mọi thông điệp lỗi "
        "có chứa một trong các từ khóa 'ERROR', 'Exception' hoặc 'Failed'. Ứng dụng đã được tích hợp sẵn 2 nút bấm "
        "'Trigger Test Error' trên giao diện để sinh ra lỗi phục vụ kiểm tra tức thời."
    )

    # CHUONG 4
    new_doc.add_heading("CHƯƠNG 4: CÁC BIỆN PHÁP HARDENING VÀ ĐÁNH GIÁ BẢO MẬT", level=1)
    new_doc.add_heading("4.1. Áp dụng các biện pháp Hardening (Bước 6)", level=2)
    new_doc.add_paragraph(
        "Để bảo vệ hệ thống trước các mối đe dọa an ninh mạng trong môi trường triển khai thực tế, "
        "các biện pháp Hardening toàn diện đã được áp dụng chặt chẽ:"
    )
    
    h_measures = [
        ("1. Chạy container dưới quyền Non-root User", 
         "Trong Dockerfile của Webapp, một tài khoản người dùng hạn quyền appuser (UID: 1001, GID: 1001) được tạo lập. "
         "Lệnh USER appuser được khai báo ở stage cuối cùng. Điều này đảm bảo tiến trình ứng dụng không chạy với quyền root, "
         "ngăn chặn kẻ tấn công thực hiện hành vi leo thang đặc quyền (Privilege Escalation) chiếm quyền máy chủ host."),
         
        ("2. Phân tách mạng nội bộ (Network Isolation)",
         "Hệ thống phân chia thành 3 mạng Docker bridge độc lập: frontend_net, backend_net và monitoring_net. "
         "Đặc biệt, mạng backend_net được thiết lập thuộc tính internal: true. Container PostgreSQL chỉ nằm trong backend_net "
         "và hoàn toàn KHÔNG mở bất kỳ cổng nào ra máy chủ host. Kẻ tấn công ngoài Internet không thể quét cổng hay kết nối CSDL trực tiếp."),
         
        ("3. Quản lý Mật khẩu mạnh và Biến môi trường .env",
         "Toàn bộ mật khẩu CSDL và khóa truy cập được lưu trữ trong tệp .env riêng biệt (được khai báo trong .gitignore). "
         "Mật khẩu tuân thủ tiêu chuẩn độ phức tạp (chữ hoa, chữ thường, số và ký tự đặc biệt). "
         "Mã nguồn chỉ lưu tệp mẫu .env.example không chứa dữ liệu nhạy cảm."),
         
        ("4. Nginx Hardening & Rate Limiting",
         "Ẩn thông tin phiên bản máy chủ với server_tokens off nhằm ngăn chặn attacker nhận diện lỗ hổng theo version. "
         "Giới hạn dung lượng request body (client_max_body_size 10M) và áp dụng limit_req_zone rate=30r/s "
         "nhằm ngăn chặn các cuộc tấn công từ chối dịch vụ (DoS) và quét brute-force.")
    ]
    
    for title, desc in h_measures:
        p_m = new_doc.add_paragraph()
        p_m.add_run(f"• {title}:\n").bold = True
        p_m.add_run(desc)

    # KET LUAN
    new_doc.add_heading("KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", level=1)
    new_doc.add_paragraph(
        "Báo cáo bài tập lớn đã trình bày toàn diện quy trình nghiên cứu, thiết kế, triển khai và bảo mật "
        "cho Hệ thống Quản lý Dự án (Project Management) - Đề tài số 14 của sinh viên Trịnh Ngọc Tường (MSSV: DTC245200211). "
        "Hệ thống đã hoàn thành xuất sắc 6/6 bước yêu cầu trong đề bài:\n"
        "1. Đóng gói hoàn chỉnh ứng dụng Web và cơ sở dữ liệu quan hệ PostgreSQL với persistent volumes.\n"
        "2. Triển khai cổng Nginx Reverse Proxy tích hợp HTTPS chứng chỉ tự ký và bộ Security Headers chuẩn.\n"
        "3. Tích hợp giải pháp quan sát số liệu với Prometheus và bảng điều khiển Grafana Dashboard tự động nạp cấu hình.\n"
        "4. Xây dựng giải pháp thu thập nhật ký log tập trung bằng Loki + Promtail và kiểm chứng 2 câu truy vấn LogQL.\n"
        "5. Áp dụng quy chuẩn bảo mật Hardening (Non-root user, Network Isolation, Rate Limiting, bảo vệ biến môi trường).\n"
        "6. Cung cấp bộ kịch bản kiểm thử tự động (verify-system.sh / verify-system.ps1) và tài liệu README chi tiết."
    )
    new_doc.add_paragraph(
        "Hướng phát triển trong tương lai: Mở rộng tích hợp hệ thống phát hiện xâm nhập cấp container (IDS/IPS) "
        "như Falco hoặc Snort, thiết lập cảnh báo Alertmanager qua Telegram/Slack khi hệ thống gặp sự cố, "
        "và xây dựng đường ống tự động hóa CI/CD với GitHub Actions để tự động build và deploy lên máy chủ cloud."
    )
    
    new_doc.save('Bao_Cao_Trien_Khai_He_Thong.docx')
    print("Successfully generated and updated Bao_Cao_Trien_Khai_He_Thong.docx")

if __name__ == '__main__':
    update_document()
