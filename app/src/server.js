const express = require('express');
const cors = require('cors');
const path = require('path');
const winston = require('winston');
const client = require('prom-client');
require('dotenv').config();

const { initDB, query, inMemoryData, isMemoryFallback } = require('./db');

const app = express();
const PORT = process.env.PORT || 3000;

// ==========================================
// 1. CẤU HÌNH WINSTON LOGGER (CHO LOKI & PROMTAIL)
// ==========================================
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss.SSS' }),
    winston.format.printf(({ timestamp, level, message, ...meta }) => {
      const metaStr = Object.keys(meta).length ? ` ${JSON.stringify(meta)}` : '';
      return `[${timestamp}] [${level.toUpperCase()}] [webapp]: ${message}${metaStr}`;
    })
  ),
  defaultMeta: { service: 'webapp', app: 'project-management' },
  transports: [
    new winston.transports.Console()
  ]
});

// ==========================================
// 2. CẤU HÌNH PROMETHEUS METRICS
// ==========================================
const register = new client.Registry();
client.collectDefaultMetrics({ register, prefix: 'pm_app_' });

const httpRequestCounter = new client.Counter({
  name: 'pm_http_requests_total',
  help: 'Tổng số lượt HTTP request đến ứng dụng Quản lý Dự án',
  labelNames: ['method', 'route', 'status_code'],
  registers: [register]
});

const httpRequestDuration = new client.Histogram({
  name: 'pm_http_request_duration_seconds',
  help: 'Thời gian phản hồi của HTTP request (seconds)',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.01, 0.05, 0.1, 0.3, 0.5, 1, 2, 5],
  registers: [register]
});

const activeProjectsGauge = new client.Gauge({
  name: 'pm_active_projects_total',
  help: 'Số lượng dự án đang hoạt động trong hệ thống',
  registers: [register]
});

const tasksGauge = new client.Gauge({
  name: 'pm_tasks_total',
  help: 'Số lượng công việc theo trạng thái',
  labelNames: ['status'],
  registers: [register]
});

// Middleware đo metrics & logging cho từng request
app.use((req, res, next) => {
  const start = process.hrtime();
  res.on('finish', () => {
    const diff = process.hrtime(start);
    const durationInSeconds = diff[0] + diff[1] / 1e9;
    const route = req.route ? req.route.path : req.path;
    const status = res.statusCode;

    httpRequestCounter.labels(req.method, route, status.toString()).inc();
    httpRequestDuration.labels(req.method, route, status.toString()).observe(durationInSeconds);

    if (status >= 500) {
      logger.error(`HTTP ${req.method} ${req.url} - Trả về lỗi server ${status} - Client IP: ${req.ip}`);
    } else if (status >= 400) {
      logger.warn(`HTTP ${req.method} ${req.url} - Mã trạng thái ${status}`);
    } else {
      logger.info(`HTTP ${req.method} ${req.url} ${status} - ${durationInSeconds.toFixed(4)}s`);
    }
  });
  next();
});

// Middleware cơ bản
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// ==========================================
// 3. ENDPOINTS METRICS & GIÁM SÁT PROMETHEUS
// ==========================================
app.get('/metrics', async (req, res) => {
  try {
    // Cập nhật gauges trước khi trả về
    if (isMemoryFallback()) {
      activeProjectsGauge.set(inMemoryData.projects.length);
      const todo = inMemoryData.tasks.filter(t => t.status === 'To Do').length;
      const inProg = inMemoryData.tasks.filter(t => t.status === 'In Progress').length;
      const done = inMemoryData.tasks.filter(t => t.status === 'Done').length;
      tasksGauge.labels('To Do').set(todo);
      tasksGauge.labels('In Progress').set(inProg);
      tasksGauge.labels('Done').set(done);
    } else {
      const pRes = await query('SELECT COUNT(*) FROM projects');
      if (pRes) activeProjectsGauge.set(parseInt(pRes.rows[0].count, 10));

      const tRes = await query('SELECT status, COUNT(*) FROM tasks GROUP BY status');
      if (tRes) {
        tRes.rows.forEach(r => tasksGauge.labels(r.status).set(parseInt(r.count, 10)));
      }
    }

    res.set('Content-Type', register.contentType);
    res.end(await register.metrics());
  } catch (ex) {
    logger.error(`Exception xảy ra khi xuất Prometheus metrics: ${ex.message}`);
    res.status(500).end(ex.message);
  }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({
    status: 'UP',
    database: isMemoryFallback() ? 'In-Memory Fallback' : 'PostgreSQL Connected',
    uptime: process.uptime(),
    timestamp: new Date().toISOString(),
    student: {
      name: 'Trịnh Ngọc Tường',
      mssv: 'DTC245200211',
      class: 'CNTTK23E',
      topic: 'Hệ thống Quản lý Dự án (Project Management) - Đề tài 14'
    }
  });
});

