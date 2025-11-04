import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useSelector } from 'react-redux';
import { FiCheckSquare, FiClock, FiCheck } from 'react-icons/fi';
import { taskService } from '../../services/taskService';
import TaskCard from '../../components/tasks/TaskCard';
import TaskModal from '../../components/tasks/TaskModal';
import Card from '../../components/ui/Card';
import Loading from '../../components/ui/Loading';
import EmptyState from '../../components/ui/EmptyState';
import { QUERY_KEYS, TASK_STATUS } from '../../utils/constants';

const UserDashboard = () => {
  const [selectedTask, setSelectedTask] = useState(null);
  const { user } = useSelector((state) => state.auth);

  const { data: myTasksData, isLoading } = useQuery({
    queryKey: [QUERY_KEYS.TASKS, { assigned_to: user?.id, page: 1, size: 10 }],
    queryFn: () => taskService.getTasks({ assigned_to: user?.id, page: 1, size: 10 }),
  });

  const todoTasks = myTasksData?.data?.tasks?.filter(t => t.status === TASK_STATUS.TODO) || [];
  const inProgressTasks = myTasksData?.data?.tasks?.filter(t => t.status === TASK_STATUS.IN_PROGRESS) || [];
  const doneTasks = myTasksData?.data?.tasks?.filter(t => t.status === TASK_STATUS.DONE) || [];

  const stats = [
    {
      title: 'To Do',
      value: todoTasks.length,
      icon: FiCheckSquare,
      color: 'bg-gray-500',
    },
    {
      title: 'In Progress',
      value: inProgressTasks.length,
      icon: FiClock,
      color: 'bg-blue-500',
    },
    {
      title: 'Completed',
      value: doneTasks.length,
      icon: FiCheck,
      color: 'bg-green-500',
    },
  ];

  if (isLoading) return <Loading />;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">My Dashboard</h1>
        <p className="text-gray-600 mt-1">Track your assigned tasks and progress</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {stats.map((stat) => (
          <Card key={stat.title}>
            <div className="flex items-center gap-4">
              <div className={`p-3 rounded-lg ${stat.color}`}>
                <stat.icon className="h-6 w-6 text-white" />
              </div>
              <div>
                <p className="text-sm text-gray-600">{stat.title}</p>
                <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
              </div>
            </div>
          </Card>
        ))}
      </div>

      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">My Tasks</h2>
        
        {myTasksData?.data?.tasks?.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {myTasksData.data.tasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onClick={setSelectedTask}
              />
            ))}
          </div>
        ) : (
          <EmptyState
            title="No tasks assigned"
            description="You don't have any tasks assigned yet"
          />
        )}
      </div>

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

export default UserDashboard;

