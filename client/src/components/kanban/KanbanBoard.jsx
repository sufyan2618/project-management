import { useState, useEffect } from 'react';
import { DragDropContext } from '@hello-pangea/dnd';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { taskService } from '../../services/taskService';
import KanbanColumn from './KanbanColumn';
import TaskModal from '../tasks/TaskModal';
import { QUERY_KEYS, TASK_STATUS } from '../../utils/constants';
import toast from 'react-hot-toast';

const KanbanBoard = ({ tasks = [], projectId = null }) => {
  const [selectedTask, setSelectedTask] = useState(null);
  const [columns, setColumns] = useState({
    [TASK_STATUS.TODO]: [],
    [TASK_STATUS.IN_PROGRESS]: [],
    [TASK_STATUS.DONE]: [],
  });

  const queryClient = useQueryClient();

  useEffect(() => {
    const grouped = {
      [TASK_STATUS.TODO]: [],
      [TASK_STATUS.IN_PROGRESS]: [],
      [TASK_STATUS.DONE]: [],
    };

    tasks.forEach((task) => {
      if (grouped[task.status]) {
        grouped[task.status].push(task);
      }
    });

    setColumns(grouped);
  }, [tasks]);

  const updateTaskMutation = useMutation({
    mutationFn: ({ id, data }) => taskService.updateTask(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries([QUERY_KEYS.TASKS]);
      queryClient.invalidateQueries([QUERY_KEYS.PROJECT_DETAIL]);
      toast.success('Task status updated!');
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to update task');
      setColumns((prev) => ({ ...prev }));
    },
  });

  const handleDragEnd = (result) => {
    const { source, destination, draggableId } = result;

    if (!destination) return;

    if (
      source.droppableId === destination.droppableId &&
      source.index === destination.index
    ) {
      return;
    }

    const sourceColumn = columns[source.droppableId];
    const destColumn = columns[destination.droppableId];
    const task = sourceColumn.find((t) => t.id.toString() === draggableId);

    if (!task) return;

    const newColumns = { ...columns };
    newColumns[source.droppableId] = sourceColumn.filter(
      (t) => t.id.toString() !== draggableId
    );
    newColumns[destination.droppableId] = [
      ...destColumn.slice(0, destination.index),
      { ...task, status: destination.droppableId },
      ...destColumn.slice(destination.index),
    ];

    setColumns(newColumns);

    updateTaskMutation.mutate({
      id: task.id,
      data: { status: destination.droppableId },
    });
  };

  const handleEditTask = (task) => {
    setSelectedTask(task);
  };

  return (
    <>
      <DragDropContext onDragEnd={handleDragEnd}>
        <div className="flex gap-4 overflow-x-auto pb-4">
          <KanbanColumn
            status={TASK_STATUS.TODO}
            tasks={columns[TASK_STATUS.TODO]}
            onEdit={handleEditTask}
          />
          <KanbanColumn
            status={TASK_STATUS.IN_PROGRESS}
            tasks={columns[TASK_STATUS.IN_PROGRESS]}
            onEdit={handleEditTask}
          />
          <KanbanColumn
            status={TASK_STATUS.DONE}
            tasks={columns[TASK_STATUS.DONE]}
            onEdit={handleEditTask}
          />
        </div>
      </DragDropContext>

      {selectedTask && (
        <TaskModal
          isOpen={!!selectedTask}
          onClose={() => setSelectedTask(null)}
          task={selectedTask}
          projectId={projectId}
        />
      )}
    </>
  );
};

export default KanbanBoard;

