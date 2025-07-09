import api from './api';

class UserService {
  // Get all users (admin only)
  async getUsers(skip = 0, limit = 20) {
    try {
      const response = await api.get(`/users?skip=${skip}&limit=${limit}`);
      
      if (response.data.success) {
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al obtener los usuarios'
      };
    }
  }

  // Get user by ID
  async getUser(userId) {
    try {
      const response = await api.get(`/users/${userId}`);
      
      if (response.data.success) {
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al obtener el usuario'
      };
    }
  }

  // Get users by role
  async getUsersByRole(role, skip = 0, limit = 20) {
    try {
      const response = await api.get(`/users/role/${role}?skip=${skip}&limit=${limit}`);
      
      if (response.data.success) {
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al obtener usuarios por rol'
      };
    }
  }

  // Update user (admin or self)
  async updateUser(userId, userData) {
    try {
      const response = await api.put(`/users/${userId}`, userData);
      
      if (response.data.success) {
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al actualizar el usuario'
      };
    }
  }

  // Delete user (admin only)
  async deleteUser(userId) {
    try {
      const response = await api.delete(`/users/${userId}`);
      
      if (response.data.success) {
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al eliminar el usuario'
      };
    }
  }

  // Activate/deactivate user (admin only)
  async toggleUserStatus(userId) {
    try {
      const response = await api.patch(`/users/${userId}/toggle-status`);
      
      if (response.data.success) {
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al cambiar el estado del usuario'
      };
    }
  }

  // Get user statistics
  async getUserStats(userId) {
    try {
      const response = await api.get(`/users/${userId}/stats`);
      
      if (response.data.success) {
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al obtener estadísticas del usuario'
      };
    }
  }

  // Search users
  async searchUsers(query, skip = 0, limit = 20) {
    try {
      const response = await api.get(`/users/search?q=${encodeURIComponent(query)}&skip=${skip}&limit=${limit}`);
      
      if (response.data.success) {
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al buscar usuarios'
      };
    }
  }
}

const userService = new UserService();
export default userService; 