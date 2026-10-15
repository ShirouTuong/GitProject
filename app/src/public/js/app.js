// Global State
let projects = [];
let tasks = [];
let members = [];
let activeTab = 'kanban';

// DOM Elements
const systemStatusChip = document.getElementById('systemStatusChip');
const systemStatusText = document.getElementById('systemStatusText');
const cardsTodo = document.getElementById('cards-todo');
const cardsInProgress = document.getElementById('cards-inprogress');
const cardsDone = document.getElementById('cards-done');
const countTodo = document.getElementById('count-todo');
const countInProgress = document.getElementById('count-inprogress');
const countDone = document.getElementById('count-done');
const projectsTableBody = document.getElementById('projectsTableBody');
const membersGrid = document.getElementById('membersGrid');
const taskProjectSelect = document.getElementById('taskProject');
const toastNotification = document.getElementById('toastNotification');

// Initialize Application
document.addEventListener('DOMContentLoaded', async () => {
  setupNavigation();
  setupModals();
  setupTestButtons();
  await checkSystemHealth();
  await loadData();
});

// 1. Navigation & Tabs
function setupNavigation() {
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(item => {
    item.addEventListener('click', (e) => {
      e.preventDefault();
      const targetTab = item.getAttribute('data-tab');
      switchTab(targetTab);
    });
  });
}

function switchTab(tabId) {
  activeTab = tabId;
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));

  const activeNav = document.querySelector(`[data-tab="${tabId}"]`);
  if (activeNav) activeNav.classList.add('active');

  const pane = document.getElementById(`tab-${tabId}`);
  if (pane) pane.classList.add('active');

  const titles = {
    kanban: 'Bảng Công Việc Kanban',
    projects: 'Quản Lý Danh Sách Dự Án',
    monitoring: 'Giám Sát & Quản Trị Hệ Thống (DevOps)',
    team: 'Đội Ngũ Dự Án'
  };
  document.getElementById('pageTitle').textContent = titles[tabId] || 'Hệ Thống Quản Lý Dự Án';
}

// 2. Load Data from Backend APIs
async function loadData() {
  try {
    const [pRes, tRes, mRes] = await Promise.all([
      fetch('/api/projects').then(r => r.json()),
      fetch('/api/tasks').then(r => r.json()),
      fetch('/api/members').then(r => r.json())
    ]);

    projects = pRes || [];
    tasks = tRes || [];
    members = mRes || [];

    updateStats();
    renderKanban();
    renderProjects();
    renderMembers();
    populateProjectSelect();
  } catch (err) {
    console.error('Lỗi khi tải dữ liệu từ máy chủ:', err);
    showToast('Lỗi nạp dữ liệu từ máy chủ API', 'error');
  }
}

// 3. Health Check
async function checkSystemHealth() {
  try {
    const res = await fetch('/api/health');
    if (res.ok) {
      const data = await res.json();
      systemStatusChip.className = 'system-status-chip';
      systemStatusText.textContent = `${data.database} (Active)`;
    } else {
      systemStatusText.textContent = 'Trạng thái bất thường';
    }
  } catch (err) {
    systemStatusText.textContent = 'Mất kết nối backend';
  }
}

// 4. Update Overview Stats
function updateStats() {
  document.getElementById('statProjects').textContent = projects.length;
  document.getElementById('statTasks').textContent = tasks.length;
  
  const completed = tasks.filter(t => t.status === 'Done').length;
  document.getElementById('statCompleted').textContent = completed;

  const rate = tasks.length > 0 ? Math.round((completed / tasks.length) * 100) : 0;
  document.getElementById('statProgress').textContent = `${rate}%`;
}

// 5. Render Kanban Cards
function renderKanban() {
  cardsTodo.innerHTML = '';
  cardsInProgress.innerHTML = '';
  cardsDone.innerHTML = '';

  const todoTasks = tasks.filter(t => t.status === 'To Do');
  const inProgressTasks = tasks.filter(t => t.status === 'In Progress');
  const doneTasks = tasks.filter(t => t.status === 'Done');

  countTodo.textContent = todoTasks.length;
  countInProgress.textContent = inProgressTasks.length;
  countDone.textContent = doneTasks.length;

  todoTasks.forEach(t => cardsTodo.appendChild(createKanbanCard(t)));
  inProgressTasks.forEach(t => cardsInProgress.appendChild(createKanbanCard(t)));
  doneTasks.forEach(t => cardsDone.appendChild(createKanbanCard(t)));
}

