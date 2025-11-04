import { useNavigate } from 'react-router-dom';
import { FiFolderPlus, FiCheckSquare, FiCalendar } from 'react-icons/fi';
import Card from '../ui/Card';
import { formatDate } from '../../utils/helpers';

const ProjectCard = ({ project }) => {
  const navigate = useNavigate();

  return (
    <Card hover onClick={() => navigate(`/projects/${project.id}`)}>
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="p-3 bg-primary-50 rounded-lg">
            <FiFolderPlus className="h-6 w-6 text-primary-600" />
          </div>
          <div>
            <h3 className="font-semibold text-lg text-gray-900">{project.title}</h3>
            <p className="text-sm text-gray-500 flex items-center gap-1 mt-1">
              <FiCalendar className="h-3 w-3" />
              {formatDate(project.created_at)}
            </p>
          </div>
        </div>
      </div>

      {project.description && (
        <p className="text-gray-600 text-sm mb-4 line-clamp-2">
          {project.description}
        </p>
      )}

      <div className="flex items-center justify-between pt-4 border-t border-gray-100">
        <div className="flex items-center gap-2 text-sm text-gray-600">
          <FiCheckSquare className="h-4 w-4" />
          <span className="font-medium">{project.task_count || 0}</span>
          <span>Tasks</span>
        </div>
      </div>
    </Card>
  );
};

export default ProjectCard;

