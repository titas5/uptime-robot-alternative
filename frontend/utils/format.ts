export const formatResponseTime = (time: number | null | undefined): string => {
  if (time == null) return '0ms';
  return `${Math.round(time)}ms`;
};

export const formatDateTime = (dateString: string): string => {
  if (!dateString) return '';
  return new Date(dateString).toLocaleString([], {
    month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit'
  });
};