function createKanbanCard(task) {
  const card = document.createElement('div');
  card.className = 'kanban-card';
  card.dataset.id = task.id;

  const proj = projects.find(p => p.id === task.project_id);
  const projName = proj ? proj.name : 'Dự án chung';

  // Action button to move status
  let nextStatusBtn = '';
  if (task.status === 'To Do') {
    nextStatusBtn = `<button class="btn-card-action" onclick="updateTaskStatus(${task.id}, 'In Progress')" title="Chuyển sang In Progress">&#9654;</button>`;
  } else if (task.status === 'In Progress') {
    nextStatusBtn = `<button class="btn-card-action" onclick="updateTaskStatus(${task.id}, 'Done')" title="Hoàn thành">&#10003;</button>`;
  } else {
    nextStatusBtn = `<button class="btn-card-action" onclick="updateTaskStatus(${task.id}, 'To Do')" title="Quay lại To Do">&#8634;</button>`;
  }

  card.innerHTML = `
    <span class="card-project-tag">${escapeHtml(projName)}</span>
    <h4 class="card-title">${escapeHtml(task.title)}</h4>
    <p class="card-desc">${escapeHtml(task.description || 'Không có mô tả')}</p>
    <div class="card-footer">
      <span class="card-priority priority-${task.priority}">${task.priority}</span>
      <div style="display:flex; align-items:center; gap:8px;">
        <span>${escapeHtml(task.assignee || 'Trịnh Ngọc Tường')}</span>
        <div class="card-actions">
          ${nextStatusBtn}
          <button class="btn-card-action" onclick="deleteTask(${task.id})" title="Xóa task">&times;</button>
        </div>
      </div>
    </div>
  `;
  return card;
}

// 6. Update Task Status
async function updateTaskStatus(taskId, newStatus) {
  try {
    const res = await fetch(`/api/tasks/${taskId}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus })
    });
    if (res.ok) {
      showToast(`Đã chuyển task sang: ${newStatus}`);
      await loadData();
    } else {
      showToast('Cập nhật trạng thái thất bại', 'error');
    }
  } catch (err) {
    showToast('Lỗi kết nối máy chủ', 'error');
  }
}

// 7. Delete Task
async function deleteTask(taskId) {
  if (!confirm('Bạn có chắc chắn muốn xóa công việc này?')) return;
  try {
    const res = await fetch(`/api/tasks/${taskId}`, { method: 'DELETE' });
    if (res.ok) {
      showToast('Đã xóa công việc');
      await loadData();
    }
  } catch (err) {
    showToast('Lỗi khi xóa công việc', 'error');
  }
}

// 8. Render Projects Table
function renderProjects() {
  projectsTableBody.innerHTML = '';
  if (!projects.length) {
    projectsTableBody.innerHTML = `<tr><td colspan="8" style="text-align:center; color:var(--text-muted);">Chưa có dự án nào</td></tr>`;
    return;
  }

  projects.forEach(p => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>#${p.id}</td>
      <td>
        <strong>${escapeHtml(p.name)}</strong>
        <div style="font-size:0.75rem; color:var(--text-muted);">${escapeHtml(p.description || '')}</div>
      </td>
      <td><span class="card-priority priority-${p.priority}">${p.priority}</span></td>
      <td>
        <div class="progress-bar-container">
          <div class="progress-bar-fill" style="width: ${p.progress}%;"></div>
        </div>
        <span>${p.progress}%</span>
      </td>
      <td><span class="service-tag tag-blue">${p.status}</span></td>
      <td>${p.deadline || 'Chưa đặt'}</td>
      <td>${escapeHtml(p.created_by || 'Trịnh Ngọc Tường')}</td>
      <td>
        <button class="btn btn-sm btn-outline" onclick="deleteProject(${p.id})">Xóa</button>
      </td>
    `;
    projectsTableBody.appendChild(tr);
  });
}