// ==========================================
// 4. ENDPOINTS KIỂM THỬ LỖI CHO LOKI LOGQL
// ==========================================
// Test 1: Tạo log Exception / ERROR cho câu truy vấn: {job="webapp"} |~ "(ERROR|Exception|Failed)"
app.get('/api/test/error', (req, res) => {
  logger.error('[TEST LOGQL] ERROR: Database connection pool exhausted! Failed to acquire transaction lock. Exception: QueryTimeoutException at ProjectService.execute()');
  res.status(500).json({
    status: 'error',
    message: 'Simulated 500 Internal Server Error for LogQL test: {job="webapp"} |~ "(ERROR|Exception|Failed)"',
    logged_at: new Date().toISOString()
  });
});

app.get('/api/test/exception', (req, res) => {
  try {
    throw new Error('NullPointerException: Project payload validation Failed during pipeline execution.');
  } catch (err) {
    logger.error(`Exception in Project controller: ${err.message}. Failed stack: ${err.stack}`);
    res.status(500).json({ error: 'Exception triggered successfully for LogQL testing' });
  }
});

// ==========================================
// 5. RESTFUL APIS - QUẢN LÝ DỰ ÁN (PROJECTS)
// ==========================================
app.get('/api/projects', async (req, res) => {
  try {
    if (isMemoryFallback()) {
      return res.json(inMemoryData.projects);
    }
    const result = await query('SELECT * FROM projects ORDER BY id DESC');
    res.json(result.rows);
  } catch (err) {
    logger.error(`Failed to fetch projects: ${err.message}`);
    res.status(500).json({ error: 'Lỗi tải danh sách dự án' });
  }
});

app.post('/api/projects', async (req, res) => {
  const { name, description, status, priority, progress, start_date, deadline, created_by } = req.body;
  if (!name) {
    return res.status(400).json({ error: 'Tên dự án là bắt buộc' });
  }

  try {
    if (isMemoryFallback()) {
      const newP = {
        id: inMemoryData.projects.length ? Math.max(...inMemoryData.projects.map(p => p.id)) + 1 : 1,
        name,
        description: description || '',
        status: status || 'Planning',
        priority: priority || 'Medium',
        progress: parseInt(progress || '0', 10),
        start_date: start_date || new Date().toISOString().split('T')[0],
        deadline: deadline || '',
        created_by: created_by || 'Trịnh Ngọc Tường'
      };
      inMemoryData.projects.unshift(newP);
      logger.info(`Tạo mới dự án thành công: [ID ${newP.id}] ${newP.name}`);
      return res.status(201).json(newP);
    }

    const result = await query(
      `INSERT INTO projects (name, description, status, priority, progress, start_date, deadline, created_by)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8) RETURNING *`,
      [name, description, status || 'Planning', priority || 'Medium', progress || 0, start_date, deadline, created_by || 'Trịnh Ngọc Tường']
    );
    logger.info(`Tạo mới dự án trong PostgreSQL: [ID ${result.rows[0].id}] ${result.rows[0].name}`);
    res.status(201).json(result.rows[0]);
  } catch (err) {
    logger.error(`Exception when creating project: ${err.message}`);
    res.status(500).json({ error: 'Không thể tạo dự án' });
  }
});

app.delete('/api/projects/:id', async (req, res) => {
  const id = parseInt(req.params.id, 10);
  try {
    if (isMemoryFallback()) {
      inMemoryData.projects = inMemoryData.projects.filter(p => p.id !== id);
      inMemoryData.tasks = inMemoryData.tasks.filter(t => t.project_id !== id);
      logger.info(`Đã xóa dự án ID ${id}`);
      return res.json({ success: true, message: `Đã xóa dự án ID ${id}` });
    }
    await query('DELETE FROM projects WHERE id = $1', [id]);
    logger.info(`Đã xóa dự án ID ${id} từ cơ sở dữ liệu`);
    res.json({ success: true });
  } catch (err) {
    logger.error(`Lỗi khi xóa dự án: ${err.message}`);
    res.status(500).json({ error: 'Xóa dự án thất bại' });
  }
});

// ==========================================
// 6. RESTFUL APIS - QUẢN LÝ CÔNG VIỆC (TASKS/KANBAN)
// ==========================================
app.get('/api/tasks', async (req, res) => {
  const { project_id } = req.query;
  try {
    if (isMemoryFallback()) {
      if (project_id) {
        return res.json(inMemoryData.tasks.filter(t => t.project_id === parseInt(project_id, 10)));
      }
      return res.json(inMemoryData.tasks);
    }
    let queryText = 'SELECT * FROM tasks';
    const params = [];
    if (project_id) {
      queryText += ' WHERE project_id = $1';
      params.push(project_id);
    }
    queryText += ' ORDER BY id ASC';
    const result = await query(queryText, params);
    res.json(result.rows);
  } catch (err) {
    logger.error(`Failed to fetch tasks: ${err.message}`);
    res.status(500).json({ error: 'Lỗi tải công việc' });
  }
});

