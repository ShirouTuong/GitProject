# ==============================================================================
# SCRIPT KIEM THU TU DONG TOAN DIEN HE THONG TREN WINDOWS POWERSHELL
# Mon: Trien khai va Quan tri He thong Phan mem
# Sinh vien: Trinh Ngoc Tuong - DTC245200211 - De tai 14
# ==============================================================================

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "      KIEM TRA HE THONG QUAN LY DU AN (PROJECT MANAGEMENT)" -ForegroundColor Cyan
Write-Host "      Sinh vien: Trinh Ngoc Tuong | MSSV: DTC245200211 | Lop: CNTTK23E | STT: 54" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan

function Check-ServiceEndpoint {
    param(
        [string]$Name,
        [string]$Url,
        [int]$ExpectedStatus
    )

    Write-Host -NoNewline "Kiem tra $Name ($Url)... "
    try {
        $httpCode = (& curl.exe -k -s -o NUL -w "%{http_code}" "$Url" 2>$null)
        if ($httpCode) {
            $statusCode = [int]$httpCode.Trim()
            if ($statusCode -eq $ExpectedStatus -or $ExpectedStatus -eq 0) {
                Write-Host "[OK] (HTTP $statusCode)" -ForegroundColor Green
            } else {
                Write-Host "[LOI] Nhan HTTP $statusCode, ky vong $ExpectedStatus" -ForegroundColor Yellow
            }
        } else {
            Write-Host "[CHUA CHAY] Khong the ket noi" -ForegroundColor DarkGray
        }
    }
    catch {
        Write-Host "[CHUA CHAY] Loi khi thuc hien kiem tra" -ForegroundColor DarkGray
    }
}

$httpPort = if ($env:HTTP_PORT) { $env:HTTP_PORT } else { 8081 }

Write-Host "`n1. DINH TUYEN & NGINX REVERSE PROXY" -ForegroundColor Yellow
Check-ServiceEndpoint "Nginx HTTP (Redirect 301)" "http://localhost:${httpPort}" 301
Check-ServiceEndpoint "Nginx HTTPS (Web Application)" "https://localhost:443" 200

Write-Host "`n2. CO SO DU LIEU & GIAM SAT HE THONG" -ForegroundColor Yellow
Check-ServiceEndpoint "Adminer (Quan ly CSDL)" "http://localhost:8080" 200
Check-ServiceEndpoint "pgAdmin 4 (Quan ly CSDL De 14)" "http://localhost:5050" 302
Check-ServiceEndpoint "Prometheus Metrics Server" "http://localhost:9090/-/healthy" 200
Check-ServiceEndpoint "Grafana Dashboard" "http://localhost:3001/api/health" 200
Check-ServiceEndpoint "Loki Log Engine" "http://localhost:3100/ready" 200

Write-Host "`n3. PROMETHEUS METRICS ENDPOINT (QUA NGINX)" -ForegroundColor Yellow
Check-ServiceEndpoint "Webapp /metrics qua Nginx" "https://localhost/metrics" 200

Write-Host "`n4. MO PHONG LOI HTTP 500 CHO CAU TRUY VAN LOGQL" -ForegroundColor Yellow
Check-ServiceEndpoint "Test 500 Nginx LogQL" "https://localhost/api/test/error" 500
Check-ServiceEndpoint "Test Webapp Exception LogQL" "https://localhost/api/test/exception" 500

Write-Host "`n==================================================================" -ForegroundColor Cyan
Write-Host "HOAN TAT KIEM THU! Ban co the xem Dashboard tai: http://localhost:3001" -ForegroundColor Green
Write-Host "==================================================================" -ForegroundColor Cyan