async function deleteProject(id) {
  if (!confirm(`Xóa dự án #${id} cùng tất cả công việc liên quan?`)) return;
  try {
    const res = await fetch(`/api/projects/${id}`, { method: 'DELETE' });
    if (res.ok) {
      showToast(`Đã xóa dự án #${id}`);
      await loadData();
    }
  } catch (err) {
    showToast('Lỗi kết nối khi xóa dự án', 'error');
  }
}

// 9. Render Members
function renderMembers() {
  membersGrid.innerHTML = '';
  members.forEach(m => {
    const card = document.createElement('div');
    card.className = 'member-card';
    card.innerHTML = `
      <div class="member-avatar">${m.avatar || 'SV'}</div>
      <div class="member-info">
        <h4>${escapeHtml(m.name)}</h4>
        <div class="member-role">${escapeHtml(m.role)}</div>
        <div class="member-email">${escapeHtml(m.email)}</div>
      </div>
    `;
    membersGrid.appendChild(card);
  });
}

function populateProjectSelect() {
  taskProjectSelect.innerHTML = '';
  projects.forEach(p => {
    const opt = document.createElement('option');
    opt.value = p.id;
    opt.textContent = p.name;
    taskProjectSelect.appendChild(opt);
  });
}

// 10. Modals & Forms
function setupModals() {
  const modalTask = document.getElementById('modalTask');
  const modalProject = document.getElementById('modalProject');

  document.getElementById('btnOpenNewTask').addEventListener('click', () => {
    modalTask.showModal();
  });

  document.getElementById('btnOpenNewProject').addEventListener('click', () => {
    modalProject.showModal();
  });

  // Form task submit
  document.getElementById('formNewTask').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
      title: document.getElementById('taskTitle').value,
      project_id: parseInt(document.getElementById('taskProject').value, 10),
      status: document.getElementById('taskStatus').value,
      priority: document.getElementById('taskPriority').value,
      assignee: document.getElementById('taskAssignee').value,
      due_date: document.getElementById('taskDueDate').value,
      description: document.getElementById('taskDesc').value
    };

    try {
      const res = await fetch('/api/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        showToast('Tạo công việc thành công!');
        closeModal('modalTask');
        document.getElementById('formNewTask').reset();
        await loadData();
      }
    } catch (err) {
      showToast('Lỗi khi tạo công việc', 'error');
    }
  });

  // Form project submit
  document.getElementById('formNewProject').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
      name: document.getElementById('projName').value,
      description: document.getElementById('projDesc').value,
      priority: document.getElementById('projPriority').value,
      progress: parseInt(document.getElementById('projProgress').value, 10),
      start_date: document.getElementById('projStartDate').value,
      deadline: document.getElementById('projDeadline').value,
      created_by: 'Trịnh Ngọc Tường'
    };

    try {
      const res = await fetch('/api/projects', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) {
        showToast('Tạo dự án mới thành công!');
        closeModal('modalProject');
        document.getElementById('formNewProject').reset();
        await loadData();
      }
    } catch (err) {
      showToast('Lỗi tạo dự án', 'error');
    }
  });
}

function closeModal(id) {
  const modal = document.getElementById(id);
  if (modal) modal.close();
}

// 11. Test Error Buttons (for Prometheus metrics & Loki LogQL verification)
function setupTestButtons() {
  document.getElementById('btnTest500').addEventListener('click', () => {
    triggerTestError('nginx');
  });
}

async function triggerTestError(type) {
  try {
    const endpoint = type === 'nginx' ? '/api/test/error' : '/api/test/exception';
    showToast(`Đang gửi request gây lỗi tới: ${endpoint}...`);
    const res = await fetch(endpoint);
    const data = await res.json().catch(() => ({}));
    showToast(`[HTTP ${res.status}] Đã tạo log lỗi! Kiểm tra Grafana Explore / Loki LogQL.`);
  } catch (err) {
    showToast('Đã gửi request lỗi (500 Server Error)', 'error');
  }
}

// Helpers
function showToast(msg, type = 'info') {
  toastNotification.textContent = msg;
  toastNotification.style.display = 'block';
  toastNotification.style.borderColor = type === 'error' ? 'var(--accent-rose)' : 'var(--accent-indigo)';
  setTimeout(() => {
    toastNotification.style.display = 'none';
  }, 3500);
}

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/[&<>'"]/g, tag => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    "'": '&#39;',
    '"': '&quot;'
  }[tag] || tag));
}
