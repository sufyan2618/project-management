import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { FiFolderPlus, FiCheckSquare, FiUsers, FiPlus } from 'react-icons/fi';
import { projectService } from '../../services/projectService';
import { taskService } from '../../services/taskService';
import ProjectCard from '../../components/projects/ProjectCard';
import ProjectModal from '../../components/projects/ProjectModal';
import Button from '../../components/ui/Button';
import Card from '../../components/ui/Card';
import Loading from '../../components/ui/Loading';
import EmptyState from '../../components/ui/EmptyState';
import { QUERY_KEYS } from '../../utils/constants';

const AdminDashboard = () => {
  const [showProjectModal, setShowProjectModal] = useState(false);
  const navigate = useNavigate();

  const { data: projectsData, isLoading: projectsLoading } = useQuery({
    queryKey: [QUERY_KEYS.PROJECTS, { page: 1, size: 6 }],
    queryFn: () => projectService.getProjects({ page: 1, size: 6 }),
  });

  const { data: tasksData } = useQuery({
    queryKey: [QUERY_KEYS.TASKS, { page: 1, size: 1 }],
    queryFn: () => taskService.getTasks({ page: 1, size: 1 }),
  });

  const stats = [
    {
      title: 'Total Projects',
      value: projectsData?.data?.total || 0,
      icon: FiFolderPlus,
      color: 'bg-blue-500',
    },
    {
      title: 'Total Tasks',
      value: tasksData?.data?.total || 0,
      icon: FiCheckSquare,
      color: 'bg-green-500',
    },
    {
      title: 'Active Users',
      value: '12',
      icon: FiUsers,
      color: 'bg-purple-500',
    },
  ];

  if (projectsLoading) return <Loading />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
          <p className="text-gray-600 mt-1">Welcome back! Here's what's happening.</p>
        </div>
        <Button onClick={() => setShowProjectModal(true)}>
          <FiPlus className="mr-2" />
          New Project
        </Button>
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
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-gray-900">Recent Projects</h2>
          <Button variant="ghost" onClick={() => navigate('/projects')}>
            View All
          </Button>
        </div>

        {projectsData?.data?.projects?.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {projectsData.data.projects.map((project) => (
              <ProjectCard key={project.id} project={project} />
            ))}
          </div>
        ) : (
          <EmptyState
            title="No projects yet"
            description="Create your first project to get started"
            action={
              <Button onClick={() => setShowProjectModal(true)}>
                <FiPlus className="mr-2" />
                Create Project
              </Button>
            }
          />
        )}
      </div>

      <ProjectModal
        isOpen={showProjectModal}
        onClose={() => setShowProjectModal(false)}
      />
    </div>
  );
};

export default AdminDashboard;

