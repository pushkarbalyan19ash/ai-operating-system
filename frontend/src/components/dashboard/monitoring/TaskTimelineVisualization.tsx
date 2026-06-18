'use client';

import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';
import { Clock } from 'lucide-react';

const TaskTimelineVisualization: React.FC = () => {
  const taskData = [
    { phase: 'Start', duration: 0.2, color: '#ef4444' },
    { phase: 'API Call', duration: 2.1, color: '#3b82f6' },
    { phase: 'Processing', duration: 4.5, color: '#10b981' },
    { phase: 'LLM Response', duration: 3.2, color: '#10b981' },
    { phase: 'Completed', duration: 1.8, color: '#f97316' },
  ];

  return (
    <div className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-lg border border-slate-700 p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold text-cyan-400 flex items-center gap-2">
          <Clock className="w-5 h-5" />
          TASK EXECUTION TIMELINE
        </h2>
        <span className="text-xs text-slate-400">8 hours</span>
      </div>

      <div className="space-y-4">
        {/* Phase Breakdown */}
        <div className="space-y-2">
          {taskData.map((item, idx) => (
            <div key={idx} className="flex items-center gap-3">
              <div className="w-24">
                <p className="text-xs font-medium text-slate-400">{item.phase}</p>
              </div>
              <div className="flex-1 bg-slate-700 rounded-full h-6 overflow-hidden relative">
                <div
                  className="h-full rounded-full flex items-center justify-center text-xs font-semibold text-white"
                  style={{
                    width: `${(item.duration / 11.8) * 100}%`,
                    backgroundColor: item.color,
                  }}
                >
                  {item.duration}s
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Timeline Bar */}
        <div className="mt-6 p-4 bg-slate-800/50 rounded-lg border border-slate-700/50">
          <p className="text-xs text-slate-400 mb-3">Timeline Visualization (5 hours - 8.25am)</p>
          <div className="flex items-center gap-2 text-xs text-slate-400">
            <span>Start</span>
            <div className="flex-1 h-2 bg-gradient-to-r from-red-500 via-blue-500 via-green-500 to-orange-500 rounded-full" />
            <span>8.25am</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TaskTimelineVisualization;
