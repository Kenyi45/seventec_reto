import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#2563eb', // Blue-600
      light: '#3b82f6', // Blue-500
      dark: '#1d4ed8', // Blue-700
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#7c3aed', // Violet-600
      light: '#8b5cf6', // Violet-500
      dark: '#6d28d9', // Violet-700
      contrastText: '#ffffff',
    },
    success: {
      main: '#10b981', // Emerald-500
      light: '#34d399', // Emerald-400
      dark: '#059669', // Emerald-600
    },
    warning: {
      main: '#f59e0b', // Amber-500
      light: '#fbbf24', // Amber-400
      dark: '#d97706', // Amber-600
    },
    error: {
      main: '#ef4444', // Red-500
      light: '#f87171', // Red-400
      dark: '#dc2626', // Red-600
    },
    info: {
      main: '#06b6d4', // Cyan-500
      light: '#22d3ee', // Cyan-400
      dark: '#0891b2', // Cyan-600
    },
    background: {
      default: '#f8fafc', // Slate-50
      paper: '#ffffff',
    },
    text: {
      primary: '#1e293b', // Slate-800
      secondary: '#64748b', // Slate-500
    },
    divider: '#e2e8f0', // Slate-200
  },
  typography: {
    fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 700,
      lineHeight: 1.2,
      letterSpacing: '-0.025em',
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
      lineHeight: 1.3,
      letterSpacing: '-0.025em',
    },
    h3: {
      fontSize: '1.5rem',
      fontWeight: 600,
      lineHeight: 1.4,
      letterSpacing: '-0.025em',
    },
    h4: {
      fontSize: '1.25rem',
      fontWeight: 600,
      lineHeight: 1.4,
      letterSpacing: '-0.025em',
    },
    h5: {
      fontSize: '1.125rem',
      fontWeight: 600,
      lineHeight: 1.4,
      letterSpacing: '-0.025em',
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 600,
      lineHeight: 1.4,
      letterSpacing: '-0.025em',
    },
    body1: {
      fontSize: '1rem',
      lineHeight: 1.6,
      letterSpacing: '0.025em',
    },
    body2: {
      fontSize: '0.875rem',
      lineHeight: 1.6,
      letterSpacing: '0.025em',
    },
    button: {
      fontSize: '0.875rem',
      fontWeight: 600,
      textTransform: 'none',
      letterSpacing: '0.025em',
    },
    caption: {
      fontSize: '0.75rem',
      lineHeight: 1.5,
      letterSpacing: '0.025em',
    },
  },
  shape: {
    borderRadius: 12,
  },
  shadows: [
    'none',
    '0px 1px 2px rgba(0, 0, 0, 0.05)',
    '0px 1px 3px rgba(0, 0, 0, 0.1), 0px 1px 2px rgba(0, 0, 0, 0.06)',
    '0px 4px 6px rgba(0, 0, 0, 0.1), 0px 2px 4px rgba(0, 0, 0, 0.06)',
    '0px 10px 15px rgba(0, 0, 0, 0.1), 0px 4px 6px rgba(0, 0, 0, 0.05)',
    '0px 20px 25px rgba(0, 0, 0, 0.1), 0px 10px 10px rgba(0, 0, 0, 0.04)',
    '0px 25px 50px rgba(0, 0, 0, 0.1), 0px 10px 20px rgba(0, 0, 0, 0.04)',
    '0px 35px 60px rgba(0, 0, 0, 0.1), 0px 15px 25px rgba(0, 0, 0, 0.04)',
    '0px 45px 70px rgba(0, 0, 0, 0.1), 0px 20px 30px rgba(0, 0, 0, 0.04)',
    '0px 55px 80px rgba(0, 0, 0, 0.1), 0px 25px 35px rgba(0, 0, 0, 0.04)',
    '0px 65px 90px rgba(0, 0, 0, 0.1), 0px 30px 40px rgba(0, 0, 0, 0.04)',
    '0px 75px 100px rgba(0, 0, 0, 0.1), 0px 35px 45px rgba(0, 0, 0, 0.04)',
    '0px 85px 110px rgba(0, 0, 0, 0.1), 0px 40px 50px rgba(0, 0, 0, 0.04)',
    '0px 95px 120px rgba(0, 0, 0, 0.1), 0px 45px 55px rgba(0, 0, 0, 0.04)',
    '0px 105px 130px rgba(0, 0, 0, 0.1), 0px 50px 60px rgba(0, 0, 0, 0.04)',
    '0px 115px 140px rgba(0, 0, 0, 0.1), 0px 55px 65px rgba(0, 0, 0, 0.04)',
    '0px 125px 150px rgba(0, 0, 0, 0.1), 0px 60px 70px rgba(0, 0, 0, 0.04)',
    '0px 135px 160px rgba(0, 0, 0, 0.1), 0px 65px 75px rgba(0, 0, 0, 0.04)',
    '0px 145px 170px rgba(0, 0, 0, 0.1), 0px 70px 80px rgba(0, 0, 0, 0.04)',
    '0px 155px 180px rgba(0, 0, 0, 0.1), 0px 75px 85px rgba(0, 0, 0, 0.04)',
    '0px 165px 190px rgba(0, 0, 0, 0.1), 0px 80px 90px rgba(0, 0, 0, 0.04)',
    '0px 175px 200px rgba(0, 0, 0, 0.1), 0px 85px 95px rgba(0, 0, 0, 0.04)',
    '0px 185px 210px rgba(0, 0, 0, 0.1), 0px 90px 100px rgba(0, 0, 0, 0.04)',
    '0px 195px 220px rgba(0, 0, 0, 0.1), 0px 95px 105px rgba(0, 0, 0, 0.04)',
    '0px 205px 230px rgba(0, 0, 0, 0.1), 0px 100px 110px rgba(0, 0, 0, 0.04)',
  ],
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          padding: '10px 24px',
          fontSize: '0.875rem',
          fontWeight: 600,
          textTransform: 'none',
          boxShadow: 'none',
          '&:hover': {
            boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.1)',
          },
        },
        contained: {
          '&:hover': {
            boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.15)',
          },
        },
        outlined: {
          borderWidth: '2px',
          '&:hover': {
            borderWidth: '2px',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.05), 0px 1px 3px rgba(0, 0, 0, 0.1)',
          border: '1px solid rgba(0, 0, 0, 0.05)',
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0px 1px 3px rgba(0, 0, 0, 0.1), 0px 1px 2px rgba(0, 0, 0, 0.06)',
        },
        elevation1: {
          boxShadow: '0px 1px 3px rgba(0, 0, 0, 0.1), 0px 1px 2px rgba(0, 0, 0, 0.06)',
        },
        elevation2: {
          boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1), 0px 2px 4px rgba(0, 0, 0, 0.06)',
        },
        elevation3: {
          boxShadow: '0px 10px 15px rgba(0, 0, 0, 0.1), 0px 4px 6px rgba(0, 0, 0, 0.05)',
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 8,
            '&:hover .MuiOutlinedInput-notchedOutline': {
              borderColor: '#2563eb',
            },
            '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
              borderColor: '#2563eb',
              borderWidth: '2px',
            },
          },
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          boxShadow: '0px 1px 3px rgba(0, 0, 0, 0.1), 0px 1px 2px rgba(0, 0, 0, 0.06)',
          backgroundColor: '#ffffff',
          color: '#1e293b',
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          backgroundColor: '#ffffff',
          borderRight: '1px solid #e2e8f0',
        },
      },
    },
    MuiListItem: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          margin: '4px 8px',
          '&:hover': {
            backgroundColor: '#f1f5f9',
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 20,
          fontWeight: 500,
        },
      },
    },
    MuiFab: {
      styleOverrides: {
        root: {
          boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.15)',
          '&:hover': {
            boxShadow: '0px 6px 12px rgba(0, 0, 0, 0.2)',
          },
        },
      },
    },
  },
});

export default theme; 