import { useState, useEffect } from 'react';
import api from '@/services/api';
import { useAuth } from '@/context/AuthContext';

export interface Monitor {
  id: number;
  url: string;
  type: string;
  status: string;
  interval: number;
}

export function useMonitors() {
  const { token, logout } = useAuth();
  const [monitors, setMonitors] = useState<Monitor[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) {
      setLoading(false);
      return;
    }
    
    const fetchMonitors = async () => {
      try {
        const res = await api.get('/monitors/');
        setMonitors(res.data);
      } catch (e: any) {
        if (e.response?.status === 401) logout();
      } finally {
        setLoading(false);
      }
    };
    
    fetchMonitors();
  }, [token]);

  return { monitors, setMonitors, loading };
}
