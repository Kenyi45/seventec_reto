import api from './api';

class PostService {
  // Get all posts
  async getPosts(skip = 0, limit = 20) {
    try {
      const response = await api.get(`/posts?skip=${skip}&limit=${limit}`);
      
      if (response.data.success) {
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al obtener las publicaciones'
      };
    }
  }

  // Get post by ID
  async getPost(postId) {
    try {
      const response = await api.get(`/posts/${postId}`);
      
      if (response.data.success) {
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al obtener la publicación'
      };
    }
  }

  // Create new post (organizers only)
  async createPost(postData) {
    try {
      const response = await api.post('/posts', postData);
      
      if (response.data.success) {
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al crear la publicación'
      };
    }
  }

  // Update post (author only)
  async updatePost(postId, postData) {
    try {
      const response = await api.put(`/posts/${postId}`, postData);
      
      if (response.data.success) {
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al actualizar la publicación'
      };
    }
  }

  // Delete post (author only)
  async deletePost(postId) {
    try {
      const response = await api.delete(`/posts/${postId}`);
      
      if (response.data.success) {
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al eliminar la publicación'
      };
    }
  }

  // Like post (participants only)
  async likePost(postId) {
    try {
      console.log('Attempting to like post:', postId);
      const response = await api.post(`/posts/${postId}/like`);
      
      if (response.data.success) {
        console.log('Like successful:', response.data);
        return { success: true, data: response.data.data };
      }
      
      console.log('Like failed:', response.data);
      return { success: false, error: response.data.message };
    } catch (error) {
      console.error('Like error:', error);
      console.error('Error details:', {
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data,
        url: error.config?.url,
        method: error.config?.method
      });
      return {
        success: false,
        error: error.response?.data?.detail || `Error al dar like (${error.response?.status || 'Unknown'})`
      };
    }
  }

  // Unlike post (participants only)
  async unlikePost(postId) {
    try {
      console.log('Attempting to unlike post:', postId);
      const response = await api.delete(`/posts/${postId}/like`);
      
      if (response.data.success) {
        console.log('Unlike successful:', response.data);
        return { success: true, data: response.data.data };
      }
      
      console.log('Unlike failed:', response.data);
      return { success: false, error: response.data.message };
    } catch (error) {
      console.error('Unlike error:', error);
      console.error('Error details:', {
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data,
        url: error.config?.url,
        method: error.config?.method
      });
      
      // Si es un error 404, significa que el like no existe
      if (error.response?.status === 404) {
        console.log('Like not found (404), treating as success since the goal is achieved');
        return { 
          success: true, 
          data: { message: 'Like removido exitosamente' },
          wasNotFound: true 
        };
      }
      
      return {
        success: false,
        error: error.response?.data?.detail || `Error al quitar like (${error.response?.status || 'Unknown'})`
      };
    }
  }

  // Add comment to post (participants only)
  async addComment(postId, commentData) {
    try {
      console.log('Adding comment:', { postId, commentData });
      const response = await api.post(`/posts/${postId}/comments`, commentData);
      
      console.log('Comment response:', response.data);
      
      if (response.data.success) {
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      console.error('Add comment error:', error);
      console.error('Error details:', {
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data,
        url: error.config?.url,
        method: error.config?.method
      });
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al agregar comentario'
      };
    }
  }

  // Get comments for post
  async getPostComments(postId, skip = 0, limit = 50) {
    try {
      const response = await api.get(`/posts/${postId}/comments?skip=${skip}&limit=${limit}`);
      
      if (response.data.success) {
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al obtener los comentarios'
      };
    }
  }

  // Get likes for post
  async getPostLikes(postId, skip = 0, limit = 50) {
    try {
      console.log('Getting likes for post:', postId);
      const response = await api.get(`/posts/${postId}/likes?skip=${skip}&limit=${limit}`);
      
      if (response.data.success) {
        console.log('Likes retrieved successfully:', response.data.data);
        return { success: true, data: response.data.data };
      }
      
      console.log('Failed to get likes:', response.data);
      return { success: false, error: response.data.message };
    } catch (error) {
      console.error('Get likes error:', error);
      console.error('Error details:', {
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data,
        url: error.config?.url,
        method: error.config?.method
      });
      return {
        success: false,
        error: error.response?.data?.detail || `Error al obtener los likes (${error.response?.status || 'Unknown'})`
      };
    }
  }

