import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useSelector } from 'react-redux';
import { FiPlus, FiSearch } from 'react-icons/fi';
import { projectService } from '../services/projectService';
import ProjectCard from '../components/projects/ProjectCard';
import ProjectModal from '../components/projects/ProjectModal';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import Loading from '../components/ui/Loading';
import EmptyState from '../components/ui/EmptyState';
import { QUERY_KEYS, USER_ROLES } from '../utils/constants';

const Projects = () => {
  const [showModal, setShowModal] = useState(false);
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);
  const { user } = useSelector((state) => state.auth);
  const isAdmin = user?.role === USER_ROLES.ADMIN;

  const { data, isLoading } = useQuery({
    queryKey: [QUERY_KEYS.PROJECTS, { search, page, size: 9 }],
    queryFn: () => projectService.getProjects({ search, page, size: 9 }),
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Projects</h1>
          <p className="text-gray-600 mt-1">Manage all your projects</p>
        </div>
        {isAdmin && (
          <Button onClick={() => setShowModal(true)}>
            <FiPlus className="mr-2" />
            New Project
          </Button>
        )}
      </div>

      <div className="relative">
        <FiSearch className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400" />
        <Input
          placeholder="Search projects..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="pl-11"
        />
      </div>

      {isLoading ? (
        <Loading />
      ) : data?.data?.projects?.length > 0 ? (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {data.data.projects.map((project) => (
              <ProjectCard key={project.id} project={project} />
            ))}
          </div>

          {data.data.total_pages > 1 && (
            <div className="flex justify-center gap-2 mt-6">
              <Button
                variant="secondary"
                disabled={page === 1}
                onClick={() => setPage(page - 1)}
              >
                Previous
              </Button>
              <span className="flex items-center px-4 text-sm text-gray-600">
                Page {page} of {data.data.total_pages}
              </span>
              <Button
                variant="secondary"
                disabled={page >= data.data.total_pages}
                onClick={() => setPage(page + 1)}
              >
                Next
              </Button>
            </div>
          )}
        </>
      ) : (
        <EmptyState
          title="No projects found"
          description={search ? "Try adjusting your search" : "Create your first project to get started"}
          action={isAdmin && (
            <Button onClick={() => setShowModal(true)}>
              <FiPlus className="mr-2" />
              Create Project
            </Button>
          )}
        />
      )}

      <ProjectModal isOpen={showModal} onClose={() => setShowModal(false)} />
    </div>
  );
};

export default Projects;

