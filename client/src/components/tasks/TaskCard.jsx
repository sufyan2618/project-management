import { FiCalendar, FiUser } from 'react-icons/fi';
import Card from '../ui/Card';
import Badge from '../ui/Badge';
import { formatDate } from '../../utils/helpers';

const TaskCard = ({ task, onClick }) => {
  return (
    <Card hover onClick={() => onClick && onClick(task)} className="cursor-pointer">
      <div className="flex items-start justify-between mb-3">
        <h4 className="font-semibold text-gray-900">{task.title}</h4>
        <Badge status={task.status}>
          {task.status.replace('-', ' ')}
        </Badge>
      </div>

      {task.description && (
        <p className="text-sm text-gray-600 mb-4 line-clamp-2">
          {task.description}
        </p>
      )}

      <div className="flex items-center gap-4 text-sm text-gray-500">
        {task.due_date && (
          <div className="flex items-center gap-1">
            <FiCalendar className="h-4 w-4" />
            {formatDate(task.due_date)}
          </div>
        )}
        <div className="flex items-center gap-1">
          <FiUser className="h-4 w-4" />
          Assigned
        </div>
      </div>
    </Card>
  );
};

export default TaskCard;

