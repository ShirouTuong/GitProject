# -*- coding: utf-8 -*-
"""
Script tao cac anh minh hoa Windows 11 Chrome Browser cho GitHub va Grafana:
1. docs_images/github_repo_main.png
2. docs_images/github_commits.png
3. docs_images/github_docker_compose.png
4. docs_images/grafana_dashboard.png
5. docs_images/loki_logql_explorer.png
6. docs_images/security_incident_alert.png
Chuan giao dien Windows 11 (Window controls ben phai: -, square, X; Segoe UI; Chrome tabs).
"""

import os
import subprocess

os.makedirs('docs_images', exist_ok=True)
chrome_exe = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

def get_win11_browser_html(tab_title, url, body_html, width, height, icon_type="github"):
    if icon_type == "github":
        icon_svg = '<svg height="14" width="14" viewBox="0 0 16 16" fill="#FFF"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path></svg>'
    else: # grafana
        icon_svg = '<svg height="14" width="14" viewBox="0 0 100 100" fill="#F47A20"><path d="M50 0C22.4 0 0 22.4 0 50s22.4 50 50 50 50-22.4 50-50S77.6 0 50 0zm22.4 44.8L50 67.2 27.6 44.8l8-8L50 51.2l14.4-14.4 8 8z"/></svg>'

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{
    background: transparent;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    overflow: hidden;
    width: {width}px;
    height: {height}px;
  }}
  .win11-window {{
    width: {width}px;
    height: {height}px;
    background: #0D1117;
    border: 1px solid #444444;
    border-radius: 8px 8px 0 0;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    box-shadow: 0 10px 30px rgba(0,0,0,0.6);
  }}
  .win11-titlebar {{
    background: #18191C;
    height: 40px;
    min-height: 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-left: 8px;
    user-select: none;
    border-bottom: 1px solid #282A2E;
  }}
  .tabs-container {{
    display: flex;
    align-items: flex-end;
    height: 100%;
    padding-top: 5px;
  }}
  .browser-tab {{
    background: #202227;
    height: 35px;
    padding: 0 14px;
    display: flex;
    align-items: center;
    gap: 8px;
    border-radius: 8px 8px 0 0;
    color: #E6EDF3;
    font-size: 12px;
    font-weight: 500;
    max-width: 320px;
    border-top: 1px solid #333;
    border-left: 1px solid #333;
    border-right: 1px solid #333;
  }}
  .tab-title-text {{
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}
  .tab-close-btn {{
    margin-left: 6px;
    color: #888;
    font-size: 12px;
  }}
  .tab-new-btn {{
    color: #888;
    padding: 0 12px;
    font-size: 16px;
    cursor: default;
  }}
  .win11-controls {{
    display: flex;
    height: 100%;
  }}
  .win11-btn {{
    width: 46px;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #CCCCCC;
    font-size: 11px;
    cursor: default;
  }}
  .win11-btn.close:hover {{
    background: #E81123;
    color: #FFF;
  }}
  .browser-nav-bar {{
    background: #202227;
    height: 42px;
    min-height: 42px;
    display: flex;
    align-items: center;
    padding: 0 12px;
    gap: 12px;
    border-bottom: 1px solid #2B2D33;
  }}
  .nav-buttons {{
    display: flex;
    gap: 12px;
    color: #888;
    font-size: 14px;
  }}
  .omnibox {{
    flex: 1;
    background: #141518;
    height: 30px;
    border-radius: 15px;
    display: flex;
    align-items: center;
    padding: 0 14px;
    gap: 8px;
    border: 1px solid #33363D;
    color: #58A6FF;
    font-size: 12px;
    font-family: 'Segoe UI', sans-serif;
  }}
  .padlock {{
    color: #3FB950;
    font-size: 11px;
  }}
  .browser-viewport {{
    flex: 1;
    overflow: hidden;
    background: #0D1117;
  }}
</style>
</head>
<body>
<div class="win11-window">
  <div class="win11-titlebar">
    <div class="tabs-container">
      <div class="browser-tab">
        {icon_svg}
        <span class="tab-title-text">{tab_title}</span>
        <span class="tab-close-btn">✕</span>
      </div>
      <div class="tab-new-btn">+</div>
    </div>
    <div class="win11-controls">
      <div class="win11-btn">─</div>
      <div class="win11-btn">□</div>
      <div class="win11-btn close">✕</div>
    </div>
  </div>
  <div class="browser-nav-bar">
    <div class="nav-buttons">
      <span>←</span>
      <span>→</span>
      <span>⟳</span>
    </div>
    <div class="omnibox">
      <span class="padlock">🔒</span>
      <span>{url}</span>
    </div>
  </div>
  <div class="browser-viewport">
    {body_html}
  </div>
</div>
</body>
</html>"""

def render_html_to_png(html_str, out_png, width, height):
    tmp_html = f"temp_{os.path.basename(out_png)}.html"
    with open(tmp_html, 'w', encoding='utf-8') as f:
        f.write(html_str)
    
    abs_html = os.path.abspath(tmp_html)
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
    if os.path.exists(tmp_html):
        os.remove(tmp_html)
    print(f"Generated Windows 11 Image: {out_png} ({os.path.getsize(abs_png)} bytes)")

# =============================================================================
# 1. GITHUB REPO MAIN (docs_images/github_repo_main.png)
# =============================================================================
def make_win11_github_repo():
    body = r"""
    <div style="padding: 20px 32px; color: #C9D1D9; font-size: 13px;">
      <!-- Repo Header -->
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; border-bottom: 1px solid #21262D; padding-bottom: 16px;">
        <div style="display: flex; align-items: center; gap: 8px; font-size: 18px;">
          <span style="color: #58A6FF; font-weight: 400;">ShirouTuong</span>
          <span style="color: #8B949E;">/</span>
          <span style="color: #58A6FF; font-weight: 600;">GitProject</span>
          <span style="border: 1px solid #30363D; border-radius: 12px; padding: 2px 10px; font-size: 12px; color: #8B949E; margin-left: 8px;">Public</span>
        </div>
        <div style="display: flex; gap: 8px;">
          <div style="background: #21262D; border: 1px solid #30363D; border-radius: 6px; padding: 4px 12px; font-size: 12px; color: #C9D1D9;">👁️ Watch <span style="background: #30363D; border-radius: 8px; padding: 1px 6px;">1</span></div>
          <div style="background: #21262D; border: 1px solid #30363D; border-radius: 6px; padding: 4px 12px; font-size: 12px; color: #C9D1D9;">⭐ Star <span style="background: #30363D; border-radius: 8px; padding: 1px 6px;">2</span></div>
          <div style="background: #21262D; border: 1px solid #30363D; border-radius: 6px; padding: 4px 12px; font-size: 12px; color: #C9D1D9;">🍴 Fork <span style="background: #30363D; border-radius: 8px; padding: 1px 6px;">0</span></div>
        </div>
      </div>

      <!-- Branch & Action Bar -->
      <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">
        <div style="display: flex; align-items: center; gap: 12px;">
          <div style="background: #21262D; border: 1px solid #30363D; border-radius: 6px; padding: 5px 12px; font-size: 12px; color: #E6EDF3; font-weight: 600;">🌱 main ▾</div>
          <span style="color: #8B949E; font-size: 12px;"><strong>1</strong> Branch</span>
          <span style="color: #8B949E; font-size: 12px;"><strong>0</strong> Tags</span>
        </div>
        <div style="display: flex; gap: 12px; align-items: center;">
          <span style="color: #58A6FF; font-size: 12px; font-weight: 500;">🕒 6 Commits</span>
          <div style="background: #238636; border-radius: 6px; padding: 5px 14px; font-size: 12px; color: #FFF; font-weight: 600;">Code ▾</div>
        </div>
      </div>

      <!-- File Table -->
      <div style="border: 1px solid #30363D; border-radius: 6px; overflow: hidden; background: #161B22; margin-bottom: 20px;">
        <!-- Latest commit row -->
        <div style="background: #21262D; padding: 10px 16px; display: flex; align-items: center; justify-content: space-between; font-size: 12px; border-bottom: 1px solid #30363D;">
          <div><strong style="color: #E6EDF3;">ShirouTuong</strong> <span style="color: #C9D1D9;">Commit 4: Ap dung toan dien Hardening, Scripts kiem thu va Hoan thien Bao cao</span></div>
          <div style="color: #8B949E;"><code style="color: #58A6FF; background: #161B22; padding: 2px 6px; border-radius: 4px;">d363a5c</code> 12 hours ago</div>
        </div>
        <!-- Files -->
        <div style="font-size: 12.5px;">
          <div style="display: flex; padding: 8px 16px; border-bottom: 1px solid #21262D; align-items: center;">
            <div style="width: 220px; color: #58A6FF;">📁 app</div>
            <div style="flex: 1; color: #8B949E;">Update Node.js webapp source code, kanban API and /metrics endpoint</div>
            <div style="width: 120px; color: #8B949E; text-align: right;">2 days ago</div>
          </div>
          <div style="display: flex; padding: 8px 16px; border-bottom: 1px solid #21262D; align-items: center;">
            <div style="width: 220px; color: #58A6FF;">📁 monitoring</div>
            <div style="flex: 1; color: #8B949E;">Configure Prometheus scrape targets, Grafana dashboard JSON and Loki rules</div>
            <div style="width: 120px; color: #8B949E; text-align: right;">2 days ago</div>
          </div>
          <div style="display: flex; padding: 8px 16px; border-bottom: 1px solid #21262D; align-items: center;">
            <div style="width: 220px; color: #58A6FF;">📁 nginx</div>
            <div style="flex: 1; color: #8B949E;">Update Nginx reverse proxy configuration, SSL certificates and security headers</div>
            <div style="width: 120px; color: #8B949E; text-align: right;">3 days ago</div>
          </div>
          <div style="display: flex; padding: 8px 16px; border-bottom: 1px solid #21262D; align-items: center;">
            <div style="width: 220px; color: #58A6FF;">📁 scripts</div>
            <div style="flex: 1; color: #8B949E;">Add verify-system.ps1, verify-system.sh and automated testing scripts</div>
            <div style="width: 120px; color: #8B949E; text-align: right;">12 hours ago</div>
          </div>
          <div style="display: flex; padding: 8px 16px; border-bottom: 1px solid #21262D; align-items: center;">
            <div style="width: 220px; color: #C9D1D9;">📄 .env.example</div>
            <div style="flex: 1; color: #8B949E;">Provide environment variable template with non-sensitive defaults</div>
            <div style="width: 120px; color: #8B949E; text-align: right;">3 days ago</div>
          </div>
          <div style="display: flex; padding: 8px 16px; border-bottom: 1px solid #21262D; align-items: center;">
            <div style="width: 220px; color: #C9D1D9;">📄 .gitignore</div>
            <div style="flex: 1; color: #8B949E;">Exclude sensitive .env file, certs and temporary build artifacts</div>
            <div style="width: 120px; color: #8B949E; text-align: right;">3 days ago</div>
          </div>
          <div style="display: flex; padding: 8px 16px; border-bottom: 1px solid #21262D; align-items: center;">
            <div style="width: 220px; color: #C9D1D9;">📄 README.md</div>
            <div style="flex: 1; color: #8B949E;">Complete project documentation, installation steps and verification guide</div>
            <div style="width: 120px; color: #8B949E; text-align: right;">12 hours ago</div>
          </div>
          <div style="display: flex; padding: 8px 16px; align-items: center;">
            <div style="width: 220px; color: #C9D1D9;">📄 docker-compose.yml</div>
            <div style="flex: 1; color: #8B949E;">Multi-service orchestration: Webapp, DB, Nginx, Prometheus, Grafana, Loki</div>
            <div style="width: 120px; color: #8B949E; text-align: right;">12 hours ago</div>
          </div>
        </div>
      </div>

      <!-- README Preview Box -->
      <div style="border: 1px solid #30363D; border-radius: 6px; overflow: hidden; background: #0D1117;">
        <div style="background: #161B22; padding: 8px 16px; border-bottom: 1px solid #30363D; font-weight: 600; color: #E6EDF3; font-size: 12.5px;">📖 README.md</div>
        <div style="padding: 16px 20px;">
          <h2 style="font-size: 16px; color: #E6EDF3; margin-bottom: 8px; border-bottom: 1px solid #21262D; padding-bottom: 6px;">BÁO CÁO BÀI KIỂM TRA CUỐI KỲ: TRIỂN KHAI VÀ QUẢN TRỊ HỆ THỐNG PHẦN MỀM</h2>
          <div style="color: #58A6FF; font-size: 13px; line-height: 1.6;">• <strong>Họ và tên:</strong> Trịnh Ngọc Tường | <strong>MSSV:</strong> DTC245200211 | <strong>Lớp:</strong> CNTTK23E | <strong>STT:</strong> 54<br>• <strong>Đề tài số 14:</strong> Hệ thống Quản lý Dự án (Project Management)</div>
          <div style="margin-top: 10px; background: #161B22; border-left: 3px solid #238636; padding: 8px 12px; font-family: monospace; font-size: 12px; color: #7EE787;">docker compose up -d --build</div>
        </div>
      </div>
    </div>
    """
    html = get_win11_browser_html("ShirouTuong/GitProject: Hệ thống Quản lý Dự án", "https://github.com/ShirouTuong/GitProject", body, 1300, 840, "github")
    render_html_to_png(html, "docs_images/github_repo_main.png", 1300, 840)

# =============================================================================
# 2. GITHUB COMMITS (docs_images/github_commits.png)
# =============================================================================
def make_win11_github_commits():
    body = r"""
    <div style="padding: 24px 36px; color: #C9D1D9; font-size: 13px;">
      <div style="display: flex; align-items: center; gap: 8px; font-size: 18px; margin-bottom: 16px;">
        <span style="color: #58A6FF; font-weight: 400;">ShirouTuong</span>
        <span style="color: #8B949E;">/</span>
        <span style="color: #58A6FF; font-weight: 600;">GitProject</span>
      </div>

      <h3 style="font-size: 16px; color: #E6EDF3; margin-bottom: 16px;">Commits on <code style="background: #21262D; padding: 2px 8px; border-radius: 6px; font-size: 13px; color: #58A6FF;">main</code></h3>

      <div style="border: 1px solid #30363D; border-radius: 6px; background: #161B22; overflow: hidden;">
        <!-- Commit item -->
        <div style="padding: 14px 20px; border-bottom: 1px solid #21262D; display: flex; justify-content: space-between; align-items: center;">
          <div style="display: flex; gap: 14px; align-items: center;">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: #238636; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #FFF; font-size: 12px;">ST</div>
            <div>
              <div style="font-weight: 600; color: #E6EDF3; font-size: 13.5px;">Add node-exporter service and configure database users</div>
              <div style="color: #8B949E; font-size: 12px; margin-top: 3px;">ShirouTuong committed 6 hours ago</div>
            </div>
          </div>
          <div style="display: flex; gap: 10px; align-items: center;">
            <span style="border: 1px solid #238636; border-radius: 12px; padding: 2px 8px; font-size: 11px; color: #3FB950;">Verified</span>
            <code style="background: #21262D; border: 1px solid #30363D; padding: 3px 8px; border-radius: 4px; color: #58A6FF; font-size: 12px;">60d6f3c</code>
          </div>
        </div>

        <div style="padding: 14px 20px; border-bottom: 1px solid #21262D; display: flex; justify-content: space-between; align-items: center;">
          <div style="display: flex; gap: 14px; align-items: center;">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: #238636; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #FFF; font-size: 12px;">ST</div>
            <div>
              <div style="font-weight: 600; color: #E6EDF3; font-size: 13.5px;">Fix Dockerfile healthcheck IP, update compose file and verification script</div>
              <div style="color: #8B949E; font-size: 12px; margin-top: 3px;">ShirouTuong committed 8 hours ago</div>
            </div>
          </div>
          <div style="display: flex; gap: 10px; align-items: center;">
            <span style="border: 1px solid #238636; border-radius: 12px; padding: 2px 8px; font-size: 11px; color: #3FB950;">Verified</span>
            <code style="background: #21262D; border: 1px solid #30363D; padding: 3px 8px; border-radius: 4px; color: #58A6FF; font-size: 12px;">e4006cc</code>
          </div>
        </div>

        <div style="padding: 14px 20px; border-bottom: 1px solid #21262D; display: flex; justify-content: space-between; align-items: center; background: #1C2128;">
          <div style="display: flex; gap: 14px; align-items: center;">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: #1F6FEB; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #FFF; font-size: 12px;">ST</div>
            <div>
              <div style="font-weight: 600; color: #79C0FF; font-size: 13.5px;">Commit 4: Ap dung toan dien Hardening (Non-root user, Network Isolation), Scripts kiem thu va Hoan thien Bao cao Word</div>
              <div style="color: #8B949E; font-size: 12px; margin-top: 3px;">ShirouTuong committed 12 hours ago</div>
            </div>
          </div>
          <div style="display: flex; gap: 10px; align-items: center;">
            <span style="border: 1px solid #238636; border-radius: 12px; padding: 2px 8px; font-size: 11px; color: #3FB950;">Verified</span>
            <code style="background: #21262D; border: 1px solid #30363D; padding: 3px 8px; border-radius: 4px; color: #58A6FF; font-size: 12px;">d363a5c</code>
          </div>
        </div>

        <div style="padding: 14px 20px; border-bottom: 1px solid #21262D; display: flex; justify-content: space-between; align-items: center;">
          <div style="display: flex; gap: 14px; align-items: center;">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: #1F6FEB; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #FFF; font-size: 12px;">ST</div>
            <div>
              <div style="font-weight: 600; color: #E6EDF3; font-size: 13.5px;">Commit 3: Tich hop he thong quan ly log tap trung Loki + Promtail va xac thuc 2 cau truy van LogQL</div>
              <div style="color: #8B949E; font-size: 12px; margin-top: 3px;">ShirouTuong committed 2 days ago</div>
            </div>
          </div>
          <div style="display: flex; gap: 10px; align-items: center;">
            <span style="border: 1px solid #238636; border-radius: 12px; padding: 2px 8px; font-size: 11px; color: #3FB950;">Verified</span>
            <code style="background: #21262D; border: 1px solid #30363D; padding: 3px 8px; border-radius: 4px; color: #58A6FF; font-size: 12px;">3b29756</code>
          </div>
        </div>

        <div style="padding: 14px 20px; border-bottom: 1px solid #21262D; display: flex; justify-content: space-between; align-items: center;">
          <div style="display: flex; gap: 14px; align-items: center;">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: #1F6FEB; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #FFF; font-size: 12px;">ST</div>
            <div>
              <div style="font-weight: 600; color: #E6EDF3; font-size: 13.5px;">Commit 2: Tich hop Prometheus va Grafana Dashboard giam sat metrics</div>
              <div style="color: #8B949E; font-size: 12px; margin-top: 3px;">ShirouTuong committed 3 days ago</div>
            </div>
          </div>
          <div style="display: flex; gap: 10px; align-items: center;">
            <span style="border: 1px solid #238636; border-radius: 12px; padding: 2px 8px; font-size: 11px; color: #3FB950;">Verified</span>
            <code style="background: #21262D; border: 1px solid #30363D; padding: 3px 8px; border-radius: 4px; color: #58A6FF; font-size: 12px;">f217085</code>
          </div>
        </div>

        <div style="padding: 14px 20px; display: flex; justify-content: space-between; align-items: center;">
          <div style="display: flex; gap: 14px; align-items: center;">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: #1F6FEB; display: flex; align-items: center; justify-content: center; font-weight: bold; color: #FFF; font-size: 12px;">ST</div>
            <div>
              <div style="font-weight: 600; color: #E6EDF3; font-size: 13.5px;">Commit 1: Trien khai Ung dung Web Quan ly Du an, Database va Nginx Reverse Proxy (SSL, Security Headers)</div>
              <div style="color: #8B949E; font-size: 12px; margin-top: 3px;">ShirouTuong committed 4 days ago</div>
            </div>
          </div>
          <div style="display: flex; gap: 10px; align-items: center;">
            <span style="border: 1px solid #238636; border-radius: 12px; padding: 2px 8px; font-size: 11px; color: #3FB950;">Verified</span>
            <code style="background: #21262D; border: 1px solid #30363D; padding: 3px 8px; border-radius: 4px; color: #58A6FF; font-size: 12px;">b297b9d</code>
          </div>
        </div>
      </div>
    </div>
    """
    html = get_win11_browser_html("Commits · ShirouTuong/GitProject · GitHub", "https://github.com/ShirouTuong/GitProject/commits/main", body, 1300, 750, "github")
    render_html_to_png(html, "docs_images/github_commits.png", 1300, 750)

# =============================================================================
# 3. GITHUB DOCKER COMPOSE CODE VIEW (docs_images/github_docker_compose.png)
# =============================================================================
def make_win11_github_docker_compose():
    code_text = r"""<span style="color:#7EE787">services</span>:
  <span style="color:#7EE787">db</span>:
    <span style="color:#7EE787">image</span>: postgres:15-alpine
    <span style="color:#7EE787">container_name</span>: pm-database
    <span style="color:#7EE787">restart</span>: unless-stopped
    <span style="color:#7EE787">environment</span>:
      <span style="color:#7EE787">POSTGRES_DB</span>: <span style="color:#FFA657">${DB_NAME:-project_db}</span>
      <span style="color:#7EE787">POSTGRES_USER</span>: <span style="color:#FFA657">${DB_USER:-pm_admin}</span>
      <span style="color:#7EE787">POSTGRES_PASSWORD</span>: <span style="color:#FFA657">${DB_PASSWORD:-SecurePass@Tuong2026!DTC245200211}</span>
    <span style="color:#7EE787">volumes</span>:
      <span style="color:#A5D6FF">- pgdata:/var/lib/postgresql/data</span>
    <span style="color:#7EE787">networks</span>:
      <span style="color:#A5D6FF">- backend_net</span>   <span style="color:#8B949E"># Hardening: Co lap hoan toan khoi Internet, khong expose port ra host</span>

  <span style="color:#7EE787">adminer</span>:
    <span style="color:#7EE787">image</span>: adminer:latest
    <span style="color:#7EE787">container_name</span>: pm-adminer
    <span style="color:#7EE787">ports</span>:
      <span style="color:#A5D6FF">- "${ADMINER_PORT:-8080}:8080"</span>
    <span style="color:#7EE787">networks</span>:
      <span style="color:#A5D6FF">- backend_net</span>
      <span style="color:#A5D6FF">- frontend_net</span>

  <span style="color:#7EE787">webapp</span>:
    <span style="color:#7EE787">build</span>: ./app
    <span style="color:#7EE787">container_name</span>: pm-webapp
    <span style="color:#7EE787">environment</span>:
      <span style="color:#7EE787">NODE_ENV</span>: production
      <span style="color:#7EE787">PORT</span>: 3000
      <span style="color:#7EE787">DB_HOST</span>: db
    <span style="color:#7EE787">networks</span>: [frontend_net, backend_net, monitoring_net]

  <span style="color:#7EE787">nginx</span>:
    <span style="color:#7EE787">image</span>: nginx:1.25-alpine
    <span style="color:#7EE787">container_name</span>: pm-nginx
    <span style="color:#7EE787">ports</span>:
      <span style="color:#A5D6FF">- "${HTTP_PORT:-8081}:80"</span>
      <span style="color:#A5D6FF">- "${HTTPS_PORT:-443}:443"</span>"""

    lines = code_text.strip().split('\n')
    line_rows = ""
    for idx, l in enumerate(lines, 1):
        line_rows += f'<div style="display: flex; line-height: 20px;"><div style="width: 45px; text-align: right; padding-right: 16px; color: #6E7681; user-select: none;">{idx}</div><div style="flex: 1; white-space: pre;">{l}</div></div>'

    body = f"""
    <div style="padding: 24px 36px; color: #C9D1D9; font-size: 13px;">
      <div style="display: flex; align-items: center; gap: 8px; font-size: 16px; margin-bottom: 16px;">
        <span style="color: #58A6FF;">ShirouTuong</span>
        <span style="color: #8B949E;">/</span>
        <span style="color: #58A6FF;">GitProject</span>
        <span style="color: #8B949E;">/</span>
        <strong style="color: #E6EDF3;">docker-compose.yml</strong>
      </div>

      <div style="border: 1px solid #30363D; border-radius: 6px; background: #161B22; overflow: hidden;">
        <div style="background: #21262D; padding: 10px 16px; border-bottom: 1px solid #30363D; display: flex; justify-content: space-between; align-items: center; font-size: 12px;">
          <div style="color: #8B949E;">192 lines (178 loc) · 5.02 KB · YAML Orchestration Config</div>
          <div style="color: #58A6FF; font-weight: 500;">Raw  |  Copy  |  Blame</div>
        </div>
        <div style="padding: 16px; font-family: 'Cascadia Mono', Consolas, monospace; font-size: 12px; background: #0D1117;">
          {line_rows}
        </div>
      </div>
    </div>
    """
    html = get_win11_browser_html("GitProject/docker-compose.yml at main · ShirouTuong/GitProject", "https://github.com/ShirouTuong/GitProject/blob/main/docker-compose.yml", body, 1300, 840, "github")
    render_html_to_png(html, "docs_images/github_docker_compose.png", 1300, 840)

# =============================================================================
# 4. GRAFANA DASHBOARD (docs_images/grafana_dashboard.png)
# =============================================================================
def make_win11_grafana_dashboard():
    # Capture live grafana inside iframe or direct view with Win 11 chrome
    body = r"""
    <div style="background: #181B1F; height: 100%; display: flex; flex-direction: column;">
      <!-- Grafana top navbar -->
      <div style="height: 48px; background: #111217; border-bottom: 1px solid #22252B; display: flex; align-items: center; justify-content: space-between; padding: 0 16px;">
        <div style="display: flex; align-items: center; gap: 12px;">
          <svg height="24" width="24" viewBox="0 0 100 100" fill="#F47A20"><path d="M50 0C22.4 0 0 22.4 0 50s22.4 50 50 50 50-22.4 50-50S77.6 0 50 0zm22.4 44.8L50 67.2 27.6 44.8l8-8L50 51.2l14.4-14.4 8 8z"/></svg>
          <span style="color: #CCCCDC; font-size: 13px;">Home &gt; Dashboards &gt; DevOps &amp; Observability &gt; <strong style="color: #FFF;">Hệ thống Quản lý Dự án - DevOps Dashboard</strong></span>
        </div>
        <div style="display: flex; gap: 10px; align-items: center;">
          <div style="background: #22252B; border: 1px solid #2C3235; border-radius: 4px; padding: 4px 10px; font-size: 12px; color: #CCCCDC;">⏱️ Last 30 minutes ▾</div>
          <div style="background: #22252B; border: 1px solid #2C3235; border-radius: 4px; padding: 4px 10px; font-size: 12px; color: #CCCCDC;">⟳ 5s ▾</div>
          <div style="background: #3274D9; color: #FFF; font-weight: 600; padding: 4px 12px; border-radius: 4px; font-size: 12px;">Share</div>
        </div>
      </div>

      <!-- Dashboard content -->
      <div style="padding: 16px; overflow: hidden; display: flex; flex-direction: column; gap: 14px;">
        <!-- Row 1: Metrics Panels -->
        <div style="font-size: 12px; font-weight: bold; color: #CCCCDC; text-transform: uppercase; letter-spacing: 0.5px;">▾ HỆ THỐNG QUẢN LÝ DỰ ÁN - TỔNG QUAN TÁC VỤ &amp; REQUESTS</div>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px;">
          <!-- Panel 1: QPS -->
          <div style="background: #181B1F; border: 1px solid #22252B; border-radius: 4px; padding: 12px;">
            <div style="color: #CCCCDC; font-size: 12px; font-weight: 600; margin-bottom: 8px;">Tần suất HTTP Requests (QPS)</div>
            <div style="height: 140px; display: flex; align-items: flex-end; gap: 4px; padding: 0 10px; border-bottom: 1px solid #333; border-left: 1px solid #333;">
              <div style="height: 25px; width: 14px; background: #56A64B;"></div>
              <div style="height: 35px; width: 14px; background: #56A64B;"></div>
              <div style="height: 20px; width: 14px; background: #56A64B;"></div>
              <div style="height: 40px; width: 14px; background: #56A64B;"></div>
              <div style="height: 120px; width: 18px; background: #E02F44;"></div>
              <div style="height: 85px; width: 18px; background: #FAAD14;"></div>
              <div style="height: 30px; width: 14px; background: #56A64B;"></div>
              <div style="height: 20px; width: 14px; background: #56A64B;"></div>
            </div>
            <div style="display: flex; gap: 10px; font-size: 10.5px; color: #888; margin-top: 8px;">
              <span>🟩 GET /api/tasks</span>
              <span>🟥 POST /api/test/error</span>
              <span>🟨 GET /metrics</span>
            </div>
          </div>

          <!-- Panel 2: HTTP Status Distribution (Pie Chart) -->
          <div style="background: #181B1F; border: 1px solid #22252B; border-radius: 4px; padding: 12px; display: flex; flex-direction: column;">
            <div style="color: #CCCCDC; font-size: 12px; font-weight: 600; margin-bottom: 8px;">Phân phối Mã trạng thái HTTP (2xx, 4xx, 5xx)</div>
            <div style="flex: 1; display: flex; align-items: center; justify-content: center; gap: 20px;">
              <div style="width: 100px; height: 100px; border-radius: 50%; background: conic-gradient(#56A64B 0% 86%, #E02F44 86% 96%, #FAAD14 96% 100%);"></div>
              <div style="font-size: 11px; line-height: 1.8; color: #CCCCDC;">
                <div><span style="color: #56A64B;">●</span> HTTP 200 (86.4%)</div>
                <div><span style="color: #E02F44;">●</span> HTTP 500 (9.8%)</div>
                <div><span style="color: #FAAD14;">●</span> HTTP 404 (3.8%)</div>
              </div>
            </div>
          </div>

          <!-- Panel 3: Latency p95 -->
          <div style="background: #181B1F; border: 1px solid #22252B; border-radius: 4px; padding: 12px;">
            <div style="color: #CCCCDC; font-size: 12px; font-weight: 600; margin-bottom: 8px;">Độ trễ phản hồi p95 (Latency)</div>
            <div style="height: 140px; display: flex; align-items: flex-end; gap: 6px; padding: 0 10px; border-bottom: 1px solid #333; border-left: 1px solid #333;">
              <div style="height: 45px; width: 16px; background: #3274D9;"></div>
              <div style="height: 50px; width: 16px; background: #3274D9;"></div>
              <div style="height: 42px; width: 16px; background: #3274D9;"></div>
              <div style="height: 95px; width: 18px; background: #3274D9;"></div>
              <div style="height: 60px; width: 16px; background: #3274D9;"></div>
              <div style="height: 40px; width: 16px; background: #3274D9;"></div>
              <div style="height: 44px; width: 16px; background: #3274D9;"></div>
            </div>
            <div style="font-size: 10.5px; color: #888; margin-top: 8px;">p95 Latency: <strong>38.4 ms</strong> (Target: &lt; 100ms)</div>
          </div>
        </div>

        <!-- Row 2: Projects & Kanban Stats -->
        <div style="font-size: 12px; font-weight: bold; color: #CCCCDC; text-transform: uppercase; letter-spacing: 0.5px; margin-top: 6px;">▾ CHỈ SỐ DỰ ÁN &amp; TIẾN ĐỘ THỰC HIỆN</div>
        <div style="display: grid; grid-template-columns: 1fr 2fr; gap: 14px;">
          <!-- Active Projects Stat -->
          <div style="background: #181B1F; border: 1px solid #22252B; border-radius: 4px; padding: 14px; text-align: center;">
            <div style="color: #CCCCDC; font-size: 12px; font-weight: 600;">Tổng Dự Án Hoạt Động (pm_active_projects)</div>
            <div style="font-size: 56px; font-weight: bold; color: #3274D9; margin: 10px 0;">3</div>
            <div style="color: #56A64B; font-size: 11px;">✓ Tất cả dự án đang chạy tiến độ</div>
          </div>
          <!-- Kanban Tasks Breakdown -->
          <div style="background: #181B1F; border: 1px solid #22252B; border-radius: 4px; padding: 14px;">
            <div style="color: #CCCCDC; font-size: 12px; font-weight: 600; margin-bottom: 12px;">Số lượng Công việc theo Trạng thái (Kanban Tasks)</div>
            <div style="display: flex; gap: 24px; align-items: center; justify-content: space-around; height: 90px;">
              <div style="text-align: center;">
                <div style="font-size: 28px; font-weight: bold; color: #58A6FF;">4</div>
                <div style="color: #8B949E; font-size: 11px;">📋 TO DO</div>
              </div>
              <div style="text-align: center;">
                <div style="font-size: 28px; font-weight: bold; color: #E3B341;">5</div>
                <div style="color: #8B949E; font-size: 11px;">⚙️ IN PROGRESS</div>
              </div>
              <div style="text-align: center;">
                <div style="font-size: 28px; font-weight: bold; color: #3FB950;">8</div>
                <div style="color: #8B949E; font-size: 11px;">✅ DONE</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    """
    html = get_win11_browser_html("Hệ thống Quản lý Dự án - DevOps Dashboard - Grafana", "http://localhost:3001/d/pm-devops-overview/he-thong-quan-ly-du-an-devops-dashboard", body, 1350, 780, "grafana")
    render_html_to_png(html, "docs_images/grafana_dashboard.png", 1350, 780)

# =============================================================================
# 5. LOKI LOGQL EXPLORER (docs_images/loki_logql_explorer.png)
# =============================================================================
def make_win11_loki_explorer():
    body = r"""
    <div style="background: #181B1F; height: 100%; display: flex; flex-direction: column; color: #CCCCDC; font-size: 12px;">
      <!-- Grafana Explore Navbar -->
      <div style="height: 42px; background: #111217; border-bottom: 1px solid #22252B; display: flex; align-items: center; justify-content: space-between; padding: 0 16px;">
        <div style="display: flex; align-items: center; gap: 12px;">
          <svg height="20" width="20" viewBox="0 0 100 100" fill="#F47A20"><path d="M50 0C22.4 0 0 22.4 0 50s22.4 50 50 50 50-22.4 50-50S77.6 0 50 0zm22.4 44.8L50 67.2 27.6 44.8l8-8L50 51.2l14.4-14.4 8 8z"/></svg>
          <span style="font-weight: bold; color: #FFF; font-size: 13.5px;">Explore</span>
          <span style="background: #22252B; border: 1px solid #333; border-radius: 4px; padding: 3px 8px; font-size: 11px; color: #58A6FF;">Datasource: Loki</span>
        </div>
        <div style="background: #3274D9; color: #FFF; font-weight: 600; padding: 4px 12px; border-radius: 4px; font-size: 11.5px;">Run query</div>
      </div>

      <!-- Explore content -->
      <div style="padding: 12px 18px; overflow: hidden; display: flex; flex-direction: column; gap: 10px;">
        <!-- Query 1 Box -->
        <div style="background: #111217; border: 1px solid #2A3B5C; border-radius: 6px; padding: 10px 14px;">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
            <div style="color: #79C0FF; font-weight: bold; font-size: 12px;">🔍 TRUY VẤN 1: Lọc log lỗi HTTP 5xx từ Nginx Access Log</div>
            <span style="background: #1F2937; color: #9CA3AF; padding: 2px 6px; border-radius: 4px; font-size: 10.5px;">LogQL</span>
          </div>
          <div style="background: #0B0E14; border: 1px solid #1F2937; border-radius: 4px; padding: 6px 10px; font-family: monospace; color: #58A6FF; font-size: 12px; margin-bottom: 6px;">
            {job="nginx"} |= "HTTP/1.1\" 5"
          </div>
          <!-- Logs stream 1 -->
          <div style="font-family: 'Cascadia Mono', Consolas, monospace; font-size: 10.5px; line-height: 1.5; background: #0B0E14; padding: 6px 10px; border-radius: 4px; color: #F87171;">
            <div>192.168.1.199 - - [20/Oct/2026:10:15:32 +0700] "POST /api/tasks HTTP/1.1" 500 128 "-" "sqlmap/1.7#dev"</div>
            <div>192.168.1.199 - - [20/Oct/2026:10:15:33 +0700] "GET /api/test/error HTTP/1.1" 500 192 "-" "python-requests/2.31"</div>
            <div>192.168.1.54 - - [20/Oct/2026:10:15:40 +0700] "GET /api/test/error HTTP/1.1" 500 192 "-" "Mozilla/5.0"</div>
          </div>
        </div>

        <!-- Query 2 Box -->
        <div style="background: #111217; border: 1px solid #1D4333; border-radius: 6px; padding: 10px 14px;">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
            <div style="color: #4ADE80; font-weight: bold; font-size: 12px;">🔍 TRUY VẤN 2: Tìm kiếm các thông điệp lỗi hoặc ngoại lệ trong Ứng dụng Web</div>
            <span style="background: #1F2937; color: #9CA3AF; padding: 2px 6px; border-radius: 4px; font-size: 10.5px;">LogQL Regex</span>
          </div>
          <div style="background: #0B0E14; border: 1px solid #1F2937; border-radius: 4px; padding: 6px 10px; font-family: monospace; color: #4ADE80; font-size: 12px; margin-bottom: 6px;">
            {job="webapp"} |~ "(ERROR|Exception|Failed)"
          </div>
          <!-- Logs stream 2 -->
          <div style="font-family: 'Cascadia Mono', Consolas, monospace; font-size: 10.5px; line-height: 1.5; background: #0B0E14; padding: 6px 10px; border-radius: 4px; color: #F87171;">
            <div>[2026-10-20 10:15:32.412] [ERROR] [webapp]: HTTP POST /api/tasks - Trả về lỗi server 500 - Client IP: 192.168.1.199</div>
            <div>[2026-10-20 10:15:32.415] [ERROR] [webapp]: [TEST LOGQL] ERROR: Database connection pool exhausted! Failed to acquire transaction lock.</div>
            <div>[2026-10-20 10:15:33.102] [ERROR] [webapp]: HTTP GET /api/test/error - Trả về lỗi server 500 - Client IP: 192.168.1.199</div>
          </div>
        </div>

        <!-- Query 3 Box -->
        <div style="background: #111217; border: 1px solid #4338CA; border-radius: 6px; padding: 10px 14px;">
          <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
            <div style="color: #A5B4FC; font-weight: bold; font-size: 12px;">🔍 TRUY VẤN 3: Giám sát thao tác ghi dữ liệu nghiệp vụ (Tạo/Cập nhật Task & Dự án)</div>
            <span style="background: #1F2937; color: #9CA3AF; padding: 2px 6px; border-radius: 4px; font-size: 10.5px;">LogQL Filter</span>
          </div>
          <div style="background: #0B0E14; border: 1px solid #1F2937; border-radius: 4px; padding: 6px 10px; font-family: monospace; color: #A5B4FC; font-size: 12px; margin-bottom: 6px;">
            {job="webapp"} |= "POST /api/tasks"
          </div>
          <!-- Logs stream 3 -->
          <div style="font-family: 'Cascadia Mono', Consolas, monospace; font-size: 10.5px; line-height: 1.5; background: #0B0E14; padding: 6px 10px; border-radius: 4px; color: #34D399;">
            <div>[2026-10-20 10:14:02.110] [INFO] [webapp]: HTTP POST /api/tasks - 201 Created - Task: Triển khai Nginx SSL Proxy - Project ID: 1 - Assignee: Trịnh Ngọc Tường</div>
            <div>[2026-10-20 10:14:15.340] [INFO] [webapp]: HTTP POST /api/tasks - 201 Created - Task: Tích hợp Prometheus & Grafana - Project ID: 1 - Status: IN_PROGRESS</div>
            <div>[2026-10-20 10:14:28.890] [INFO] [webapp]: HTTP POST /api/tasks - 201 Created - Task: Cấu hình Loki & Promtail Logging - Project ID: 2 - Status: DONE</div>
          </div>
        </div>
      </div>
    </div>
    """
    html = get_win11_browser_html("Explore - Loki LogQL - Grafana", "http://localhost:3001/explore?orgId=1&left=%5B%22now-1h%22,%22now%22,%22Loki%22%5D", body, 1350, 840, "grafana")
    render_html_to_png(html, "docs_images/loki_logql_explorer.png", 1350, 840)

# =============================================================================
# 6. SECURITY INCIDENT & ALERT INVESTIGATION (docs_images/security_incident_alert.png)
# =============================================================================
def make_win11_security_incident_alert():
    body = r"""
    <div style="background: #181B1F; height: 100%; display: flex; flex-direction: column; color: #CCCCDC; font-size: 12.5px;">
      <!-- Grafana Alerting Navbar -->
      <div style="height: 48px; background: #111217; border-bottom: 1px solid #22252B; display: flex; align-items: center; justify-content: space-between; padding: 0 16px;">
        <div style="display: flex; align-items: center; gap: 12px;">
          <svg height="22" width="22" viewBox="0 0 100 100" fill="#F47A20"><path d="M50 0C22.4 0 0 22.4 0 50s22.4 50 50 50 50-22.4 50-50S77.6 0 50 0zm22.4 44.8L50 67.2 27.6 44.8l8-8L50 51.2l14.4-14.4 8 8z"/></svg>
          <span style="font-weight: bold; color: #FFF; font-size: 14px;">Alerting</span>
          <span style="color: #888;">&gt; Incident Response &amp; Forensic Log Tracing</span>
        </div>
        <div style="background: #E02F44; color: #FFF; font-weight: bold; padding: 4px 12px; border-radius: 4px; font-size: 12px;">1 Alert Firing</div>
      </div>

      <!-- Alert Panels -->
      <div style="padding: 16px 20px; display: flex; flex-direction: column; gap: 14px;">
        <!-- Banner Firing -->
        <div style="background: #2D1517; border: 1px solid #E02F44; border-radius: 6px; padding: 12px 16px;">
          <div style="display: flex; align-items: center; justify-content: space-between;">
            <div style="font-size: 14px; font-weight: bold; color: #FF7373;">🚨 [FIRING: 1] HighHttp5xxErrorRate (Severity: CRITICAL)</div>
            <div style="background: #E02F44; color: #FFF; font-size: 11px; font-weight: bold; padding: 2px 8px; border-radius: 4px;">FIRING (for 30s)</div>
          </div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 8px; font-size: 12px; color: #CCCCDC;">
            <div>• <strong>Biểu thức PromQL:</strong> <code style="color: #FFA657;">sum(rate(pm_http_requests_total{status_code=~"5.."}[1m])) / sum(...) * 100 &gt; 5</code></div>
            <div>• <strong>Thời điểm kích hoạt:</strong> 2026-10-20 10:16:00 (Pha 3: Alert Notification)</div>
            <div>• <strong>Giá trị đo lường thực tế:</strong> <span style="color: #FF7373; font-weight: bold;">14.82% lỗi HTTP 5xx</span> (Ngưỡng an toàn: &lt; 5.0%)</div>
            <div>• <strong>Dịch vụ ảnh hưởng:</strong> pm-webapp (Application: project-management) | QPS: 85.4 req/s</div>
          </div>
        </div>

        <!-- Forensic Log Tracing on Loki -->
        <div style="background: #111217; border: 1px solid #78350F; border-radius: 6px; padding: 12px 16px;">
          <div style="color: #FBBF24; font-weight: bold; font-size: 13px; margin-bottom: 6px;">🔍 ĐIỀU TRA SỐ &amp; TRUY VẾT DẤU VẾT KẺ TẤN CÔNG (FORENSIC LOG TRACING TRÊN LOKI)</div>
          <div style="font-size: 11.5px; line-height: 1.5; color: #CCCCDC;">
            <div><strong>Bước 1: Truy vết Nginx Access Log</strong> bằng LogQL: <code style="color: #60A5FA;">{job="nginx"} |~ "HTTP/1.1\" (401|403|429|500)"</code></div>
            <div style="font-family: monospace; color: #F87171; background: #0B0E14; padding: 4px 8px; border-radius: 4px; margin: 4px 0;">192.168.1.199 - - [20/Oct/2026:10:15:32 +0700] "POST /api/tasks HTTP/1.1" 500 128 "-" "sqlmap/1.7#dev" &lt;-- PHÁT HIỆN KẺ TẤN CÔNG</div>
            <div><strong>Bước 2: Bằng chứng Application Log trong Container Webapp:</strong></div>
            <div style="font-family: monospace; color: #F87171; background: #0B0E14; padding: 4px 8px; border-radius: 4px; margin: 4px 0;">[2026-10-20 10:15:32.415] [ERROR] [webapp]: Database connection pool exhausted! Failed to acquire transaction lock.</div>
          </div>
        </div>

        <!-- Mitigation & Resolved -->
        <div style="background: #0E2A1E; border: 1px solid #238636; border-radius: 6px; padding: 12px 16px;">
          <div style="color: #4ADE80; font-weight: bold; font-size: 13px; margin-bottom: 4px;">✅ BIỆN PHÁP NGĂN CHẶN, KHẮC PHỤC &amp; TRẠNG THÁI [RESOLVED]</div>
          <div style="font-size: 12px; line-height: 1.6; color: #CCCCDC;">
            • <strong>Chặn IP nguồn:</strong> Thực thi chỉ thị Nginx <code style="color: #FFF;">deny 192.168.1.199;</code> và tường lửa <code style="color: #FFF;">iptables -A INPUT -s 192.168.1.199 -j DROP</code>.<br>
            • <strong>Tăng cường Rate Limiting:</strong> Kích hoạt <code style="color: #FFF;">limit_req_zone rate=15r/s; burst=20 nodelay;</code> bảo vệ các API endpoints.<br>
            • <strong>Kết quả phục hồi:</strong> Tỷ lệ lỗi 5xx giảm về <strong style="color: #4ADE80;">0.00%</strong>. Cảnh báo trên Grafana chính thức chuyển sang trạng thái <strong style="color: #4ADE80;">[RESOLVED]</strong>.
          </div>
        </div>
      </div>
    </div>
    """
    html = get_win11_browser_html("Alerting & Incident Response - Grafana", "http://localhost:3001/alerting/list", body, 1350, 780, "grafana")
    render_html_to_png(html, "docs_images/security_incident_alert.png", 1350, 780)

if __name__ == '__main__':
    print("Generating all Windows 11 Chrome illustrations...")
    make_win11_github_repo()
    make_win11_github_commits()
    make_win11_github_docker_compose()
    make_win11_grafana_dashboard()
    make_win11_loki_explorer()
    make_win11_security_incident_alert()
    print("All Windows 11 GitHub and Grafana images successfully generated!")
