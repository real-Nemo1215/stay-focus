'use client'

import { useEffect, useState, useMemo, useCallback } from 'react'
import { supabase } from '@/lib/supabaseClient'
import { useRouter } from 'next/navigation'
import { ACCOUNTS_CONFIG, getAccountMeta } from '@/lib/accountConfig'

// Helper date utilities (local time based)
const getLocalDateString = (date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const formatDisplayDate = (date) => {
  return date.toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
    year: 'numeric',
  })
}

// Avatar Renderer Component (supports emojis, local files '/avatar.jpg', or web URLs)
function RenderAvatar({ avatar, name, className = 'w-6 h-6' }) {
  const [imgError, setImgError] = useState(false)
  const isImage = !imgError && avatar && (avatar.startsWith('http') || avatar.startsWith('/') || avatar.startsWith('data:'))

  if (isImage) {
    return (
      <img
        src={avatar}
        alt={name || 'avatar'}
        onError={() => setImgError(true)}
        className={`rounded-full object-cover border border-[#E5BEC5] inline-block aspect-square flex-shrink-0 align-middle ${className}`}
      />
    )
  }
  return <span className="inline-block select-none text-base leading-none align-middle">{avatar || '👤'}</span>
}

export default function FocusDashboard() {
  const router = useRouter()
  const [user, setUser] = useState(null)
  const [profile, setProfile] = useState(null)
  const [partner, setPartner] = useState(null)
  const [loading, setLoading] = useState(true)

  // Tabs: 'today' | 'yesterday' | 'monthly'
  const [activeTab, setActiveTab] = useState('today')
  const [myGoals, setMyGoals] = useState([])
  const [partnerGoals, setPartnerGoals] = useState([])
  const [newGoal, setNewGoal] = useState('')
  const [isSubmittingGoal, setIsSubmittingGoal] = useState(false)

  // Current and Yesterday Date computations
  const { todayISO, yesterdayISO, todayFormatted, yesterdayFormatted, currentMonthFormatted } = useMemo(() => {
    const now = new Date()
    const yesterday = new Date()
    yesterday.setDate(now.getDate() - 1)

    return {
      todayISO: getLocalDateString(now),
      yesterdayISO: getLocalDateString(yesterday),
      todayFormatted: formatDisplayDate(now),
      yesterdayFormatted: formatDisplayDate(yesterday),
      currentMonthFormatted: now.toLocaleDateString('en-US', { month: 'long', year: 'numeric' }),
    }
  }, [])

  // 1. Check Auth State
  useEffect(() => {
    let isMounted = true

    const getSession = async () => {
      try {
        const { data: { session } } = await supabase.auth.getSession()
        if (!session) {
          router.push('/auth')
          return
        }
        if (isMounted) {
          setUser(session.user)
        }
      } catch (err) {
        console.error('Session error:', err)
        router.push('/auth')
      }
    }
    getSession()

    const { data: authListener } = supabase.auth.onAuthStateChange((_event, session) => {
      if (!session) {
        router.push('/auth')
      } else {
        setUser(session?.user || null)
      }
    })

    return () => {
      isMounted = false
      authListener?.subscription?.unsubscribe()
    }
  }, [router])

  // Determine current user's name and partner
  const getUserMeta = useCallback((currentUser) => {
    if (!currentUser) return { myName: 'User', partnerName: 'Partner' }
    const email = (currentUser.email || '').toLowerCase()
    const metaName = currentUser.user_metadata?.full_name || ''

    if (email.includes('nemo') || metaName.toLowerCase() === 'nemo') {
      return { myName: 'Nemo', partnerName: 'pikachu' }
    } else if (email.includes('pikachu') || metaName.toLowerCase() === 'pikachu') {
      return { myName: 'pikachu', partnerName: 'Nemo' }
    }
    return { myName: metaName || 'User', partnerName: 'Partner' }
  }, [])

  // 2. Fetch Profile & Partner Data
  const fetchProfileAndPartner = useCallback(async (currentUser) => {
    if (!currentUser) return
    const { myName, partnerName } = getUserMeta(currentUser)

    try {
      let { data: myProf, error: myProfErr } = await supabase
        .from('profiles')
        .select('*')
        .eq('id', currentUser.id)
        .maybeSingle()

      if (!myProf || myProfErr) {
        const { data: insertedProf } = await supabase
          .from('profiles')
          .upsert({
            id: currentUser.id,
            name: myName,
            email: currentUser.email,
            username: myName.toLowerCase(),
          })
          .select()
          .single()
        myProf = insertedProf || { id: currentUser.id, name: myName, email: currentUser.email }
      }

      setProfile(myProf)

      const { data: partnerProf } = await supabase
        .from('profiles')
        .select('*')
        .ilike('name', partnerName)
        .maybeSingle()

      if (partnerProf) {
        setPartner(partnerProf)
        if (myProf?.partner_id !== partnerProf.id) {
          await supabase.from('profiles').update({ partner_id: partnerProf.id }).eq('id', currentUser.id)
        }
        if (partnerProf.partner_id !== currentUser.id) {
          await supabase.from('profiles').update({ partner_id: currentUser.id }).eq('id', partnerProf.id)
        }
      } else {
        setPartner({
          id: 'pending-' + partnerName,
          name: partnerName,
          email: `${partnerName.toLowerCase()}@focus.app`,
        })
      }
    } catch (err) {
      console.error('Error fetching profile:', err)
      setProfile({ id: currentUser.id, name: myName, email: currentUser.email })
      setPartner({ id: 'pending-' + partnerName, name: partnerName })
    } finally {
      setLoading(false)
    }
  }, [getUserMeta])

  useEffect(() => {
    if (user) {
      fetchProfileAndPartner(user)
    }
  }, [user, fetchProfileAndPartner])

  // 3. Fetch Goals & Realtime Subscription
  useEffect(() => {
    if (!profile) return

    const fetchGoals = async () => {
      try {
        const { data: myData } = await supabase
          .from('goals')
          .select('*')
          .eq('user_id', profile.id)
          .order('created_at', { ascending: true })

        setMyGoals(myData || [])

        if (partner?.id && !partner.id.startsWith('pending-')) {
          const { data: partData } = await supabase
            .from('goals')
            .select('*')
            .eq('user_id', partner.id)
            .order('created_at', { ascending: true })
          setPartnerGoals(partData || [])
        }
      } catch (e) {
        console.error('Failed to fetch goals:', e)
      }
    }
    fetchGoals()

    const channel = supabase
      .channel(`focus-sync-${profile.id}`)
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'goals' },
        (payload) => {
          if (payload.eventType === 'INSERT') {
            if (payload.new.user_id === profile.id) {
              setMyGoals((prev) => (prev.some((g) => g.id === payload.new.id) ? prev : [...prev, payload.new]))
            } else if (partner && payload.new.user_id === partner.id) {
              setPartnerGoals((prev) => (prev.some((g) => g.id === payload.new.id) ? prev : [...prev, payload.new]))
            }
          } else if (payload.eventType === 'UPDATE') {
            if (payload.new.user_id === profile.id) {
              setMyGoals((prev) => prev.map((g) => (g.id === payload.new.id ? payload.new : g)))
            } else {
              setPartnerGoals((prev) => prev.map((g) => (g.id === payload.new.id ? payload.new : g)))
            }
          } else if (payload.eventType === 'DELETE') {
            setMyGoals((prev) => prev.filter((g) => g.id !== payload.old.id))
            setPartnerGoals((prev) => prev.filter((g) => g.id !== payload.old.id))
          }
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [profile, partner])

  // Helper date extractor for any goal
  const getGoalDateString = useCallback((g) => {
    if (g.target_date) return g.target_date
    if (g.created_at) {
      try {
        const d = new Date(g.created_at)
        return getLocalDateString(d)
      } catch {
        return g.created_at.slice(0, 10)
      }
    }
    return todayISO
  }, [todayISO])

  // Helper filter for item dates
  const filterGoalsByTab = useCallback((goalsList, tab) => {
    return goalsList.filter((g) => {
      if (tab === 'monthly') {
        return g.type === 'monthly'
      }

      const itemDate = getGoalDateString(g)

      if (tab === 'today') {
        return g.type === 'daily' && (itemDate === todayISO || !g.created_at)
      }

      if (tab === 'yesterday') {
        return g.type === 'daily' && itemDate === yesterdayISO
      }

      return false
    })
  }, [todayISO, yesterdayISO, getGoalDateString])

  // 4. Goal Actions
  const addGoal = async (e) => {
    e.preventDefault()
    if (!newGoal.trim() || !user || activeTab === 'yesterday') return
    setIsSubmittingGoal(true)
    const goalTitle = newGoal.trim()
    setNewGoal('')

    const goalType = activeTab === 'monthly' ? 'monthly' : 'daily'

    const payload = {
      user_id: user.id,
      title: goalTitle,
      type: goalType,
      is_completed: false,
    }

    try {
      let { data, error } = await supabase
        .from('goals')
        .insert({
          ...payload,
          target_date: todayISO,
        })
        .select()
        .single()

      if (error && error.message && error.message.includes('target_date')) {
        const fallbackRes = await supabase
          .from('goals')
          .insert(payload)
          .select()
          .single()
        data = fallbackRes.data
        error = fallbackRes.error
      }

      if (error) throw error
      if (data) {
        setMyGoals((prev) => (prev.some((g) => g.id === data.id) ? prev : [...prev, data]))
      }
    } catch (err) {
      alert('Error adding focus item: ' + err.message)
    } finally {
      setIsSubmittingGoal(false)
    }
  }

  // Copy yesterday's unfinished goal into today
  const copyToToday = async (goal) => {
    try {
      const payload = {
        user_id: user.id,
        title: goal.title,
        type: 'daily',
        is_completed: false,
      }

      let { data, error } = await supabase
        .from('goals')
        .insert({
          ...payload,
          target_date: todayISO,
        })
        .select()
        .single()

      if (error && error.message && error.message.includes('target_date')) {
        const fallbackRes = await supabase
          .from('goals')
          .insert(payload)
          .select()
          .single()
        data = fallbackRes.data
        error = fallbackRes.error
      }

      if (error) throw error
      if (data) {
        setMyGoals((prev) => (prev.some((g) => g.id === data.id) ? prev : [...prev, data]))
        setActiveTab('today')
      }
    } catch (err) {
      alert('Error copying to today: ' + err.message)
    }
  }

  const toggleGoal = async (goal) => {
    const nextState = !goal.is_completed
    setMyGoals((prev) =>
      prev.map((g) => (g.id === goal.id ? { ...g, is_completed: nextState } : g))
    )

    const { error } = await supabase
      .from('goals')
      .update({ is_completed: nextState })
      .eq('id', goal.id)

    if (error) {
      console.error('Failed to toggle focus item:', error)
      setMyGoals((prev) =>
        prev.map((g) => (g.id === goal.id ? { ...g, is_completed: goal.is_completed } : g))
      )
    }
  }

  const deleteGoal = async (id) => {
    setMyGoals((prev) => prev.filter((g) => g.id !== id))
    const { error } = await supabase.from('goals').delete().eq('id', id)
    if (error) console.error('Failed to delete focus item:', error)
  }

  // Progress metrics for active tab
  const activeMyGoals = useMemo(() => filterGoalsByTab(myGoals, activeTab), [myGoals, activeTab, filterGoalsByTab])
  const activePartnerGoals = useMemo(() => filterGoalsByTab(partnerGoals, activeTab), [partnerGoals, activeTab, filterGoalsByTab])

  const myCompletedCount = useMemo(() => activeMyGoals.filter((g) => g.is_completed).length, [activeMyGoals])
  const partnerCompletedCount = useMemo(() => activePartnerGoals.filter((g) => g.is_completed).length, [activePartnerGoals])

  const myProgress = activeMyGoals.length > 0 ? Math.round((myCompletedCount / activeMyGoals.length) * 100) : 0
  const partnerProgress = activePartnerGoals.length > 0 ? Math.round((partnerCompletedCount / activePartnerGoals.length) * 100) : 0

  if (loading || !user || !profile) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-[#FAF3F5] via-[#F4E4E7] to-[#EBD2D7] text-[#800020] gap-3">
        <span className="text-4xl animate-spin">💫</span>
        <p className="font-bold text-[#800020]">Loading Stay Focus...</p>
      </div>
    )
  }

  const partnerDisplayName = partner?.name || (profile?.name === 'Nemo' ? 'pikachu' : 'Nemo')

  const myMeta = getAccountMeta(profile.name)
  const partnerMeta = getAccountMeta(partnerDisplayName)

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#FAF4F6] via-[#F5E6E9] to-[#EED6DC] p-4 md:p-8 text-gray-800">
      <div className="max-w-5xl mx-auto">
        {/* Header Bar */}
        <header className="flex flex-col sm:flex-row justify-between items-center gap-4 mb-6 bg-white/95 backdrop-blur-md p-4 px-6 rounded-3xl border border-[#800020]/15 shadow-sm">
          <div className="flex items-center gap-3.5">
            <div className="w-12 h-12 rounded-2xl bg-[#F7E7EA] flex items-center justify-center text-2xl border border-[#E5BEC5] shadow-inner">
              🎯
            </div>
            <div>
              <h1 className="text-2xl font-black text-[#800020] tracking-tight">Stay Focus</h1>
              <p className="text-xs text-[#733844] font-semibold">
                {profile.name} & {partnerDisplayName} &bull; Shared Focus Space
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="text-xs bg-[#FAF0F3] text-[#800020] px-3.5 py-1.5 rounded-xl font-bold border border-[#E2B7C1] flex items-center gap-2 shadow-sm">
              <RenderAvatar avatar={myMeta.avatar} name={profile.name} className="w-6 h-6" />
              <span>{profile.name}</span>
            </div>
            <button
              onClick={() => supabase.auth.signOut()}
              className="text-xs bg-white hover:bg-[#FCEDF0] text-[#800020] border border-[#E2B7C1] font-bold px-4 py-2 rounded-xl transition cursor-pointer shadow-sm"
            >
              Sign Out
            </button>
          </div>
        </header>

        {/* Tab & Date Navigation */}
        <div className="flex flex-col items-center mb-8 gap-3">
          {/* Main Navigation Tabs */}
          <div className="bg-white/95 p-1.5 rounded-full border border-[#800020]/20 shadow-md shadow-[#800020]/5 inline-flex gap-1.5 max-w-full overflow-x-auto">
            <button
              onClick={() => setActiveTab('today')}
              className={`px-5 py-2.5 rounded-full text-xs sm:text-sm font-bold transition-all cursor-pointer flex items-center gap-1.5 whitespace-nowrap ${
                activeTab === 'today'
                  ? 'bg-gradient-to-r from-[#800020] via-[#8B1E3F] to-[#5C0A19] text-white shadow-md shadow-[#800020]/25'
                  : 'text-[#662B37] hover:text-[#800020] hover:bg-[#FAF0F3]'
              }`}
            >
              <span>☀️</span> Today&apos;s Focus
            </button>
            <button
              onClick={() => setActiveTab('yesterday')}
              className={`px-5 py-2.5 rounded-full text-xs sm:text-sm font-bold transition-all cursor-pointer flex items-center gap-1.5 whitespace-nowrap ${
                activeTab === 'yesterday'
                  ? 'bg-gradient-to-r from-[#800020] via-[#8B1E3F] to-[#5C0A19] text-white shadow-md shadow-[#800020]/25'
                  : 'text-[#662B37] hover:text-[#800020] hover:bg-[#FAF0F3]'
              }`}
            >
              <span>⏳</span> Yesterday&apos;s Focus
            </button>
            <button
              onClick={() => setActiveTab('monthly')}
              className={`px-5 py-2.5 rounded-full text-xs sm:text-sm font-bold transition-all cursor-pointer flex items-center gap-1.5 whitespace-nowrap ${
                activeTab === 'monthly'
                  ? 'bg-gradient-to-r from-[#800020] via-[#8B1E3F] to-[#5C0A19] text-white shadow-md shadow-[#800020]/25'
                  : 'text-[#662B37] hover:text-[#800020] hover:bg-[#FAF0F3]'
              }`}
            >
              <span>🌙</span> Monthly Focus
            </button>
          </div>

          {/* Prominent Date & Day Display Banner */}
          <div className="bg-[#FAF0F3] border border-[#E5BEC5] text-[#800020] px-4 py-1.5 rounded-2xl text-xs sm:text-sm font-bold flex items-center gap-2 shadow-sm">
            <span>📅</span>
            {activeTab === 'today' && <span>Today: <strong>{todayFormatted}</strong></span>}
            {activeTab === 'yesterday' && <span>Yesterday: <strong>{yesterdayFormatted}</strong> (Read-Only)</span>}
            {activeTab === 'monthly' && <span>Monthly Focus for <strong>{currentMonthFormatted}</strong></span>}
          </div>
        </div>

        {/* Two-Column Focus Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-8">
          {/* User's Focus Column */}
          <div className="bg-white rounded-3xl shadow-sm border border-[#800020]/15 p-6 flex flex-col justify-between">
            <div>
              <div className="flex justify-between items-center mb-3">
                <h2 className="text-lg sm:text-xl font-black text-[#800020] flex items-center gap-2.5">
                  <RenderAvatar avatar={myMeta.avatar} name={profile.name} className="w-8 h-8" />
                  <span>{profile.name}&apos;s Focus</span>
                </h2>
                <span className="text-xs font-bold px-3 py-1 bg-[#FAF0F3] text-[#800020] rounded-full border border-[#E5BEC5]">
                  {myCompletedCount}/{activeMyGoals.length} Done
                </span>
              </div>

              {/* Progress bar */}
              <div className="w-full bg-[#FAF0F3] border border-[#F0D5DA] rounded-full h-2.5 mb-5 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-[#800020] to-[#9C1B33] h-2.5 rounded-full transition-all duration-500"
                  style={{ width: `${myProgress}%` }}
                />
              </div>

              {/* Add Focus Form (Only for Today and Monthly - Hidden on Yesterday) */}
              {activeTab !== 'yesterday' ? (
                <form onSubmit={addGoal} className="flex gap-2 mb-5">
                  <input
                    type="text"
                    value={newGoal}
                    onChange={(e) => setNewGoal(e.target.value)}
                    placeholder={
                      activeTab === 'monthly'
                        ? 'Add a monthly focus item...'
                        : "Add today's focus item..."
                    }
                    className="flex-1 p-3 text-sm bg-[#FAF5F6] border border-[#DFC0C7] rounded-xl focus:bg-white focus:outline-none focus:ring-2 focus:ring-[#800020] transition"
                  />
                  <button
                    type="submit"
                    disabled={isSubmittingGoal || !newGoal.trim()}
                    className="bg-gradient-to-r from-[#800020] to-[#8B1E3F] hover:from-[#6B001A] hover:to-[#5C0A19] text-white px-5 py-3 rounded-xl font-bold text-sm disabled:opacity-50 transition shadow-sm cursor-pointer"
                  >
                    Add
                  </button>
                </form>
              ) : (
                <div className="mb-5 p-3 bg-[#FAF3F5] rounded-xl border border-[#E9CAD1] text-xs text-[#7A3341] font-medium flex items-center justify-between">
                  <span>🔒 Yesterday&apos;s list is archived.</span>
                  <span className="text-[11px] text-[#800020] font-bold">Use &apos;+ Today&apos; to carry over</span>
                </div>
              )}

              {/* Goal List */}
              <ul className="space-y-2.5">
                {activeMyGoals.length === 0 ? (
                  <li className="text-center py-10 text-[#9E6772] text-sm italic bg-[#FAF5F6] rounded-2xl border border-dashed border-[#E5CBD1]">
                    {activeTab === 'yesterday'
                      ? "No focus items recorded for yesterday. ⏳"
                      : activeTab === 'monthly'
                      ? "No monthly focus items yet. Add one above! 🌙"
                      : "No focus items yet for today. Add one above! ✨"}
                  </li>
                ) : (
                  activeMyGoals.map((goal) => (
                    <li
                      key={goal.id}
                      className="group flex items-center justify-between bg-[#FAF3F5] hover:bg-[#F7EAEF] p-3.5 rounded-xl border border-[#E9CAD1] transition"
                    >
                      <label className="flex items-center gap-3 cursor-pointer select-none flex-1">
                        <input
                          type="checkbox"
                          checked={goal.is_completed}
                          onChange={() => toggleGoal(goal)}
                          className="w-5 h-5 accent-[#800020] rounded cursor-pointer transition"
                        />
                        <span
                          className={`text-sm transition-all ${
                            goal.is_completed
                              ? 'line-through text-gray-400'
                              : 'text-gray-900 font-semibold'
                          }`}
                        >
                          {goal.title}
                        </span>
                      </label>

                      <div className="flex items-center gap-1.5">
                        {/* If in Yesterday tab and item is not completed, offer 1-click move to today */}
                        {activeTab === 'yesterday' && !goal.is_completed && (
                          <button
                            onClick={() => copyToToday(goal)}
                            className="text-[11px] bg-white hover:bg-[#800020] text-[#800020] hover:text-white border border-[#800020]/30 font-bold px-2.5 py-1 rounded-lg transition shadow-xs cursor-pointer"
                            title="Copy to Today's Focus"
                          >
                            + Today
                          </button>
                        )}
                        <button
                          onClick={() => deleteGoal(goal.id)}
                          className="text-gray-300 hover:text-red-600 text-xs px-2 py-1 transition cursor-pointer"
                          title="Delete item"
                        >
                          ✕
                        </button>
                      </div>
                    </li>
                  ))
                )}
              </ul>
            </div>
          </div>

          {/* Partner's Focus Column */}
          <div className="bg-white rounded-3xl shadow-sm border border-[#800020]/15 p-6 flex flex-col justify-between">
            <div>
              <div className="flex justify-between items-center mb-3">
                <h2 className="text-lg sm:text-xl font-black text-[#5C0A19] flex items-center gap-2.5">
                  <RenderAvatar avatar={partnerMeta.avatar} name={partnerDisplayName} className="w-8 h-8" />
                  <span>{partnerDisplayName}&apos;s Focus</span>
                </h2>
                <span className="text-xs font-bold px-3 py-1 bg-[#FAF0F3] text-[#800020] rounded-full border border-[#E5BEC5]">
                  {partnerCompletedCount}/{activePartnerGoals.length} Done
                </span>
              </div>

              {/* Progress bar */}
              <div className="w-full bg-[#FAF0F3] border border-[#F0D5DA] rounded-full h-2.5 mb-5 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-[#8B1E3F] to-[#5C0A19] h-2.5 rounded-full transition-all duration-500"
                  style={{ width: `${partnerProgress}%` }}
                />
              </div>

              {/* Partner Focus items list */}
              <ul className="space-y-2.5">
                {activePartnerGoals.length === 0 ? (
                  <li className="text-center py-12 text-[#9E6772] text-sm italic bg-[#FAF5F6] rounded-2xl border border-dashed border-[#E5CBD1]">
                    {partnerDisplayName} hasn&apos;t added any {activeTab === 'yesterday' ? "yesterday's" : activeTab === 'monthly' ? 'monthly' : "today's"} focus items. 🎯
                  </li>
                ) : (
                  activePartnerGoals.map((goal) => (
                    <li
                      key={goal.id}
                      className="flex items-center gap-3 bg-[#FAF3F5] p-3.5 rounded-xl border border-[#E9CAD1]"
                    >
                      <input
                        type="checkbox"
                        checked={goal.is_completed}
                        disabled
                        className="w-5 h-5 accent-[#800020] rounded opacity-80"
                      />
                      <span
                        className={`text-sm ${
                          goal.is_completed
                            ? 'line-through text-gray-400'
                            : 'text-gray-900 font-semibold'
                        }`}
                      >
                        {goal.title}
                      </span>
                    </li>
                  ))
                )}
              </ul>
            </div>

            <div className="mt-8 text-center text-xs text-[#800020]/60 font-medium">
              ⚡ Real-time synced with {partnerDisplayName}&apos;s Focus
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
