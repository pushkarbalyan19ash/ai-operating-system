'use client';

import { create } from 'zustand';

interface Metric {
  success_rate: number;
  avg_execution_time: number;
  total_tokens_used: number;
  error_rate: number;
  active_agents: number;
  system_metrics?: any;
  cost_analysis?: any;
}

interface MonitoringState {
  metrics: Metric | null;
  setMetrics: (metrics: Metric) => void;
  updateMetric: (key: keyof Metric, value: any) => void;
}

export const useMonitoringStore = create<MonitoringState>((set) => ({
  metrics: null,
  
  setMetrics: (metrics: Metric) => set({ metrics }),
  
  updateMetric: (key: keyof Metric, value: any) =>
    set((state) => ({
      metrics: state.metrics ? { ...state.metrics, [key]: value } : null
    }))
}));
