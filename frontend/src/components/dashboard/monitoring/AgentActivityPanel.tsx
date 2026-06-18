'use client';

import React, { useState, useEffect } from 'react';
import { Cpu, Activity } from 'lucide-react';

interface Agent {
  id: string;
  name: string;
  status: 'active' | 'idle' | 'error';
  tasksCompleted: number;
  currentTask?: string;
}

const AgentActivityPanel: React.FC = () => {
  const [agents, setAgents] = useState<Agent[]>([
    {
      id: '1',
      name: 'Research Agent',
      status: 'active',
      tasksCompleted: 1242,
      currentTask: 'Analyzing market trends...'
    },
    {
      id: '2',
      name: 'TaskBot 42',
      status: 'active',
      tasksCompleted: 856,
      currentTask: 'Processing queue...'
    },
    {
      id: '3',
      name: 'Web Crawler AI',
      status: 'active',
      tasksCompleted: 634,
      currentTask: 'Indexing pages...'
    }
  ]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-500/20 text-green-400 border-green-500/30';
      case 'idle':
        return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
      case 'error':
        return 'bg-red-500/20 text-red-400 border-red-500/30';
      default:
        return 'bg-slate-500/20 text-slate-400 border-slate-500/30';
    }
  };

  return (
    <div className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-lg border border-slate-700 p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold text-cyan-400 flex items-center gap-2">
          <Activity className="w-5 h-5" />
          AI AGENT ACTIVITY
        </h2>
        <span className="text-xs text-slate-400">Live</span>
      </div>

      <div className="space-y-3">
        {agents.map((agent) => (
          <div
            key={agent.id}
            className="flex items-center justify-between p-3 bg-slate-800/50 rounded-lg border border-slate-700/50 hover:border-cyan-500/50 transition-all"
          >
            <div className="flex items-center gap-3 flex-1">
              <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
              <div className="flex-1">
                <p className="text-sm font-medium text-slate-200">{agent.name}</p>
                <p className="text-xs text-slate-400">{agent.currentTask}</p>
              </div>
            </div>
            <div
              className={`px-3 py-1 rounded-full border text-xs font-semibold ${getStatusColor(agent.status)}`}
            >
              {agent.status.toUpperCase()}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-4 pt-4 border-t border-slate-700">
        <p className="text-xs text-slate-400">Active Agents: <span className="text-green-400 font-semibold">3/12</span></p>
      </div>
    </div>
  );
};

export default AgentActivityPanel;
