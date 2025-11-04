import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useSelector } from 'react-redux';
import { FiSearch, FiFilter, FiGrid, FiList } from 'react-icons/fi';
import { taskService } from '../services/taskService';
import TaskCard from '../components/tasks/TaskCard';
import TaskModal from '../components/tasks/TaskModal';
import KanbanBoard from '../components/kanban/KanbanBoard';
import Input from '../components/ui/Input';
import Select from '../components/ui/Select';
import Loading from '../components/ui/Loading';
import EmptyState from '../components/ui/EmptyState';
import { QUERY_KEYS, TASK_STATUS } from '../utils/constants';

const Tasks = () => {
  const [selectedTask, setSelectedTask] = useState(null);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [viewMode, setViewMode] = useState('kanban');
  const { user } = useSelector((state) => state.auth);

  const { data, isLoading } = useQuery({
    queryKey: [QUERY_KEYS.TASKS, { assigned_to: user?.id, search, status: statusFilter }],
    queryFn: () => taskService.getTasks({
      assigned_to: user?.id,
      search,
      status: statusFilter,
      page: 1,
      size: 20,
    }),
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
        <p className="text-gray-600 mt-1">View and manage your assigned tasks</p>
      </div>

      <div className="flex flex-col lg:flex-row gap-4">
        <div className="flex-1 relative">
          <FiSearch className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400" />
          <Input
            placeholder="Search tasks..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-11"
          />
        </div>
        <div className="flex items-center gap-3 flex-wrap">
          <div className="flex items-center gap-2 bg-white border border-gray-200 rounded-lg p-1">
            <button
              onClick={() => setViewMode('kanban')}
              className={`px-3 py-1.5 rounded-md transition-colors ${
                viewMode === 'kanban'
                  ? 'bg-primary-600 text-white'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <FiGrid className="inline mr-1" />
              Kanban
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`px-3 py-1.5 rounded-md transition-colors ${
                viewMode === 'list'
                  ? 'bg-primary-600 text-white'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <FiList className="inline mr-1" />
              List
            </button>
          </div>

          {viewMode === 'list' && (
            <div className="flex items-center gap-2">
              <FiFilter className="text-gray-400" />
              <Select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                options={[
                  { value: '', label: 'All Status' },
                  { value: TASK_STATUS.TODO, label: 'To Do' },
                  { value: TASK_STATUS.IN_PROGRESS, label: 'In Progress' },
                  { value: TASK_STATUS.DONE, label: 'Done' },
                ]}
                className="w-40"
              />
            </div>
          )}
        </div>
      </div>

      {isLoading ? (
        <Loading />
      ) : data?.data?.tasks?.length > 0 ? (
        viewMode === 'kanban' ? (
          <KanbanBoard tasks={data.data.tasks} />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {data.data.tasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onClick={setSelectedTask}
              />
            ))}
          </div>
        )
      ) : (
        <EmptyState
          title="No tasks found"
          description={search || statusFilter ? "Try adjusting your filters" : "You don't have any tasks assigned yet"}
        />
      )}

      {selectedTask && (
        <TaskModal
          isOpen={!!selectedTask}
          onClose={() => setSelectedTask(null)}
          task={selectedTask}
        />
      )}
    </div>
  );
};

export default Tasks;

