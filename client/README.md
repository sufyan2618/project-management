# TaskFlow Frontend

A modern, production-ready React application for project and task management.

## Features

- 🔐 JWT Authentication with role-based access control
- 📊 Different dashboards for Admin and User roles
- 📁 Project management with task tracking
- ✅ Task management with status filtering
- 🎯 **Kanban Board with Drag & Drop** - Intuitive task status management
- 🔄 Toggle between Kanban and List views
- 🎨 Beautiful, responsive UI with Tailwind CSS
- 🔄 React Query for efficient data fetching
- 🗂️ Redux Toolkit for state management
- 🍞 Toast notifications for user feedback
- 🎯 Protected routes with role-based access

## Tech Stack

- **React 19** - UI Library
- **Redux Toolkit** - State Management
- **React Query (TanStack Query)** - Server State Management
- **React Router v6** - Routing
- **Tailwind CSS** - Styling
- **@hello-pangea/dnd** - Drag & Drop for Kanban board
- **Axios** - HTTP Client
- **React Hot Toast** - Notifications
- **React Icons** - Icon Library
- **date-fns** - Date formatting

## Getting Started

### Prerequisites

- Node.js 18+ and Yarn

### Installation

1. Install dependencies:
```bash
yarn install
```

2. Create a `.env` file in the root directory:
```
VITE_API_BASE_URL=http://localhost:8000
```

3. Start the development server:
```bash
yarn dev
```

The application will be available at `http://localhost:5173`

## Project Structure

```
src/
├── components/          # Reusable components
│   ├── ui/             # Base UI components (Button, Card, Modal, etc.)
│   ├── layout/         # Layout components (Navbar, Sidebar, etc.)
│   ├── projects/       # Project-related components
│   └── tasks/          # Task-related components
├── pages/              # Page components
│   ├── auth/           # Authentication pages
│   └── dashboards/     # Dashboard pages
├── services/           # API services
├── store/              # Redux store and slices
├── utils/              # Utility functions and constants
├── App.jsx             # Main App component with routing
└── main.jsx            # Application entry point
```

## Features Overview

### For Admin Users
- View all projects with task counts
- Create, edit, and delete projects
- Create and assign tasks to users
- View comprehensive dashboard with statistics
- **Kanban board with drag-and-drop to update task status**
- Toggle between Kanban and List views

### For Regular Users
- View assigned projects
- View and manage assigned tasks
- Track task progress (To Do, In Progress, Done)
- Personal dashboard with task statistics
- **Kanban board with drag-and-drop functionality**
- Easily update task status by dragging cards between columns

## Available Scripts

- `yarn dev` - Start development server
- `yarn build` - Build for production
- `yarn preview` - Preview production build
- `yarn lint` - Run ESLint

## API Integration

The frontend communicates with the FastAPI backend. Make sure the backend is running on `http://localhost:8000`.

All API requests include JWT authentication tokens stored in localStorage.

## Responsive Design

The application is fully responsive and works seamlessly on:
- Desktop (1024px+)
- Tablet (768px - 1023px)
- Mobile (< 768px)

## Toast Notifications

Toast notifications are shown for:
- Successful operations (create, update, delete)
- API errors
- Authentication events (login, logout)
- Validation errors

## Security

- JWT tokens stored securely in localStorage
- Protected routes with authentication checks
- Role-based access control for admin features
- Automatic token expiry handling

## License

MIT
