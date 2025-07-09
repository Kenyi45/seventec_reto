import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Paper,
  Button,
  TextField,
  Avatar,
  Divider,
  Chip,
  IconButton,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  ArrowBack,
  Favorite,
  FavoriteBorder,
  Send,
  Edit,
  Delete,
} from '@mui/icons-material';
import { formatDistanceToNow } from 'date-fns';
import { es } from 'date-fns/locale';
import postService from '../../services/postService';
import { useAuth } from '../../contexts/AuthContext';
import { useNotification } from '../../contexts/NotificationContext';

const PostDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [post, setPost] = useState(null);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const { user } = useAuth();
  const { showSuccess, showError } = useNotification();

  useEffect(() => {
    loadPost();
    loadComments();
  }, [id]);

  const loadPost = async () => {
    try {
      const response = await postService.getPost(id);
      if (response.success) {
        setPost(response.data);
      } else {
        showError(response.error || 'Error al cargar la publicación');
        navigate('/');
      }
    } catch (error) {
      showError('Error al cargar la publicación');
      navigate('/');
    } finally {
      setLoading(false);
    }
  };

  const loadComments = async () => {
    try {
      const response = await postService.getPostComments(id);
      if (response.success) {
        setComments(response.data);
      } else {
        showError(response.error || 'Error al cargar los comentarios');
      }
    } catch (error) {
      showError('Error al cargar los comentarios');
    }
  };

  const handleLike = async () => {
    try {
      console.log('Handling like for post:', id, 'User:', user?.id);
      
      // Verificar que el usuario esté autenticado
      if (!user?.id) {
        showError('Debes estar autenticado para dar like');
        return;
      }
      
      const response = await postService.toggleLike(id);
      console.log('Toggle like response:', response);
      
      if (response.success) {
        // Asegurar que post.likes sea un array
        const currentLikes = post.likes || [];
        const isLiked = currentLikes.includes(user.id);
        
        // Si el like no existía (wasNotFound), asegurar que no esté en el array
        const newLikes = response.wasNotFound 
          ? currentLikes.filter(userId => userId !== user.id)
          : isLiked 
            ? currentLikes.filter(userId => userId !== user.id)
            : [...currentLikes, user.id];
        
        console.log('Updating post likes:', {
          postId: id,
          oldLikes: currentLikes,
          newLikes,
          isLiked,
          wasNotFound: response.wasNotFound,
          userId: user.id
        });
        
        setPost(prev => ({
          ...prev,
          likes: newLikes,
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

  const handleAddComment = async (e) => {
    e.preventDefault();
    if (!newComment.trim()) return;

    setSubmitting(true);
    try {
      const response = await postService.addComment(id, { content: newComment });
      if (response.success) {
        setComments(prev => [response.data, ...prev]);
        setNewComment('');
        showSuccess('Comentario agregado');
      } else {
        showError(response.error || 'Error al agregar comentario');
      }
    } catch (error) {
      showError('Error al agregar comentario');
    } finally {
      setSubmitting(false);
    }
  };

  const handleDeleteComment = async (commentId) => {
    try {
      const response = await postService.deleteComment(commentId);
      if (response.success) {
        setComments(prev => prev.filter(comment => comment.id !== commentId));
        showSuccess('Comentario eliminado');
      } else {
        showError(response.error || 'Error al eliminar comentario');
      }
    } catch (error) {
      showError('Error al eliminar comentario');
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress size={60} />
      </Box>
    );
  }

  if (!post) {
    return (
      <Alert severity="error">
        No se pudo cargar la publicación
      </Alert>
    );
  }

  const isLiked = post.likes?.includes(user.id);
  const isOwner = post.author_id === user.id;

  return (
    <Box>
      <Box display="flex" alignItems="center" mb={3}>
        <IconButton onClick={() => navigate('/')} sx={{ mr: 2 }}>
          <ArrowBack />
        </IconButton>
        <Typography variant="h4" component="h1">
          Detalle de Publicación
        </Typography>
      </Box>

      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Box display="flex" alignItems="center" justifyContent="space-between" mb={3}>
          <Box display="flex" alignItems="center" gap={2}>
            <Avatar>
              {post.author_name?.[0]?.toUpperCase()}
            </Avatar>
            <Box>
              <Typography variant="h6">
                {post.author_name}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {formatDistanceToNow(new Date(post.created_at), { addSuffix: true, locale: es })}
              </Typography>
            </Box>
          </Box>
          {isOwner && (
            <Box>
              <IconButton onClick={() => navigate(`/posts/${post.id}/edit`)}>
                <Edit />
              </IconButton>
            </Box>
          )}
        </Box>

        <Typography variant="h5" gutterBottom>
          {post.title}
        </Typography>

        <Typography variant="body1" paragraph>
          {post.content}
        </Typography>

        {post.tags && post.tags.length > 0 && (
          <Box display="flex" gap={1} flexWrap="wrap" mb={3}>
            {post.tags.map((tag, index) => (
              <Chip key={index} label={tag} size="small" />
            ))}
          </Box>
        )}

        <Box display="flex" alignItems="center" gap={2}>
          <Button
            variant={isLiked ? 'contained' : 'outlined'}
            color="error"
            startIcon={isLiked ? <Favorite /> : <FavoriteBorder />}
            onClick={handleLike}
          >
            {post.likes?.length || 0} Likes
          </Button>
          <Typography variant="body2" color="text.secondary">
            {comments.length} comentarios
          </Typography>
        </Box>
      </Paper>

      <Paper elevation={2} sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Comentarios
        </Typography>

        <Box component="form" onSubmit={handleAddComment} mb={3}>
          <TextField
            fullWidth
            multiline
            rows={3}
            placeholder="Escribe un comentario..."
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            sx={{ mb: 2 }}
          />
          <Button
            type="submit"
            variant="contained"
            disabled={!newComment.trim() || submitting}
            startIcon={<Send />}
          >
            {submitting ? 'Enviando...' : 'Comentar'}
          </Button>
        </Box>

        <Divider sx={{ mb: 2 }} />

        {comments.length === 0 ? (
          <Typography variant="body2" color="text.secondary" textAlign="center" py={4}>
            No hay comentarios aún. ¡Sé el primero en comentar!
          </Typography>
        ) : (
          <Box>
            {comments.map((comment) => (
              <Box key={comment.id} mb={2}>
                <Box display="flex" alignItems="center" justifyContent="space-between" mb={1}>
                  <Box display="flex" alignItems="center" gap={2}>
                    <Avatar size="small">
                      {comment.author_name?.[0]?.toUpperCase()}
                    </Avatar>
                    <Box>
                      <Typography variant="subtitle2">
                        {comment.author_name}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {formatDistanceToNow(new Date(comment.created_at), { addSuffix: true, locale: es })}
                      </Typography>
                    </Box>
                  </Box>
                  {comment.author_id === user.id && (
                    <IconButton 
                      size="small" 
                      onClick={() => handleDeleteComment(comment.id)}
                    >
                      <Delete />
                    </IconButton>
                  )}
                </Box>
                <Typography variant="body2" sx={{ ml: 6 }}>
                  {comment.content}
                </Typography>
                <Divider sx={{ mt: 2 }} />
              </Box>
            ))}
          </Box>
        )}
      </Paper>
    </Box>
  );
};

export default PostDetail; 