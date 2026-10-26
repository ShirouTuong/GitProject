# -*- coding: utf-8 -*-
"""
Script thiet lap cac Alert Rules tren Grafana Alerting cho He thong Quan ly Du an
Tuong ung voi Muc 3.3 trong Bao cao: Mo phong Su co An toan Thong tin & Canh bao Alerting
"""
import urllib.request
import urllib.error
import base64
import json
import os

GRAFANA_URL = "http://localhost:3001"
AUTH_HEADER = "Basic " + base64.b64encode(b"admin:AdminSecure@2026!").decode()

def api_request(path, method="GET", data=None):
    url = f"{GRAFANA_URL}{path}"
    headers = {
        "Authorization": AUTH_HEADER,
        "Content-Type": "application/json"
    }
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8")
        print(f"HTTP Error {e.code} on {path}: {err_msg}")
        return None

def setup_alerts():
    # 1. Lay hoac tao thu muc Alerts
    folders = api_request("/api/folders")
    folder_uid = "bg1ikms7pibk0e"
    if not folders:
        f_resp = api_request("/api/folders", method="POST", data={"title": "DevOps & Observability"})
        if f_resp and "uid" in f_resp:
            folder_uid = f_resp["uid"]
    else:
        folder_uid = folders[0]["uid"]

    print(f"Using Folder UID: {folder_uid}")

    # 2. Dinh nghia cac Alert Rules theo tieu chuan Bao cao Muc 3.3
    rules = [
        {
            "uid": "alert_http_5xx_incident",
            "title": "High HTTP 5xx Error Rate Incident (An Toàn Thông Tin)",
            "folderUID": folder_uid,
            "ruleGroup": "Security & Incident Alerts",
            "noDataState": "OK",
            "execErrState": "Error",
            "for": "0s",
            "annotations": {
                "summary": "Cảnh báo Tỷ lệ Lỗi HTTP 5xx vượt ngưỡng an toàn (> 5%)",
                "description": "Hệ thống phát hiện dấu hiệu bất thường: Tỷ lệ mã phản hồi 5xx tăng đột biến trên cổng Nginx / Webapp, nghi vấn tấn công từ chối dịch vụ hoặc cạn kiệt tài nguyên CSDL."
            },
            "labels": {
                "severity": "critical",
                "team": "devops-soc",
                "incident": "security-attack-simulation"
            },
            "condition": "C",
            "data": [
                {
                    "refId": "A",
                    "queryType": "",
                    "relativeTimeRange": {"from": 300, "to": 0},
                    "datasourceUid": "Prometheus",
                    "model": {
                        "editorMode": "code",
                        "expr": 'sum(rate(pm_http_requests_total{status_code=~"5.."}[1m])) or vector(0)',
                        "intervalMs": 1000,
                        "maxDataPoints": 43200,
                        "range": True,
                        "refId": "A"
                    }
                },
                {
                    "refId": "B",
                    "queryType": "",
                    "relativeTimeRange": {"from": 300, "to": 0},
                    "datasourceUid": "__expr__",
                    "model": {
                        "conditions": [
                            {
                                "evaluator": {"params": [0], "type": "gt"},
                                "operator": {"type": "and"},
                                "query": {"params": ["B"]},
                                "reducer": {"params": [], "type": "last"},
                                "type": "query"
                            }
                        ],
                        "datasource": {"name": "Expression", "type": "__expr__", "uid": "__expr__"},
                        "expression": "A",
                        "reducer": "last",
                        "refId": "B",
                        "type": "reduce"
                    }
                },
                {
                    "refId": "C",
                    "queryType": "",
                    "relativeTimeRange": {"from": 300, "to": 0},
                    "datasourceUid": "__expr__",
                    "model": {
                        "conditions": [
                            {
                                "evaluator": {"params": [0.1], "type": "gt"},
                                "operator": {"type": "and"},
                                "query": {"params": ["C"]},
                                "reducer": {"params": [], "type": "last"},
                                "type": "query"
                            }
                        ],
                        "datasource": {"name": "Expression", "type": "__expr__", "uid": "__expr__"},
                        "expression": "$B > 0.1",
                        "refId": "C",
                        "type": "math"
                    }
                }
            ]
        },
        {
            "uid": "alert_webapp_container_down",
            "title": "Web Application Container Status (Health Check)",
            "folderUID": folder_uid,
            "ruleGroup": "Security & Incident Alerts",
            "noDataState": "Alerting",
            "execErrState": "Error",
            "for": "0s",
            "annotations": {
                "summary": "Giám sát trạng thái khả dụng của Container Web Application",
                "description": "Container pm-webapp không phản hồi HTTP probe từ Prometheus."
            },
            "labels": {
                "severity": "warning",
                "team": "devops-soc"
            },
            "condition": "C",
            "data": [
                {
                    "refId": "A",
                    "queryType": "",
                    "relativeTimeRange": {"from": 300, "to": 0},
                    "datasourceUid": "Prometheus",
                    "model": {
                        "editorMode": "code",
                        "expr": 'up{job="webapp"}',
                        "intervalMs": 1000,
                        "maxDataPoints": 43200,
                        "range": True,
                        "refId": "A"
                    }
                },
                {
                    "refId": "B",
                    "queryType": "",
                    "relativeTimeRange": {"from": 300, "to": 0},
                    "datasourceUid": "__expr__",
                    "model": {
                        "conditions": [
                            {
                                "evaluator": {"params": [0], "type": "gt"},
                                "operator": {"type": "and"},
                                "query": {"params": ["B"]},
                                "reducer": {"params": [], "type": "last"},
                                "type": "query"
                            }
                        ],
                        "datasource": {"name": "Expression", "type": "__expr__", "uid": "__expr__"},
                        "expression": "A",
                        "reducer": "last",
                        "refId": "B",
                        "type": "reduce"
                    }
                },
                {
                    "refId": "C",
                    "queryType": "",
                    "relativeTimeRange": {"from": 300, "to": 0},
                    "datasourceUid": "__expr__",
                    "model": {
                        "conditions": [
                            {
                                "evaluator": {"params": [1], "type": "lt"},
                                "operator": {"type": "and"},
                                "query": {"params": ["C"]},
                                "reducer": {"params": [], "type": "last"},
                                "type": "query"
                            }
                        ],
                        "datasource": {"name": "Expression", "type": "__expr__", "uid": "__expr__"},
                        "expression": "$B < 1",
                        "refId": "C",
                        "type": "math"
                    }
                }
            ]
        }
    ]

    for rule in rules:
        resp = api_request("/api/v1/provisioning/alert-rules", method="POST", data=rule)
        if resp:
            print(f"Created Alert Rule: {rule['title']} (UID: {rule['uid']})")
        else:
            # Thu update neu da ton tai
            resp_put = api_request(f"/api/v1/provisioning/alert-rules/{rule['uid']}", method="PUT", data=rule)
            if resp_put:
                print(f"Updated Alert Rule: {rule['title']} (UID: {rule['uid']})")

    # Save to yaml file provisioning so it persists
    os.makedirs("monitoring/grafana/provisioning/alerting", exist_ok=True)
    yaml_content = """apiVersion: 1

groups:
  - orgId: 1
    name: Security & Incident Alerts
    folder: DevOps & Observability
    interval: 10s
    rules:
      - uid: alert_http_5xx_incident
        title: High HTTP 5xx Error Rate Incident (An Toàn Thông Tin)
        condition: C
        data:
          - refId: A
            relativeTimeRange:
              from: 300
              to: 0
            datasourceUid: Prometheus
            model:
              editorMode: code
              expr: sum(rate(pm_http_requests_total{status_code=~"5.."}[1m])) or vector(0)
              intervalMs: 1000
              maxDataPoints: 43200
              range: true
              refId: A
          - refId: B
            relativeTimeRange:
              from: 300
              to: 0
            datasourceUid: __expr__
            model:
              conditions:
                - evaluator:
                    params:
                      - 0
                    type: gt
                  operator:
                    type: and
                  query:
                    params:
                      - B
                  reducer:
                    params: []
                    type: last
                  type: query
              datasource:
                name: Expression
                type: __expr__
                uid: __expr__
              expression: A
              reducer: last
              refId: B
              type: reduce
          - refId: C
            relativeTimeRange:
              from: 300
              to: 0
            datasourceUid: __expr__
            model:
              conditions:
                - evaluator:
                    params:
                      - 0.1
                    type: gt
                  operator:
                    type: and
                  query:
                    params:
                      - C
                  reducer:
                    params: []
                    type: last
                  type: query
              datasource:
                name: Expression
                type: __expr__
                uid: __expr__
              expression: $B > 0.1
              refId: C
              type: math
        noDataState: OK
        execErrState: Error
        for: 0s
        annotations:
          summary: "Cảnh báo Tỷ lệ Lỗi HTTP 5xx vượt ngưỡng an toàn (> 5%)"
          description: "Hệ thống phát hiện dấu hiệu bất thường: Tỷ lệ mã phản hồi 5xx tăng đột biến trên cổng Nginx / Webapp, nghi vấn tấn công từ chối dịch vụ hoặc cạn kiệt tài nguyên CSDL."
        labels:
          severity: critical
          team: devops-soc
          incident: security-attack-simulation

      - uid: alert_webapp_container_down
        title: Web Application Container Status (Health Check)
        condition: C
        data:
          - refId: A
            relativeTimeRange:
              from: 300
              to: 0
            datasourceUid: Prometheus
            model:
              editorMode: code
              expr: up{job="webapp"}
              intervalMs: 1000
              maxDataPoints: 43200
              range: true
              refId: A
          - refId: B
            relativeTimeRange:
              from: 300
              to: 0
            datasourceUid: __expr__
            model:
              conditions:
                - evaluator:
                    params:
                      - 0
                    type: gt
                  operator:
                    type: and
                  query:
                    params:
                      - B
                  reducer:
                    params: []
                    type: last
                  type: query
              datasource:
                name: Expression
                type: __expr__
                uid: __expr__
              expression: A
              reducer: last
              refId: B
              type: reduce
          - refId: C
            relativeTimeRange:
              from: 300
              to: 0
            datasourceUid: __expr__
            model:
              conditions:
                - evaluator:
                    params:
                      - 1
                    type: lt
                  operator:
                    type: and
                  query:
                    params:
                      - C
                  reducer:
                    params: []
                    type: last
                  type: query
              datasource:
                name: Expression
                type: __expr__
                uid: __expr__
              expression: $B < 1
              refId: C
              type: math
        noDataState: Alerting
        execErrState: Error
        for: 0s
        annotations:
          summary: "Giám sát trạng thái khả dụng của Container Web Application"
          description: "Container pm-webapp không phản hồi HTTP probe từ Prometheus."
        labels:
          severity: warning
          team: devops-soc
"""
    with open("monitoring/grafana/provisioning/alerting/alert_rules.yaml", "w", encoding="utf-8") as f:
        f.write(yaml_content)
    print("Provisioned alert_rules.yaml file successfully!")

if __name__ == "__main__":
    setup_alerts()
