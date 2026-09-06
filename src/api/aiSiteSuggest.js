import { apiFetch } from './client'

/**
 * Request AI-generated plaza site fields for a URL.
 * The provider credentials remain on the backend.
 *
 * @param {string} url
 * @returns {Promise<{
 *   name: string,
 *   url: string,
 *   desc: string,
 *   detail: string,
 *   category: string | null,
 *   tags: string[]
 * }>}
 */
export async function suggestSiteFromUrl(url) {
  const value = String(url || '').trim()
  if (!value) {
    throw new Error('请填写网址')
  }
  return apiFetch('/plaza/ai-suggest', {
    method: 'POST',
    body: JSON.stringify({ url: value })
  })
}
