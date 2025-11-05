import { Droppable } from '@hello-pangea/dnd';
import { cn } from '../../utils/helpers';
import KanbanCard from './KanbanCard';

const statusConfig = {
  'todo': {
    title: 'To Do',
    bgColor: 'bg-gray-50',
    borderColor: 'border-gray-200',
    textColor: 'text-gray-700',
    badgeColor: 'bg-gray-100',
  },
  'in-progress': {
    title: 'In Progress',
    bgColor: 'bg-blue-50',
    borderColor: 'border-blue-200',
    textColor: 'text-blue-700',
    badgeColor: 'bg-blue-100',
  },
  'done': {
    title: 'Done',
    bgColor: 'bg-green-50',
    borderColor: 'border-green-200',
    textColor: 'text-green-700',
    badgeColor: 'bg-green-100',
  },
};

const KanbanColumn = ({ status, tasks, onEdit }) => {
  const config = statusConfig[status] || statusConfig['todo'];

  return (
    <div className="flex-1 min-w-[300px]">
      <div className={cn('rounded-lg border-2', config.borderColor, config.bgColor)}>
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h3 className={cn('font-semibold text-lg', config.textColor)}>
              {config.title}
            </h3>
            <span className={cn('px-2.5 py-1 rounded-full text-sm font-medium', config.badgeColor, config.textColor)}>
              {tasks.length}
            </span>
          </div>
        </div>

        <Droppable droppableId={status}>
          {(provided, snapshot) => (
            <div
              ref={provided.innerRef}
              {...provided.droppableProps}
              className={cn(
                'p-4 min-h-[500px] transition-colors',
                snapshot.isDraggingOver && 'bg-primary-50'
              )}
            >
              {tasks.length > 0 ? (
                tasks.map((task, index) => (
                  <KanbanCard
                    key={task.id}
                    task={task}
                    index={index}
                    onEdit={onEdit}
                  />
                ))
              ) : (
                <div className="flex items-center justify-center h-32 text-gray-400 text-sm">
                  Drop tasks here
                </div>
              )}
              {provided.placeholder}
            </div>
          )}
        </Droppable>
      </div>
    </div>
  );
};

export default KanbanColumn;

