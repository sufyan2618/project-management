import { Draggable } from '@hello-pangea/dnd';
import { FiCalendar, FiUser, FiEdit2 } from 'react-icons/fi';
import { formatDate } from '../../utils/helpers';
import { cn } from '../../utils/helpers';

const KanbanCard = ({ task, index, onEdit }) => {
  return (
    <Draggable draggableId={task.id.toString()} index={index}>
      {(provided, snapshot) => (
        <div
          ref={provided.innerRef}
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          className={cn(
            'bg-white rounded-lg p-4 mb-3 border border-gray-200 shadow-sm hover:shadow-md transition-shadow cursor-move',
            snapshot.isDragging && 'shadow-lg ring-2 ring-primary-500'
          )}
        >
          <div className="flex items-start justify-between mb-2">
            <h4 className="font-semibold text-gray-900 flex-1 pr-2">
              {task.title}
            </h4>
            <button
              onClick={(e) => {
                e.stopPropagation();
                onEdit(task);
              }}
              className="text-gray-400 hover:text-primary-600 transition-colors p-1"
            >
              <FiEdit2 className="h-4 w-4" />
            </button>
          </div>

          {task.description && (
            <p className="text-sm text-gray-600 mb-3 line-clamp-2">
              {task.description}
            </p>
          )}

          <div className="flex items-center gap-3 text-xs text-gray-500">
            {task.due_date && (
              <div className="flex items-center gap-1">
                <FiCalendar className="h-3 w-3" />
                <span>{formatDate(task.due_date)}</span>
              </div>
            )}
            <div className="flex items-center gap-1">
              <FiUser className="h-3 w-3" />
              <span>Assigned</span>
            </div>
          </div>

          {task.project_id && (
            <div className="mt-2 pt-2 border-t border-gray-100">
              <span className="text-xs text-gray-500">
                Project ID: {task.project_id}
              </span>
            </div>
          )}
        </div>
      )}
    </Draggable>
  );
};

export default KanbanCard;

