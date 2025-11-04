import { useState, useEffect } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { projectService } from '../../services/projectService';
import Modal from '../ui/Modal';
import Input from '../ui/Input';
import Button from '../ui/Button';
import { QUERY_KEYS } from '../../utils/constants';
import toast from 'react-hot-toast';

const ProjectModal = ({ isOpen, onClose, project = null }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
  });

  const queryClient = useQueryClient();
  const isEdit = !!project;

  useEffect(() => {
    if (project) {
      setFormData({
        title: project.title || '',
        description: project.description || '',
      });
    } else {
      setFormData({ title: '', description: '' });
    }
  }, [project]);

  const createMutation = useMutation({
    mutationFn: projectService.createProject,
    onSuccess: () => {
      queryClient.invalidateQueries([QUERY_KEYS.PROJECTS]);
      toast.success('Project created successfully!');
      onClose();
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to create project');
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }) => projectService.updateProject(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries([QUERY_KEYS.PROJECTS]);
      queryClient.invalidateQueries([QUERY_KEYS.PROJECT_DETAIL]);
      toast.success('Project updated successfully!');
      onClose();
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to update project');
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (isEdit) {
      updateMutation.mutate({ id: project.id, data: formData });
    } else {
      createMutation.mutate(formData);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={isEdit ? 'Edit Project' : 'Create New Project'}
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="Project Title"
          name="title"
          value={formData.title}
          onChange={handleChange}
          placeholder="Enter project title"
          required
        />

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Description
          </label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows={4}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all"
            placeholder="Enter project description (optional)"
          />
        </div>

        <div className="flex gap-3 pt-4">
          <Button
            type="button"
            variant="secondary"
            onClick={onClose}
            className="flex-1"
          >
            Cancel
          </Button>
          <Button
            type="submit"
            className="flex-1"
            isLoading={createMutation.isPending || updateMutation.isPending}
          >
            {isEdit ? 'Update' : 'Create'}
          </Button>
        </div>
      </form>
    </Modal>
  );
};

export default ProjectModal;

