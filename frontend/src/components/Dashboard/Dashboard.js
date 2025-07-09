import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  IconButton,
  TextField,
  InputAdornment,
  Chip,
  Avatar,
  CircularProgress,
  Fab,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Alert,
  Grid,
  Paper,
  Divider,
  Badge,
  Skeleton,
} from '@mui/material';
import {
  Search,
  Favorite,
  FavoriteBorder,
  Comment,
  Share,
  Add,
  Edit,
  Delete,
  TrendingUp,
  Visibility,
  Schedule,
  Person,
} from '@mui/icons-material';
import { formatDistanceToNow } from 'date-fns';
import { es } from 'date-fns/locale';
import postService from '../../services/postService';
import { useAuth } from '../../contexts/AuthContext';
import { useNotification } from '../../contexts/NotificationContext';

const Dashboard = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [deleteDialog, setDeleteDialog] = useState({ open: false, post: null });
  const { user, isOrganizer, isAuthenticated } = useAuth();
  const { showSuccess, showError } = useNotification();
  const navigate = useNavigate();

  useEffect(() => {
    loadPosts();
    // Polling cada 5 segundos para actualizar automáticamente (sin mostrar errores)
    const interval = setInterval(() => {
      loadPosts(false);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const loadPosts = async (showErrors = true) => {
    try {
      if (showErrors) setLoading(true);
      const response = await postService.getPosts();
      if (response.success) {
        setPosts(response.data);
      } else if (showErrors) {
        showError(response.error || 'Error al cargar las publicaciones');
      }
    } catch (error) {
      if (showErrors) {
        showError('Error al cargar las publicaciones');
      }
    } finally {
      if (showErrors) setLoading(false);
    }
  };

  const handleLike = async (postId) => {
    try {
      console.log('Handling like for post:', postId, 'User:', user?.id);
      
      // Verificar que el usuario esté autenticado
      if (!user?.id) {
        showError('Debes estar autenticado para dar like');
        return;
      }
      
      const response = await postService.toggleLike(postId);
      console.log('Toggle like response:', response);
      
      if (response.success) {
        // Update local state
        setPosts(posts.map(post => {
          if (post.id === postId) {
            // Asegurar que post.likes sea un array
            const currentLikes = post.likes || [];
            const isLiked = currentLikes.includes(user?.id);
            
            // Si el like no existía (wasNotFound), asegurar que no esté en el array
            const newLikes = response.wasNotFound 
              ? currentLikes.filter(id => id !== user?.id)
              : isLiked 
                ? currentLikes.filter(id => id !== user?.id)
                : [...currentLikes, user?.id];
            
            console.log('Updating post likes:', {
              postId,
              oldLikes: currentLikes,
              newLikes,
              isLiked,
              wasNotFound: response.wasNotFound,
              userId: user?.id
            });
            
            return {
              ...post,
              likes: newLikes,
            };
          }
          return post;
        }));
        
        // Mostrar mensaje de éxito
        const message = response.wasNotFound ? 'Like removido (no existía)' : 'Like actualizado correctamente';
        showSuccess(message);
      } else {
        showError(response.error || 'Error al cambiar like');
      }
    } catch (error) {
      console.error('Handle like error:', error);
      showError('Error al cambiar like');
    }
  };

  const testApiConnection = async () => {
    try {
      const result = await postService.testApiConnection();
      if (result.success) {
        showSuccess('API conectada correctamente');
        console.log('API test result:', result.data);
      } else {
        showError(result.error);
      }
    } catch (error) {
      showError('Error al probar la API');
    }
  };

  const checkAuthStatus = async () => {
    try {
      const result = await postService.checkAuthStatus();
      if (result.success) {
        showSuccess('Autenticación válida');
        console.log('Auth result:', result.data);
      } else {
        showError(result.error);
      }
    } catch (error) {
      showError('Error al verificar autenticación');
    }
  };

  const syncLikesForPost = async (postId) => {
    try {
      const result = await postService.syncLikesState(postId);
      if (result.success) {
        showSuccess(`Likes sincronizados para post ${postId}`);
        console.log('Sync result:', result.data);
        
        // Actualizar el estado local con los datos sincronizados
        setPosts(posts.map(post => {
          if (post.id === postId) {
            return {
              ...post,
              likes: result.data.likes.map(like => like.user_id)
            };
          }
          return post;
        }));
      } else {
        showError(result.error);
      }
    } catch (error) {
      showError('Error al sincronizar likes');
    }
  };

  const handleDeletePost = async () => {
    try {
      const response = await postService.deletePost(deleteDialog.post.id);
      if (response.success) {
        setPosts(posts.filter(post => post.id !== deleteDialog.post.id));
        setDeleteDialog({ open: false, post: null });
        showSuccess('Publicación eliminada correctamente');
      } else {
        showError(response.error || 'Error al eliminar la publicación');
      }
    } catch (error) {
      showError('Error al eliminar la publicación');
    }
  };

  const filteredPosts = posts.filter(post =>
    post.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    post.content?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const PostCard = ({ post }) => {
    const isLiked = post.likes?.includes(user?.id);
    const isOwner = post.author_id === user?.id;

    return (
      <Card 
        elevation={0}
        sx={{ 
          mb: 3, 
          cursor: 'pointer',
          border: '1px solid #e2e8f0',
          borderRadius: 3,
          transition: 'all 0.3s ease',
          '&:hover': {
            transform: 'translateY(-4px)',
            boxShadow: '0px 20px 25px rgba(0, 0, 0, 0.1), 0px 10px 10px rgba(0, 0, 0, 0.04)',
            borderColor: 'primary.main',
          },
        }}
        onClick={() => navigate(`/posts/${post.id}`)}
      >
        <CardContent sx={{ p: 3 }}>
          {/* Header */}
          <Box display="flex" alignItems="center" justifyContent="space-between" mb={3}>
            <Box display="flex" alignItems="center" gap={2}>
              <Avatar 
                sx={{ 
                  width: 48, 
                  height: 48,
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  fontSize: '1.2rem',
                  fontWeight: 'bold'
                }}
              >
                {post.author_name?.[0]?.toUpperCase()}
              </Avatar>
              <Box>
                <Typography variant="subtitle1" fontWeight="600" color="text.primary">
                  {post.author_name}
                </Typography>
                <Box display="flex" alignItems="center" gap={1}>
                  <Schedule sx={{ fontSize: 16, color: 'text.secondary' }} />
                  <Typography variant="caption" color="text.secondary">
                    {formatDistanceToNow(new Date(post.created_at), { addSuffix: true, locale: es })}
                  </Typography>
                </Box>
              </Box>
            </Box>
            
            {(isOwner || isOrganizer) && (
              <Box display="flex" gap={1}>
                <IconButton 
                  size="small"
                  onClick={(e) => {
                    e.stopPropagation();
                    navigate(`/posts/${post.id}/edit`);
                  }}
                  sx={{ 
                    color: 'primary.main',
                    '&:hover': { backgroundColor: 'primary.light', color: 'white' }
                  }}
                >
                  <Edit fontSize="small" />
                </IconButton>
                <IconButton 
                  size="small"
                  onClick={(e) => {
                    e.stopPropagation();
                    setDeleteDialog({ open: true, post });
                  }}
                  sx={{ 
                    color: 'error.main',
                    '&:hover': { backgroundColor: 'error.light', color: 'white' }
                  }}
                >
                  <Delete fontSize="small" />
                </IconButton>
              </Box>
            )}
          </Box>
          
          {/* Content */}
          <Typography 
            variant="h5" 
            gutterBottom 
            sx={{ 
              fontWeight: 600,
              color: 'text.primary',
              mb: 2
            }}
          >
            {post.title}
          </Typography>
          
          <Typography 
            variant="body1" 
            color="text.secondary" 
            paragraph
            sx={{ 
              lineHeight: 1.7,
              mb: 3
            }}
          >
            {post.content?.length > 200 
              ? `${post.content.substring(0, 200)}...` 
              : post.content}
          </Typography>
          
          {/* Tags */}
          {post.tags && post.tags.length > 0 && (
            <Box display="flex" gap={1} flexWrap="wrap" mb={3}>
              {post.tags.map((tag, index) => (
                <Chip 
                  key={index} 
                  label={tag} 
                  size="small" 
                  variant="outlined"
                  sx={{ 
                    borderRadius: 2,
                    borderColor: 'primary.main',
                    color: 'primary.main',
                    '&:hover': {
                      backgroundColor: 'primary.main',
                      color: 'white',
                    }
                  }}
                />
              ))}
            </Box>
          )}
        </CardContent>
        
        <Divider />
        
        <CardActions sx={{ p: 3, pt: 2 }}>
          <Box display="flex" alignItems="center" gap={3}>
            <Box display="flex" alignItems="center" gap={1}>
              <IconButton 
                size="small"
                onClick={(e) => {
                  e.stopPropagation();
                  handleLike(post.id);
                }}
                sx={{ 
                  color: isLiked ? 'error.main' : 'text.secondary',
                  '&:hover': { 
                    backgroundColor: 'error.light',
                    color: 'white'
                  }
                }}
              >
                <Favorite fontSize="small" />
              </IconButton>
                        <Typography variant="body2" color="text.secondary" fontWeight={500}>
            {post.likes?.length || 0}
            {process.env.NODE_ENV === 'development' && (
              <span style={{ fontSize: '0.7rem', color: '#666' }}>
                {' '}({isLiked ? 'Liked' : 'Not liked'})
              </span>
            )}
          </Typography>
            </Box>
            
            <Box display="flex" alignItems="center" gap={1}>
              <IconButton 
                size="small"
                onClick={(e) => {
                  e.stopPropagation();
                  navigate(`/posts/${post.id}`);
                }}
                sx={{ 
                  color: 'text.secondary',
                  '&:hover': { 
                    backgroundColor: 'primary.light',
                    color: 'white'
                  }
                }}
              >
                <Comment fontSize="small" />
              </IconButton>
              <Typography variant="body2" color="text.secondary" fontWeight={500}>
                {post.comments?.length || 0}
              </Typography>
            </Box>
            
            <Box display="flex" alignItems="center" gap={1}>
              <IconButton 
                size="small"
                sx={{ 
                  color: 'text.secondary',
                  '&:hover': { 
                    backgroundColor: 'success.light',
                    color: 'white'
                  }
                }}
              >
                <Share fontSize="small" />
              </IconButton>
              <Typography variant="body2" color="text.secondary" fontWeight={500}>
                Compartir
              </Typography>
            </Box>
          </Box>
          
          <Button
            variant="outlined"
            size="small"
            onClick={(e) => {
              e.stopPropagation();
              navigate(`/posts/${post.id}`);
            }}
            sx={{ 
              ml: 'auto',
              borderRadius: 2,
              textTransform: 'none',
              fontWeight: 600,
              '&:hover': {
                backgroundColor: 'primary.main',
                color: 'white',
                borderColor: 'primary.main',
              }
            }}
          >
            Leer más
          </Button>
        </CardActions>
      </Card>
    );
  };

  if (loading) {
    return (
      <Box>
        {/* Header Skeleton */}
        <Box sx={{ mb: 4 }}>
          <Skeleton variant="text" width={300} height={48} sx={{ mb: 2 }} />
          <Skeleton variant="rectangular" width="100%" height={56} sx={{ borderRadius: 2 }} />
        </Box>
        
        {/* Posts Skeleton */}
        {[1, 2, 3].map((item) => (
          <Card key={item} elevation={0} sx={{ mb: 3, border: '1px solid #e2e8f0', borderRadius: 3 }}>
            <CardContent sx={{ p: 3 }}>
              <Box display="flex" alignItems="center" gap={2} mb={3}>
                <Skeleton variant="circular" width={48} height={48} />
                <Box sx={{ flex: 1 }}>
                  <Skeleton variant="text" width={150} height={24} />
                  <Skeleton variant="text" width={100} height={16} />
                </Box>
              </Box>
              <Skeleton variant="text" width="80%" height={32} sx={{ mb: 2 }} />
              <Skeleton variant="text" width="100%" height={20} sx={{ mb: 1 }} />
              <Skeleton variant="text" width="90%" height={20} sx={{ mb: 1 }} />
              <Skeleton variant="text" width="70%" height={20} sx={{ mb: 2 }} />
              <Box display="flex" gap={1}>
                <Skeleton variant="rectangular" width={60} height={24} sx={{ borderRadius: 1 }} />
                <Skeleton variant="rectangular" width={80} height={24} sx={{ borderRadius: 1 }} />
              </Box>
            </CardContent>
          </Card>
        ))}
      </Box>
    );
  }

  return (
    <Box>
      {/* Debug Information */}
      {process.env.NODE_ENV === 'development' && (
        <Alert 
          severity="info" 
          sx={{ 
            mb: 3,
            borderRadius: 2,
            '& .MuiAlert-icon': { fontSize: 20 }
          }}
        >
          <Typography variant="body2">
            <strong>Debug Info:</strong><br />
            Autenticado: {isAuthenticated ? 'Sí' : 'No'}<br />
            Usuario: {user?.full_name || 'No disponible'}<br />
            Rol: {user?.role || 'No disponible'}<br />
            Es Organizador: {isOrganizer ? 'Sí' : 'No'}<br />
            ID Usuario: {user?.id || 'No disponible'}<br />
            Total Posts: {posts.length}<br />
            Posts con Likes: {posts.filter(p => p.likes && p.likes.length > 0).length}<br />
            Total Likes: {filteredPosts.reduce((total, post) => total + (post.likes?.length || 0), 0)}
          </Typography>
          <Box sx={{ mt: 2 }}>
            <Button
              variant="outlined"
              size="small"
              onClick={testApiConnection}
              sx={{ mr: 1 }}
            >
              Probar API
            </Button>
            <Button
              variant="outlined"
              size="small"
              onClick={checkAuthStatus}
              sx={{ mr: 1 }}
            >
              Verificar Auth
            </Button>
            <Button
              variant="outlined"
              size="small"
              onClick={() => console.log('API URL:', process.env.REACT_APP_API_URL || 'http://localhost:8000')}
              sx={{ mr: 1 }}
            >
              Ver URL API
            </Button>
            <Button
              variant="outlined"
              size="small"
              onClick={() => {
                const postId = posts[0]?.id;
                if (postId) {
                  syncLikesForPost(postId);
                } else {
                  showError('No hay posts disponibles');
                }
              }}
            >
              Sincronizar Likes
            </Button>
          </Box>
        </Alert>
      )}

      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
          <Box>
            <Typography 
              variant="h3" 
              component="h1" 
              sx={{ 
                fontWeight: 700,
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                backgroundClip: 'text',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                mb: 1
              }}
            >
              Dashboard
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Bienvenido de vuelta, {user?.name}. Aquí tienes las últimas publicaciones.
            </Typography>
          </Box>
          {isOrganizer && (
            <Button
              variant="contained"
              startIcon={<Add />}
              onClick={() => navigate('/create-post')}
              sx={{
                borderRadius: 2,
                px: 3,
                py: 1.5,
                textTransform: 'none',
                fontWeight: 600,
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                '&:hover': {
                  background: 'linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%)',
                  transform: 'translateY(-2px)',
                  boxShadow: '0px 8px 16px rgba(102, 126, 234, 0.3)',
                },
              }}
            >
              Nueva Publicación
            </Button>
          )}
        </Box>

        {/* Search Bar */}
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Buscar publicaciones por título o contenido..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          sx={{ 
            mb: 3,
            '& .MuiOutlinedInput-root': {
              borderRadius: 3,
              backgroundColor: 'white',
              '&:hover .MuiOutlinedInput-notchedOutline': {
                borderColor: 'primary.main',
              },
            },
          }}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <Search sx={{ color: 'text.secondary' }} />
              </InputAdornment>
            ),
          }}
        />
      </Box>

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Paper 
            elevation={0} 
            sx={{ 
              p: 3, 
              borderRadius: 3,
              border: '1px solid #e2e8f0',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              textAlign: 'center'
            }}
          >
            <TrendingUp sx={{ fontSize: 40, mb: 1 }} />
            <Typography variant="h4" fontWeight="bold">
              {filteredPosts.length}
            </Typography>
            <Typography variant="body2" sx={{ opacity: 0.9 }}>
              Publicaciones
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper 
            elevation={0} 
            sx={{ 
              p: 3, 
              borderRadius: 3,
              border: '1px solid #e2e8f0',
              background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
              color: 'white',
              textAlign: 'center'
            }}
          >
            <Visibility sx={{ fontSize: 40, mb: 1 }} />
            <Typography variant="h4" fontWeight="bold">
              {filteredPosts.reduce((total, post) => total + (post.views_count || 0), 0)}
            </Typography>
            <Typography variant="body2" sx={{ opacity: 0.9 }}>
              Visualizaciones
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper 
            elevation={0} 
            sx={{ 
              p: 3, 
              borderRadius: 3,
              border: '1px solid #e2e8f0',
              background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
              color: 'white',
              textAlign: 'center'
            }}
          >
            <Favorite sx={{ fontSize: 40, mb: 1 }} />
            <Typography variant="h4" fontWeight="bold">
              {filteredPosts.reduce((total, post) => total + (post.likes?.length || 0), 0)}
            </Typography>
            <Typography variant="body2" sx={{ opacity: 0.9 }}>
              Likes Totales
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Paper 
            elevation={0} 
            sx={{ 
              p: 3, 
              borderRadius: 3,
              border: '1px solid #e2e8f0',
              background: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
              color: 'white',
              textAlign: 'center'
            }}
          >
            <Person sx={{ fontSize: 40, mb: 1 }} />
            <Typography variant="h4" fontWeight="bold">
              {new Set(filteredPosts.map(post => post.author_id)).size}
            </Typography>
            <Typography variant="body2" sx={{ opacity: 0.9 }}>
              Autores Únicos
            </Typography>
          </Paper>
        </Grid>
      </Grid>

      {/* Posts */}
      {filteredPosts.length === 0 ? (
        <Paper 
          elevation={0} 
          sx={{ 
            p: 8, 
            textAlign: 'center',
            borderRadius: 3,
            border: '1px solid #e2e8f0',
            background: 'white'
          }}
        >
          <Box sx={{ mb: 3 }}>
            <Search sx={{ fontSize: 80, color: 'text.secondary', mb: 2 }} />
            <Typography variant="h5" color="text.secondary" gutterBottom>
              {searchTerm ? 'No se encontraron publicaciones' : 'No hay publicaciones disponibles'}
            </Typography>
            <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
              {searchTerm 
                ? 'Intenta con otros términos de búsqueda' 
                : 'Sé el primero en crear una publicación'
              }
            </Typography>
            {isOrganizer && !searchTerm && (
              <Button
                variant="contained"
                startIcon={<Add />}
                onClick={() => navigate('/create-post')}
                sx={{
                  borderRadius: 2,
                  px: 3,
                  py: 1.5,
                  textTransform: 'none',
                  fontWeight: 600,
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  '&:hover': {
                    background: 'linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%)',
                    transform: 'translateY(-2px)',
                    boxShadow: '0px 8px 16px rgba(102, 126, 234, 0.3)',
                  },
                }}
              >
                Crear primera publicación
              </Button>
            )}
          </Box>
        </Paper>
      ) : (
        <Box>
          {filteredPosts.map((post) => (
            <PostCard key={post.id} post={post} />
          ))}
        </Box>
      )}

      {isOrganizer && (
        <Fab
          color="primary"
          aria-label="add"
          sx={{
            position: 'fixed',
            bottom: 24,
            right: 24,
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            '&:hover': {
              background: 'linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%)',
              transform: 'scale(1.1)',
              boxShadow: '0px 8px 16px rgba(102, 126, 234, 0.3)',
            },
          }}
          onClick={() => navigate('/create-post')}
        >
          <Add />
        </Fab>
      )}

      <Dialog
        open={deleteDialog.open}
        onClose={() => setDeleteDialog({ open: false, post: null })}
        PaperProps={{
          sx: {
            borderRadius: 3,
            maxWidth: 400,
          }
        }}
      >
        <DialogTitle sx={{ pb: 1 }}>
          <Typography variant="h6" fontWeight="600">
            Confirmar eliminación
          </Typography>
        </DialogTitle>
        <DialogContent sx={{ pb: 2 }}>
          <Typography variant="body1" color="text.secondary">
            ¿Estás seguro de que deseas eliminar la publicación "{deleteDialog.post?.title}"? 
            Esta acción no se puede deshacer.
          </Typography>
        </DialogContent>
        <DialogActions sx={{ p: 3, pt: 1 }}>
          <Button 
            onClick={() => setDeleteDialog({ open: false, post: null })}
            variant="outlined"
            sx={{ borderRadius: 2, textTransform: 'none', fontWeight: 600 }}
          >
            Cancelar
          </Button>
          <Button 
            onClick={handleDeletePost} 
            color="error" 
            variant="contained"
            sx={{ 
              borderRadius: 2, 
              textTransform: 'none', 
              fontWeight: 600,
              background: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
              '&:hover': {
                background: 'linear-gradient(135deg, #dc2626 0%, #b91c1c 100%)',
              }
            }}
          >
            Eliminar
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Dashboard; 