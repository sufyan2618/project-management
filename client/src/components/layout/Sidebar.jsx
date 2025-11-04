import { NavLink } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { FiHome, FiFolderPlus, FiCheckSquare, FiX } from 'react-icons/fi';
import { USER_ROLES } from '../../utils/constants';
import { cn } from '../../utils/helpers';

const Sidebar = ({ isOpen, onClose }) => {
  const { user } = useSelector((state) => state.auth);
  const isAdmin = user?.role === USER_ROLES.ADMIN;

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: FiHome, roles: ['admin', 'user'] },
    { name: 'Projects', href: '/projects', icon: FiFolderPlus, roles: ['admin', 'user'] },
    { name: 'My Tasks', href: '/tasks', icon: FiCheckSquare, roles: ['user'] },
  ];

  const filteredNavigation = navigation.filter((item) =>
    item.roles.includes(user?.role)
  );

  return (
    <>
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={cn(
          'fixed top-0 left-0 h-full w-64 bg-white border-r border-gray-200 transform transition-transform duration-300 ease-in-out z-50',
          isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        )}
      >
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-xl font-bold text-primary-600">TaskFlow</h2>
          <button
            onClick={onClose}
            className="lg:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
          >
            <FiX className="h-5 w-5 text-gray-600" />
          </button>
        </div>

        <nav className="p-4 space-y-2">
          {filteredNavigation.map((item) => (
            <NavLink
              key={item.name}
              to={item.href}
              onClick={onClose}
              className={({ isActive }) =>
                cn(
                  'flex items-center gap-3 px-4 py-3 rounded-lg font-medium transition-colors',
                  isActive
                    ? 'bg-primary-50 text-primary-600'
                    : 'text-gray-700 hover:bg-gray-100'
                )
              }
            >
              <item.icon className="h-5 w-5" />
              {item.name}
            </NavLink>
          ))}
        </nav>

        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200">
          <div className="px-4 py-2 bg-gray-50 rounded-lg">
            <p className="text-xs text-gray-500 mb-1">Logged in as</p>
            <p className="text-sm font-medium text-gray-900 capitalize">{user?.role}</p>
          </div>
        </div>
      </aside>
    </>
  );
};

export default Sidebar;