  // Test API connectivity
  async testApiConnection() {
    try {
      console.log('Testing API connection...');
      const response = await api.get('/posts');
      console.log('API connection successful:', response.status);
      return { success: true, data: response.data };
    } catch (error) {
      console.error('API connection failed:', error);
      return {
        success: false,
        error: `API connection failed: ${error.message}`
      };
    }
  }

  // Check authentication status
  async checkAuthStatus() {
    try {
      const token = localStorage.getItem('accessToken');
      const user = localStorage.getItem('user');
      
      console.log('Auth status check:', {
        hasToken: !!token,
        tokenLength: token ? token.length : 0,
        hasUser: !!user,
        userData: user ? JSON.parse(user) : null
      });
      
      if (!token) {
        return { success: false, error: 'No token found' };
      }
      
      // Try to get current user to verify token
      const response = await api.get('/auth/me');
      return { success: true, data: response.data };
    } catch (error) {
      console.error('Auth check failed:', error);
      return {
        success: false,
        error: `Auth check failed: ${error.response?.data?.detail || error.message}`
      };
    }
  }

  // Sync likes state from backend
  async syncLikesState(postId) {
    try {
      console.log('Syncing likes state for post:', postId);
      const likesResponse = await this.getPostLikes(postId);
      
      if (likesResponse.success) {
        const user = JSON.parse(localStorage.getItem('user'));
        const isLiked = user ? likesResponse.data.some(like => like.user_id === user.id) : false;
        
        console.log('Likes state synced:', {
          postId,
          totalLikes: likesResponse.data.length,
          isLiked,
          userId: user?.id
        });
        
        return {
          success: true,
          data: {
            likes: likesResponse.data,
            isLiked,
            totalCount: likesResponse.data.length
          }
        };
      }
      
      return likesResponse;
    } catch (error) {
      console.error('Sync likes error:', error);
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al sincronizar likes'
      };
    }
  }

  // Toggle like (like/unlike based on current state)
  async toggleLike(postId) {
    try {
      const user = JSON.parse(localStorage.getItem('user'));
      // Verificar si el usuario existe y tiene ID
      if (!user || !user.id) {
        return {
          success: false,
          error: 'Usuario no autenticado'
        };
      }

      console.log('Starting toggle like process:', { postId, userId: user.id });

      // First check if user has liked the post
      const likesResponse = await this.getPostLikes(postId);
      console.log('Likes response:', likesResponse);
      
      if (likesResponse.success) {
        // Buscar si el usuario ya dio like
        const isLiked = likesResponse.data.some(like => like.user_id === user.id);
        
        console.log('Toggle like debug:', {
          postId,
          userId: user.id,
          isLiked,
          likesData: likesResponse.data,
          likesCount: likesResponse.data.length
        });
        
        if (isLiked) {
          console.log('User has liked the post, attempting to unlike...');
          return await this.unlikePost(postId);
        } else {
          console.log('User has not liked the post, attempting to like...');
          return await this.likePost(postId);
        }
      } else {
        console.log('Failed to get likes, attempting to like directly...');
        return await this.likePost(postId);
      }
    } catch (error) {
      console.error('Toggle like error:', error);
      
      // Si es un error 404 al obtener likes, intentar dar like directamente
      if (error.response?.status === 404) {
        console.log('Post not found, attempting to like directly...');
        const user = JSON.parse(localStorage.getItem('user'));
        if (user && user.id) {
          return await this.likePost(postId);
        }
      }
      
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al cambiar like'
      };
    }
  }

  // Delete comment (comment author only)
  async deleteComment(commentId) {
    try {
      const response = await api.delete(`/comments/${commentId}`);
      
      if (response.data.success) {
        return { success: true, data: response.data.data };
      }
      
      return { success: false, error: response.data.message };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Error al eliminar comentario'
      };
    }
  }
}

export default new PostService(); 