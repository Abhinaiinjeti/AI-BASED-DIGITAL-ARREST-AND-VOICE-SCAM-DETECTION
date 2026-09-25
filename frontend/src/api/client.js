/**
 * API Client for AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION
 */

const BASE_URL = '/api';

export async function checkBackendHealth() {
  try {
    const res = await fetch(`${BASE_URL}/health`);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return await res.json();
  } catch (err) {
    return { status: 'offline', error: err.message };
  }
}

export async function fetchModelInfo() {
  const res = await fetch(`${BASE_URL}/models/info`);
  if (!res.ok) throw new Error('Failed to fetch model info');
  return await res.json();
}

export async function analyzeText(text, language = null) {
  const payload = { text };
  if (language && language !== 'auto') {
    payload.language = language;
  }
  const res = await fetch(`${BASE_URL}/analyze/text`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || errData.error || `Server responded with ${res.status}`);
  }
  return await res.json();
}

export async function analyzeAudio(audioBlob, fileName = 'recording.wav', language = null) {
  const formData = new FormData();
  formData.append('file', audioBlob, fileName);
  if (language && language !== 'auto') {
    formData.append('language', language);
  }

  const res = await fetch(`${BASE_URL}/analyze/audio`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    throw new Error(errData.detail || errData.error || `Audio analysis failed (${res.status})`);
  }
  return await res.json();
}

export async function fetchHistory(limit = 50, offset = 0) {
  const res = await fetch(`${BASE_URL}/history?limit=${limit}&offset=${offset}`);
  if (!res.ok) throw new Error('Failed to fetch history');
  return await res.json();
}

export async function clearHistory() {
  const res = await fetch(`${BASE_URL}/history`, { method: 'DELETE' });
  if (!res.ok) throw new Error('Failed to purge history');
  return await res.json();
}

export async function fetchStatistics() {
  const res = await fetch(`${BASE_URL}/stats`);
  if (!res.ok) throw new Error('Failed to fetch dashboard statistics');
  return await res.json();
}

export async function fetchDemos() {
  const res = await fetch(`${BASE_URL}/demos`);
  if (!res.ok) throw new Error('Failed to fetch demonstration presets');
  return await res.json();
}
