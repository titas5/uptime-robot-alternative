import { useState } from 'react';
import api from '@/services/api';
import { useRouter } from 'next/router';
import Link from 'next/link';

export default function NewMonitor() {
  const router = useRouter();
  const [url, setUrl] = useState('https://');
  const [type, setType] = useState('http');
  const [interval, setInterval] = useState(5);
  const [keyword, setKeyword] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post('/monitors/', { url, type, interval, keyword: keyword || null });
      router.push('/dashboard');
    } catch (err) {
      alert('Failed to create monitor');
    }
  };

  return (
    <div className="container" style={{ maxWidth: '600px', marginTop: '2rem' }}>
      <div className="card">
        <h1 className="title" style={{ fontSize: '1.5rem' }}>Create Monitor</h1>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Monitor Type</label>
            <select value={type} onChange={e => setType(e.target.value)}>
              <option value="http">HTTP(S)</option>
              <option value="ping">Ping</option>
              <option value="keyword">Keyword</option>
            </select>
          </div>
          <div className="form-group">
            <label>Target URL / IP</label>
            <input type="text" value={url} onChange={e => setUrl(e.target.value)} required />
          </div>
          {type === 'keyword' && (
            <div className="form-group">
              <label>Keyword to Search</label>
              <input type="text" value={keyword} onChange={e => setKeyword(e.target.value)} required />
            </div>
          )}
          <div className="form-group">
            <label>Interval (minutes)</label>
            <input type="number" value={interval} onChange={e => setInterval(Number(e.target.value))} min={1} max={60} />
          </div>
          
          <div style={{ display: 'flex', gap: '1rem', marginTop: '2rem' }}>
            <button type="submit" className="btn-primary">Create</button>
            <Link href="/dashboard" style={{ paddingTop: '0.75rem', color: 'var(--text-secondary)' }}>Cancel</Link>
          </div>
        </form>
      </div>
    </div>
  );
}
