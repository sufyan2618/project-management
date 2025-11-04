import { useState, useEffect } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { taskService } from '../../services/taskService';
import { projectService } from '../../services/projectService';
import Modal from '../ui/Modal';
import Input from '../ui/Input';
import Select from '../ui/Select';
import Button from '../ui/Button';
import { QUERY_KEYS, TASK_STATUS } from '../../utils/constants';
import toast from 'react-hot-toast';

const TaskModal = ({ isOpen, onClose, task = null, projectId = null }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    project_id: projectId || '',
    assigned_to: '',
    status: TASK_STATUS.TODO,
    due_date: '',
  });

  const queryClient = useQueryClient();
  const isEdit = !!task;

  const { data: projectsData } = useQuery({
    queryKey: [QUERY_KEYS.PROJECTS],
    queryFn: () => projectService.getProjects({ size: 100 }),
  });

  useEffect(() => {
    if (task) {
      setFormData({
        title: task.title || '',
        description: task.description || '',
        project_id: task.project_id || '',
        assigned_to: task.assigned_to || '',
        status: task.status || TASK_STATUS.TODO,
        due_date: task.due_date ? task.due_date.split('T')[0] : '',
      });
    } else if (projectId) {
      setFormData(prev => ({ ...prev, project_id: projectId }));
    }
  }, [task, projectId]);

  const createMutation = useMutation({
    mutationFn: taskService.createTask,
    onSuccess: () => {
      queryClient.invalidateQueries([QUERY_KEYS.TASKS]);
      queryClient.invalidateQueries([QUERY_KEYS.PROJECT_DETAIL]);
      toast.success('Task created successfully!');
      onClose();
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to create task');
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }) => taskService.updateTask(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries([QUERY_KEYS.TASKS]);
      queryClient.invalidateQueries([QUERY_KEYS.PROJECT_DETAIL]);
      toast.success('Task updated successfully!');
      onClose();
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Failed to update task');
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const taskData = {
      ...formData,
      assigned_to: parseInt(formData.assigned_to),
      project_id: parseInt(formData.project_id),
    };

    if (isEdit) {
      updateMutation.mutate({ id: task.id, data: taskData });
    } else {
      createMutation.mutate(taskData);
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const statusOptions = [
    { value: TASK_STATUS.TODO, label: 'To Do' },
    { value: TASK_STATUS.IN_PROGRESS, label: 'In Progress' },
    { value: TASK_STATUS.DONE, label: 'Done' },
  ];

  const projectOptions = projectsData?.data?.projects?.map(project => ({
    value: project.id,
    label: project.title,
  })) || [];

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={isEdit ? 'Edit Task' : 'Create New Task'}
      size="lg"
    >
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="Task Title"
          name="title"
          value={formData.title}
          onChange={handleChange}
          placeholder="Enter task title"
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
            rows={3}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all"
            placeholder="Enter task description (optional)"
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <Select
            label="Project"
            name="project_id"
            value={formData.project_id}
            onChange={handleChange}
            options={[
              { value: '', label: 'Select Project' },
              ...projectOptions,
            ]}
            required
          />

          <Select
            label="Status"
            name="status"
            value={formData.status}
            onChange={handleChange}
            options={statusOptions}
            required
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <Input
            label="Assigned To (User ID)"
            name="assigned_to"
            type="number"
            value={formData.assigned_to}
            onChange={handleChange}
            placeholder="Enter user ID"
            required
          />

          <Input
            label="Due Date"
            name="due_date"
            type="date"
            value={formData.due_date}
            onChange={handleChange}
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

export default TaskModal;

