import api from './api';

class StoryService {
  // Get all active stories
  async getStories(skip = 0, limit = 20) {
    try {
      const response = await api.get(`/stories?skip=${skip}&limit=${limit}`);
      
      if (response.data.success) {
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al obtener las historias'
      };
    }
  }

  // Get story by ID
  async getStory(storyId) {
    try {
      const response = await api.get(`/stories/${storyId}`);
      
      if (response.data.success) {
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al obtener la historia'
      };
    }
  }

  // Create new story (organizers only)
  async createStory(storyData) {
    try {
      const response = await api.post('/stories', storyData);
      
      if (response.data.success) {
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al crear la historia'
      };
    }
  }

  // Update story (author only)
  async updateStory(storyId, storyData) {
    try {
      const response = await api.put(`/stories/${storyId}`, storyData);
      
      if (response.data.success) {
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al actualizar la historia'
      };
    }
  }

  // Delete story (author only)
  async deleteStory(storyId) {
    try {
      const response = await api.delete(`/stories/${storyId}`);
      
      if (response.data.success) {
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al eliminar la historia'
      };
    }
  }

  // View story (increment view count)
  async viewStory(storyId) {
    try {
      console.log('StoryService.viewStory called with ID:', storyId);
      console.log('StoryService.viewStory ID type:', typeof storyId);
      
      const response = await api.get(`/stories/${storyId}`);
      
      console.log('StoryService.viewStory response:', response.data);
      
      if (response.data.success) {
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      console.error('StoryService.viewStory error:', error);
      console.error('StoryService.viewStory error response:', error.response?.data);
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al ver la historia'
      };
    }
  }

  // Get story views
  async getStoryViews(storyId, skip = 0, limit = 50) {
    try {
      const response = await api.get(`/stories/${storyId}/views?skip=${skip}&limit=${limit}`);
      
      if (response.data.success) {
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al obtener las vistas de la historia'
      };
    }
  }

  // Get expired stories (for cleanup)
  async getExpiredStories() {
    try {
      const response = await api.get('/stories/expired');
      
      if (response.data.success) {
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al obtener historias expiradas'
      };
    }
  }
}

const storyService = new StoryService();
export default storyService; 