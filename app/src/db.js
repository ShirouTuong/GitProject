const { Pool } = require('pg');

let pool = null;
let isConnected = false;
let useMemoryFallback = true;

let inMemoryData = {
  projects: [
    {
      id: 1,
      name: "Xây dựng Cổng thông tin Sinh viên ICTU",
      description: "Nâng cấp giao diện và tích hợp SSO cho hệ thống sinh viên Đại học CNTT & TT.",
      status: "In Progress",
      priority: "High",
      progress: 65,
      start_date: "2026-09-01",
      deadline: "2026-11-15",
      created_by: "Trịnh Ngọc Tường"
    },
    {
      id: 2,
      name: "Hệ thống Quản lý Dự án Microservices",
      description: "Bài kiểm tra cuối kỳ môn Triển khai và Quản trị Hệ thống Phần mềm.",
      status: "In Progress",
      priority: "Critical",
      progress: 90,
      start_date: "2026-10-01",
      deadline: "2026-10-25",
      created_by: "Trịnh Ngọc Tường"
    },
    {
      id: 3,
      name: "Tối ưu hóa Giám sát Hệ thống với Grafana & Loki",
      description: "Thu thập metrics hạ tầng và tập trung hóa logs container trên môi trường Docker.",
      status: "Completed",
      priority: "Medium",
      progress: 100,
      start_date: "2026-09-15",
      deadline: "2026-10-10",
      created_by: "Admin"
    }
  ],
  tasks: [
    {
      id: 1,
      project_id: 2,
      title: "Thiết kế Dockerfile và docker-compose.yml",
      description: "Đóng gói ứng dụng web, cấu hình non-root user và phân tách mạng nội bộ.",
      status: "Done",
      priority: "High",
      assignee: "Trịnh Ngọc Tường",
      due_date: "2026-10-16"
    },
    {
      id: 2,
      project_id: 2,
      title: "Cấu hình Nginx Reverse Proxy & SSL",
      description: "Thiết lập reverse proxy chuyển tiếp port 80/443, SSL tự ký và Security Headers.",
      status: "Done",
      priority: "High",
      assignee: "Trịnh Ngọc Tường",
      due_date: "2026-10-18"
    },
    {
      id: 3,
      project_id: 2,
      title: "Tích hợp Prometheus và Grafana Dashboard",
      description: "Scrape metrics từ cAdvisor và web application endpoint /metrics.",
      status: "In Progress",
      priority: "High",
      assignee: "Trịnh Ngọc Tường",
      due_date: "2026-10-20"
    },
    {
      id: 4,
      project_id: 2,
      title: "Cấu hình Loki + Promtail và xác thực LogQL",
      description: "Thu thập Docker container logs và viết 2 câu truy vấn LogQL kiểm chứng.",
      status: "In Progress",
      priority: "Medium",
      assignee: "Trịnh Ngọc Tường",
      due_date: "2026-10-22"
    },
    {
      id: 5,
      project_id: 2,
      title: "Thực hiện Hardening & Hoàn thiện Báo cáo Word",
      description: "Áp dụng security best practices và cập nhật file báo cáo cuối kỳ.",
      status: "To Do",
      priority: "High",
      assignee: "Trịnh Ngọc Tường",
      due_date: "2026-10-24"
    }
  ],
  members: [
    { id: 1, name: "Trịnh Ngọc Tường", email: "tuong.dtc245200211@ictu.edu.vn", role: "Project Manager / DevOps", avatar: "TT" },
    { id: 2, name: "Nguyễn Văn An", email: "an.ictu@edu.vn", role: "Frontend Developer", avatar: "NA" },
    { id: 3, name: "Trần Thị Mai", email: "mai.ictu@edu.vn", role: "Backend Developer", avatar: "TM" },
    { id: 4, name: "Lê Quốc Bảo", email: "bao.ictu@edu.vn", role: "QA / Security Engineer", avatar: "LB" }
  ]
};

async function initDB(logger) {
  const dbHost = process.env.DB_HOST || 'db';
  const dbPort = parseInt(process.env.DB_PORT || '5432', 10);
  const dbName = process.env.DB_NAME || 'project_db';
  const dbUser = process.env.DB_USER || 'admin_user';
  const dbPassword = process.env.DB_PASSWORD || 'SecurePass@2026';

  pool = new Pool({
    host: dbHost,
    port: dbPort,
    database: dbName,
    user: dbUser,
    password: dbPassword,
    connectionTimeoutMillis: 4000
  });

  try {
    const client = await pool.connect();
    logger.info(`[Database] Kết nối thành công đến PostgreSQL tại ${dbHost}:${dbPort}/${dbName}`);

    await client.query(`
      CREATE TABLE IF NOT EXISTS projects (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        description TEXT,
        status VARCHAR(50) DEFAULT 'Planning',
        priority VARCHAR(50) DEFAULT 'Medium',
        progress INT DEFAULT 0,
        start_date DATE,
        deadline DATE,
        created_by VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );

      CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        project_id INT REFERENCES projects(id) ON DELETE CASCADE,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        status VARCHAR(50) DEFAULT 'To Do',
        priority VARCHAR(50) DEFAULT 'Medium',
        assignee VARCHAR(100),
        due_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );

      CREATE TABLE IF NOT EXISTS team_members (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(150) UNIQUE NOT NULL,
        role VARCHAR(100),
        avatar VARCHAR(10)
      );
    `);

    const resCount = await client.query('SELECT COUNT(*) FROM projects');
    if (parseInt(resCount.rows[0].count, 10) === 0) {
      logger.info('[Database] Khởi tạo dữ liệu mẫu cho hệ thống Quản lý Dự án...');
      for (const p of inMemoryData.projects) {
        await client.query(
          `INSERT INTO projects (id, name, description, status, priority, progress, start_date, deadline, created_by)
           VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)`,
          [p.id, p.name, p.description, p.status, p.priority, p.progress, p.start_date, p.deadline, p.created_by]
        );
      }
      for (const t of inMemoryData.tasks) {
        await client.query(
          `INSERT INTO tasks (id, project_id, title, description, status, priority, assignee, due_date)
           VALUES ($1, $2, $3, $4, $5, $6, $7, $8)`,
          [t.id, t.project_id, t.title, t.description, t.status, t.priority, t.assignee, t.due_date]
        );
      }
      for (const m of inMemoryData.members) {
        await client.query(
          `INSERT INTO team_members (id, name, email, role, avatar)
           VALUES ($1, $2, $3, $4, $5)`,
          [m.id, m.name, m.email, m.role, m.avatar]
        );
      }
      await client.query(`SELECT setval('projects_id_seq', (SELECT MAX(id) FROM projects));`);
      await client.query(`SELECT setval('tasks_id_seq', (SELECT MAX(id) FROM tasks));`);
      await client.query(`SELECT setval('team_members_id_seq', (SELECT MAX(id) FROM team_members));`);
    }

    client.release();
    isConnected = true;
    useMemoryFallback = false;
  } catch (err) {
    logger.warn(`[Database] Không thể kết nối PostgreSQL (${err.message}). Kích hoạt chế độ In-Memory Fallback.`);
    isConnected = false;
    useMemoryFallback = true;
  }
}

async function query(text, params) {
  if (!isConnected || !pool) {
    return null;
  }
  return pool.query(text, params);
}

module.exports = {
  initDB,
  query,
  inMemoryData,
  isMemoryFallback: () => !isConnected
};

