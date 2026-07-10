interface WebSocketEvent {
  type: string
  agent?: string
  claim?: string
  confidence?: number
  evidence_count?: number
  message?: string
  timestamp: string
  [key: string]: any
}

interface AgentFeedProps {
  events: WebSocketEvent[]
}

export default function AgentFeed({ events }: AgentFeedProps) {
  const getEventIcon = (type: string) => {
    switch (type) {
      case 'run_started':
        return '🚀'
      case 'agent_started':
        return '🤖'
      case 'evidence_found':
        return '🔍'
      case 'agent_completed':
        return '✅'
      case 'synthesis_started':
        return '📝'
      case 'run_completed':
        return '🎉'
      case 'agent_failed':
      case 'run_failed':
        return '❌'
      default:
        return '•'
    }
  }

  const getEventColor = (type: string) => {
    switch (type) {
      case 'run_started':
      case 'run_completed':
        return 'border-green-500 bg-green-50'
      case 'agent_started':
        return 'border-blue-500 bg-blue-50'
      case 'evidence_found':
        return 'border-purple-500 bg-purple-50'
      case 'agent_completed':
        return 'border-green-500 bg-green-50'
      case 'synthesis_started':
        return 'border-yellow-500 bg-yellow-50'
      case 'agent_failed':
      case 'run_failed':
        return 'border-red-500 bg-red-50'
      default:
        return 'border-gray-300 bg-white'
    }
  }

  const formatEventMessage = (event: WebSocketEvent) => {
    switch (event.type) {
      case 'connected':
        return event.message || 'Connected to research stream'
      case 'run_started':
        return `Research started for ${event.company_name}`
      case 'agent_started':
        return `${event.agent} started`
      case 'evidence_found':
        return event.claim || 'Evidence found'
      case 'agent_completed':
        return `${event.agent} completed (${event.evidence_count} evidence)`
      case 'synthesis_started':
        return 'Synthesizing narrative from evidence...'
      case 'synthesis_completed':
        return 'Narrative synthesis complete'
      case 'run_completed':
        return `Research complete: ${event.total_evidence} total evidence`
      case 'agent_failed':
        return `${event.agent} failed: ${event.error}`
      case 'run_failed':
        return `Research failed: ${event.error}`
      default:
        return event.type
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold">Live Agent Activity</h2>
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-sm text-gray-600">{events.length} events</span>
        </div>
      </div>

      <div className="space-y-2 max-h-[600px] overflow-y-auto">
        {events.map((event, i) => (
          <div
            key={i}
            className={`flex items-start gap-3 p-3 rounded border-l-4 ${getEventColor(event.type)} transition-all duration-200 hover:shadow-sm`}
          >
            <span className="text-xl flex-shrink-0">{getEventIcon(event.type)}</span>

            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                {event.agent && (
                  <span className="font-medium text-sm text-gray-900 capitalize">
                    {event.agent.replace('_', ' ')}
                  </span>
                )}
                <span className="text-xs text-gray-500">
                  {event.type.replace('_', ' ')}
                </span>
              </div>

              <p className="text-sm text-gray-700 break-words">
                {formatEventMessage(event)}
              </p>

              {event.confidence !== undefined && (
                <div className="mt-1">
                  <span className="text-xs text-gray-600">
                    Confidence: {(event.confidence * 100).toFixed(0)}%
                  </span>
                </div>
              )}
            </div>

            <span className="text-xs text-gray-400 flex-shrink-0">
              {new Date(event.timestamp).toLocaleTimeString()}
            </span>
          </div>
        ))}

        {events.length === 0 && (
          <div className="text-center py-12">
            <div className="text-4xl mb-3">⏳</div>
            <p className="text-gray-500">Waiting for agents to start...</p>
            <p className="text-xs text-gray-400 mt-1">
              Live updates will appear here
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
