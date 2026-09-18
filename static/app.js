const state = { token: sessionStorage.getItem('nestEggToken') || '' };
const colors = ['#6EC6E8', '#FFD447', '#E94B3C', '#3B8C5A', '#8B5A2B'];
const $ = (id) => document.getElementById(id);

function setMessage(element, text, success = false) {
  element.textContent = text;
  element.className = success ? 'message success' : 'message';
}

async function request(path, options = {}) {
  const headers = { ...(options.headers || {}) };
  if (state.token) headers.Authorization = `Bearer ${state.token}`;
  const response = await fetch(path, { ...options, headers });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.detail || data.message || `Request failed (${response.status})`);
  return data;
}

function normalizeGoal(row) {
  if (!Array.isArray(row)) return row;
  return { id: row[0], title: row[1], budget: row[2], roomId: row[3], progress: row[4], priority: row[5] ?? 1 };
}

function escapeHtml(value) {
  return String(value).replace(/[&<>\'"]/g, (character) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[character]));
}

function bubbleSize(priority) { return `${86 + (Math.max(1, Math.min(5, Number(priority) || 1)) * 25)}px`; }

function isOverAchievementBox(bubble) {
  const box = $('achievementBox').getBoundingClientRect();
  const rect = bubble.getBoundingClientRect();
  const overlaps = rect.left < box.right && rect.right > box.left && rect.top < box.bottom && rect.bottom > box.top;
  $('achievementBox').classList.toggle('ready', overlaps);
  return overlaps;
}

function launchFireworks(bubble) {
  const fireworks = $('fireworks');
  const fieldRect = $('goalField').getBoundingClientRect();
  const bubbleRect = bubble.getBoundingClientRect();
  const sparkColors = ['#FFD447', '#E94B3C', '#6EC6E8', '#3B8C5A', '#8B5A2B'];
  for (let index = 0; index < 28; index += 1) {
    const spark = document.createElement('span');
    const angle = Math.PI * 2 * index / 28;
    const distance = 55 + Math.random() * 90;
    spark.className = 'spark';
    spark.style.left = `${bubbleRect.left - fieldRect.left + bubbleRect.width / 2}px`;
    spark.style.top = `${bubbleRect.top - fieldRect.top + bubbleRect.height / 2}px`;
    spark.style.setProperty('--dx', `${Math.cos(angle) * distance}px`);
    spark.style.setProperty('--dy', `${Math.sin(angle) * distance}px`);
    spark.style.setProperty('--spark-color', sparkColors[index % sparkColors.length]);
    fireworks.appendChild(spark);
    setTimeout(() => spark.remove(), 850);
  }
}

async function completeGoal(bubble) {
  const goal = JSON.parse(bubble.dataset.goal);
  bubble.disabled = true;
  try {
    const result = await request('/goal/update_goal', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ goal_id: Number(goal.id), title: goal.title, active: false, priority: Number(goal.priority) || 1 })
    });
    if (!result.success) throw new Error(result.message || 'Could not complete goal.');
    launchFireworks(bubble);
    bubble.remove();
    setMessage($('goalMessage'), 'Goal achieved! ✦', true);
  } catch (error) {
    bubble.disabled = false;
    setMessage($('goalMessage'), error.message);
  }
}

function animateBubbles() {
  const field = $('bubbleLayer');
  field.querySelectorAll('.goal-bubble').forEach((bubble) => {
    const position = bubble._position;
    if (!position) return;
    const size = bubble.offsetWidth;
    position.x += position.vx;
    position.y += position.vy;
    if (position.x <= 0 || position.x + size >= field.clientWidth) {
      position.vx *= -1;
      position.x = Math.max(0, Math.min(field.clientWidth - size, position.x));
    }
    if (position.y <= 0 || position.y + size >= field.clientHeight) {
      position.vy *= -1;
      position.y = Math.max(0, Math.min(field.clientHeight - size, position.y));
    }
    bubble.style.left = `${position.x}px`;
    bubble.style.top = `${position.y}px`;
  });
  requestAnimationFrame(animateBubbles);
}

