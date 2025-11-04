import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { FiArrowLeft, FiPlus, FiFilter, FiGrid, FiList } from 'react-icons/fi';
import { projectService } from '../services/projectService';
import TaskCard from '../components/tasks/TaskCard';
import TaskModal from '../components/tasks/TaskModal';
import KanbanBoard from '../components/kanban/KanbanBoard';
import Button from '../components/ui/Button';
import Card from '../components/ui/Card';
import Select from '../components/ui/Select';
import Loading from '../components/ui/Loading';
import EmptyState from '../components/ui/EmptyState';
import { QUERY_KEYS, TASK_STATUS } from '../utils/constants';
import { formatDate } from '../utils/helpers';

const ProjectDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [showTaskModal, setShowTaskModal] = useState(false);
  const [selectedTask, setSelectedTask] = useState(null);
  const [statusFilter, setStatusFilter] = useState('');
  const [viewMode, setViewMode] = useState('kanban');

  const { data, isLoading } = useQuery({
    queryKey: [QUERY_KEYS.PROJECT_DETAIL, id],
    queryFn: () => projectService.getProject(id),
  });

  const project = data?.data;
  const tasks = project?.tasks || [];
  
  const filteredTasks = statusFilter
    ? tasks.filter(task => task.status === statusFilter)
    : tasks;

  const handleTaskClick = (task) => {
    setSelectedTask(task);
  };

  if (isLoading) return <Loading />;

  return (
    <div className="space-y-6">
      <Button
        variant="ghost"
        onClick={() => navigate('/projects')}
        className="mb-4"
      >
        <FiArrowLeft className="mr-2" />
        Back to Projects
      </Button>

      <Card>
        <div className="flex items-start justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{project?.title}</h1>
            <p className="text-gray-600 mt-2">{project?.description}</p>
            <p className="text-sm text-gray-500 mt-2">
              Created on {formatDate(project?.created_at)}
            </p>
          </div>
          <Button onClick={() => setShowTaskModal(true)}>
            <FiPlus className="mr-2" />
            Add Task
          </Button>
        </div>
      </Card>

      <div className="flex items-center justify-between flex-wrap gap-4">
        <h2 className="text-xl font-semibold text-gray-900">
          Tasks ({filteredTasks.length})
        </h2>
        <div className="flex items-center gap-3">
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

      {tasks.length > 0 ? (
        viewMode === 'kanban' ? (
          <KanbanBoard tasks={tasks} projectId={parseInt(id)} />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredTasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onClick={handleTaskClick}
              />
            ))}
          </div>
        )
      ) : (
        <EmptyState
          title="No tasks yet"
          description="Add your first task to this project"
          action={
            <Button onClick={() => setShowTaskModal(true)}>
              <FiPlus className="mr-2" />
              Add Task
            </Button>
          }
        />
      )}

      <TaskModal
        isOpen={showTaskModal}
        onClose={() => setShowTaskModal(false)}
        projectId={parseInt(id)}
      />

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

export default ProjectDetail;

