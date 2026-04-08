import React from 'react';

export default function StatusBadge({ status }: { status: string }) {
  return (
    <span className={`badge ${status.toLowerCase()}`}>
      {status.toUpperCase()}
    </span>
  );
}
