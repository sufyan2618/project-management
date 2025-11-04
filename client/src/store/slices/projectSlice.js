import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  selectedProject: null,
  filters: {
    search: '',
    page: 1,
    size: 10,
  },
};

const projectSlice = createSlice({
  name: 'project',
  initialState,
  reducers: {
    setSelectedProject: (state, action) => {
      state.selectedProject = action.payload;
    },
    
    setFilters: (state, action) => {
      state.filters = { ...state.filters, ...action.payload };
    },
    
    resetFilters: (state) => {
      state.filters = initialState.filters;
    },
    
    clearSelectedProject: (state) => {
      state.selectedProject = null;
    },
  },
});

export const {
  setSelectedProject,
  setFilters,
  resetFilters,
  clearSelectedProject,
} = projectSlice.actions;

export default projectSlice.reducer;

