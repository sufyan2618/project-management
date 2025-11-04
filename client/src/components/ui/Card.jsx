import { cn } from '../../utils/helpers';

const Card = ({ children, className = '', onClick, hover = false }) => {
  return (
    <div
      className={cn(
        'bg-white rounded-lg shadow-md border border-gray-200 p-6',
        hover && 'hover:shadow-lg transition-shadow duration-200 cursor-pointer',
        className
      )}
      onClick={onClick}
    >
      {children}
    </div>
  );
};

export default Card;

