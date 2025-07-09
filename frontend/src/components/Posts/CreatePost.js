import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Paper,
  Typography,
  TextField,
  Button,
  Chip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  Divider,
} from '@mui/material';
import { Save, Cancel, Add } from '@mui/icons-material';
import postService from '../../services/postService';
import { useAuth } from '../../contexts/AuthContext';
import { useNotification } from '../../contexts/NotificationContext';

const CreatePost = () => {
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    tags: [],
    event_type: '',
  });
  const [newTag, setNewTag] = useState('');
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  const { user, isOrganizer } = useAuth();
  const { showSuccess, showError } = useNotification();
  const navigate = useNavigate();

  // Redirect if not organizer
  if (!isOrganizer) {
    navigate('/');
    return null;
  }

  const eventTypes = [
    'Conferencia',
    'Workshop',
    'Seminario',
    'Networking',
    'Reunión',
    'Capacitación',
    'Lanzamiento',
    'Otro',
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: '',
      }));
    }
  };

  const handleAddTag = () => {
    if (newTag.trim() && !formData.tags.includes(newTag.trim())) {
      setFormData(prev => ({
        ...prev,
        tags: [...prev.tags, newTag.trim()],
      }));
      setNewTag('');
    }
  };

  const handleRemoveTag = (tagToRemove) => {
    setFormData(prev => ({
      ...prev,
      tags: prev.tags.filter(tag => tag !== tagToRemove),
    }));
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddTag();
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.title.trim()) newErrors.title = 'El título es requerido';
    if (!formData.content.trim()) newErrors.content = 'El contenido es requerido';
    if (!formData.event_type) newErrors.event_type = 'El tipo de evento es requerido';
    if (formData.title.length > 100) newErrors.title = 'El título no puede exceder 100 caracteres';
    if (formData.content.length > 2000) newErrors.content = 'El contenido no puede exceder 2000 caracteres';

    return newErrors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = validateForm();
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setLoading(true);
    setErrors({});

    try {
      const postData = {
        ...formData,
        title: formData.title.trim(),
        content: formData.content.trim(),
      };
      
      const newPost = await postService.createPost(postData);
      showSuccess('Publicación creada exitosamente');
      navigate('/');
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Error al crear la publicación';
      showError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    navigate('/');
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Crear Nueva Publicación
      </Typography>
      
      <Paper elevation={2} sx={{ p: 3 }}>
        <Box component="form" onSubmit={handleSubmit}>
          <TextField
            fullWidth
            required
            label="Título del evento"
            name="title"
            value={formData.title}
            onChange={handleChange}
            error={!!errors.title}
            helperText={errors.title}
            margin="normal"
            placeholder="Ej: Conferencia sobre Innovación Tecnológica"
          />

          <FormControl fullWidth margin="normal" error={!!errors.event_type}>
            <InputLabel>Tipo de evento *</InputLabel>
            <Select
              name="event_type"
              value={formData.event_type}
              label="Tipo de evento *"
              onChange={handleChange}
            >
              {eventTypes.map((type) => (
                <MenuItem key={type} value={type}>
                  {type}
                </MenuItem>
              ))}
            </Select>
            {errors.event_type && (
              <Typography variant="caption" color="error" sx={{ mt: 1 }}>
                {errors.event_type}
              </Typography>
            )}
          </FormControl>

          <TextField
            fullWidth
            required
            multiline
            rows={6}
            label="Descripción del evento"
            name="content"
            value={formData.content}
            onChange={handleChange}
            error={!!errors.content}
            helperText={errors.content}
            margin="normal"
            placeholder="Describe el evento, fecha, lugar, objetivos, etc."
          />

          <Divider sx={{ my: 2 }} />

          <Typography variant="h6" gutterBottom>
            Etiquetas (Tags)
          </Typography>
          
          <Box display="flex" gap={1} mb={2}>
            <TextField
              label="Agregar etiqueta"
              value={newTag}
              onChange={(e) => setNewTag(e.target.value)}
              onKeyPress={handleKeyPress}
              size="small"
              placeholder="Ej: tecnología, networking"
            />
            <Button
              variant="outlined"
              onClick={handleAddTag}
              disabled={!newTag.trim()}
              startIcon={<Add />}
            >
              Agregar
            </Button>
          </Box>

          <Box display="flex" gap={1} flexWrap="wrap" mb={2}>
            {formData.tags.map((tag) => (
              <Chip
                key={tag}
                label={tag}
                onDelete={() => handleRemoveTag(tag)}
                color="primary"
                variant="outlined"
              />
            ))}
          </Box>

          <Divider sx={{ my: 2 }} />

          <Box display="flex" gap={2} justifyContent="flex-end">
            <Button
              variant="outlined"
              onClick={handleCancel}
              disabled={loading}
              startIcon={<Cancel />}
            >
              Cancelar
            </Button>
            <Button
              type="submit"
              variant="contained"
              disabled={loading}
              startIcon={<Save />}
            >
              {loading ? 'Creando...' : 'Crear Publicación'}
            </Button>
          </Box>
        </Box>
      </Paper>
    </Box>
  );
};

export default CreatePost; 