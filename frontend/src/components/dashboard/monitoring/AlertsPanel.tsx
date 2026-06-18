'use client';

import React from 'react';
import { AlertTriangle, AlertCircle, TrendingUp } from 'lucide-react';

interface Alert {
  id: string;
  type: 'error' | 'warning' | 'info';
  message: string;
  timestamp: string;
}

const AlertsPanel: React.FC = () => {
  const alerts: Alert[] = [
    {
      id: '1',
      type: 'error',
      message: 'High Error Rate Detected',
      timestamp: '2 mins ago'
    },
    {
      id: '2',
      type: 'warning',
      message: 'Excessive Logging Warning',
      timestamp: '5 mins ago'
    },
    {
      id: '3',
      type: 'error',
      message: 'Cost Threshold Exceeded',
      timestamp: '12 mins ago'
    }
  ];

  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'error':
        return <AlertCircle className="w-5 h-5" />;
      case 'warning':
        return <AlertTriangle className="w-5 h-5" />;
      case 'info':
        return <TrendingUp className="w-5 h-5" />;
      default:
        return null;
    }
  };

  const getAlertColor = (type: string) => {
    switch (type) {
      case 'error':
        return 'bg-red-500/20 text-red-400 border-red-500/30';
      case 'warning':
        return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
      case 'info':
        return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
      default:
        return 'bg-slate-500/20 text-slate-400 border-slate-500/30';
    }
  };

  return (
    <div className="bg-gradient-to-br from-slate-900 to-slate-800 rounded-lg border border-slate-700 p-6">
      <h2 className="text-lg font-semibold text-cyan-400 flex items-center gap-2 mb-4">
        <AlertTriangle className="w-5 h-5" />
        ALERTS
      </h2>

      <div className="space-y-3">
        {alerts.map((alert) => (
          <div
            key={alert.id}
            className={`flex items-start gap-3 p-3 rounded-lg border ${getAlertColor(alert.type)}`}
          >
            <div className="mt-0.5">{getAlertIcon(alert.type)}</div>
            <div className="flex-1">
              <p className="text-sm font-medium">{alert.message}</p>
              <p className="text-xs opacity-70 mt-1">{alert.timestamp}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AlertsPanel;
