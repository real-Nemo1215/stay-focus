/**
 * ==============================================================================
 * Account Configuration & Custom Avatars
 * ==============================================================================
 * You can customize the pictures/avatars for Nemo and pikachu here!
 *
 * Supported avatar formats:
 * 1. Emoji: '🐠', '⚡', '🐱', '🌸', etc.
 * 2. Web Image URL: 'https://example.com/avatar.jpg'
 * 3. Local file in public folder: '/nemo.png' (place the image file in the public/ folder)
 */

export const ACCOUNTS_CONFIG = {
  nemo: {
    username: 'Nemo',
    email: 'nemo@focus.app',
    avatar: '🐠', // 👈 Edit Nemo's picture or emoji here
  },
  pikachu: {
    username: 'pikachu',
    email: 'pikachu@focus.app',
    avatar: '⚡', // 👈 Edit pikachu's picture or emoji here
  },
}

export function getAccountMeta(nameOrEmail) {
  const key = (nameOrEmail || '').toLowerCase()
  if (key.includes('nemo')) {
    return ACCOUNTS_CONFIG.nemo
  }
  if (key.includes('pikachu')) {
    return ACCOUNTS_CONFIG.pikachu
  }
  return {
    username: nameOrEmail || 'User',
    email: `${(nameOrEmail || 'user').toLowerCase()}@focus.app`,
    avatar: '👤',
  }
}
