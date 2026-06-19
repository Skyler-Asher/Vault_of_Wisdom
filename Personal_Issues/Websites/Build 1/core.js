/**
 * core.js
 * Shared constants and utility functions for the Personal Day Planner.
 */

// ── CONSTANTS ──────────────────────────────────────────────
const COLORS = {
  purple: { hex: '#7C6FE0', dim: 'rgba(124,111,224,0.12)', border: 'rgba(124,111,224,0.22)' },
  teal:   { hex: '#2EC090', dim: 'rgba(46,192,144,0.12)',  border: 'rgba(46,192,144,0.22)'  },
  amber:  { hex: '#E8A030', dim: 'rgba(232,160,48,0.12)',  border: 'rgba(232,160,48,0.22)'  },
  coral:  { hex: '#E86840', dim: 'rgba(232,104,64,0.12)',  border: 'rgba(232,104,64,0.22)'  },
  gray:   { hex: '#666662', dim: 'rgba(102,102,98,0.12)',  border: 'rgba(102,102,98,0.22)'  },
};

const KEYS = {
  STATE: 'monday_schedule_v2',
  ORDER: 'day_order_v1',
  SECTIONS: 'day_sections_v1',
  BANK: 'task_bank_v1',
  CUSTOM_DAY_TASKS: 'day_custom_tasks_v1'
};

const ICON_LABELS = {
  'ti-run':'Run','ti-barbell':'Lift','ti-book-2':'Read','ti-pencil':'Write',
  'ti-brain':'Think','ti-chart-line':'Trade','ti-moon':'Wind down','ti-coffee':'Coffee',
  'ti-meditation':'Meditate','ti-device-laptop':'Deep work','ti-notes':'Debrief',
  'ti-walk':'Walk','ti-music':'Music','ti-heart-rate-monitor':'Health','ti-star':'Task'
};

// ── UTILITIES ──────────────────────────────────────────────

/**
 * Escapes HTML characters to prevent XSS.
 */
function escHtml(s) {
  return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

/**
 * Parses a comma-separated string into an array of tags.
 */
function parseTags(value) {
  return String(value || '')
    .split(',')
    .map(tag => tag.trim())
    .filter(Boolean)
    .slice(0, 6);
}

/**
 * Gets a task's tags, falling back to parsing the duration if tags array is missing.
 */
function getTaskTags(task) {
  if (Array.isArray(task.tags) && task.tags.length) return task.tags;
  return parseTags(task.duration || '');
}

/**
 * Shakes an element visually to indicate an error/invalid state.
 */
function shake(el) {
  if (!el) return;
  el.style.transition = 'none';
  el.style.borderColor = 'var(--coral)';
  setTimeout(() => { 
    el.style.transition = 'border-color 0.4s'; 
    el.style.borderColor = ''; 
  }, 600);
}

/**
 * Formats a Date object to YYYY-MM-DD in local time.
 */
function getISODateString(d) {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${day}`;
}

/**
 * Returns a namespaced day-specific key or the global key if applicable.
 */
function getDayKey(baseKey, dateStr) {
  if (baseKey === KEYS.BANK) return baseKey;
  return `${baseKey}_${dateStr}`;
}

