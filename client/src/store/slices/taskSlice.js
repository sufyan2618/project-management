import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  selectedTask: null,
  filters: {
    status: '',
    search: '',
    page: 1,
    size: 10,
    project_id: null,
  },
};

const taskSlice = createSlice({
  name: 'task',
  initialState,
  reducers: {
    setSelectedTask: (state, action) => {
      state.selectedTask = action.payload;
    },
    
    setFilters: (state, action) => {
      state.filters = { ...state.filters, ...action.payload };
    },
    
    resetFilters: (state) => {
      state.filters = initialState.filters;
    },
    
    clearSelectedTask: (state) => {
      state.selectedTask = null;
    },
  },
});

export const {
  setSelectedTask,
  setFilters,
  resetFilters,
  clearSelectedTask,
} = taskSlice.actions;

export default taskSlice.reducer;

