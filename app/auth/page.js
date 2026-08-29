'use client'

import { useState } from 'react'
import { supabase } from '@/lib/supabaseClient'
import { useRouter } from 'next/navigation'

const ALLOWED_ACCOUNTS = {
  nemo: {
    username: 'Nemo',
    email: 'nemo@focus.app',
    avatar: '🐠',
  },
  pikachu: {
    username: 'pikachu',
    email: 'pikachu@focus.app',
    avatar: '⚡',
  },
}

export default function AuthPage() {
  const [selectedUsername, setSelectedUsername] = useState('Nemo')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const router = useRouter()

  const handleSelectAccount = (username) => {
    setSelectedUsername(username)
    setError(null)
    setPassword('')
  }

  const handleLogin = async (e) => {
    e.preventDefault()
    setError(null)
    setLoading(true)

    const key = selectedUsername.trim().toLowerCase()
    const account = ALLOWED_ACCOUNTS[key]

    if (!account) {
      setError('Invalid account. Only Nemo and pikachu accounts can log in.')
      setLoading(false)
      return
    }

    try {
      const { data, error: signInError } = await supabase.auth.signInWithPassword({
        email: account.email,
        password: password,
      })

      if (signInError) {
        if (signInError.message.toLowerCase().includes('email not confirmed')) {
          throw new Error(
            'Email confirmation is required by your Supabase project. Please run the updated supabase/schema.sql in your Supabase SQL Editor to auto-confirm both accounts.'
          )
        }

        if (
          signInError.message.toLowerCase().includes('invalid login credentials') ||
          signInError.message.toLowerCase().includes('user not found')
        ) {
          const { data: signUpData, error: signUpError } = await supabase.auth.signUp({
            email: account.email,
            password: password,
            options: {
              data: { full_name: account.username },
            },
          })

          if (signUpError) {
            throw signUpError
          }

          if (signUpData?.session) {
            router.push('/')
            return
          } else {
            throw new Error(
              'Account initialized! Please run supabase/schema.sql in your Supabase SQL Editor to activate and auto-confirm.'
            )
          }
        }

        throw signInError
      }

      if (data?.session) {
        router.push('/')
      }
    } catch (err) {
      setError(err.message || 'Failed to log in.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#FAF3F5] via-[#F4E4E7] to-[#EBD2D7] p-4">
      <div className="bg-white/95 backdrop-blur-md p-8 md:p-10 rounded-3xl shadow-2xl shadow-[#800020]/10 w-full max-w-md border border-[#800020]/15 transition-all">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-[#F7E7EA] text-[#800020] text-3xl mb-3 shadow-inner border border-[#E5BEC5]">
            🎯
          </div>
          <h1 className="text-3xl font-black text-[#800020] tracking-tight">Focus</h1>
          <p className="text-sm text-[#733844] mt-1 font-medium">
            Sign in to your shared Focus workspace
          </p>
        </div>

        {/* Account Selector Cards */}
        <div className="mb-6">
          <label className="block text-[11px] font-bold uppercase tracking-wider text-[#9E5765] mb-2.5 text-center">
            Select Account
          </label>
          <div className="grid grid-cols-2 gap-3">
            {Object.values(ALLOWED_ACCOUNTS).map((acc) => {
              const isSelected = selectedUsername.toLowerCase() === acc.username.toLowerCase()
              return (
                <button
                  key={acc.username}
                  type="button"
                  onClick={() => handleSelectAccount(acc.username)}
                  className={`p-4 rounded-2xl border flex flex-col items-center gap-1.5 transition-all cursor-pointer ${
                    isSelected
                      ? 'bg-[#FCF0F3] border-[#800020] ring-2 ring-[#800020]/30 shadow-md shadow-[#800020]/10'
                      : 'bg-white border-[#E6CBD1] hover:border-[#800020]/40'
                  }`}
                >
                  <span className="text-3xl mb-1">{acc.avatar}</span>
                  <span className={`text-base font-bold ${isSelected ? 'text-[#800020]' : 'text-gray-700'}`}>
                    {acc.username}
                  </span>
                </button>
              )
            })}
          </div>
        </div>

        <form onSubmit={handleLogin} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-[#541622] mb-1.5">
              Password for <span className="text-[#800020] font-bold">{selectedUsername}</span>
            </label>
            <input
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full p-3.5 bg-[#FAF3F5] border border-[#DFC0C7] rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-[#800020] text-gray-800 transition"
            />
          </div>

          {error && (
            <div className="bg-[#FCEDF0] border border-[#F0B8C3] text-[#800020] text-xs p-3.5 rounded-xl leading-relaxed">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-[#800020] via-[#8B1E3F] to-[#5C0A19] hover:from-[#6B001A] hover:to-[#4A0512] text-white p-3.5 rounded-xl font-bold shadow-lg shadow-[#800020]/25 transition cursor-pointer disabled:opacity-50 mt-2"
          >
            {loading ? 'Signing in...' : `Log In as ${selectedUsername} 🎯`}
          </button>
        </form>

        <div className="mt-8 text-center text-xs text-[#800020]/50 font-medium">
          Focus &bull; Shared Goal Tracker
        </div>
      </div>
    </div>
  )
}