app.post('/api/tasks', async (req, res) => {
  const { project_id, title, description, status, priority, assignee, due_date } = req.body;
  if (!title) {
    return res.status(400).json({ error: 'Tiêu đề công việc là bắt buộc' });
  }

  try {
    if (isMemoryFallback()) {
      const newT = {
        id: inMemoryData.tasks.length ? Math.max(...inMemoryData.tasks.map(t => t.id)) + 1 : 1,
        project_id: parseInt(project_id || '1', 10),
        title,
        description: description || '',
        status: status || 'To Do',
        priority: priority || 'Medium',
        assignee: assignee || 'Trịnh Ngọc Tường',
        due_date: due_date || ''
      };
      inMemoryData.tasks.push(newT);
      logger.info(`Thêm task mới: [ID ${newT.id}] "${newT.title}" trạng thái "${newT.status}"`);
      return res.status(201).json(newT);
    }

    const result = await query(
      `INSERT INTO tasks (project_id, title, description, status, priority, assignee, due_date)
       VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING *`,
      [project_id || 1, title, description, status || 'To Do', priority || 'Medium', assignee || 'Trịnh Ngọc Tường', due_date]
    );
    logger.info(`Đã lưu task vào DB: [ID ${result.rows[0].id}] "${result.rows[0].title}"`);
    res.status(201).json(result.rows[0]);
  } catch (err) {
    logger.error(`Exception when creating task: ${err.message}`);
    res.status(500).json({ error: 'Không thể tạo công việc' });
  }
});

app.patch('/api/tasks/:id/status', async (req, res) => {
  const id = parseInt(req.params.id, 10);
  const { status } = req.body;
  if (!status) return res.status(400).json({ error: 'Thiếu status' });

  try {
    if (isMemoryFallback()) {
      const task = inMemoryData.tasks.find(t => t.id === id);
      if (!task) return res.status(404).json({ error: 'Không tìm thấy task' });
      task.status = status;
      logger.info(`Cập nhật trạng thái task ID ${id} -> ${status}`);
      return res.json(task);
    }

    const result = await query(
      'UPDATE tasks SET status = $1 WHERE id = $2 RETURNING *',
      [status, id]
    );
    if (!result.rows.length) return res.status(404).json({ error: 'Không tìm thấy task' });
    logger.info(`Cập nhật trạng thái task ID ${id} -> ${status} trong CSDL`);
    res.json(result.rows[0]);
  } catch (err) {
    logger.error(`Lỗi khi cập nhật trạng thái task: ${err.message}`);
    res.status(500).json({ error: 'Cập nhật thất bại' });
  }
});

app.delete('/api/tasks/:id', async (req, res) => {
  const id = parseInt(req.params.id, 10);
  try {
    if (isMemoryFallback()) {
      inMemoryData.tasks = inMemoryData.tasks.filter(t => t.id !== id);
      logger.info(`Xóa task ID ${id}`);
      return res.json({ success: true });
    }
    await query('DELETE FROM tasks WHERE id = $1', [id]);
    res.json({ success: true });
  } catch (err) {
    logger.error(`Exception when deleting task: ${err.message}`);
    res.status(500).json({ error: 'Không thể xóa task' });
  }
});

// ==========================================
// 7. RESTFUL APIS - THÀNH VIÊN (MEMBERS)
// ==========================================
app.get('/api/members', async (req, res) => {
  try {
    if (isMemoryFallback()) return res.json(inMemoryData.members);
    const result = await query('SELECT * FROM team_members ORDER BY id ASC');
    res.json(result.rows);
  } catch (err) {
    logger.error(`Lỗi lấy danh sách thành viên: ${err.message}`);
    res.status(500).json({ error: 'Lỗi tải thành viên' });
  }
});

// Khởi chạy server và kết nối DB
const server = app.listen(PORT, '0.0.0.0', () => {
  logger.info(`================================================================`);
  logger.info(`[HỆ THỐNG QUẢN LÝ DỰ ÁN] Khởi chạy thành công trên cổng ${PORT}`);
  logger.info(`Sinh viên: Trịnh Ngọc Tường | MSSV: DTC245200211 | Lớp: CNTTK23E - ICTU 2026`);
  logger.info(`Metrics Prometheus: http://localhost:${PORT}/metrics`);
  logger.info(`Health check: http://localhost:${PORT}/api/health`);
  logger.info(`================================================================`);
});

initDB(logger);

module.exports = { app, server };

