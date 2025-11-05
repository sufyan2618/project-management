import { format, formatDistanceToNow } from 'date-fns';
import clsx from 'clsx';

export const formatDate = (date) => {
  if (!date) return '';
  return format(new Date(date), 'MMM dd, yyyy');
};

export const formatDateTime = (date) => {
  if (!date) return '';
  return format(new Date(date), 'MMM dd, yyyy HH:mm');
};

export const formatRelativeTime = (date) => {
  if (!date) return '';
  return formatDistanceToNow(new Date(date), { addSuffix: true });
};

export const getStatusColor = (status) => {
  const colors = {
    'todo': 'bg-gray-100 text-gray-800',
    'in-progress': 'bg-blue-100 text-blue-800',
    'done': 'bg-green-100 text-green-800',
  };
  return colors[status] || colors.todo;
};

export const getInitials = (name) => {
  if (!name) return '';
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);
};

export const cn = (...classes) => {
  return clsx(...classes);
};

export const truncate = (str, length = 50) => {
  if (!str) return '';
  if (str.length <= length) return str;
  return str.substring(0, length) + '...';
};


export const getErrorMessage = (error, defaultMessage = 'An error occurred') => {
  const detail = error?.response?.data?.detail;
  
  if (!detail) {
    return defaultMessage;
  }
  
  if (Array.isArray(detail)) {
    const firstError = detail[0];
    if (firstError?.msg) {
      let message = firstError.msg;
      
      if (message.startsWith('Value error, ')) {
        message = message.replace('Value error, ', '');
      }
      
      return message;
    }
    return 'Validation failed. Please check your input.';
  }
  
  if (typeof detail === 'string') {
    return detail;
  }
  

  return defaultMessage;
};

