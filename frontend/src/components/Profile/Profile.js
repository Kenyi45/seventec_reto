import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  TextField,
  Button,
  Avatar,
  Divider,
  Alert,
} from '@mui/material';
import { Save, Edit, Person } from '@mui/icons-material';
import { useAuth } from '../../contexts/AuthContext';
import { useNotification } from '../../contexts/NotificationContext';

const Profile = () => {
  const { user, updateProfile } = useAuth();
  const { showSuccess, showError } = useNotification();
  const [editing, setEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: user?.name || '',
    email: user?.email || '',
    phone: user?.phone || '',
    department: user?.department || '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await updateProfile(formData);
      setEditing(false);
      showSuccess('Perfil actualizado correctamente');
    } catch (error) {
      showError('Error al actualizar el perfil');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    setFormData({
      name: user?.name || '',
      email: user?.email || '',
      phone: user?.phone || '',
      department: user?.department || '',
    });
    setEditing(false);
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Mi Perfil
      </Typography>

      <Paper elevation={2} sx={{ p: 3, maxWidth: 600 }}>
        <Box display="flex" alignItems="center" gap={3} mb={3}>
          <Avatar sx={{ width: 80, height: 80, fontSize: '2rem' }}>
            {user?.name?.[0]?.toUpperCase()}
          </Avatar>
          <Box>
            <Typography variant="h5">
              {user?.name}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {user?.role === 'organizer' ? 'Organizador' : 'Participante'}
            </Typography>
          </Box>
        </Box>

        <Divider sx={{ mb: 3 }} />

        <Box component="form" onSubmit={handleSubmit}>
          <TextField
            fullWidth
            label="Nombre completo"
            name="name"
            value={formData.name}
            onChange={handleChange}
            disabled={!editing}
            margin="normal"
            InputProps={{
              startAdornment: <Person sx={{ color: 'text.secondary', mr: 1 }} />,
            }}
          />

          <TextField
            fullWidth
            label="Correo electrónico"
            name="email"
            value={formData.email}
            onChange={handleChange}
            disabled={true} // Email usually shouldn't be editable
            margin="normal"
            helperText="El correo electrónico no se puede modificar"
          />

          <TextField
            fullWidth
            label="Teléfono"
            name="phone"
            value={formData.phone}
            onChange={handleChange}
            disabled={!editing}
            margin="normal"
          />

          <TextField
            fullWidth
            label="Departamento"
            name="department"
            value={formData.department}
            onChange={handleChange}
            disabled={!editing}
            margin="normal"
          />

          <Box display="flex" gap={2} justifyContent="flex-end" mt={3}>
            {editing ? (
              <>
                <Button
                  variant="outlined"
                  onClick={handleCancel}
                  disabled={loading}
                >
                  Cancelar
                </Button>
                <Button
                  type="submit"
                  variant="contained"
                  disabled={loading}
                  startIcon={<Save />}
                >
                  {loading ? 'Guardando...' : 'Guardar Cambios'}
                </Button>
              </>
            ) : (
              <Button
                variant="contained"
                onClick={() => setEditing(true)}
                startIcon={<Edit />}
              >
                Editar Perfil
              </Button>
            )}
          </Box>
        </Box>
      </Paper>
    </Box>
  );
};

export default Profile; 