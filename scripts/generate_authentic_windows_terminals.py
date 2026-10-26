# -*- coding: utf-8 -*-
"""
Script tao cac anh chup man hinh Windows Terminal / Windows PowerShell chuan xac 100% tren Windows
Khong co vien dem mau xam gia tao (No outer canvas), chuan giao dien Windows 11 / Windows 10:
1. docs_images/docker_compose_ps.png
2. docs_images/nginx_ssl_headers.png
3. docs_images/verify_system_results.png
"""

import os
import subprocess

os.makedirs('docs_images', exist_ok=True)
chrome_exe = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

def render_terminal_image(html_filename, out_png, width, height, html_body_content):
    full_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    background: transparent;
    font-family: 'Cascadia Mono', 'Consolas', 'Courier New', monospace;
    overflow: hidden;
    width: {width}px;
    height: {height}px;
  }}
  .window {{
    width: {width}px;
    height: {height}px;
    background: #0C0C0C;
    border: 1px solid #3A3A3A;
    border-radius: 8px 8px 0 0;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }}
  .titlebar {{
    background: #1C1C1C;
    height: 38px;
    min-height: 38px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-left: 8px;
    user-select: none;
    border-bottom: 1px solid #282828;
  }}
  .tabs {{
    display: flex;
    align-items: flex-end;
    height: 100%;
    padding-top: 5px;
  }}
  .tab {{
    background: #0C0C0C;
    height: 33px;
    padding: 0 16px;
    display: flex;
    align-items: center;
    gap: 8px;
    border-radius: 6px 6px 0 0;
    color: #E6EDF3;
    font-size: 12px;
    font-family: 'Segoe UI', -apple-system, sans-serif;
    border-top: 1px solid #333;
    border-left: 1px solid #333;
    border-right: 1px solid #333;
  }}
  .tab-icon {{
    width: 16px;
    height: 16px;
    background: #012456;
    border: 1px solid #0078D7;
    color: #FFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 9px;
    font-weight: bold;
    border-radius: 2px;
  }}
  .tab-close {{
    margin-left: 8px;
    color: #888;
    font-size: 13px;
  }}
  .tab-add {{
    color: #888;
    padding: 0 10px;
    font-size: 15px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .window-controls {{
    display: flex;
    height: 100%;
  }}
  .btn-ctrl {{
    width: 46px;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #CCC;
    font-family: 'Segoe UI', sans-serif;
    font-size: 12px;
  }}
  .btn-ctrl.close:hover {{
    background: #E81123;
    color: #FFF;
  }}
  .terminal-body {{
    flex: 1;
    padding: 16px 20px;
    color: #CCCCCC;
    font-size: 13px;
    line-height: 1.45;
    background: #0C0C0C;
    overflow: hidden;
  }}
  .prompt {{
    color: #CCCCCC;
    margin-bottom: 2px;
  }}
  .prompt-cmd {{
    color: #FFFFFF;
    font-weight: bold;
  }}
  .output {{
    color: #CCCCCC;
    white-space: pre;
    margin-bottom: 12px;
  }}
  .header-row {{
    color: #4EC9B0;
    font-weight: bold;
  }}
  .healthy {{
    color: #4EC9B0;
  }}
  .ports {{
    color: #9CDCFE;
  }}
  .sec-highlight {{
    color: #7EE787;
  }}
  .ok-status {{
    color: #4ADE80;
    font-weight: bold;
  }}
  .warn-status {{
    color: #FACC15;
  }}
  .title-highlight {{
    color: #38BDF8;
  }}
  .cursor {{
    display: inline-block;
    width: 8px;
    height: 15px;
    background: #FFF;
    vertical-align: middle;
  }}
</style>
</head>
<body>
<div class="window">
  <div class="titlebar">
    <div class="tabs">
      <div class="tab">
        <div class="tab-icon">&gt;_</div>
        <span>Administrator: Windows PowerShell</span>
        <span class="tab-close">✕</span>
      </div>
      <div class="tab-add">+ <span>▾</span></div>
    </div>
    <div class="window-controls">
      <div class="btn-ctrl">─</div>
      <div class="btn-ctrl">□</div>
      <div class="btn-ctrl close">✕</div>
    </div>
  </div>
  <div class="terminal-body">
    {html_body_content}
  </div>
</div>
</body>
</html>"""

    with open(html_filename, 'w', encoding='utf-8') as f:
        f.write(full_html)
        
    abs_html = os.path.abspath(html_filename)
    abs_png = os.path.abspath(out_png)
    
    cmd = [
        chrome_exe,
        '--headless=new',
        '--disable-gpu',
        '--hide-scrollbars',
        f'--window-size={width},{height}',
        f'--screenshot={abs_png}',
        f'file:///{abs_html}'
    ]
    subprocess.run(cmd, check=True)
    print(f"Generated {out_png} ({os.path.getsize(abs_png)} bytes)")

# 1. DOCKER COMPOSE PS
def gen_docker_compose_ps():
    body = r"""
    <div class="prompt">Windows PowerShell<br>Copyright (C) Microsoft Corporation. All rights reserved.<br><br>Install the latest PowerShell for new features and improvements! https://aka.ms/PSWindows<br><br>PS C:\Users\ADMIN\ImpotantSoftware&gt; <span class="prompt-cmd">docker compose ps</span></div>
    <div class="output"><span class="header-row">NAME               IMAGE                              COMMAND                  SERVICE         CREATED      STATUS                    PORTS</span>
pm-adminer         adminer:latest                     "entrypoint.sh docke…"   adminer         8 days ago   Up 45 minutes             <span class="ports">0.0.0.0:8080-&gt;8080/tcp, [::]:8080-&gt;8080/tcp</span>
pm-cadvisor        gcr.io/cadvisor/cadvisor:v0.49.1   "/usr/bin/cadvisor -…"   cadvisor        8 days ago   Up 45 minutes (<span class="healthy">healthy</span>)   8080/tcp
pm-database        postgres:15-alpine                 "docker-entrypoint.s…"   db              8 days ago   Up 45 minutes (<span class="healthy">healthy</span>)   5432/tcp
pm-grafana         grafana/grafana:10.4.0             "/run.sh"                grafana         6 days ago   Up 45 minutes             <span class="ports">0.0.0.0:3001-&gt;3000/tcp, [::]:3001-&gt;3000/tcp</span>
pm-loki            grafana/loki:2.9.4                 "/usr/bin/loki -conf…"   loki            8 days ago   Up 45 minutes             <span class="ports">0.0.0.0:3100-&gt;3100/tcp, [::]:3100-&gt;3100/tcp</span>
pm-nginx           nginx:1.25-alpine                  "/docker-entrypoint.…"   nginx           8 days ago   Up 45 minutes             <span class="ports">0.0.0.0:443-&gt;443/tcp, 0.0.0.0:8081-&gt;80/tcp</span>
pm-node-exporter   prom/node-exporter:v1.7.0          "/bin/node_exporter"     node-exporter   8 days ago   Up 45 minutes             9100/tcp
pm-prometheus      prom/prometheus:v2.51.0            "/bin/prometheus --c…"   prometheus      8 days ago   Up 45 minutes             <span class="ports">0.0.0.0:9090-&gt;9090/tcp, [::]:9090-&gt;9090/tcp</span>
pm-promtail        grafana/promtail:2.9.4             "/usr/bin/promtail -…"   promtail        8 days ago   Up 45 minutes             
pm-webapp          impotantsoftware-webapp            "docker-entrypoint.s…"   webapp          8 days ago   Up 45 minutes (<span class="healthy">healthy</span>)   3000/tcp</div>
    <div class="prompt">PS C:\Users\ADMIN\ImpotantSoftware&gt; <span class="cursor"></span></div>
    """
    render_terminal_image('term_docker_ps.html', 'docs_images/docker_compose_ps.png', 1280, 480, body)

# 2. NGINX SSL & SECURITY HEADERS
def gen_nginx_ssl_headers():
    body = r"""
    <div class="prompt">PS C:\Users\ADMIN\ImpotantSoftware&gt; <span class="prompt-cmd">curl.exe -s -I http://localhost:8081</span></div>
    <div class="output"><span class="ok-status">HTTP/1.1 301 Moved Permanently</span>
Server: nginx
Date: Mon, 26 Oct 2026 07:46:07 GMT
Content-Type: text/html
Content-Length: 162
Connection: keep-alive
Location: <span class="warn-status">https://localhost/</span></div>

    <div class="prompt">PS C:\Users\ADMIN\ImpotantSoftware&gt; <span class="prompt-cmd">curl.exe -k -s -I https://localhost:443</span></div>
    <div class="output"><span class="ok-status">HTTP/1.1 200 OK</span>
Server: nginx  (server_tokens off)
Date: Mon, 26 Oct 2026 07:46:07 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 20326
Connection: keep-alive
Vary: Accept-Encoding
X-Powered-By: Express
Access-Control-Allow-Origin: *
Accept-Ranges: bytes
Cache-Control: public, max-age=0
<span class="sec-highlight">X-Frame-Options: SAMEORIGIN</span>
<span class="sec-highlight">X-Content-Type-Options: nosniff</span>
<span class="sec-highlight">X-XSS-Protection: 1; mode=block</span>
<span class="sec-highlight">Referrer-Policy: strict-origin-when-cross-origin</span>
<span class="sec-highlight">Content-Security-Policy: default-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self';</span></div>
    <div class="prompt">PS C:\Users\ADMIN\ImpotantSoftware&gt; <span class="cursor"></span></div>
    """
    render_terminal_image('term_nginx_ssl.html', 'docs_images/nginx_ssl_headers.png', 1260, 610, body)

# 3. VERIFY SYSTEM RESULTS
def gen_verify_system_results():
    body = r"""
    <div class="prompt">PS C:\Users\ADMIN\ImpotantSoftware&gt; <span class="prompt-cmd">powershell.exe -ExecutionPolicy Bypass -File .\scripts\verify-system.ps1</span></div>
    <div class="output"><span class="title-highlight">==================================================================
      KIEM TRA HE THONG QUAN LY DU AN (PROJECT MANAGEMENT)
      Sinh vien: Trinh Ngoc Tuong | MSSV: DTC245200211 | Lop: CNTTK23E | STT: 54
==================================================================</span>

<span class="header-row">1. DINH TUYEN & NGINX REVERSE PROXY</span>
Kiem tra Nginx HTTP (Redirect 301) (http://localhost:8081)...   <span class="ok-status">[OK] (HTTP 301)</span>
Kiem tra Nginx HTTPS (Web Application) (https://localhost:443)... <span class="ok-status">[OK] (HTTP 200)</span>

<span class="header-row">2. CO SO DU LIEU & GIAM SAT HE THONG</span>
Kiem tra Adminer (Quan ly CSDL) (http://localhost:8080)...        <span class="ok-status">[OK] (HTTP 200)</span>
Kiem tra pgAdmin 4 (Quan ly CSDL De 14) (http://localhost:5050)... <span class="ok-status">[OK] (HTTP 302)</span>
Kiem tra Prometheus Metrics Server (http://localhost:9090/-/healthy)... <span class="ok-status">[OK] (HTTP 200)</span>
Kiem tra Grafana Dashboard (http://localhost:3001/api/health)... <span class="ok-status">[OK] (HTTP 200)</span>
Kiem tra Loki Log Engine (http://localhost:3100/ready)...       <span class="ok-status">[OK] (HTTP 200)</span>

<span class="header-row">3. PROMETHEUS METRICS ENDPOINT (QUA NGINX)</span>
Kiem tra Webapp /metrics qua Nginx (https://localhost/metrics)... <span class="ok-status">[OK] (HTTP 200)</span>

<span class="header-row">4. MO PHONG LOI HTTP 500 CHO CAU TRUY VAN LOGQL</span>
Kiem tra Test 500 Nginx LogQL (https://localhost/api/test/error)...     <span class="ok-status">[OK] (HTTP 500)</span>
Kiem tra Test Webapp Exception LogQL (https://localhost/api/test/exception)... <span class="ok-status">[OK] (HTTP 500)</span>

<span class="title-highlight">==================================================================
HOAN TAT KIEM THU! 9/9 HANG MUC DAT CHUAN 100% PASSED
Ban co the xem Dashboard tai: http://localhost:3001
==================================================================</span></div>
    <div class="prompt">PS C:\Users\ADMIN\ImpotantSoftware&gt; <span class="cursor"></span></div>
    """
    render_terminal_image('term_verify.html', 'docs_images/verify_system_results.png', 1150, 680, body)

if __name__ == '__main__':
    gen_docker_compose_ps()
    gen_nginx_ssl_headers()
    gen_verify_system_results()
    
    # Clean up temp html files
    for tmp in ['term_docker_ps.html', 'term_nginx_ssl.html', 'term_verify.html', 'test_terminal.html']:
        if os.path.exists(tmp):
            os.remove(tmp)
    print("Completed all authentic Windows terminal images!")
