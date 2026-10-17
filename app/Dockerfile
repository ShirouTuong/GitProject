# ========================================================
# Dockerfile: Project Management System (Node.js Express)
# Multi-stage build + Hardening with Non-root User
# Sinh vien: Trinh Ngoc Tuong - DTC245200211 - De tai 14
# ========================================================

# ----------------- Stage 1: Dependencies Builder -----------------
FROM node:20-alpine AS builder

WORKDIR /usr/src/app

COPY package*.json ./
RUN npm ci --only=production

# ----------------- Stage 2: Hardened Production Runtime -----------------
FROM node:20-alpine AS runner

# Hardening: Tao non-root user va group voi UID/GID co dinh (1001)
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

WORKDIR /usr/src/app

# Sao chep node_modules tu builder stage
COPY --from=builder --chown=appuser:appgroup /usr/src/app/node_modules ./node_modules
COPY --chown=appuser:appgroup package*.json ./
COPY --chown=appuser:appgroup src ./src

# Thiet lap moi truong san pham
ENV NODE_ENV=production \
    PORT=3000

# Chuyen sang non-root user (Hardening yeu cau de bai)
USER appuser

EXPOSE 3000

# Kiem tra trang thai song con cua container
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:3000/api/health || exit 1


CMD ["node", "src/server.js"]
