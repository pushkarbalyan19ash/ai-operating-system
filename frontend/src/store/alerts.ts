'use client';

import { create } from 'zustand';

interface AlertItem {
  id: string;
  alert_type: 'error' | 'warning' | 'info';
  message: string;
  timestamp: string;
  severity: string;
  metadata?: any;
}

interface AlertsState {
  alerts: AlertItem[];
  addAlerts: (alerts: AlertItem[]) => void;
  clearAlerts: () => void;
  removeAlert: (id: string) => void;
}

export const useAlertsStore = create<AlertsState>((set) => ({
  alerts: [],
  
  addAlerts: (alerts: AlertItem[]) => set({ alerts }),
  
  clearAlerts: () => set({ alerts: [] }),
  
  removeAlert: (id: string) =>
    set((state) => ({
      alerts: state.alerts.filter((alert) => alert.id !== id)
    }))
}));
