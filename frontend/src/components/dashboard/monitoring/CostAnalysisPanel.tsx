'use client';

import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { DollarSign } from 'lucide-react';

const CostAnalysisPanel: React.FC = () => {
  const costData = [
    { period: 'Sat', cost: 45 },
    { period: 'Sun', cost: 52 },
    { period: 'Mon', cost: 38 },
    { period: 'Tue', cost: 61 },
    { period: 'Wed', cost: 55 },
    { period: 'Thu', cost: 67 },
    { period: 'Fri', cost: 48 },
  ];

  return (
    <div className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-lg border border-slate-700 p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold text-cyan-400 flex items-center gap-2">
          <DollarSign className="w-5 h-5" />
          COST ANALYSIS
        </h2>
        <span className="text-xs text-slate-400">Weekly breakdown</span>
      </div>

      <div className="mb-6">
        <p className="text-4xl font-bold text-white mb-2">$782</p>
        <p className="text-xs text-slate-400">This week • <span className="text-red-400">+8.3% vs last week</span></p>
      </div>

      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={costData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="period" stroke="#94a3b8" style={{ fontSize: '12px' }} />
          <YAxis stroke="#94a3b8" style={{ fontSize: '12px' }} />
          <Tooltip
            contentStyle={{
              backgroundColor: '#0f172a',
              border: '1px solid #475569',
              borderRadius: '8px',
              color: '#fff'
            }}
            formatter={(value) => [`$${value}`, 'Cost']}
          />
          <Line
            type="monotone"
            dataKey="cost"
            stroke="#06b6d4"
            strokeWidth={2}
            dot={false}
            isAnimationActive={true}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default CostAnalysisPanel;
