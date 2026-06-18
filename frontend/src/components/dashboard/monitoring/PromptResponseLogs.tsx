'use client';

import React from 'react';
import { MessageSquare, ChevronDown } from 'lucide-react';

interface LogEntry {
  id: string;
  prompt: string;
  response: string;
  tool: string;
  result: string;
  status: 'success' | 'error';
}

const PromptResponseLogs: React.FC = () => {
  const logs: LogEntry[] = [
    {
      id: '1',
      prompt: 'Gather market research on AI trends',
      response: 'Compiling report...',
      tool: 'Web Search result retrieved',
      result: 'Summary generated',
      status: 'success'
    },
    {
      id: '2',
      prompt: 'Analyze competitor pricing',
      response: 'Processing data...',
      tool: 'Database Query',
      result: 'Analysis complete',
      status: 'success'
    }
  ];

  const [expandedId, setExpandedId] = React.useState<string | null>(null);

  return (
    <div className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-lg border border-slate-700 p-6">
      <h2 className="text-lg font-semibold text-cyan-400 flex items-center gap-2 mb-4">
        <MessageSquare className="w-5 h-5" />
        PROMPT & RESPONSE LOGS
      </h2>

      <div className="space-y-2 max-h-96 overflow-y-auto">
        {logs.map((log) => (
          <div
            key={log.id}
            className="bg-slate-800/50 rounded-lg border border-slate-700/50 overflow-hidden"
          >
            <button
              onClick={() => setExpandedId(expandedId === log.id ? null : log.id)}
              className="w-full p-3 flex items-start justify-between hover:bg-slate-700/30 transition-colors"
            >
              <div className="text-left flex-1">
                <p className="text-xs font-medium text-cyan-400 truncate">💬 Prompt</p>
                <p className="text-xs text-slate-400 mt-1 line-clamp-2">{log.prompt}</p>
              </div>
              <ChevronDown
                className={`w-4 h-4 text-slate-400 transition-transform ${expandedId === log.id ? 'rotate-180' : ''}`}
              />
            </button>

            {expandedId === log.id && (
              <div className="border-t border-slate-700/50 p-3 space-y-2 bg-slate-800/20">
                <div>
                  <p className="text-xs text-slate-400 font-semibold">Response:</p>
                  <p className="text-xs text-slate-300 mt-1">{log.response}</p>
                </div>
                <div>
                  <p className="text-xs text-slate-400 font-semibold">Tool:</p>
                  <p className="text-xs text-slate-300 mt-1">{log.tool}</p>
                </div>
                <div>
                  <p className="text-xs text-slate-400 font-semibold">Result:</p>
                  <p className="text-xs text-slate-300 mt-1">{log.result}</p>
                </div>
                <div className="flex items-center gap-2 mt-2 pt-2 border-t border-slate-700/50">
                  <div
                    className={`w-2 h-2 rounded-full ${log.status === 'success' ? 'bg-green-500' : 'bg-red-500'}`}
                  />
                  <span className={`text-xs font-semibold ${log.status === 'success' ? 'text-green-400' : 'text-red-400'}`}>
                    {log.status.toUpperCase()}
                  </span>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default PromptResponseLogs;
