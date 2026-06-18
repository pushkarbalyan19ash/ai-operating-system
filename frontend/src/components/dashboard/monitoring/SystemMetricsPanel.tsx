'use client';

import React from 'react';
import { Activity } from 'lucide-react';

interface MetricGauge {
  label: string;
  value: number;
  color: string;
}

const SystemMetricsPanel: React.FC = () => {
  const metrics: MetricGauge[] = [
    { label: 'CPU', value: 62, color: 'from-blue-500 to-blue-600' },
    { label: 'RAM', value: 75, color: 'from-purple-500 to-purple-600' },
    { label: 'GPU', value: 48, color: 'from-cyan-500 to-cyan-600' },
  ];

  return (
    <div className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-lg border border-slate-700 p-6">
      <h2 className="text-lg font-semibold text-cyan-400 flex items-center gap-2 mb-4">
        <Activity className="w-5 h-5" />
        SYSTEM RESOURCES
      </h2>

      <div className="space-y-4">
        {metrics.map((metric, idx) => (
          <div key={idx}>
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium text-slate-300">{metric.label}</span>
              <span className="text-sm font-bold text-white">{metric.value}%</span>
            </div>
            <div className="w-full bg-slate-700/50 rounded-full h-2 overflow-hidden">
              <div
                className={`h-full rounded-full bg-gradient-to-r ${metric.color} transition-all duration-300`}
                style={{ width: `${metric.value}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SystemMetricsPanel;