function renderGoals(rows) {
  const field = $('bubbleLayer');
  const goals = Array.isArray(rows) ? rows.map(normalizeGoal) : [];
  if (!goals.length) {
    field.innerHTML = '<div class="field-note"><span class="field-note-icon">✦</span><strong>No goals here yet</strong><span>Use the little console below to plant the first one.</span></div>';
    return;
  }
  field.innerHTML = goals.map((goal, index) => {
    const priority = Math.max(1, Math.min(5, Number(goal.priority) || 1));
    return `<button class="goal-bubble" type="button" data-goal='${JSON.stringify(goal).replace(/'/g, '&#39;')}' style="--bubble-size:${bubbleSize(priority)};--bubble-color:${colors[index % colors.length]};" aria-label="Increase priority for ${escapeHtml(goal.title)}"><span class="bubble-title">${escapeHtml(goal.title)}</span></button>`;
  }).join('');
  field.querySelectorAll('.goal-bubble').forEach((bubble, index) => {
    const size = Number.parseInt(bubble.style.getPropertyValue('--bubble-size'), 10);
    bubble._position = {
      x: 20 + ((index * 137) % Math.max(1, field.clientWidth - size - 20)),
      y: 20 + ((index * 83) % Math.max(1, field.clientHeight - size - 20)),
      vx: index % 2 ? 0.45 + index * 0.04 : -0.35 - index * 0.03,
      vy: index % 3 ? 0.3 + index * 0.035 : -0.4 - index * 0.025
    };
    bubble.addEventListener('click', () => {
      if (!bubble._dragged) increasePriority(bubble);
      bubble._dragged = false;
    });
    bubble.addEventListener('pointerdown', (event) => {
      event.preventDefault();
      if (bubble.setPointerCapture) bubble.setPointerCapture(event.pointerId);
      bubble._dragStart = { x: event.clientX, y: event.clientY };
      bubble._dragged = false;
      bubble.classList.add('dragging');
    });
    bubble.addEventListener('pointermove', (event) => {
      if (!bubble._dragStart) return;
      const deltaX = event.clientX - bubble._dragStart.x;
      const deltaY = event.clientY - bubble._dragStart.y;
      if (Math.abs(deltaX) + Math.abs(deltaY) > 5) bubble._dragged = true;
      bubble._position.x += deltaX;
      bubble._position.y += deltaY;
      bubble._dragStart.x = event.clientX;
      bubble._dragStart.y = event.clientY;
      bubble.style.left = `${bubble._position.x}px`;
      bubble.style.top = `${bubble._position.y}px`;
      isOverAchievementBox(bubble);
    });
    const finishDrag = async () => {
      const dragged = bubble._dragged;
      bubble._dragStart = null;
      bubble.classList.remove('dragging');
      const shouldComplete = dragged && isOverAchievementBox(bubble);
      if (shouldComplete) await completeGoal(bubble);
      $('achievementBox').classList.remove('ready');
    };
    bubble.addEventListener('pointerup', finishDrag);
    bubble.addEventListener('pointercancel', finishDrag);
  });
}

async function loadGoals() {
  if (!state.token) return;
  setMessage($('goalMessage'), 'Gathering your goals...');
  try {
    renderGoals(await request('/goal/get_goal'));
    setMessage($('goalMessage'), 'Tap a bubble to give that goal a little more importance.', true);
  } catch (error) { setMessage($('goalMessage'), error.message); }
}

async function increasePriority(bubble) {
  const goal = JSON.parse(bubble.dataset.goal);
  const oldPriority = Math.max(1, Math.min(5, Number(goal.priority) || 1));
  const priority = oldPriority >= 5 ? 1 : oldPriority + 1;
  bubble.disabled = true;
  try {
    const result = await request('/goal/update_goal', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ goal_id: Number(goal.id), title: goal.title, active: true, priority })
    });
    if (!result.success) throw new Error(result.message || 'Could not update priority.');
    bubble.style.setProperty('--bubble-size', bubbleSize(priority));
    goal.priority = priority;
    bubble.dataset.goal = JSON.stringify(goal);
    setMessage($('goalMessage'), priority === 5 && oldPriority === 5 ? 'This goal is at maximum priority.' : 'Priority updated.', true);
  } catch (error) { setMessage($('goalMessage'), error.message); }
  bubble.disabled = false;
}

function enterGarden() {
  $('loginScreen').hidden = true;
  $('goalScreen').hidden = false;
  $('console').hidden = false;
  $('logoutButton').hidden = false;
  $('loginState').textContent = 'Signed in';
}

$('loginForm').addEventListener('submit', async (event) => {
  event.preventDefault();
  const button = event.currentTarget.querySelector('button');
  button.disabled = true;
  setMessage($('loginMessage'), 'Opening your garden...');
  const params = new URLSearchParams({ username: $('username').value, password: $('password').value });
  try {
    const result = await request(`/auth/login?${params}`);
    if (!result.success) throw new Error(result.message || 'Invalid credentials.');
    state.token = result.message;
    sessionStorage.setItem('nestEggToken', state.token);
    enterGarden();
  } catch (error) { setMessage($('loginMessage'), error.message); }
  button.disabled = false;
});

$('goalForm').addEventListener('submit', async (event) => {
  event.preventDefault();
  const form = event.currentTarget;
  const button = form.querySelector('button');
  button.disabled = true;
  try {
    const result = await request('/goal/create_goal', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: $('goalTitle').value })
    });
    if (!result.success) throw new Error(result.message || 'Could not create goal.');
    $('goalForm').reset();
    setMessage($('goalMessage'), 'A new goal has bloomed.', true);
    await loadGoals();
  } catch (error) { setMessage($('goalMessage'), error.message); }
  button.disabled = false;
});

$('refreshButton').addEventListener('click', loadGoals);
$('logoutButton').addEventListener('click', () => {
  state.token = '';
  sessionStorage.removeItem('nestEggToken');
  $('loginScreen').hidden = false;
  $('goalScreen').hidden = true;
  $('console').hidden = true;
  $('logoutButton').hidden = true;
  $('loginState').textContent = 'Not signed in';
});

if (state.token) {
  enterGarden();
  loadGoals();
}

requestAnimationFrame(animateBubbles);
