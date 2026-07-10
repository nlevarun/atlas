'use client'

import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import AgentFeed from '@/components/AgentFeed'
import Link from 'next/link'

interface RunStatus {
  run_id: string
  company_name: string
  status: string
  started_at: string
  agent_count: number
  evidence_count: number
}

interface WebSocketEvent {
  type: string
  agent?: string
  claim?: string
  confidence?: number
  evidence_count?: number
  timestamp: string
  [key: string]: any
}

export default function DossierPage() {
  const params = useParams()
  const runId = params.runId as string

  const [wsStatus, setWsStatus] = useState('connecting')
  const [events, setEvents] = useState<WebSocketEvent[]>([])
  const [runStatus, setRunStatus] = useState<RunStatus | null>(null)
  const [report, setReport] = useState<any>(null)

  // Fetch initial status
  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const res = await fetch(`http://localhost:8000/api/research/${runId}/status`)
        if (res.ok) {
          const data = await res.json()
          setRunStatus(data)
        }
      } catch (err) {
        console.error('Failed to fetch status:', err)
      }
    }

    fetchStatus()
    const interval = setInterval(fetchStatus, 2000)
    return () => clearInterval(interval)
  }, [runId])

  // Fetch report when completed
  useEffect(() => {
    if (runStatus?.status === 'completed') {
      const fetchReport = async () => {
        try {
          const res = await fetch(`http://localhost:8000/api/research/${runId}/report`)
          if (res.ok) {
            const data = await res.json()
            setReport(data)
          }
        } catch (err) {
          console.error('Failed to fetch report:', err)
        }
      }
      fetchReport()
    }
  }, [runStatus?.status, runId])

  // WebSocket connection
  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/research/${runId}`)

    ws.onopen = () => {
      setWsStatus('connected')
      console.log('WebSocket connected')
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        console.log('WebSocket event:', data)
        setEvents(prev => [...prev, data])
      } catch (err) {
        console.error('Failed to parse WebSocket message:', err)
      }
    }

    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
      setWsStatus('error')
    }

    ws.onclose = () => {
      console.log('WebSocket closed')
      setWsStatus('disconnected')
    }

    return () => {
      ws.close()
    }
  }, [runId])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'connected': return 'text-green-600'
      case 'connecting': return 'text-yellow-600'
      case 'error': return 'text-red-600'
      case 'disconnected': return 'text-gray-600'
      default: return 'text-gray-600'
    }
  }

  const getStatusBadgeColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-green-100 text-green-800'
      case 'running_agents': return 'bg-blue-100 text-blue-800'
      case 'synthesizing': return 'bg-purple-100 text-purple-800'
      case 'failed': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b">
        <div className="container mx-auto px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <Link href="/" className="text-blue-600 hover:underline text-sm mb-2 block">
                ← Back to Search
              </Link>
              <h1 className="text-3xl font-bold">
                {runStatus?.company_name || 'Loading...'}
              </h1>
              <p className="text-gray-600 text-sm mt-1">
                Research Run: {runId.slice(0, 8)}
              </p>
            </div>

            <div className="text-right">
              {runStatus && (
                <div className="space-y-2">
                  <div className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${getStatusBadgeColor(runStatus.status)}`}>
                    {runStatus.status}
                  </div>
                  <div className="text-sm text-gray-600">
                    <div>{runStatus.agent_count} agents • {runStatus.evidence_count} evidence</div>
                    <div className={`${getStatusColor(wsStatus)} font-medium`}>
                      Stream: {wsStatus}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="container mx-auto px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Live Feed */}
          <div>
            <AgentFeed events={events} />
          </div>

          {/* Report Preview */}
          <div>
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold mb-4">Research Report</h2>

              {report ? (
                <div className="space-y-6">
                  {report.agent_reports?.map((agentReport: any, idx: number) => (
                    <div key={idx} className="border-l-4 border-blue-500 pl-4">
                      <h3 className="font-semibold text-lg capitalize mb-2">
                        {agentReport.agent.replace('_', ' ')}
                      </h3>
                      <p className="text-gray-700 mb-3">{agentReport.summary}</p>

                      <div className="space-y-2">
                        {agentReport.evidence?.map((evidence: any, eIdx: number) => (
                          <div key={eIdx} className="bg-gray-50 rounded p-3 text-sm">
                            <div className="flex items-start justify-between mb-1">
                              <span className="font-medium text-gray-900">{evidence.claim}</span>
                              <span className="text-xs text-gray-500 ml-2">
                                {(evidence.confidence * 100).toFixed(0)}%
                              </span>
                            </div>
                            <div className="text-xs text-gray-600 italic mt-1">
                              "{evidence.raw_excerpt.slice(0, 150)}..."
                            </div>
                            {evidence.source_url && (
                              <a
                                href={evidence.source_url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-xs text-blue-600 hover:underline mt-1 block"
                              >
                                {evidence.source_type} →
                              </a>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              ) : runStatus?.status === 'completed' ? (
                <p className="text-gray-600">Loading report...</p>
              ) : (
                <div className="text-center py-12">
                  <div className="animate-pulse">
                    <div className="w-16 h-16 bg-blue-100 rounded-full mx-auto mb-4"></div>
                    <p className="text-gray-600">Research in progress...</p>
                    <p className="text-sm text-gray-500 mt-2">
                      Agents are gathering evidence
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
