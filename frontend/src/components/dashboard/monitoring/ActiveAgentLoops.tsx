'use client';

import React from 'react';
import { PieChart, Pie, Cell, Legend, Tooltip, ResponsiveContainer } from 'recharts';
import { Zap } from 'lucide-react';

interface LoopData {
  name: string;
  value: number;
  color: string;
}

const ActiveAgentLoops: React.FC = () => {
  const loopsData: LoopData[] = [
    { name: 'Active', value: 14, color: '#10b981' },
    { name: 'Samples', value: 9, color: '#f59e0b' },
    { name: 'Retries', value: 3, color: '#3b82f6' },
  ];

  const totalLoops = loopsData.reduce((sum, item) => sum + item.value, 0);

  return (
    <div className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-lg border border-slate-700 p-6">
      <h2 className="text-lg font-semibold text-cyan-400 flex items-center gap-2 mb-4">
        <Zap className="w-5 h-5" />
        ACTIVE AGENT LOOPS
      </h2>

      <ResponsiveContainer width="100%" height={200}>
        <PieChart>
          <Pie
            data={loopsData}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={90}
            paddingAngle={2}
            dataKey="value"
          >
            {loopsData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              backgroundColor: '#0f172a',
              border: '1px solid #475569',
              borderRadius: '8px',
              color: '#fff'
            }}
          />
        </PieChart>
      </ResponsiveContainer>

      <div className="text-center mt-4">
        <p className="text-3xl font-bold text-white">{totalLoops}</p>
        <p className="text-xs text-slate-400 mt-2">Total Active Loops</p>
      </div>

      <div className="mt-4 space-y-2">
        {loopsData.map((item, idx) => (
          <div key={idx} className="flex items-center justify-between text-xs">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }} />
              <span className="text-slate-300">{item.name}</span>
            </div>
            <span className="font-semibold text-white">{item.value}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ActiveAgentLoops;
