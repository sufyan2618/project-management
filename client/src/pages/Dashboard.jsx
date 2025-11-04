import { useSelector } from 'react-redux';
import AdminDashboard from './dashboards/AdminDashboard';
import UserDashboard from './dashboards/UserDashboard';
import { USER_ROLES } from '../utils/constants';

const Dashboard = () => {
  const { user } = useSelector((state) => state.auth);
  
  if (user?.role === USER_ROLES.ADMIN) {
    return <AdminDashboard />;
  }
  
  return <UserDashboard />;
};

export default Dashboard;

