import api from './api';

class AuthService {
  // Register new user
  async register(userData) {
    try {
      const response = await api.post('/auth/register', userData);
      
      if (response.data.success) {
        const { access_token, user } = response.data.data;
        this.setToken(access_token);
        this.setUser(user);
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error en el registro'
      };
    }
  }

  // Login user
  async login(credentials) {
    try {
      const response = await api.post('/auth/login', credentials);
      
      if (response.data.success) {
        const { access_token, user } = response.data.data;
        this.setToken(access_token);
        this.setUser(user);
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error en el inicio de sesión'
      };
    }
  }

  // Logout user
  logout() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('user');
    window.location.href = '/login';
  }

  // Get current user profile
  async getCurrentUser() {
    try {
      const response = await api.get('/auth/me');
      
      if (response.data.success) {
        this.setUser(response.data.data);
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al obtener el perfil'
      };
    }
  }

  // Update user profile
  async updateProfile(profileData) {
    try {
      const response = await api.put('/auth/me', profileData);
      
      if (response.data.success) {
        this.setUser(response.data.data);
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al actualizar el perfil'
      };
    }
  }

  // Refresh token
  async refreshToken() {
    try {
      const response = await api.post('/auth/refresh');
      
      if (response.data.success) {
        const { access_token, user } = response.data.data;
        this.setToken(access_token);
        this.setUser(user);
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al renovar el token'
      };
    }
  }

  // Update FCM token for notifications
  async updateFCMToken(fcmToken) {
    try {
      const response = await api.post('/auth/fcm-token', { fcm_token: fcmToken });
      
      if (response.data.success) {
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al actualizar token FCM'
      };
    }
  }

  // Helper methods
  setToken(token) {
    localStorage.setItem('accessToken', token);
  }

  getToken() {
    return localStorage.getItem('accessToken');
  }

  setUser(user) {
    localStorage.setItem('user', JSON.stringify(user));
  }

  getUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }

  isAuthenticated() {
    return !!this.getToken();
  }

  isOrganizer() {
    const user = this.getUser();
    return user && user.role === 'organizer';
  }

  isParticipant() {
    const user = this.getUser();
    return user && user.role === 'participant';
  }
}

export default new AuthService(); 