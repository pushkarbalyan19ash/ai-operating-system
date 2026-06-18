'use client';

import { useEffect, useState, useCallback, useRef } from 'react';
import { useMonitoringStore } from '@/store/monitoring';
import { useAlertsStore } from '@/store/alerts';

interface WebSocketMessage {
  channel: string;
  timestamp: string;
  data: any;
}

export const useMonitoringWebSocket = (clientId: string) => {
  const [isConnected, setIsConnected] = useState(false);
  const [reconnectAttempts, setReconnectAttempts] = useState(0);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>();
  
  const { setMetrics } = useMonitoringStore();
  const { addAlerts, clearAlerts } = useAlertsStore();

  const MAX_RECONNECT_ATTEMPTS = 5;
  const RECONNECT_DELAY = 3000;
  const WS_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8001';

  // Connect to WebSocket
  const connect = useCallback(() => {
    try {
      const ws = new WebSocket(`${WS_URL}/api/ws/monitoring/${clientId}`);

      ws.onopen = () => {
        console.log('WebSocket connected');
        setIsConnected(true);
        setReconnectAttempts(0);
        
        // Subscribe to channels
        ws.send(JSON.stringify({
          action: 'subscribe',
          channel: 'metrics'
        }));
        ws.send(JSON.stringify({
          action: 'subscribe',
          channel: 'alerts'
        }));
      };

      ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data);
          handleMessage(message);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        setIsConnected(false);
      };

      ws.onclose = () => {
        console.log('WebSocket disconnected');
        setIsConnected(false);
        attemptReconnect();
      };

      wsRef.current = ws;
    } catch (error) {
      console.error('Error establishing WebSocket connection:', error);
      attemptReconnect();
    }
  }, [clientId]);

  // Handle incoming messages
  const handleMessage = useCallback((message: WebSocketMessage) => {
    switch (message.channel) {
      case 'metrics':
        setMetrics(message.data);
        break;
      case 'alerts':
        clearAlerts();
        addAlerts(message.data.alerts);
        break;
      case 'subscription':
        console.log('Subscription status:', message.data);
        break;
      default:
        console.log('Unknown message channel:', message.channel);
    }
  }, [setMetrics, addAlerts, clearAlerts]);

  // Attempt to reconnect with exponential backoff
  const attemptReconnect = useCallback(() => {
    if (reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
      const delay = RECONNECT_DELAY * Math.pow(2, reconnectAttempts);
      console.log(`Reconnecting in ${delay}ms... (Attempt ${reconnectAttempts + 1}/${MAX_RECONNECT_ATTEMPTS})`);
      
      reconnectTimeoutRef.current = setTimeout(() => {
        setReconnectAttempts(prev => prev + 1);
        connect();
      }, delay);
    } else {
      console.error('Max reconnection attempts reached');
    }
  }, [reconnectAttempts, connect]);

  // Subscribe to a channel
  const subscribe = useCallback((channel: string) => {
    if (wsRef.current && isConnected) {
      wsRef.current.send(JSON.stringify({
        action: 'subscribe',
        channel
      }));
    }
  }, [isConnected]);

  // Unsubscribe from a channel
  const unsubscribe = useCallback((channel: string) => {
    if (wsRef.current && isConnected) {
      wsRef.current.send(JSON.stringify({
        action: 'unsubscribe',
        channel
      }));
    }
  }, [isConnected]);

  // Send custom message
  const send = useCallback((data: any) => {
    if (wsRef.current && isConnected) {
      wsRef.current.send(JSON.stringify(data));
    } else {
      console.warn('WebSocket not connected');
    }
  }, [isConnected]);

  // Initialize connection on mount
  useEffect(() => {
    connect();

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [connect]);

  return {
    isConnected,
    subscribe,
    unsubscribe,
    send,
    reconnectAttempts
  };
};
