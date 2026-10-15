Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "      KIEM TRA HE THONG QUAN LY DU AN (PROJECT MANAGEMENT)" -ForegroundColor Cyan
Write-Host "      Sinh vien: Trinh Ngoc Tuong | MSSV: DTC245200211 | STT: 54" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan

function Check-ServiceEndpoint {
    param(
        [string]$Name,
        [string]$Url,
        [int]$ExpectedStatus
    )

    Write-Host -NoNewline "Kiem tra $Name ($Url)... "
    try {
        $request = [System.Net.HttpWebRequest]::Create($Url)
        $request.ServerCertificateValidationCallback = { $true }
        $request.Timeout = 4000
        $request.AllowAutoRedirect = $false
        
        $response = $request.GetResponse()
        $statusCode = [int]$response.StatusCode
        $response.Close()

        if ($statusCode -eq $ExpectedStatus -or $ExpectedStatus -eq 0) {
            Write-Host "[OK] (HTTP $statusCode)" -ForegroundColor Green
        }
        else {
            Write-Host "[LOI] Nhan HTTP $statusCode, ky vong $ExpectedStatus" -ForegroundColor Red
        }
    }
    catch [System.Net.WebException] {
        if ($_.Response) {
            $statusCode = [int]$_.Response.StatusCode
            if ($statusCode -eq $ExpectedStatus) {
                Write-Host "[OK] (HTTP $statusCode)" -ForegroundColor Green
            }
            else {
                Write-Host "[LOI] Nhan HTTP $statusCode, ky vong $ExpectedStatus" -ForegroundColor Yellow
            }
        }
        else {
            Write-Host "[CHUA CHAY] Dich vu chua san sang tren cong nay" -ForegroundColor DarkGray
        }
    }
    catch {
        Write-Host "[CHUA CHAY] Dich vu chua san sang" -ForegroundColor DarkGray
    }
}

Write-Host "`n1. DINH TUYEN & NGINX REVERSE PROXY" -ForegroundColor Yellow
Check-ServiceEndpoint "Nginx Port 80 (Redirect 301)" "http://localhost:80" 301
Check-ServiceEndpoint "Nginx Port 443 (HTTPS WebApp)" "https://localhost:443" 200

Write-Host "`n2. CO SO DU LIEU & GIAM SAT HE THONG" -ForegroundColor Yellow
Check-ServiceEndpoint "Adminer (Quan ly CSDL)" "http://localhost:8080" 200
Check-ServiceEndpoint "Prometheus Metrics Server" "http://localhost:9090/-/healthy" 200
Check-ServiceEndpoint "Grafana Dashboard" "http://localhost:3001/api/health" 200
Check-ServiceEndpoint "Loki Log Engine" "http://localhost:3100/ready" 200

Write-Host "`n3. PROMETHEUS METRICS ENDPOINT" -ForegroundColor Yellow
Check-ServiceEndpoint "Webapp /metrics" "http://localhost:3000/metrics" 200

Write-Host "`n4. MO PHONG LOI HTTP 500 CHO CAU TRUY VAN LOGQL" -ForegroundColor Yellow
Check-ServiceEndpoint "Test 500 Nginx LogQL" "http://localhost:3000/api/test/error" 500
Check-ServiceEndpoint "Test Webapp Exception LogQL" "http://localhost:3000/api/test/exception" 500

Write-Host "`n==================================================================" -ForegroundColor Cyan
Write-Host "HOAN TAT KIEM THU! Ban co the xem Dashboard tai: http://localhost:3001" -ForegroundColor Green
Write-Host "==================================================================" -ForegroundColor Cyan
