'use client';

import React, { useEffect, useState } from 'react';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { AlertCircle, TrendingUp, Clock, Zap, AlertTriangle, Activity } from 'lucide-react';
import AgentActivityPanel from './monitoring/AgentActivityPanel';
import TaskTimelineVisualization from './monitoring/TaskTimelineVisualization';
import CostAnalysisPanel from './monitoring/CostAnalysisPanel';
import SystemMetricsPanel from './monitoring/SystemMetricsPanel';
import AlertsPanel from './monitoring/AlertsPanel';
import PromptResponseLogs from './monitoring/PromptResponseLogs';
import ActiveAgentLoops from './monitoring/ActiveAgentLoops';

interface MetricCard {
  title: string;
  value: string;
  unit?: string;
  trend?: 'up' | 'down' | 'stable';
  icon: React.ReactNode;
  color: string;
}

const MonitoringDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<MetricCard[]>([
    {
      title: 'SUCCESS RATE',
      value: '92',
      unit: '%',
      trend: 'up',
      icon: <TrendingUp className="w-6 h-6" />,
      color: 'from-green-500 to-green-600'
    },
    {
      title: 'AVG EXECUTION TIME',
      value: '14.3',
      unit: 's',
      trend: 'stable',
      icon: <Clock className="w-6 h-6" />,
      color: 'from-blue-500 to-blue-600'
    },
    {
      title: 'TOKEN USAGE',
      value: '3.8K',
      unit: 'task',
      trend: 'up',
      icon: <Zap className="w-6 h-6" />,
      color: 'from-cyan-500 to-cyan-600'
    },
    {
      title: 'ERRORS',
      value: '5.2',
      unit: '%',
      trend: 'down',
      icon: <AlertCircle className="w-6 h-6" />,
      color: 'from-orange-500 to-orange-600'
    }
  ]);

  const [systemMetrics, setSystemMetrics] = useState([
    { time: '10h', cpu: 45, memory: 62, gpu: 38 },
    { time: '11h', cpu: 52, memory: 68, gpu: 42 },
    { time: '12h', cpu: 48, memory: 65, gpu: 40 },
    { time: '1p', cpu: 61, memory: 72, gpu: 55 },
    { time: '2p', cpu: 55, memory: 70, gpu: 48 },
    { time: '3p', cpu: 58, memory: 75, gpu: 52 },
  ]);

  useEffect(() => {
    // Simulate real-time updates
    const interval = setInterval(() => {
      setSystemMetrics(prev => {
        const newData = [...prev.slice(1)];
        newData.push({
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          cpu: Math.random() * 80 + 20,
          memory: Math.random() * 60 + 40,
          gpu: Math.random() * 70 + 20
        });
        return newData;
      });
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6 overflow-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent mb-2">
          Monitoring Autonomous AI Agents
        </h1>
        <p className="text-slate-400">Real-time agent performance and system metrics</p>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {metrics.map((metric, idx) => (
          <div
            key={idx}
            className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-lg border border-slate-700 p-6 hover:border-cyan-500 transition-all duration-300"
          >
            <div className="flex justify-between items-start mb-4">
              <div className={`text-sm font-semibold text-slate-300 flex items-center gap-2`}>
                <span>{metric.icon}</span>
                {metric.title}
              </div>
              {metric.trend === 'up' && <span className="text-green-400 text-xs">↑</span>}
              {metric.trend === 'down' && <span className="text-red-400 text-xs">↓</span>}
            </div>
            <div className="flex items-baseline gap-2">
              <span className={`text-3xl font-bold bg-gradient-to-r ${metric.color} bg-clip-text text-transparent`}>
                {metric.value}
              </span>
              {metric.unit && <span className="text-sm text-slate-400">{metric.unit}</span>}
            </div>
          </div>
        ))}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        {/* Left Column */}
        <div className="lg:col-span-1 space-y-6">
          {/* Agent Activity */}
          <AgentActivityPanel />

          {/* Cost Analysis */}
          <CostAnalysisPanel />
        </div>

        {/* Center Column */}
        <div className="lg:col-span-2 space-y-6">
          {/* Task Timeline */}
          <TaskTimelineVisualization />

          {/* System Metrics */}
          <div className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-lg border border-slate-700 p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold text-cyan-400 flex items-center gap-2">
                <Activity className="w-5 h-5" />
                SYSTEM METRICS
              </h2>
              <span className="text-xs text-slate-400">Last 24 hours</span>
            </div>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={systemMetrics}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="time" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0f172a',
                    border: '1px solid #475569',
                    borderRadius: '8px',
                    color: '#fff'
                  }}
                />
                <Legend />
                <Line type="monotone" dataKey="cpu" stroke="#3b82f6" strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="memory" stroke="#a855f7" strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="gpu" stroke="#06b6d4" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Bottom Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Alerts */}
        <AlertsPanel />

        {/* Active Agent Loops */}
        <ActiveAgentLoops />

        {/* Prompt & Response Logs */}
        <PromptResponseLogs />
      </div>
    </div>
  );
};

export default MonitoringDashboard;
