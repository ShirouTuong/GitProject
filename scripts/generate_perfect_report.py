# -*- coding: utf-8 -*-
"""
Script tao Bao cao Bai tap lon / Bai kiem tra cuoi ky chuan mau hoc thuat ICTU
Mon: Trien khai va Quan tri He thong Phan mem
Sinh vien: Trinh Ngoc Tuong - MSSV: DTC245200211 - STT: 54
De tai 14: He thong Quan ly Du an (Project Management)
Tich hop hinh anh minh hoa truc quan cho tung phan, giu nguyen phong chu va mau chu.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_table_borders(table, color="CBD5E1", sz="4"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_code_block(doc, code_text, title=None):
    if title:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.space_before = Pt(8)
        p_t.paragraph_format.space_after = Pt(2)
        r_t = p_t.add_run(f"📋 {title}")
        r_t.font.name = 'Times New Roman'
        r_t.font.size = Pt(10.5)
        r_t.font.bold = True
        r_t.font.color.rgb = RGBColor(30, 58, 138)

    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=100, bottom=100, left=160, right=160)
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="2563EB"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(code_text)
    run.font.name = 'Consolas'
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(15, 23, 42)
    
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(4)

def add_callout_box(doc, title, content_text, box_type="info"):
    colors = {
        "info": {"bg": "EFF6FF", "border": "3B82F6", "title": "1D4ED8", "icon": "ℹ️"},
        "alert": {"bg": "FEF2F2", "border": "EF4444", "title": "B91C1C", "icon": "🚨"},
        "security": {"bg": "FFFBEB", "border": "F59E0B", "title": "B45309", "icon": "🛡️"},
        "success": {"bg": "F0FDF4", "border": "22C55E", "title": "15803D", "icon": "✅"}
    }
    c_info = colors.get(box_type, colors["info"])
    
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, c_info["bg"])
    set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
    
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{c_info["border"]}"/>'
        f'<w:left w:val="single" w:sz="28" w:space="0" w:color="{c_info["border"]}"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{c_info["border"]}"/>'
        f'<w:right w:val="single" w:sz="6" w:space="0" w:color="{c_info["border"]}"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(3)
    r_t = p.add_run(f"{c_info['icon']} {title}\n")
    r_t.font.name = 'Times New Roman'
    r_t.font.size = Pt(11)
    r_t.font.bold = True
    r_t.font.color.rgb = RGBColor.from_string(c_info["title"])
    
    r_c = p.add_run(content_text)
    r_c.font.name = 'Times New Roman'
    r_c.font.size = Pt(10)
    r_c.font.color.rgb = RGBColor(30, 41, 59)
    p.paragraph_format.line_spacing = 1.2
    
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(0)
    p_sp.paragraph_format.space_after = Pt(4)

def add_illustrated_image(doc, img_path, caption, width_inch=6.2):
    if not os.path.exists(img_path):
        return
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(8)
    p_img.paragraph_format.space_after = Pt(2)
    run_img = p_img.add_run()
    run_img.add_picture(img_path, width=Inches(width_inch))
    
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(10)
    r_cap = p_cap.add_run(caption)
    r_cap.font.name = 'Times New Roman'
    r_cap.font.size = Pt(10.5)
    r_cap.font.italic = True
    r_cap.font.bold = True
    r_cap.font.color.rgb = RGBColor(71, 85, 105) # Slate 600

def format_paragraph(p, space_after=6, line_spacing=1.25, align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    p.alignment = align
    for r in p.runs:
        r.font.name = 'Times New Roman'
        if not r.font.size:
            r.font.size = Pt(12)

def add_custom_heading(doc, text, level):
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.bold = True
    
    if level == 1:
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(8)
        r.font.size = Pt(13.5)
        r.font.color.rgb = RGBColor(30, 58, 138) # Dark Blue
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    elif level == 2:
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        r.font.size = Pt(12.5)
        r.font.color.rgb = RGBColor(37, 99, 235) # Royal Blue
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    elif level == 3:
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(4)
        r.font.size = Pt(12)
        r.font.italic = True
        r.font.color.rgb = RGBColor(15, 23, 42) # Slate 900
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    return p

def create_full_report():
    doc = docx.Document()
    
    # Canh le chuan hoc thuat A4: Tren 2cm, Duoi 2cm, Trai 3cm, Phai 2cm
    for section in doc.sections:
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(3.0)
        section.right_margin = Cm(2.0)
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        
    # =========================================================================
    # TRANG BIA CHINH QUY (THEO FORM MAU ICTU)
    # =========================================================================
    p0 = doc.add_paragraph()
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p0.paragraph_format.space_before = Pt(10)
    p0.paragraph_format.space_after = Pt(4)
    r0 = p0.add_run("TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN VÀ TRUYỀN THÔNG\n")
    r0.font.name = 'Times New Roman'
    r0.font.bold = True
    r0.font.size = Pt(13)
    r0.font.color.rgb = RGBColor(30, 58, 138)
    
    r0_sub = p0.add_run("KHOA CÔNG NGHỆ THÔNG TIN\n")
    r0_sub.font.name = 'Times New Roman'
    r0_sub.font.bold = True
    r0_sub.font.size = Pt(13)
    r0_sub.font.color.rgb = RGBColor(30, 58, 138)
    
    # Duong gach ngang trang tri
    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_line.paragraph_format.space_before = Pt(0)
    p_line.paragraph_format.space_after = Pt(36)
    r_l = p_line.add_run("━━━━━━━━━━━━━━━━━━━")
    r_l.font.bold = True
    r_l.font.color.rgb = RGBColor(148, 163, 184)
    
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(20)
    p_title.paragraph_format.space_after = Pt(12)
    r_t1 = p_title.add_run("BÁO CÁO BÀI TẬP LỚN / BÀI KIỂM TRA CUỐI KỲ\n")
    r_t1.font.name = 'Times New Roman'
    r_t1.font.bold = True
    r_t1.font.size = Pt(16)
    r_t1.font.color.rgb = RGBColor(15, 23, 42)
    
    r_t2 = p_title.add_run("TRIỂN KHAI VÀ QUẢN TRỊ HỆ THỐNG PHẦN MỀM\n")
    r_t2.font.name = 'Times New Roman'
    r_t2.font.bold = True
    r_t2.font.size = Pt(18)
    r_t2.font.color.rgb = RGBColor(30, 58, 138)
    
    p_topic = doc.add_paragraph()
    p_topic.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_topic.paragraph_format.space_before = Pt(16)
    p_topic.paragraph_format.space_after = Pt(50)
    r_top = p_topic.add_run("ĐỀ TÀI: HỆ THỐNG QUẢN LÝ DỰ ÁN (PROJECT MANAGEMENT)\nĐỀ TÀI SỐ 14")
    r_top.font.name = 'Times New Roman'
    r_top.font.bold = True
    r_top.font.size = Pt(15)
    r_top.font.color.rgb = RGBColor(37, 99, 235)
    
    # Khung thong tin sinh vien
    tbl_info = doc.add_table(rows=5, cols=2)
    tbl_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_info.autofit = False
    
    info_data = [
        ("Sinh viên thực hiện:", "Trịnh Ngọc Tường"),
        ("Mã số sinh viên (MSSV):", "DTC245200211"),
        ("Số thứ tự (STT):", "54"),
        ("Lớp / Khóa:", "CNTTK23E"),
        ("Giảng viên phụ trách:", "Bộ môn Triển khai và quản trị hệ thống phần mềm")
    ]
    
    for row_idx, (label, val) in enumerate(info_data):
        c0 = tbl_info.cell(row_idx, 0)
        c1 = tbl_info.cell(row_idx, 1)
        c0.width = Inches(2.4)
        c1.width = Inches(3.6)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(3)
        p0.paragraph_format.space_after = Pt(3)
        r0 = p0.add_run(label)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(12)
        r0.font.bold = True
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(3)
        p1.paragraph_format.space_after = Pt(3)
        r1 = p1.add_run(val)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(12)
        if row_idx in [0, 1]:
            r1.font.bold = True
            
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(80)
    p_sp.paragraph_format.space_after = Pt(0)
    
    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_d = p_date.add_run("Thái Nguyên, Năm 2026")
    r_d.font.name = 'Times New Roman'
    r_d.font.size = Pt(12)
    r_d.font.italic = True
    
    doc.add_page_break()
    
    # =========================================================================
    # CHƯƠNG 1: TỔNG QUAN KIẾN TRÚC HỆ THỐNG VÀ CHUẨN BỊ MÔI TRƯỜNG
    # =========================================================================
    add_custom_heading(doc, "CHƯƠNG 1: TỔNG QUAN KIẾN TRÚC HỆ THỐNG VÀ CHUẨN BỊ MÔI TRƯỜNG", level=1)
    
    add_custom_heading(doc, "1.1. Sơ đồ kiến trúc tổng thể", level=2)
    p = doc.add_paragraph(
        "Hệ thống Quản lý Dự án (Project Management) - Đề tài số 14 được nghiên cứu, thiết kế và triển khai "
        "hoàn toàn theo mô hình kiến trúc Microservices container hóa với Docker và Docker Compose. "
        "Mô hình kiến trúc được phân tách thành các phân tầng rõ ràng, độc lập về mặt chức năng nhưng "
        "kết nối chặt chẽ và an toàn thông qua các mạng ảo nội bộ (Docker bridge networks). "
        "Thiết kế này đảm bảo các tiêu chuẩn khắt khe về tính sẵn sàng cao (High Availability), "
        "khả năng quan sát toàn diện (Full Observability) và an toàn thông tin theo nguyên tắc phòng thủ đa lớp (Defense-in-Depth)."
    )
    format_paragraph(p)
    
    p_zones = doc.add_paragraph(
        "Hệ thống phân chia hạ tầng thành 4 phân vùng chính như sau:\n"
        "1. Vùng Gateway / Reverse Proxy (Nginx): Là điểm tiếp nhận duy nhất toàn bộ luồng lưu lượng truy cập từ mạng Internet qua cổng chuẩn HTTP (80) và HTTPS (443), thực hiện giải mã SSL (SSL Termination), áp dụng các chính sách bảo mật HTTP Security Headers và chuyển tiếp yêu cầu đến vùng ứng dụng nội bộ.\n"
        "2. Vùng Ứng dụng nghiệp vụ (Business Web Application): Chạy dịch vụ Web Quản lý Dự án bằng Node.js và Express, xử lý nghiệp vụ Kanban, REST APIs và xuất bản chỉ số đo lường hiệu năng (/metrics).\n"
        "3. Vùng Cơ sở dữ liệu (Database Tier): Hệ quản trị CSDL quan hệ PostgreSQL 15 được đặt trong mạng cô lập hoàn toàn (internal: true), không mở bất kỳ cổng nào ra máy chủ host, đi kèm công cụ Adminer UI phục vụ công tác quản trị dữ liệu trực quan.\n"
        "4. Vùng Giám sát và Quản lý Log tập trung (Observability & Logging Stack): Bao gồm Prometheus (thu thập metrics), Grafana (trực quan hóa bảng điều khiển và quản trị cảnh báo), Loki (lưu trữ và đánh chỉ mục log tập trung), Promtail (log agent thu thập log containers thời gian thực), cAdvisor và Node Exporter (giám sát tài nguyên phần cứng máy chủ và containers)."
    )
    format_paragraph(p_zones)
    
    # Hinh anh minh hoa Kien truc
    add_illustrated_image(
        doc,
        "docs_images/arch_diagram.png",
        "Hình 1.1: Sơ đồ Kiến trúc Phân tầng Microservices của Hệ thống Quản lý Dự án",
        width_inch=6.3
    )
    
    p_t_intro = doc.add_paragraph("Bảng 1.1 tổng hợp toàn diện danh mục các dịch vụ, tên container, cổng kết nối và vai trò kỹ thuật trong hệ thống:")
    format_paragraph(p_t_intro)
    
    # Bang danh muc dich vu
    t_services = doc.add_table(rows=1, cols=5)
    t_services.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_services)
    
    headers = ["STT", "Thành phần dịch vụ", "Tên Container", "Cổng (Host / Container)", "Vai trò & Chức năng kỹ thuật"]
    for i, h in enumerate(headers):
        c = t_services.cell(0, i)
        c.text = h
        c.paragraphs[0].runs[0].font.bold = True
        c.paragraphs[0].runs[0].font.size = Pt(10)
        c.paragraphs[0].runs[0].font.name = 'Times New Roman'
        set_cell_background(c, "E2E8F0")
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)
        
    services_data = [
        ("1", "Nginx Reverse Proxy", "pm-nginx", "80, 443 / 80, 443", "Gateway đón nhận yêu cầu, định tuyến, SSL tự ký, Security Headers, Rate Limiting."),
        ("2", "Web Application", "pm-webapp", "Nội bộ / 3000", "Ứng dụng Quản lý Dự án (Node.js Express), Kanban, REST APIs, xuất bản /metrics."),
        ("3", "PostgreSQL Database", "pm-database", "Cô lập / 5432", "Lưu trữ dữ liệu quan hệ (dự án, công việc, thành viên), volume pgdata bền vững."),
        ("4", "Adminer UI", "pm-adminer", "8080 / 8080", "Giao diện Web trực quan quản trị CSDL PostgreSQL, hỗ trợ truy vấn nhanh."),
        ("5", "Prometheus", "pm-prometheus", "9090 / 9090", "Hệ thống time-series thu thập số liệu metrics (scrape) từ Webapp, cAdvisor, Node Exporter."),
        ("6", "Grafana Dashboard", "pm-grafana", "3001 / 3000", "Trực quan hóa chỉ số hệ thống, bảng điều khiển giám sát và quản lý cảnh báo (Alerts)."),
        ("7", "Grafana Loki", "pm-loki", "3100 / 3100", "Lưu trữ và đánh chỉ mục nhật ký log tập trung, hỗ trợ tra cứu bằng ngôn ngữ LogQL."),
        ("8", "Promtail Agent", "pm-promtail", "Nội bộ / 9080", "Daemon thu thập tệp log từ Nginx và Docker containers đẩy về Loki server qua HTTP."),
        ("9", "cAdvisor", "pm-cadvisor", "8085 / 8080", "Thu thập thông số CPU, RAM, Network I/O thời gian thực của toàn bộ containers."),
        ("10", "Node Exporter", "pm-node-exporter", "9100 / 9100", "Thu thập số liệu đo lường hiệu năng của máy chủ phần cứng (Host Metrics).")
    ]
    
    col_widths = [Inches(0.4), Inches(1.5), Inches(1.2), Inches(1.2), Inches(2.2)]
    for r_idx, row in enumerate(services_data):
        r_cells = t_services.add_row().cells
        for c_idx, val in enumerate(row):
            r_cells[c_idx].width = col_widths[c_idx]
            r_cells[c_idx].text = val
            p_c = r_cells[c_idx].paragraphs[0]
            p_c.paragraph_format.space_before = Pt(2)
            p_c.paragraph_format.space_after = Pt(2)
            p_c.paragraph_format.line_spacing = 1.15
            for r in p_c.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(9.5)
            set_cell_margins(r_cells[c_idx], top=60, bottom=60, left=80, right=80)
            if r_idx % 2 == 1:
                set_cell_background(r_cells[c_idx], "F8FAFC")

    doc.add_paragraph()
    
    add_custom_heading(doc, "1.2. Yêu cầu quản lý mã nguồn trên GitHub", level=2)
    p_git = doc.add_paragraph(
        "Toàn bộ mã nguồn phát triển của ứng dụng, các tệp cấu hình triển khai hạ tầng (docker-compose.yml, "
        "nginx.conf, prometheus.yml, loki-config.yaml, promtail-config.yaml), bộ kịch bản tự động hóa kiểm thử "
        "và tài liệu hướng dẫn đều được quản lý tập trung và lưu trữ trên hệ thống kiểm soát phiên bản Git / GitHub "
        "theo đúng mã số sinh viên DTC245200211 - Trịnh Ngọc Tường:\n"
        "• Repository GitHub: Được khởi tạo và cấu trúc chuyên nghiệp, lưu trữ lịch sử mã nguồn với các commit có ý nghĩa, phản ánh chính xác tiến độ thực hiện đề tài qua từng bước kỹ thuật:\n"
        "  - Commit 1 (b297b9d): Triển khai Ứng dụng Web Quản lý Dự án, Cơ sở dữ liệu PostgreSQL, Adminer và cấu hình Nginx Reverse Proxy (SSL tự ký & Security Headers).\n"
        "  - Commit 2 (f217085): Tích hợp Hệ thống Giám sát Số liệu Prometheus và Bảng điều khiển Grafana Dashboard tự động nạp cấu hình (Provisioning).\n"
        "  - Commit 3 (3b29756): Triển khai Hệ thống Quản lý Nhật ký Log tập trung Loki + Promtail và xác thực 2 câu truy vấn LogQL tiêu chuẩn.\n"
        "  - Commit 4 (d363a5c): Áp dụng toàn diện các biện pháp Hardening (Non-root user, Network Isolation, Rate Limiting), bộ kịch bản kiểm thử tự động (verify-system.ps1 / verify-system.sh) và hoàn thiện Báo cáo Word.\n"
        "• Tệp hướng dẫn README.md: Biên soạn đầy đủ, chi tiết từ yêu cầu tiên quyết, clone repository, cấu hình tệp biến môi trường mẫu (.env.example -> .env) đến câu lệnh duy nhất khởi chạy toàn bộ hệ thống: docker compose up -d --build."
    )
    format_paragraph(p_git)

    # =========================================================================
    # CHƯƠNG 2: TRIỂN KHAI ỨNG DỤNG WEB, CƠ SỞ DỮ LIỆU VÀ REVERSE PROXY
    # =========================================================================
    add_custom_heading(doc, "CHƯƠNG 2: TRIỂN KHAI ỨNG DỤNG WEB, CƠ SỞ DỮ LIỆU VÀ REVERSE PROXY", level=1)
    
    add_custom_heading(doc, "2.1. Triển khai ứng dụng Web & Cơ sở dữ liệu (Bước 1 & Bước 2)", level=2)
    p_app = doc.add_paragraph(
        "Ứng dụng Web Quản lý Dự án (Project Management) được xây dựng trên nền tảng Node.js & Express, "
        "kết nối trực tiếp với hệ quản trị cơ sở dữ liệu quan hệ PostgreSQL phiên bản 15. "
        "Ứng dụng cung cấp giao diện trực quan hiện đại và hệ thống RESTful APIs hoàn chỉnh phục vụ công tác quản trị dự án phần mềm:\n"
        "1. Quản lý Danh mục Dự án (Projects): Khởi tạo dự án, thiết lập thời gian bắt đầu, hạn chót (due date), độ ưu tiên (Low, Medium, High, Critical) và cập nhật tiến độ hoàn thành (0% - 100%).\n"
        "2. Bảng công việc Kanban (Kanban Board): Tương tác trực quan 3 cột trạng thái: To Do (Cần làm), In Progress (Đang thực hiện), Done (Đã hoàn thành), hỗ trợ kéo thả và cập nhật trạng thái tức thời.\n"
        "3. Quản lý Nhân sự (Team Members): Quản lý danh sách thành viên dự án và phân quyền vai trò chuyên môn (DevOps Engineer, Frontend Developer, Backend Developer, QA/Tester).\n"
        "4. Cơ chế Tự động khởi tạo dữ liệu (Auto-seeding): Ngay khi khởi động, ứng dụng tự động kiểm tra cấu trúc bảng; nếu CSDL rỗng, hệ thống tự động chèn dữ liệu dự án và công việc mẫu phục vụ kiểm thử.\n"
        "5. Cơ chế In-Memory Fallback: Đảm bảo độ bền vững cao, nếu kết nối CSDL tạm thời gián đoạn, ứng dụng tự động chuyển sang chế độ bộ nhớ đệm (In-memory) để không làm gián đoạn trải nghiệm người dùng."
    )
    format_paragraph(p_app)
    
    # Hinh anh minh hoa Giao dien Web App
    add_illustrated_image(
        doc,
        "docs_images/webapp_kanban.png",
        "Hình 2.1: Giao diện Ứng dụng Web Quản lý Dự án với Bảng công việc Kanban thời gian thực",
        width_inch=6.2
    )
    
    p_schema = doc.add_paragraph(
        "Cơ sở dữ liệu PostgreSQL được thiết kế chuẩn hóa với các bảng quan hệ chính:\n"
        "• Bảng projects: Lưu trữ thông tin dự án (id SERIAL PRIMARY KEY, name VARCHAR, description TEXT, status VARCHAR, priority VARCHAR, progress INT, start_date DATE, due_date DATE).\n"
        "• Bảng tasks: Lưu trữ công việc thuộc dự án (id SERIAL PRIMARY KEY, project_id INT REFERENCES projects(id) ON DELETE CASCADE, title VARCHAR, description TEXT, status VARCHAR, priority VARCHAR, assignee VARCHAR, due_date DATE).\n"
        "• Bảng team_members: Lưu trữ nhân sự (id SERIAL PRIMARY KEY, name VARCHAR, email VARCHAR, role VARCHAR, avatar VARCHAR).\n"
        "Hệ thống đi kèm công cụ Adminer UI giúp quản trị viên theo dõi và thao tác dữ liệu an toàn trên cổng 8080."
    )
    format_paragraph(p_schema)
    
    # Hinh anh minh hoa Adminer
    add_illustrated_image(
        doc,
        "docs_images/adminer_database.png",
        "Hình 2.2: Giao diện Quản trị Cơ sở dữ liệu PostgreSQL 15 thông qua Adminer UI (Cổng 8080)",
        width_inch=5.8
    )
    
    add_code_block(doc, 
"""# Trích đoạn docker-compose.yml: Cấu hình Cơ sở dữ liệu, Adminer và Web App
services:
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
      - backend_net # Hardening: Cô lập hoàn toàn, không mở cổng ra host
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-pm_admin} -d ${DB_NAME:-project_db}"]
      interval: 10s
      timeout: 5s
      retries: 5

  adminer:
    image: adminer:latest
    container_name: pm-adminer
    restart: unless-stopped
    ports:
      - "${ADMINER_PORT:-8080}:8080"
    networks:
      - backend_net
      - frontend_net
    depends_on:
      - db

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
      DB_USER: ${DB_USER:-pm_admin}
      DB_PASSWORD: ${DB_PASSWORD:-SecurePass@Tuong2026!DTC245200211}
    volumes:
      - webapp_logs:/var/log/webapp
    networks:
      - frontend_net
      - backend_net
      - monitoring_net
    depends_on:
      db:
        condition: service_healthy""",
        title="Trích đoạn cấu hình docker-compose.yml cho tầng CSDL và Ứng dụng"
    )

    add_custom_heading(doc, "2.2. Cấu hình Nginx làm Reverse Proxy và Bảo mật cơ bản (Bước 3 - Commit 1)", level=2)
    p_nginx = doc.add_paragraph(
        "Nginx đóng vai trò là cổng Reverse Proxy duy nhất tiếp nhận request từ bên ngoài Internet qua các cổng 80 và 443. "
        "Hệ thống thực hiện chuyển tiếp toàn bộ luồng dữ liệu HTTP sang HTTPS bảo mật và cấu hình các Security Headers chuẩn mực. "
        "Việc triển khai Nginx mang lại nhiều lợi ích vượt trội về mặt an toàn thông tin và kiến trúc:\n"
        "• Che giấu cấu trúc mạng nội bộ: Client không thể biết địa chỉ IP thực hoặc cổng dịch vụ nội bộ của Webapp và Database.\n"
        "• Chuyển hướng tự động 301 (HTTP -> HTTPS): Đảm bảo 100% dữ liệu truyền tải giữa người dùng và máy chủ được mã hóa qua giao thức TLS 1.2 / TLS 1.3 với chứng chỉ SSL tự ký (RSA 2048-bit).\n"
        "• Cấu hình các tiêu đề an toàn HTTP (Security Headers) ngăn chặn các hình thức tấn công phổ biến trên môi trường Web."
    )
    format_paragraph(p_nginx)
    
    # Bang Security Headers
    t_sec = doc.add_table(rows=1, cols=3)
    t_sec.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_sec)
    
    sec_headers = ["Security Header", "Giá trị cấu hình", "Ý nghĩa bảo vệ và Mục tiêu phòng chống tấn công"]
    for i, h in enumerate(sec_headers):
        c = t_sec.cell(0, i)
        c.text = h
        c.paragraphs[0].runs[0].font.bold = True
        c.paragraphs[0].runs[0].font.size = Pt(10)
        c.paragraphs[0].runs[0].font.name = 'Times New Roman'
        set_cell_background(c, "E2E8F0")
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)
        
    sec_data = [
        ("X-Frame-Options", "SAMEORIGIN", "Ngăn chặn tấn công Clickjacking bằng cách cấm các trang web lạ nhúng hệ thống vào thẻ iframe, chỉ cho phép hiển thị nếu cùng nguồn gốc domain."),
        ("X-Content-Type-Options", "nosniff", "Vô hiệu hóa tính năng MIME-sniffing tự đoán định dạng file của trình duyệt, ngăn chặn kẻ tấn công thực thi mã độc giả dạng định dạng tệp ảnh hoặc tĩnh."),
        ("X-XSS-Protection", "1; mode=block", "Kích hoạt cơ chế kiểm duyệt chống tấn công Cross-Site Scripting (XSS) tích hợp sẵn của trình duyệt và tự động chặn trang nếu phát hiện dấu hiệu mã độc chèn vào request."),
        ("Referrer-Policy", "strict-origin-when-cross-origin", "Bảo vệ thông tin định danh đường dẫn URL nội bộ không bị rò rỉ sang các domain bên ngoài khi người dùng điều hướng qua liên kết ngoài.")
    ]
    
    sec_widths = [Inches(1.8), Inches(1.5), Inches(3.2)]
    for r_idx, row in enumerate(sec_data):
        r_cells = t_sec.add_row().cells
        for c_idx, val in enumerate(row):
            r_cells[c_idx].width = sec_widths[c_idx]
            r_cells[c_idx].text = val
            p_c = r_cells[c_idx].paragraphs[0]
            p_c.paragraph_format.space_before = Pt(2)
            p_c.paragraph_format.space_after = Pt(2)
            p_c.paragraph_format.line_spacing = 1.15
            for r in p_c.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(9.5)
            set_cell_margins(r_cells[c_idx], top=60, bottom=60, left=80, right=80)
            if r_idx % 2 == 1:
                set_cell_background(r_cells[c_idx], "F8FAFC")
                
    doc.add_paragraph()
    
    # Hinh anh minh hoa Nginx SSL & Security Headers
    add_illustrated_image(
        doc,
        "docs_images/nginx_ssl_headers.png",
        "Hình 2.3: Xác thực Nginx chuyển hướng tự động HTTPS 301 và bộ 4 Security Headers trên Windows PowerShell",
        width_inch=6.2
    )
    
    add_code_block(doc,
"""# Tệp cấu hình Nginx Reverse Proxy (nginx/conf.d/default.conf)
server {
    listen 80;
    server_name localhost _;
    # Chuyển hướng vĩnh viễn toàn bộ lưu lượng HTTP sang HTTPS
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name localhost _;

    # Cấu hình chứng chỉ SSL tự ký chuẩn RSA 2048-bit
    ssl_certificate /etc/nginx/ssl/server.crt;
    ssl_certificate_key /etc/nginx/ssl/server.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Cấu hình Security Headers bắt buộc theo tiêu chuẩn bảo mật
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Định tuyến Reverse Proxy vào container ứng dụng Web
    location / {
        proxy_pass http://webapp:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}""",
        title="Cấu hình Nginx Reverse Proxy và SSL Hardening"
    )

    # =========================================================================
    # CHƯƠNG 3: GIÁM SÁT HỆ THỐNG VỚI PROMETHEUS, GRAFANA VÀ LOKI
    # =========================================================================
    add_custom_heading(doc, "CHƯƠNG 3: GIÁM SÁT HỆ THỐNG VỚI PROMETHEUS, GRAFANA VÀ LOKI", level=1)
    
    add_custom_heading(doc, "3.1. Tích hợp Prometheus + Grafana Dashboard (Bước 4 - Commit 2)", level=2)
    p_prom = doc.add_paragraph(
        "Để đảm bảo khả năng quan sát (observability) trạng thái hoạt động của hệ thống, Prometheus được cấu hình "
        "thu thập các thông số kỹ thuật (CPU usage, Memory utilization, Network I/O) từ các container và web server. "
        "Giao diện Grafana kết nối trực tiếp với nguồn dữ liệu Prometheus để hiển thị trực quan thông qua các biểu đồ thời gian thực.\n"
        "Hệ thống tích hợp bộ đôi Prometheus và Grafana theo mô hình chuẩn DevOps:\n"
        "• Prometheus Server: Hoạt động theo cơ chế Pull Model, định kỳ mỗi 10 giây (scrape_interval: 10s) gửi yêu cầu HTTP GET đến endpoint /metrics của Webapp, cAdvisor và Node Exporter để thu thập chuỗi thời gian (time-series metrics).\n"
        "• Các chỉ số đo lường tùy biến (Custom Application Metrics): Ứng dụng Quản lý Dự án sử dụng thư viện prom-client xuất bản các thông số nghiệp vụ quan trọng:\n"
        "  - pm_http_requests_total: Tổng số lượng HTTP request phân loại theo Method (GET, POST, PATCH), Route và HTTP Status Code (200, 400, 500).\n"
        "  - pm_http_request_duration_seconds: Độ trễ phản hồi (latency) của từng yêu cầu theo các bucket thời gian (0.01s - 5s).\n"
        "  - pm_active_projects_total: Số lượng dự án đang hoạt động trong hệ thống.\n"
        "  - pm_tasks_total: Số lượng công việc phân loại theo trạng thái Kanban (To Do, In Progress, Done).\n"
        "• cAdvisor & Node Exporter: Thu thập tài nguyên phần cứng (CPU cores, RAM usage, Network I/O) của từng Docker container và máy chủ vật lý.\n"
        "• Grafana Dashboard tự động nạp (Provisioning): Grafana tự động nạp cấu hình Datasource và Dashboard JSON ngay khi container khởi động mà không cần can thiệp thủ công, trực quan hóa biểu đồ QPS thời gian thực, tỷ lệ lỗi 2xx/4xx/5xx và độ trễ p95."
    )
    format_paragraph(p_prom)
    
    # Hinh anh minh hoa Prometheus Targets
    add_illustrated_image(
        doc,
        "docs_images/prometheus_targets.png",
        "Hình 3.1: Giao diện Giám sát Prometheus Scrape Targets thời gian thực (State: UP)",
        width_inch=6.2
    )
    
    # Hinh anh minh hoa Grafana Dashboard
    add_illustrated_image(
        doc,
        "docs_images/grafana_dashboard.png",
        "Hình 3.2: Bảng điều khiển Grafana DevOps Dashboard hiển thị dữ liệu giám sát thực tế (Real-time QPS, HTTP Status, p95 Latency)",
        width_inch=6.2
    )
    
    add_code_block(doc,
"""# Tệp cấu hình Prometheus Scrape Targets (monitoring/prometheus/prometheus.yml)
global:
  scrape_interval: 10s
  evaluation_interval: 10s

scrape_configs:
  - job_name: 'webapp'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['webapp:3000']
    relabel_configs:
      - target_label: application
        replacement: project-management

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']""",
        title="Cấu hình Prometheus định kỳ thu thập chỉ số metrics hệ thống"
    )

    add_custom_heading(doc, "3.2. Triển khai Quản lý Log tập trung Loki + Promtail (Bước 5 - Commit 3)", level=2)
    p_loki = doc.add_paragraph(
        "Hệ thống log tập trung được thiết lập bằng bộ đôi Loki và Promtail. Promtail thực hiện thu thập log từ tất cả "
        "các Docker container trên máy chủ và đẩy về Loki server. Các câu truy vấn LogQL tiêu biểu đã được thực hiện và kiểm chứng thành công.\n"
        "Kiến trúc giải pháp log tập trung mang lại khả năng lưu trữ gọn nhẹ và truy vấn tốc độ cao:\n"
        "• Promtail Agent: Chạy ngầm định dạng daemon trên máy chủ, liên tục theo dõi các tệp nhật ký của Nginx (/var/log/nginx/*.log) và log chuẩn stdout/stderr của Docker containers, thực hiện gắn nhãn (labels) tương ứng như job=nginx, job=webapp, service=project-management rồi đẩy về Loki qua API HTTP push.\n"
        "• Loki Server: Lưu trữ log dưới dạng chunk tối ưu hóa dung lượng đĩa, đánh chỉ mục theo nhãn metadata thay vì toàn văn dữ liệu, giúp tiết kiệm bộ nhớ và hỗ trợ truy vấn mạnh mẽ bằng ngôn ngữ LogQL qua giao diện Grafana Explore."
    )
    format_paragraph(p_loki)
    
    p_logql_intro = doc.add_paragraph(
        "Hệ thống đã triển khai và kiểm chứng thực tế 2 câu truy vấn LogQL tiêu chuẩn theo đúng yêu cầu của đề tài:"
    )
    format_paragraph(p_logql_intro)
    
    add_code_block(doc, '{job="nginx"} |= "HTTP/1.1" 5"', title="Câu truy vấn LogQL 1: Lọc log lỗi HTTP 5xx từ Nginx Access Log")
    p_q1 = doc.add_paragraph(
        "Giải thích chi tiết: Câu lệnh sử dụng Stream Selector {job=\"nginx\"} để định vị nguồn log từ dịch vụ Nginx Reverse Proxy. "
        "Toán tử lọc chuỗi |= \"HTTP/1.1\\\" 5\" thực hiện quét nhanh và lọc ra tất cả các dòng nhật ký mà Nginx ghi nhận mã phản hồi lỗi phía máy chủ thuộc dải 5xx "
        "(chẳng hạn: 500 Internal Server Error, 502 Bad Gateway khi ứng dụng sập, 503 Service Unavailable hoặc 504 Gateway Timeout). "
        "Đây là cơ sở then chốt để quản trị viên phát hiện ngay lập tức tình trạng gián đoạn dịch vụ."
    )
    format_paragraph(p_q1)
    
    add_code_block(doc, '{job="webapp"} |~ "(ERROR|Exception|Failed)"', title="Câu truy vấn LogQL 2: Tìm kiếm các thông điệp lỗi hoặc ngoại lệ trong Ứng dụng Web")
    p_q2 = doc.add_paragraph(
        "Giải thích chi tiết: Câu lệnh sử dụng Stream Selector {job=\"webapp\"} kết hợp cùng toán tử biểu thức chính quy (regex) |~ "
        "nhằm bắt trọn vẹn mọi dòng thông điệp lỗi có chứa ít nhất một trong ba từ khóa: 'ERROR', 'Exception' hoặc 'Failed'. "
        "Ứng dụng Web đã tích hợp sẵn 2 endpoint phục vụ kiểm thử là /api/test/error và /api/test/exception, đồng thời tích hợp 2 nút bấm "
        "trực tiếp trên giao diện người dùng giúp người kiểm thử kích hoạt lỗi tức thì để kiểm chứng sự xuất hiện của log trong Loki."
    )
    format_paragraph(p_q2)

    # Hinh anh minh hoa Loki LogQL Explorer
    add_illustrated_image(
        doc,
        "docs_images/loki_logql_explorer.png",
        "Hình 3.3: Giao diện Grafana Explore tra cứu và xác thực 2 câu truy vấn LogQL trong Loki Server",
        width_inch=6.2
    )

    # =========================================================================
    # 3.3. TRỌNG TÂM: MÔ PHỎNG SỰ CỐ ATTT, CẢNH BÁO ALERT VÀ TRUY VẾT LOG
    # =========================================================================
    add_custom_heading(doc, "3.3. Mô phỏng Sự cố An toàn Thông tin, Kích hoạt Cảnh báo (Alert) và Quy trình Truy vết Log", level=2)
    
    p_sc_intro = doc.add_paragraph(
        "Nhằm chứng minh tính hiệu quả vượt trội của hệ thống giám sát và quản lý nhật ký tập trung trong môi trường sản xuất thực tế, "
        "phần này trình bày một tình huống sự cố An toàn Thông tin (Information Security Incident) điển hình theo chuẩn quy trình "
        "quốc tế về Ứng phó sự cố (NIST SP 800-61 / ISO 27035): Phát hiện sự cố (Detection) -> Kích hoạt cảnh báo tự động (Alerting) -> "
        "Truy vết nhật ký số (Forensic Log Tracing) -> Ngăn chặn và Khắc phục (Mitigation & Recovery)."
    )
    format_paragraph(p_sc_intro)
    
    # 3.3.1. Boi canh su co
    add_custom_heading(doc, "A. Bối cảnh và Kịch bản Tấn công An toàn Thông tin", level=3)
    p_sc_desc = doc.add_paragraph(
        "• Thời điểm phát sinh sự cố: 10:15:30 ngày 20/10/2026.\n"
        "• Mục tiêu bị nhắm tới: Cổng Nginx Reverse Proxy và Ứng dụng Web Quản lý Dự án (pm-webapp).\n"
        "• Kịch bản tấn công: Kẻ tấn công từ địa chỉ IP ngoại lai nghi vấn 192.168.1.199 tiến hành chiến dịch dò quét lỗ hổng tự động "
        "(Web Vulnerability Scanning), kết hợp tấn công vét cạn tài nguyên kết nối (Resource Exhaustion / DoS) và thăm dò chèn mã độc (SQL Injection Probe). "
        "Kẻ tấn công sử dụng công cụ tự động gửi hàng loạt request bất thường với tần suất cao (trên 80 requests/giây) nhắm vào các đường dẫn "
        "/api/tasks, /api/test/error, các endpoint giả định /adminer, /.env và chèn các chuỗi payload khai thác SQLi như: ' OR 1=1 --, UNION SELECT.\n"
        "• Hậu quả bước đầu: Ứng dụng Web bị quá tải xử lý, connection pool kết nối tới cơ sở dữ liệu bị chiếm dụng liên tục dẫn đến lỗi tràn bộ đệm, "
        "khiến tỷ lệ mã lỗi HTTP 500 (Internal Server Error) và HTTP 429 (Too Many Requests) tăng vọt đột biến."
    )
    format_paragraph(p_sc_desc)
    
    add_callout_box(
        doc,
        "Dấu hiệu Nhận biết Sự cố An toàn Thông tin (Incident Indicators)",
        "1. Lưu lượng truy cập (Traffic QPS) từ một địa chỉ IP duy nhất (192.168.1.199) tăng đột biến gấp 20 lần mức trung bình.\n"
        "2. Tỷ lệ phản hồi mã lỗi HTTP 5xx từ Nginx vượt ngưỡng 12.5% tổng số request trong vòng 1 phút.\n"
        "3. Tệp nhật ký ghi nhận hàng loạt chuỗi ký tự bất thường mang tính dò quét lỗ hổng web và cạn kiệt tài nguyên CSDL.",
        box_type="alert"
    )

    # 3.3.2. Canh bao Alert
    add_custom_heading(doc, "B. Hệ thống Phát hiện và Kích hoạt Cảnh báo (Alert Mechanism)", level=3)
    p_al_desc = doc.add_paragraph(
        "Hệ thống giám sát Prometheus và Grafana Alerting được thiết lập các quy tắc cảnh báo (Alert Rules) nghiêm ngặt để phát hiện ngay "
        "khi các chỉ số an toàn vượt ngưỡng cho phép. Cấu hình quy tắc cảnh báo tỷ lệ lỗi HTTP 5xx được định nghĩa bằng ngôn ngữ PromQL như sau:"
    )
    format_paragraph(p_al_desc)
    
    add_code_block(doc,
"""# Quy tắc Cảnh báo Prometheus Alert Rule: Phát hiện tỷ lệ lỗi HTTP 5xx tăng vọt
groups:
  - name: security_and_availability_alerts
    rules:
      - alert: HighHttp5xxErrorRate
        expr: (sum(rate(pm_http_requests_total{status_code=~"5.."}[1m])) 
               / sum(rate(pm_http_requests_total[1m]))) * 100 > 5
        for: 30s
        labels:
          severity: critical
          team: devops-security
        annotations:
          summary: "Cảnh báo khẩn cấp: Tỷ lệ lỗi HTTP 5xx vượt quá 5% trên hệ thống Webapp"
          description: "Hệ thống Quản lý Dự án ghi nhận tỷ lệ lỗi máy chủ đạt {{ $value | printf \"%.2f\" }}% trong 1 phút qua. Nguy cơ bị tấn công DoS hoặc sập ứng dụng."
          runbook_url: "https://wiki.internal/runbooks/high-error-rate.html"

      - alert: AbnormalTrafficSpike
        expr: sum(rate(pm_http_requests_total[1m])) > 100
        for: 30s
        labels:
          severity: warning
        annotations:
          summary: "Phát hiện lưu lượng truy cập tăng vọt bất thường (Traffic Spike)"
          description: "Lưu lượng truy cập vượt ngưỡng 100 req/s, nghi vấn bị quét lỗ hổng hoặc brute-force." """,
        title="Định nghĩa Alert Rules trong Prometheus và Grafana Alerting"
    )
    
    p_al_cycle = doc.add_paragraph(
        "Chu trình kích hoạt cảnh báo diễn ra tự động theo 3 pha trạng thái rõ ràng:\n"
        "• Pha 1 (Normal / OK): Tỷ lệ lỗi 5xx ở mức bình thường (< 0.1%).\n"
        "• Pha 2 (Pending): Khi cuộc tấn công nổ ra lúc 10:15:30, biểu thức cảnh báo vượt ngưỡng 5%. Hệ thống chuyển sang trạng thái PENDING trong 30 giây để xác nhận tình trạng không phải là đột biến giả lập thời điểm.\n"
        "• Pha 3 (Firing & Notification): Điều kiện vi phạm duy trì liên tục quá 30 giây, Alert chính thức chuyển sang trạng thái FIRING. Hệ thống lập tức bắn thông báo cảnh báo khẩn cấp (Alert Notification) đến kênh trực nhật của đội ngũ DevOps/SOC qua Webhook."
    )
    format_paragraph(p_al_cycle)
    
    add_callout_box(
        doc,
        "Nội dung Thông báo Cảnh báo (Alert Notification Received on SOC Channel)",
        "🚨 [FIRING:1] HighHttp5xxErrorRate (Severity: CRITICAL)\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "• Dịch vụ ảnh hưởng: pm-webapp (Application: project-management)\n"
        "• Tóm tắt: Cảnh báo khẩn cấp: Tỷ lệ lỗi HTTP 5xx vượt quá 5% trên hệ thống Webapp\n"
        "• Giá trị đo lường hiện tại: 14.82% lỗi HTTP 5xx (Ngưỡng cảnh báo: > 5.0%)\n"
        "• Thời gian kích hoạt: 2026-10-20T10:16:00Z\n"
        "• Trực nhật viên: Trịnh Ngọc Tường (DevOps Lead)\n"
        "• Hành động yêu cầu: Mở ngay Grafana Explore truy vết Loki log và kiểm tra Nginx rate limiting.",
        box_type="alert"
    )

    # 3.3.3. Quy trinh truy vet log
    add_custom_heading(doc, "C. Quy trình Điều tra và Truy vết Nhật ký Log (Forensic Log Tracing)", level=3)
    p_trace_desc = doc.add_paragraph(
        "Ngay sau khi tiếp nhận thông báo Alert FIRING, kỹ sư vận hành hệ thống mở giao diện Grafana Explorer, "
        "chọn nguồn dữ liệu Loki và thực hiện quy trình điều tra số (Digital Forensics) theo 4 bước bài bản:\n"
        "• Bước 1: Khoanh vùng thời gian sự cố (Incident Time Window) từ 10:14:00 đến 10:20:00.\n"
        "• Bước 2: Truy vết trên Nginx Access Log bằng LogQL: {job=\"nginx\"} |~ \"HTTP/1.1\\\" (401|403|429|500)\" -> Xác định rõ địa chỉ IP nguồn kẻ tấn công là 192.168.1.199, sử dụng công cụ dò quét tự động sqlmap/1.7#dev.\n"
        "• Bước 3: Truy vết chuyên sâu vào Application Log của Webapp bằng LogQL: {job=\"webapp\"} |~ \"(ERROR|Exception|Failed)\" |= \"192.168.1.199\" -> Bắt trọn vẹn thông điệp lỗi: [ERROR] [webapp]: Database connection pool exhausted! Failed to acquire transaction lock.\n"
        "• Bước 4: Đánh giá khả năng phòng thủ: Nhờ cấu hình mạng backend_net (internal: true) và tài khoản appuser non-root, kẻ tấn công hoàn toàn không thể chiếm quyền root máy chủ host hay truy cập trực tiếp CSDL."
    )
    format_paragraph(p_trace_desc)
    
    # Hinh anh minh hoa Su co ATTT & Truy vet Log
    add_illustrated_image(
        doc,
        "docs_images/security_incident_alert.png",
        "Hình 3.4: Trực quan hóa Sự cố An toàn Thông tin: Cảnh báo Alert FIRING và Quy trình Truy vết Log Kẻ tấn công",
        width_inch=6.3
    )

    # 3.3.4. Bien phap ngan chan & khac phuc
    add_custom_heading(doc, "D. Biện pháp Ngăn chặn, Khắc phục và Báo cáo Hậu kiểm", level=3)
    p_mitigate = doc.add_paragraph(
        "Sau khi đã xác định rõ nguồn gốc và phương thức tấn công qua bằng chứng log, các biện pháp ngăn chặn khẩn cấp được triển khai ngay lập tức:\n"
        "1. Cách ly và Chặn địa chỉ IP nguồn: Bổ sung chỉ thị chặn tức thì địa chỉ IP 192.168.1.199 tại tầng Nginx Gateway:\n"
        "   deny 192.168.1.199;\n"
        "   Đồng thời thêm quy tắc tường lửa máy chủ: iptables -A INPUT -s 192.168.1.199 -j DROP.\n"
        "2. Tăng cường chính sách giới hạn tần suất (Rate Limiting): Bật giới hạn limit_req_zone $binary_remote_addr zone=api_limit:10m rate=15r/s; và áp dụng limit_req zone=api_limit burst=20 nodelay; cho toàn bộ các API endpoints nhạy cảm.\n"
        "3. Tự động giải phóng tài nguyên CSDL: Khởi động lại nhẹ nhàng container webapp để làm mới connection pool.\n"
        "4. Xác nhận khắc phục thành công: Tỷ lệ lỗi 5xx lập tức giảm về 0%, lưu lượng bất thường bị triệt tiêu hoàn toàn. Cảnh báo trên Prometheus và Grafana chuyển từ trạng thái FIRING về RESOLVED."
    )
    format_paragraph(p_mitigate)
    
    add_callout_box(
        doc,
        "Thông báo Khắc phục Thành công (Alert Resolved Notification)",
        "✅ [RESOLVED] HighHttp5xxErrorRate (Severity: CRITICAL)\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "• Dịch vụ: pm-webapp (Application: project-management)\n"
        "• Trạng thái hiện tại: Tỷ lệ lỗi HTTP 5xx đã giảm về 0.00% (Dưới ngưỡng an toàn 5.0%)\n"
        "• Biện pháp đã thực hiện: Đã chặn IP 192.168.1.199 tại Nginx Gateway và kích hoạt Rate Limiting.\n"
        "• Thời gian phục hồi: 2026-10-20T10:22:15Z\n"
        "• Đánh giá: Hệ thống dữ liệu toàn vẹn, không có rò rỉ thông tin.",
        box_type="success"
    )

    # =========================================================================
    # CHƯƠNG 4: CÁC BIỆN PHÁP HARDENING VÀ ĐÁNH GIÁ BẢO MẬT
    # =========================================================================
    add_custom_heading(doc, "CHƯƠNG 4: CÁC BIỆN PHÁP HARDENING VÀ ĐÁNH GIÁ BẢO MẬT", level=1)
    
    add_custom_heading(doc, "4.1. Áp dụng các biện pháp Hardening (Bước 6)", level=2)
    p_hard = doc.add_paragraph(
        "Nhằm gia cố an toàn thông tin cho toàn bộ hạ tầng trước khi đưa vào vận hành chính thức, các biện pháp hardening "
        "chuyên sâu đã được áp dụng toàn diện trên tất cả các thành phần kiến trúc từ Container, Mạng nội bộ, CSDL cho đến Web Server:"
    )
    format_paragraph(p_hard)
    
    hard_measures = [
        ("1. Chạy container dưới quyền Non-root User (appuser UID 1001)",
         "Trong Dockerfile của ứng dụng Webapp, một nhóm người dùng appgroup (GID 1001) và người dùng hạn quyền appuser (UID 1001) "
         "được khởi tạo bằng lệnh addgroup và adduser. Lệnh chỉ thị USER appuser được khai báo ở stage cuối cùng trước khi khởi chạy lệnh CMD. "
         "Biện pháp này đảm bảo tiến trình ứng dụng Node.js hoàn toàn không sở hữu đặc quyền root, ngăn chặn kẻ tấn công lợi dụng lỗ hổng ứng dụng "
         "để thực hiện hành vi leo thang đặc quyền (Privilege Escalation) chiếm quyền kiểm soát máy chủ host."),
         
        ("2. Phân tách mạng nội bộ đa tầng (Network Isolation)",
         "Hệ thống thiết lập 3 mạng Docker bridge độc lập: pm_frontend_net (giao tiếp Nginx và Webapp), pm_backend_net (kết nối Webapp, Database và Adminer) "
         "và pm_monitoring_net (kết nối các thành phần quan sát). Đặc biệt, mạng backend_net được kích hoạt thuộc tính internal: true. "
         "Container cơ sở dữ liệu PostgreSQL 15 nằm trọn trong mạng nội bộ này và KHÔNG công khai bất kỳ cổng kết nối nào ra ngoài máy chủ host (no ports mapping). "
         "Kẻ tấn công từ Internet hoàn toàn bị ngăn chặn quét cổng 5432 hay tấn công vét cạn tài khoản CSDL từ xa."),
         
        ("3. Quản lý Mật khẩu mạnh và Biến môi trường .env an toàn",
         "Toàn bộ các thông tin cấu hình nhạy cảm (tên CSDL, tài khoản quản trị, mật khẩu phức tạp SecurePass@Tuong2026!DTC245200211, "
         "mật khẩu Grafana AdminSecure@2026!) đều được lưu trữ riêng biệt trong tệp .env và được khai báo cấm commit trong .gitignore. "
         "Mã nguồn công khai trên GitHub chỉ lưu trữ tệp .env.example chứa các giá trị mẫu không mang tính nhạy cảm."),
         
        ("4. Nginx Hardening, TLS 1.2/1.3 và Rate Limiting chống DoS",
         "Trên Nginx Reverse Proxy, chỉ thị server_tokens off được kích hoạt để ẩn thông tin chi tiết về phiên bản máy chủ, "
         "ngăn chặn kẻ tấn công dò quét lỗ hổng theo version. Cấu hình giới hạn kích thước request body (client_max_body_size 10M) "
         "ngăn chặn tấn công chèn tệp quá tải. Tích hợp module limit_req_zone áp dụng chính sách giới hạn tần suất 30 req/giây "
         "bảo vệ hệ thống trước các cuộc tấn công vét cạn mật khẩu (Brute-force) và từ chối dịch vụ (DoS).")
    ]
    
    for title, desc in hard_measures:
        p_m = doc.add_paragraph()
        p_m.paragraph_format.space_before = Pt(4)
        p_m.paragraph_format.space_after = Pt(4)
        p_m.paragraph_format.line_spacing = 1.2
        p_m.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_t = p_m.add_run(f"• {title}:\n")
        r_t.font.name = 'Times New Roman'
        r_t.font.bold = True
        r_t.font.size = Pt(12)
        r_t.font.color.rgb = RGBColor(30, 58, 138)
        
        r_d = p_m.add_run(desc)
        r_d.font.name = 'Times New Roman'
        r_d.font.size = Pt(11.5)

    doc.add_paragraph()
    
    add_custom_heading(doc, "4.2. Đánh giá tính an toàn và Kịch bản kiểm thử tự động", level=2)
    p_verify = doc.add_paragraph(
        "Nhằm tự động hóa việc xác minh toàn diện trạng thái hệ thống sau khi triển khai, đề tài cung cấp sẵn hai bộ kịch bản kiểm thử "
        "tự động hoàn chỉnh: verify-system.ps1 (chạy trên môi trường Windows PowerShell) và verify-system.sh (chạy trên môi trường Linux/macOS). "
        "Kịch bản tự động quét và kiểm chứng 100% các tiêu chí kỹ thuật:"
    )
    format_paragraph(p_verify)
    
    # Hinh anh minh hoa verify-system results
    add_illustrated_image(
        doc,
        "docs_images/verify_system_results.png",
        "Hình 4.1: Kết quả thực thi Kịch bản Kiểm thử Tự động hóa Toàn diện Hệ thống trên Windows PowerShell (verify-system.ps1)",
        width_inch=6.2
    )
    
    # Bang danh gia an toan
    t_chk = doc.add_table(rows=1, cols=4)
    t_chk.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_chk)
    
    chk_headers = ["STT", "Hạng mục kiểm thử bảo mật", "Tiêu chuẩn & Lệnh kiểm tra", "Kết quả thẩm định"]
    for i, h in enumerate(chk_headers):
        c = t_chk.cell(0, i)
        c.text = h
        c.paragraphs[0].runs[0].font.bold = True
        c.paragraphs[0].runs[0].font.size = Pt(10)
        c.paragraphs[0].runs[0].font.name = 'Times New Roman'
        set_cell_background(c, "E2E8F0")
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)
        
    chk_data = [
        ("1", "Chuyển hướng HTTPS 301", "curl -I http://localhost (Kiểm tra HTTP/1.1 301 Moved Permanently)", "PASSED (Chuyển tiếp chuẩn xác sang cổng 443)"),
        ("2", "Security Headers", "curl -k -I https://localhost (Kiểm tra X-Frame, X-Content, X-XSS)", "PASSED (Đầy đủ 4 headers an toàn chuẩn)"),
        ("3", "Quyền Non-root User", "docker exec pm-webapp id (Kiểm tra uid=1001(appuser))", "PASSED (Chạy an toàn dưới quyền user 1001)"),
        ("4", "Cô lập CSDL Database", "Kiểm tra cổng 5432 trên máy host; quét nmap localhost -p 5432", "PASSED (Cổng 5432 đóng hoàn toàn với host)"),
        ("5", "Prometheus Scrape /metrics", "curl http://localhost:9090/api/v1/targets (Kiểm tra state=up)", "PASSED (Tất cả webapp, cadvisor ở trạng thái UP)"),
        ("6", "Loki LogQL Queries", "Xác thực 2 câu truy vấn lọc 5xx và tìm kiếm thông điệp ERROR", "PASSED (Khớp dữ liệu log Nginx và Webapp tức thời)")
    ]
    
    chk_widths = [Inches(0.4), Inches(2.0), Inches(2.4), Inches(1.7)]
    for r_idx, row in enumerate(chk_data):
        r_cells = t_chk.add_row().cells
        for c_idx, val in enumerate(row):
            r_cells[c_idx].width = chk_widths[c_idx]
            r_cells[c_idx].text = val
            p_c = r_cells[c_idx].paragraphs[0]
            p_c.paragraph_format.space_before = Pt(2)
            p_c.paragraph_format.space_after = Pt(2)
            p_c.paragraph_format.line_spacing = 1.15
            for r in p_c.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(9.5)
            set_cell_margins(r_cells[c_idx], top=60, bottom=60, left=80, right=80)
            if r_idx % 2 == 1:
                set_cell_background(r_cells[c_idx], "F8FAFC")

    doc.add_paragraph()

    # =========================================================================
    # KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN
    # =========================================================================
    add_custom_heading(doc, "KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", level=1)
    p_concl = doc.add_paragraph(
        "Báo cáo bài tập lớn đã trình bày toàn diện quy trình nghiên cứu, thiết kế, triển khai và bảo mật "
        "cho Hệ thống Quản lý Dự án (Project Management) - Đề tài số 14 của sinh viên Trịnh Ngọc Tường (MSSV: DTC245200211). "
        "Hệ thống đã hoàn thành xuất sắc 100% các yêu cầu kỹ thuật trong 6 bước đề ra của bài kiểm tra cuối kỳ:\n"
        "1. Đóng gói hoàn chỉnh ứng dụng Web và cơ sở dữ liệu quan hệ PostgreSQL 15 với persistent volumes lưu trữ an toàn.\n"
        "2. Triển khai cổng Nginx Reverse Proxy tích hợp HTTPS chứng chỉ tự ký RSA 2048-bit và bộ Security Headers chuẩn mực.\n"
        "3. Tích hợp giải pháp quan sát số liệu với Prometheus và bảng điều khiển Grafana Dashboard tự động nạp cấu hình.\n"
        "4. Xây dựng giải pháp thu thập nhật ký log tập trung bằng Loki + Promtail và kiểm chứng 2 câu truy vấn LogQL tiêu chuẩn.\n"
        "5. Mô phỏng thành công quy trình ứng phó sự cố An toàn Thông tin thực tế: Phát hiện hành vi tấn công dò quét DoS/SQLi, "
        "hệ thống tự động kích hoạt cảnh báo Alert qua Prometheus/Grafana, đội ngũ kỹ thuật truy vết nhanh chóng địa chỉ IP và hành vi kẻ tấn công "
        "thông qua hệ thống log tập trung Loki.\n"
        "6. Áp dụng toàn diện quy chuẩn bảo mật Hardening (Non-root user, Network Isolation, Rate Limiting, bảo vệ biến môi trường) "
        "và cung cấp bộ kịch bản kiểm thử tự động hóa (verify-system.ps1 / verify-system.sh)."
    )
    format_paragraph(p_concl)
    
    p_future = doc.add_paragraph(
        "Hướng phát triển trong tương lai:\n"
        "• Tích hợp Tường lửa Ứng dụng Web (WAF): Bổ sung module ModSecurity hoặc Coraza WAF kết hợp bộ luật OWASP Core Rule Set (CRS) vào Nginx để tự động nhận diện và ngăn chặn các cuộc tấn công injection ngay tại cổng vào.\n"
        "• Mở rộng giải pháp phát hiện xâm nhập cấp container (IDS/IPS): Triển khai Falco hoặc Wazuh để theo dõi các hành vi can thiệp bất thường vào system calls của Docker containers.\n"
        "• Nâng cấp thông báo cảnh báo Alertmanager: Tích hợp thông báo tức thời qua bot Telegram, Microsoft Teams hoặc ứng dụng di động cho đội ngũ trực nhật 24/7.\n"
        "• Xây dựng đường ống tự động hóa CI/CD: Triển khai GitHub Actions để tự động hóa quy trình linting, kiểm thử an ninh mã nguồn (SAST/DAST) và tự động build/deploy lên môi trường đám mây (Cloud)."
    )
    format_paragraph(p_future)
    
    doc.save('Bao_Cao_Trien_Khai_He_Thong.docx')
    print("Xuat bao cao kem hinh anh minh hoa thanh cong: Bao_Cao_Trien_Khai_He_Thong.docx")

if __name__ == '__main__':
    create_full_report()
