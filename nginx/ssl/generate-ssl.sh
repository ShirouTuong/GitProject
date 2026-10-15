#!/bin/bash
# ==============================================================================
# Script sinh chung chi SSL Tu ky (Self-signed Certificate) cho Nginx
# Sinh vien: Trinh Ngoc Tuong - DTC245200211 - De tai 14
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SSL_KEY="$SCRIPT_DIR/server.key"
SSL_CRT="$SCRIPT_DIR/server.crt"

echo "[INFO] Dang tao chung chi SSL tu ky cho localhost (Nginx HTTPS)..."
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout "$SSL_KEY" \
  -out "$SSL_CRT" \
  -subj "/C=VN/ST=ThaiNguyen/L=ThaiNguyen/O=ICTU/OU=DevOps/CN=localhost"

echo "[SUCCESS] Da tao chung chi thanh cong:"
echo "  - Private Key: $SSL_KEY"
echo "  - Certificate: $SSL_CRT"
