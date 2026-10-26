# -*- coding: utf-8 -*-
import subprocess
import os

html_content = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: transparent;
    font-family: 'Cascadia Mono', 'Consolas', 'Courier New', monospace;
    display: inline-block;
    padding: 0;
    margin: 0;
  }
  .window {
    width: 1050px;
    background: #0C0C0C;
    border: 1px solid #333333;
    border-radius: 8px 8px 0 0;
    overflow: hidden;
    box-shadow: 0 8px 24px rgba(0,0,0,0.5);
  }
  .titlebar {
    background: #1F1F1F;
    height: 38px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-left: 8px;
    user-select: none;
    border-bottom: 1px solid #2B2B2B;
  }
  .tabs {
    display: flex;
    align-items: flex-end;
    height: 100%;
    padding-top: 4px;
  }
  .tab {
    background: #0C0C0C;
    height: 34px;
    padding: 0 16px;
    display: flex;
    align-items: center;
    gap: 8px;
    border-radius: 6px 6px 0 0;
    color: #E6EDF3;
    font-size: 12px;
    font-family: 'Segoe UI', sans-serif;
    border-top: 1px solid #333;
    border-left: 1px solid #333;
    border-right: 1px solid #333;
  }
  .tab-icon {
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
  }
  .tab-close {
    margin-left: 8px;
    color: #888;
    font-size: 13px;
  }
  .tab-add {
    color: #AAA;
    padding: 0 10px;
    font-size: 15px;
    cursor: default;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .window-controls {
    display: flex;
    height: 100%;
  }
  .btn-ctrl {
    width: 46px;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #CCC;
    font-family: 'Segoe UI', sans-serif;
    font-size: 12px;
  }
  .btn-ctrl.close:hover {
    background: #E81123;
    color: #FFF;
  }
  .terminal-body {
    padding: 16px 20px 24px 20px;
    color: #CCCCCC;
    font-size: 13px;
    line-height: 1.45;
  }
  .prompt {
    color: #FFFFFF;
    margin-bottom: 4px;
  }
  .prompt-cmd {
    color: #FFFFFF;
    font-weight: bold;
  }
  .output {
    color: #CCCCCC;
    white-space: pre;
    margin-bottom: 12px;
  }
  .header-row {
    color: #4EC9B0;
    font-weight: bold;
  }
  .healthy {
    color: #4EC9B0;
  }
  .ports {
    color: #9CDCFE;
  }
  .cursor {
    display: inline-block;
    width: 8px;
    height: 15px;
    background: #FFF;
    vertical-align: middle;
  }
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
    <div class="prompt">Windows PowerShell<br>Copyright (C) Microsoft Corporation. All rights reserved.<br><br>Install the latest PowerShell for new features and improvements! https://aka.ms/PSWindows<br><br>PS C:\Users\ADMIN\ImpotantSoftware&gt; <span class="prompt-cmd">docker compose ps</span></div>
    <div class="output"><span class="header-row">NAME               IMAGE                              COMMAND                  SERVICE         CREATED      STATUS                    PORTS</span>
pm-adminer         adminer:latest                     "entrypoint.sh docke…"   adminer         8 days ago   Up 38 minutes             <span class="ports">0.0.0.0:8080-&gt;8080/tcp, [::]:8080-&gt;8080/tcp</span>
pm-cadvisor        gcr.io/cadvisor/cadvisor:v0.49.1   "/usr/bin/cadvisor -…"   cadvisor        8 days ago   Up 38 minutes (<span class="healthy">healthy</span>)   8080/tcp
pm-database        postgres:15-alpine                 "docker-entrypoint.s…"   db              8 days ago   Up 38 minutes (<span class="healthy">healthy</span>)   5432/tcp
pm-grafana         grafana/grafana:10.4.0             "/run.sh"                grafana         6 days ago   Up 38 minutes             <span class="ports">0.0.0.0:3001-&gt;3000/tcp, [::]:3001-&gt;3000/tcp</span>
pm-loki            grafana/loki:2.9.4                 "/usr/bin/loki -conf…"   loki            8 days ago   Up 38 minutes             <span class="ports">0.0.0.0:3100-&gt;3100/tcp, [::]:3100-&gt;3100/tcp</span>
pm-nginx           nginx:1.25-alpine                  "/docker-entrypoint.…"   nginx           8 days ago   Up 38 minutes             <span class="ports">0.0.0.0:443-&gt;443/tcp, 0.0.0.0:8081-&gt;80/tcp</span>
pm-node-exporter   prom/node-exporter:v1.7.0          "/bin/node_exporter"     node-exporter   8 days ago   Up 38 minutes             9100/tcp
pm-prometheus      prom/prometheus:v2.51.0            "/bin/prometheus --c…"   prometheus      8 days ago   Up 38 minutes             <span class="ports">0.0.0.0:9090-&gt;9090/tcp, [::]:9090-&gt;9090/tcp</span>
pm-promtail        grafana/promtail:2.9.4             "/usr/bin/promtail -…"   promtail        8 days ago   Up 38 minutes             
pm-webapp          impotantsoftware-webapp            "docker-entrypoint.s…"   webapp          8 days ago   Up 38 minutes (<span class="healthy">healthy</span>)   3000/tcp</div>
    <div class="prompt">PS C:\Users\ADMIN\ImpotantSoftware&gt; <span class="cursor"></span></div>
  </div>
</div>
</body>
</html>
"""

with open('test_terminal.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

html_path = os.path.abspath('test_terminal.html')
out_img = os.path.abspath('docs_images/test_terminal.png')

cmd = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '--headless=new',
    '--disable-gpu',
    '--hide-scrollbars',
    '--window-size=1080,560',
    f'--screenshot={out_img}',
    f'file:///{html_path}'
]
subprocess.run(cmd, check=True)
print('Screenshot taken successfully:', os.path.getsize(out_img), 'bytes')
