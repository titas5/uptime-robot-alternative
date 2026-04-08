import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import api from '@/services/api';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function MonitorDetail() {
  const router = useRouter();
  const { id } = router.query;
  const [monitor, setMonitor] = useState<any>(null);
  const [logs, setLogs] = useState<any[]>([]);
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    if (!id) return;
    const fetchData = async () => {
      try {
        const [monRes, logsRes, statsRes] = await Promise.all([
          api.get(`/monitors/`),
          api.get(`/monitors/${id}/logs`),
          api.get(`/monitors/${id}/stats`)
        ]);
        const m = monRes.data.find((x: any) => x.id === Number(id));
        setMonitor(m);
        // Reverse logs so chronologically Left->Right for charting
        setLogs([...logsRes.data].reverse());
        setStats(statsRes.data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchData();
  }, [id]);

  if (!monitor) return <div className="container">Loading...</div>;

  const chartData = logs.map(l => ({
    time: new Date(l.checked_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    response_time: l.response_time || 0
  }));

  const timelineLogs = [...logs].reverse().slice(0, 50);

  return (
    <div className="container">
      <div style={{ marginBottom: '2rem' }}>
        <Link href="/dashboard" style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', color: 'var(--text-secondary)' }}>
          <ArrowLeft size={16} /> Back to Dashboard
        </Link>
      </div>

      <div className="card" style={{ marginBottom: '2rem' }}>
        <div className="monitor-header">
          <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{monitor.url}</h1>
          <span className={`badge ${monitor.status}`}>{monitor.status}</span>
        </div>
        
        <div className="monitor-stats">
          <div className="stat-item">
            <span className="stat-label">24h Uptime</span>
            <span className="stat-value">{stats?.uptime_24h}%</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">7d Uptime</span>
            <span className="stat-value">{stats?.uptime_7d}%</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">30d Uptime</span>
            <span className="stat-value">{stats?.uptime_30d}%</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Interval</span>
            <span className="stat-value">{monitor.interval}m</span>
          </div>
        </div>
      </div>

      <h2 style={{ marginBottom: '1rem' }}>Response Time</h2>
      <div className="card" style={{ height: '300px', marginBottom: '2rem' }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
            <XAxis dataKey="time" stroke="var(--text-secondary)" />
            <YAxis stroke="var(--text-secondary)" />
            <Tooltip contentStyle={{ backgroundColor: 'var(--bg-secondary)', border: '1px solid var(--border)' }} />
            <Line type="monotone" dataKey="response_time" stroke="var(--accent)" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <h2 style={{ marginBottom: '1rem' }}>Recent Event Logs</h2>
      <div className="card" style={{ padding: '0', overflow: 'hidden' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ background: 'rgba(0,0,0,0.2)', textAlign: 'left' }}>
              <th style={{ padding: '1rem' }}>Status</th>
              <th style={{ padding: '1rem' }}>Response Time</th>
              <th style={{ padding: '1rem' }}>Date & Time</th>
            </tr>
          </thead>
          <tbody>
            {timelineLogs.map((log: any) => (
              <tr key={log.id} style={{ borderTop: '1px solid var(--border)' }}>
                <td style={{ padding: '1rem' }}>
                  <span className={`badge ${log.status}`}>{log.status}</span>
                </td>
                <td style={{ padding: '1rem' }}>{Math.round(log.response_time || 0)}ms</td>
                <td style={{ padding: '1rem', color: 'var(--text-secondary)' }}>
                  {new Date(log.checked_at).toLocaleString()}
                </td>
              </tr>
            ))}
            {timelineLogs.length === 0 && (
              <tr>
                <td colSpan={3} style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
                  No logs available yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
