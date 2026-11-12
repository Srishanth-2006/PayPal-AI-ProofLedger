const API_BASE = '/api';

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`);
  return res.json();
}

export async function getMilestones() {
  const res = await fetch(`${API_BASE}/escrow`);
  if (!res.ok) throw new Error('Failed to fetch milestones');
  return res.json();
}

export async function getMilestone(id) {
  const res = await fetch(`${API_BASE}/escrow/${id}`);
  if (!res.ok) throw new Error('Failed to fetch milestone details');
  return res.json();
}

export async function createMilestone(data) {
  const res = await fetch(`${API_BASE}/escrow/create`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to create escrow milestone');
  }
  return res.json();
}

export async function authorizeMilestone(id, orderId) {
  const res = await fetch(`${API_BASE}/escrow/${id}/authorize`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ order_id: orderId }),
  });
  if (!res.ok) throw new Error('Failed to authorize milestone hold');
  return res.json();
}

export async function captureMilestone(id) {
  const res = await fetch(`${API_BASE}/escrow/${id}/capture`, {
    method: 'POST',
  });
  if (!res.ok) throw new Error('Failed to capture escrow funds');
  return res.json();
}

export async function voidMilestone(id, reason) {
  const res = await fetch(`${API_BASE}/escrow/${id}/void`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ reason }),
  });
  if (!res.ok) throw new Error('Failed to void escrow authorization');
  return res.json();
}

export async function submitProof(id, formData) {
  const res = await fetch(`${API_BASE}/proof/${id}/submit`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Failed to submit deliverable proof');
  }
  return res.json();
}

export async function getLedgerBlocks(milestoneId = null) {
  const url = milestoneId ? `${API_BASE}/ledger/blocks?milestone_id=${milestoneId}` : `${API_BASE}/ledger/blocks`;
  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to fetch ledger blocks');
  return res.json();
}

export async function verifyLedgerIntegrity() {
  const res = await fetch(`${API_BASE}/ledger/verify`);
  if (!res.ok) throw new Error('Failed to verify ledger integrity');
  return res.json();
}

export async function getDisputePack(milestoneId, disputeReference = null) {
  const url = disputeReference 
    ? `${API_BASE}/disputes/${milestoneId}/pack?dispute_reference=${disputeReference}` 
    : `${API_BASE}/disputes/${milestoneId}/pack`;
  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to fetch dispute evidence pack');
  return res.json();
}

export function getDisputePdfUrl(milestoneId) {
  return `${API_BASE}/disputes/${milestoneId}/download-pdf`;
}

export async function getSampleDeliverables() {
  const res = await fetch(`${API_BASE}/samples`);
  if (!res.ok) return [];
  return res.json();
}

export async function simulateWebhook(eventType, milestoneId) {
  const res = await fetch(`${API_BASE}/webhooks/simulate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ event_type: eventType, milestone_id: milestoneId }),
  });
  if (!res.ok) throw new Error('Failed to simulate webhook');
  return res.json();
}
