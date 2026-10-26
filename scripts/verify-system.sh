
echo "=================================================================="
echo "      KIỂM TRA TRẠNG THÁI HỆ THỐNG QUẢN LÝ DỰ ÁN (PROJECT MANAGEMENT)"
echo "      Sinh viên: Trịnh Ngọc Tường | MSSV: DTC245200211 | Lớp: CNTTK23E | STT: 54"
echo "=================================================================="

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

check_endpoint() {
    local name="$1"
    local url="$2"
    local expected="$3"

    echo -n "Kiểm tra $name ($url)... "
    response=$(curl -k -s -o /dev/null -w "%{http_code}" "$url" || echo "FAILED")

    if [[ "$response" == "$expected" ]] || [[ "$expected" == "*" && "$response" != "FAILED" ]]; then
        echo -e "${GREEN}[OK] (HTTP $response)${NC}"
    else
        echo -e "${RED}[LỖI] (Nhận HTTP $response, kỳ vọng $expected)${NC}"
    fi
}

echo ""
echo "1. KIỂM TRA ĐỊNH TUYẾN & NGINX REVERSE PROXY"
check_endpoint "Nginx HTTP -> HTTPS Redirect" "http://localhost:80" "301"
check_endpoint "Nginx HTTPS WebApp" "https://localhost:443" "200"

echo ""
echo "2. KIỂM TRA BẢO MẬT NGINX SECURITY HEADERS"
headers=$(curl -k -s -I "https://localhost:443")
for header in "X-Frame-Options: SAMEORIGIN" "X-Content-Type-Options: nosniff" "X-XSS-Protection: 1; mode=block"; do
    if echo "$headers" | grep -iq "$header"; then
        echo -e "Header $header: ${GREEN}[HỢP LỆ]${NC}"
    else
        echo -e "Header $header: ${YELLOW}[THIẾU HOẶC KHÁC]${NC}"
    fi
done

echo ""
echo "3. KIỂM TRA CÔNG CỤ QUẢN TRỊ CSDL & GIÁM SÁT"
check_endpoint "Adminer (Quản trị DB)" "http://localhost:8080" "200"
check_endpoint "Prometheus Server" "http://localhost:9090/-/healthy" "200"
check_endpoint "Grafana Dashboard" "http://localhost:3001/api/health" "200"
check_endpoint "Loki Log Engine" "http://localhost:3100/ready" "200"

echo ""
echo "4. KIỂM TRA PROMETHEUS METRICS CỦA WEB APP"
check_endpoint "Webapp Prometheus Metrics" "http://localhost:3000/metrics" "200"

echo ""
echo "5. TẠO REQUEST LỖI THỬ NGHIỆM ĐỂ XÁC MINH LOGQL & PROMETHEUS 5XX"
echo "Gửi request gây lỗi HTTP 500..."
curl -k -s "https://localhost/api/test/error" > /dev/null || true
curl -k -s "http://localhost:3000/api/test/exception" > /dev/null || true
echo -e "${GREEN}[HOÀN TẤT] Đã tạo log lỗi. Kiểm tra câu truy vấn LogQL trên Grafana Explore:${NC}"
echo "  - Truy vấn 1: {job=\"nginx\"} |= \"HTTP/1.1\" 5\""
echo "  - Truy vấn 2: {job=\"webapp\"} |~ \"(ERROR|Exception|Failed)\""
echo "=================================================================="
