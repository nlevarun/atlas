'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function Home() {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const router = useRouter()

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const res = await fetch('http://localhost:8000/api/research/company', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ company_name: query })
      })

      if (!res.ok) {
        throw new Error('Failed to start research')
      }

      const data = await res.json()
      router.push(`/dossier/${data.run_id}`)
    } catch (err) {
      console.error(err)
      setError('Failed to start research. Please try again.')
      setLoading(false)
    }
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gradient-to-b from-gray-50 to-gray-100">
      <div className="text-center mb-12">
        <h1 className="text-6xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600">
          Atlas
        </h1>
        <p className="text-xl text-gray-600">
          AI Operating System for Company Intelligence
        </p>
        <p className="text-sm text-gray-500 mt-2">
          Evidence-backed research powered by specialized agents
        </p>
      </div>

      <form onSubmit={handleSearch} className="w-full max-w-2xl">
        <div className="bg-white rounded-2xl shadow-xl p-8">
          <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-3">
            Research Company
          </label>
          <input
            id="search"
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Enter company name or ticker (e.g., Anthropic, TSLA)"
            className="w-full px-6 py-4 border-2 border-gray-300 rounded-lg text-lg focus:outline-none focus:border-blue-500 transition-colors"
            disabled={loading}
          />

          {error && (
            <div className="mt-3 text-red-600 text-sm">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading || !query.trim()}
            className="mt-6 w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-4 rounded-lg hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium text-lg transition-all shadow-lg hover:shadow-xl"
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Starting Research...
              </span>
            ) : (
              'Start Research'
            )}
          </button>
        </div>
      </form>

      <div className="mt-12 text-center text-sm text-gray-500">
        <p className="mb-2">Phase 0: Scaffold Implementation</p>
        <p>Proving the pipeline end-to-end with dummy agent</p>
      </div>
    </main>
  )
}
