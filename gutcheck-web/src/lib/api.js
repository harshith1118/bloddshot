/**
 * API client for GutCheck backend
 */

const API_BASE_URL = '';

/**
 * Analyze a blood test PDF
 * @param {File} file - The PDF file to analyze
 * @returns {Promise<Object>} Analysis results
 */
export async function analyzeBloodTestPDF(file) {
  const formData = new FormData();
  formData.append('pdf', file);

  const response = await fetch(`${API_BASE_URL}/api/analyze`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Analysis failed' }));
    throw new Error(error.detail || 'Failed to analyze blood test');
  }

  return response.json();
}

/**
 * Health check endpoint
 * @returns {Promise<Object>} Health status
 */
export async function healthCheck() {
  const response = await fetch(`${API_BASE_URL}/api/health`);
  if (!response.ok) {
    throw new Error('Backend service is not available');
  }
  return response.json();
}
