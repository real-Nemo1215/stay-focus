
export const ACCOUNTS_CONFIG = {
  nemo: {
    username: 'Nemo',
    email: 'nemo@focus.app',
    avatar: '/nemo.png'
  },
  pikachu: {
    username: 'Pikachu',
    email: 'pikachu@focus.app',
    avatar: '/nemo.png',
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
