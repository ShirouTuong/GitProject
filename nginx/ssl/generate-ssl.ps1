# ==============================================================================
# Script sinh chung chi SSL Tu ky (Self-signed Certificate) cho Nginx tren Windows
# Sinh vien: Trinh Ngoc Tuong - DTC245200211 - De tai 14
# ==============================================================================
$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$sslKey = Join-Path $scriptDir "server.key"
$sslCrt = Join-Path $scriptDir "server.crt"

Write-Host "[INFO] Dang tao chung chi SSL tu ky cho Nginx..." -ForegroundColor Cyan

$opensslPaths = @(
    "openssl",
    "C:\Program Files\Git\usr\bin\openssl.exe",
    "C:\Program Files (x86)\Git\usr\bin\openssl.exe"
)

$opensslCmd = $null
foreach ($path in $opensslPaths) {
    if (Get-Command $path -ErrorAction SilentlyContinue) {
        $opensslCmd = $path
        break
    }
}

if ($opensslCmd) {
    & $opensslCmd req -x509 -nodes -days 365 -newkey rsa:2048 `
      -keyout $sslKey `
      -out $sslCrt `
      -subj "/C=VN/ST=ThaiNguyen/L=ThaiNguyen/O=ICTU/OU=DevOps/CN=localhost"
    Write-Host "[SUCCESS] Da tao chung chi SSL thanh cong bang OpenSSL!" -ForegroundColor Green
} else {
    Write-Host "[WARNING] Khong tim thay OpenSSL. Su dung chung chi co san." -ForegroundColor Yellow
}
