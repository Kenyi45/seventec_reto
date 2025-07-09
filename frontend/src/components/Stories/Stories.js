import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  TextField,
  Avatar,
  Card,
  CardContent,
  Grid,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  CircularProgress,
  Fab,
  Alert,
} from '@mui/material';
import { Add, Visibility, AccessTime, Delete } from '@mui/icons-material';
import { formatDistanceToNow } from 'date-fns';
import { es } from 'date-fns/locale';
import { useAuth } from '../../contexts/AuthContext';
import { useNotification } from '../../contexts/NotificationContext';
import storyService from '../../services/storyService';

const Stories = () => {
  const [stories, setStories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [createDialog, setCreateDialog] = useState(false);
  const [selectedStory, setSelectedStory] = useState(null);
  const [newStory, setNewStory] = useState({
    content: '',
    image_url: '',
  });
  const { user, isOrganizer, isAuthenticated } = useAuth();
  const { showSuccess, showError } = useNotification();

  useEffect(() => {
    loadStories();
  }, []);

  const loadStories = async () => {
    try {
      setLoading(true);
      const result = await storyService.getStories();
      
      if (result.success) {
        setStories(result.data);
      } else {
        showError(result.error);
      }
    } catch (error) {
      showError('Error al cargar las historias');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateStory = async () => {
    try {
      const result = await storyService.createStory(newStory);
      
      if (result.success) {
        setStories(prev => [result.data, ...prev]);
        setNewStory({ content: '', image_url: '' });
        setCreateDialog(false);
        showSuccess('Historia creada exitosamente');
      } else {
        showError(result.error);
      }
    } catch (error) {
      showError('Error al crear la historia');
    }
  };

  const handleViewStory = async (story) => {
    try {
      console.log('Viewing story:', story);
      console.log('Story ID:', story.id);
      console.log('Story ID type:', typeof story.id);
      
      // Incrementar vista
      const result = await storyService.viewStory(story.id);
      
      if (result.success) {
        setStories(prev => prev.map(s => 
          s.id === story.id 
            ? { ...s, views_count: s.views_count + 1 }
            : s
        ));
        setSelectedStory(story);
      } else {
        showError(result.error);
      }
    } catch (error) {
      console.error('Error viewing story:', error);
      showError('Error al ver la historia');
    }
  };

  const handleDeleteStory = async (storyId) => {
    try {
      const result = await storyService.deleteStory(storyId);
      
      if (result.success) {
        setStories(prev => prev.filter(s => s.id !== storyId));
        showSuccess('Historia eliminada');
      } else {
        showError(result.error);
      }
    } catch (error) {
      showError('Error al eliminar la historia');
    }
  };

  const getTimeRemaining = (expiresAt) => {
    const now = new Date();
    const expiry = new Date(expiresAt);
    const hoursRemaining = Math.max(0, Math.ceil((expiry - now) / (1000 * 60 * 60)));
    return hoursRemaining;
  };

  const StoryCard = ({ story }) => {
    const isOwner = story.author_id === user?.id;
    const hoursRemaining = getTimeRemaining(story.expires_at);

    return (
      <Card elevation={2} sx={{ cursor: 'pointer', position: 'relative' }}>
        <CardContent>
          <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
            <Box display="flex" alignItems="center" gap={2}>
              <Avatar size="small">
                {story.author_name?.[0]?.toUpperCase()}
              </Avatar>
              <Box>
                <Typography variant="subtitle2">
                  {story.author_name}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  {formatDistanceToNow(new Date(story.created_at), { addSuffix: true, locale: es })}
                </Typography>
              </Box>
            </Box>
            {(isOwner || isOrganizer) && (
              <Button
                size="small"
                onClick={(e) => {
                  e.stopPropagation();
                  handleDeleteStory(story.id);
                }}
                startIcon={<Delete />}
              >
                Eliminar
              </Button>
            )}
          </Box>
          
          <Typography variant="body2" color="text.secondary" paragraph>
            {story.content?.length > 100 
              ? `${story.content.substring(0, 100)}...` 
              : story.content}
          </Typography>
          
          {story.image_url && (
            <Box mb={2}>
              <img 
                src={story.image_url} 
                alt="Story" 
                style={{ width: '100%', maxHeight: 200, objectFit: 'cover', borderRadius: 8 }}
              />
            </Box>
          )}
          
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Chip 
              icon={<AccessTime />}
              label={`${hoursRemaining}h restantes`}
              size="small"
              color={hoursRemaining < 6 ? 'error' : 'primary'}
            />
            <Box display="flex" alignItems="center" gap={1}>
              <Visibility fontSize="small" />
              <Typography variant="caption">
                {story.views_count || 0}
              </Typography>
            </Box>
          </Box>
          
          <Button
            fullWidth
            variant="outlined"
            onClick={() => handleViewStory(story)}
            sx={{ mt: 2 }}
          >
            Ver historia completa
          </Button>
        </CardContent>
      </Card>
    );
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress size={60} />
      </Box>
    );
  }

  return (
    <Box>
      {/* Debug Information */}
      {process.env.NODE_ENV === 'development' && (
        <Alert severity="info" sx={{ mb: 2 }}>
          <Typography variant="body2">
            <strong>Debug Info:</strong><br />
            Autenticado: {isAuthenticated ? 'Sí' : 'No'}<br />
            Usuario: {user?.full_name || 'No disponible'}<br />
            Rol: {user?.role || 'No disponible'}<br />
            Es Organizador: {isOrganizer ? 'Sí' : 'No'}<br />
            ID Usuario: {user?.id || 'No disponible'}
          </Typography>
        </Alert>
      )}

      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          Historias
        </Typography>
        {isOrganizer && (
          <Button
            variant="contained"
            startIcon={<Add />}
            onClick={() => setCreateDialog(true)}
          >
            Nueva Historia
          </Button>
        )}
      </Box>

      <Typography variant="body2" color="text.secondary" paragraph>
        Las historias desaparecen automáticamente después de 24 horas
      </Typography>

      {stories.length === 0 ? (
        <Box textAlign="center" py={8}>
          <Typography variant="h6" color="text.secondary">
            No hay historias disponibles
          </Typography>
          {isOrganizer && (
            <Button
              variant="contained"
              startIcon={<Add />}
              onClick={() => setCreateDialog(true)}
              sx={{ mt: 2 }}
            >
              Crear primera historia
            </Button>
          )}
        </Box>
      ) : (
        <Grid container spacing={3}>
          {stories.map((story) => (
            <Grid item xs={12} sm={6} md={4} key={story.id}>
              <StoryCard story={story} />
            </Grid>
          ))}
        </Grid>
      )}

      {isOrganizer && (
        <Fab
          color="primary"
          aria-label="add story"
          sx={{
            position: 'fixed',
            bottom: 16,
            right: 16,
          }}
          onClick={() => setCreateDialog(true)}
        >
          <Add />
        </Fab>
      )}

      {/* Dialog para crear historia */}
      <Dialog
        open={createDialog}
        onClose={() => setCreateDialog(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Crear Nueva Historia</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Contenido"
            fullWidth
            multiline
            rows={4}
            variant="outlined"
            value={newStory.content}
            onChange={(e) => setNewStory(prev => ({ ...prev, content: e.target.value }))}
            sx={{ mb: 2 }}
          />
          <TextField
            margin="dense"
            label="URL de la imagen (opcional)"
            fullWidth
            variant="outlined"
            value={newStory.image_url}
            onChange={(e) => setNewStory(prev => ({ ...prev, image_url: e.target.value }))}
            placeholder="https://example.com/image.jpg"
          />
          <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
            Esta historia será visible por 24 horas
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateDialog(false)}>
            Cancelar
          </Button>
          <Button
            onClick={handleCreateStory}
            variant="contained"
            disabled={!newStory.content}
          >
            Crear Historia
          </Button>
        </DialogActions>
      </Dialog>

      {/* Dialog para ver historia completa */}
      <Dialog
        open={!!selectedStory}
        onClose={() => setSelectedStory(null)}
        maxWidth="md"
        fullWidth
      >
        {selectedStory && (
          <>
            <DialogTitle>{selectedStory.title}</DialogTitle>
            <DialogContent>
              <Box display="flex" alignItems="center" gap={2} mb={2}>
                <Avatar>
                  {selectedStory.author_name?.[0]?.toUpperCase()}
                </Avatar>
                <Box>
                  <Typography variant="subtitle1">
                    {selectedStory.author_name}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {formatDistanceToNow(new Date(selectedStory.created_at), { addSuffix: true, locale: es })}
                  </Typography>
                </Box>
              </Box>
              <Typography variant="body1" paragraph>
                {selectedStory.content}
              </Typography>
              {selectedStory.image_url && (
                <Box mb={2}>
                  <img 
                    src={selectedStory.image_url} 
                    alt="Story" 
                    style={{ width: '100%', maxHeight: 200, objectFit: 'cover', borderRadius: 8 }}
                  />
                </Box>
              )}
              <Chip 
                icon={<AccessTime />}
                label={`${getTimeRemaining(selectedStory.expires_at)}h restantes`}
                size="small"
                color={getTimeRemaining(selectedStory.expires_at) < 6 ? 'error' : 'primary'}
              />
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setSelectedStory(null)}>
                Cerrar
              </Button>
            </DialogActions>
          </>
        )}
      </Dialog>
    </Box>
  );
};

export default Stories; 