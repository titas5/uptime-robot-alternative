import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { Activity } from 'lucide-react';
import { useMonitors } from '@/hooks/useMonitors';
import StatusBadge from '@/components/StatusBadge';

export default function Dashboard() {
  const { token, logout } = useAuth();
  const router = useRouter();
  const { monitors, loading } = useMonitors();

  if (!token) return null;

  return (
    <div className="dashboard-layout">
      <header className="header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontWeight: 'bold' }}>
          <Activity color="var(--accent)" /> UptimeMonitor
        </div>
        <div style={{ display: 'flex', gap: '1rem' }}>
          <Link href="/dashboard/new"><button className="btn-primary" style={{ padding: '0.5rem 1rem' }}>+ New Monitor</button></Link>
          <button onClick={logout} style={{ color: 'var(--text-secondary)' }}>Logout</button>
        </div>
      </header>

      <main className="container">
        <h1 className="title">Your Monitors</h1>
        {loading ? (
          <p style={{ color: 'var(--text-secondary)' }}>Loading monitors...</p>
        ) : (
          <div className="monitor-list">
            {monitors.map(m => (
              <div key={m.id} className="monitor-card" onClick={() => router.push(`/dashboard/${m.id}`)}>
                <div className="monitor-header">
                  <span style={{ fontWeight: 600, wordBreak: 'break-all' }}>{m.url.replace(/^https?:\/\//, '')}</span>
                  <StatusBadge status={m.status} />
                </div>
                <div style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>Type: {m.type.toUpperCase()} • Every {m.interval}m</div>
              </div>
            ))}
            {monitors.length === 0 && (
              <p style={{ color: 'var(--text-secondary)' }}>No monitors found. Create one to get started!</p>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
