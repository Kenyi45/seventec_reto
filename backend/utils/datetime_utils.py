from datetime import datetime, timedelta
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class DateTimeFormatter:
    """
    DateTime formatter class for formatting dates and times.
    Follows Single Responsibility Principle (SRP).
    """
    
    @staticmethod
    def format_relative_time(dt: datetime, reference_time: Optional[datetime] = None) -> str:
        """
        Format datetime as relative time (e.g., "2 hours ago", "3 days ago").
        """
        try:
            if reference_time is None:
                reference_time = datetime.utcnow()
            
            diff = reference_time - dt
            
            if diff.days < 0:
                return "En el futuro"
            elif diff.days == 0:
                # Same day
                if diff.seconds < 60:
                    return "Ahora mismo"
                elif diff.seconds < 3600:
                    minutes = diff.seconds // 60
                    return f"Hace {minutes} minuto{'s' if minutes != 1 else ''}"
                else:
                    hours = diff.seconds // 3600
                    return f"Hace {hours} hora{'s' if hours != 1 else ''}"
            elif diff.days == 1:
                return "Ayer"
            elif diff.days < 7:
                return f"Hace {diff.days} día{'s' if diff.days != 1 else ''}"
            elif diff.days < 30:
                weeks = diff.days // 7
                return f"Hace {weeks} semana{'s' if weeks != 1 else ''}"
            elif diff.days < 365:
                months = diff.days // 30
                return f"Hace {months} mes{'es' if months != 1 else ''}"
            else:
                years = diff.days // 365
                return f"Hace {years} año{'s' if years != 1 else ''}"
                
        except Exception as e:
            logger.error(f"Error formatting relative time: {e}")
            return "Fecha desconocida"
    
    @staticmethod
    def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """Format datetime as string"""
        try:
            return dt.strftime(format_str)
        except Exception as e:
            logger.error(f"Error formatting datetime: {e}")
            return "Fecha inválida"
    
    @staticmethod
    def format_date(dt: datetime, format_str: str = "%Y-%m-%d") -> str:
        """Format date as string"""
        try:
            return dt.strftime(format_str)
        except Exception as e:
            logger.error(f"Error formatting date: {e}")
            return "Fecha inválida"
    
    @staticmethod
    def format_time(dt: datetime, format_str: str = "%H:%M:%S") -> str:
        """Format time as string"""
        try:
            return dt.strftime(format_str)
        except Exception as e:
            logger.error(f"Error formatting time: {e}")
            return "Hora inválida"
    
    @staticmethod
    def format_time_remaining(dt: datetime, reference_time: Optional[datetime] = None) -> str:
        """
        Format time remaining until a future datetime.
        """
        try:
            if reference_time is None:
                reference_time = datetime.utcnow()
            
            diff = dt - reference_time
            
            if diff.total_seconds() <= 0:
                return "Expirado"
            
            days = diff.days
            hours = diff.seconds // 3600
            minutes = (diff.seconds % 3600) // 60
            
            if days > 0:
                return f"{days} día{'s' if days != 1 else ''} restante{'s' if days != 1 else ''}"
            elif hours > 0:
                return f"{hours} hora{'s' if hours != 1 else ''} restante{'s' if hours != 1 else ''}"
            elif minutes > 0:
                return f"{minutes} minuto{'s' if minutes != 1 else ''} restante{'s' if minutes != 1 else ''}"
            else:
                return "Menos de un minuto"
                
        except Exception as e:
            logger.error(f"Error formatting time remaining: {e}")
            return "Tiempo desconocido"
    
    @staticmethod
    def is_recent(dt: datetime, hours: int = 24) -> bool:
        """Check if datetime is recent (within specified hours)"""
        try:
            now = datetime.utcnow()
            return (now - dt).total_seconds() < hours * 3600
        except Exception as e:
            logger.error(f"Error checking if datetime is recent: {e}")
            return False
    
    @staticmethod
    def is_expired(dt: datetime, reference_time: Optional[datetime] = None) -> bool:
        """Check if datetime has expired"""
        try:
            if reference_time is None:
                reference_time = datetime.utcnow()
            return dt < reference_time
        except Exception as e:
            logger.error(f"Error checking if datetime is expired: {e}")
            return True
    
    @staticmethod
    def add_hours(dt: datetime, hours: int) -> datetime:
        """Add hours to datetime"""
        try:
            return dt + timedelta(hours=hours)
        except Exception as e:
            logger.error(f"Error adding hours to datetime: {e}")
            return dt
    
    @staticmethod
    def add_days(dt: datetime, days: int) -> datetime:
        """Add days to datetime"""
        try:
            return dt + timedelta(days=days)
        except Exception as e:
            logger.error(f"Error adding days to datetime: {e}")
            return dt
    
    @staticmethod
    def get_start_of_day(dt: datetime) -> datetime:
        """Get start of day for datetime"""
        try:
            return dt.replace(hour=0, minute=0, second=0, microsecond=0)
        except Exception as e:
            logger.error(f"Error getting start of day: {e}")
            return dt
    
    @staticmethod
    def get_end_of_day(dt: datetime) -> datetime:
        """Get end of day for datetime"""
        try:
            return dt.replace(hour=23, minute=59, second=59, microsecond=999999)
        except Exception as e:
            logger.error(f"Error getting end of day: {e}")
            return dt


class DateTimeValidator:
    """
    DateTime validator class for validating dates and times.
    Follows Single Responsibility Principle (SRP).
    """
    
    @staticmethod
    def is_valid_datetime(dt_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> bool:
        """Validate datetime string"""
        try:
            datetime.strptime(dt_str, format_str)
            return True
        except ValueError:
            return False
        except Exception as e:
            logger.error(f"Error validating datetime: {e}")
            return False
    
    @staticmethod
    def is_valid_date(date_str: str, format_str: str = "%Y-%m-%d") -> bool:
        """Validate date string"""
        try:
            datetime.strptime(date_str, format_str)
            return True
        except ValueError:
            return False
        except Exception as e:
            logger.error(f"Error validating date: {e}")
            return False
    
    @staticmethod
    def is_future_datetime(dt: datetime, reference_time: Optional[datetime] = None) -> bool:
        """Check if datetime is in the future"""
        try:
            if reference_time is None:
                reference_time = datetime.utcnow()
            return dt > reference_time
        except Exception as e:
            logger.error(f"Error checking if datetime is in future: {e}")
            return False
    
    @staticmethod
    def is_within_range(dt: datetime, start: datetime, end: datetime) -> bool:
        """Check if datetime is within range"""
        try:
            return start <= dt <= end
        except Exception as e:
            logger.error(f"Error checking if datetime is within range: {e}")
            return False


# Utility functions for convenience
def format_relative_time(dt: datetime, reference_time: Optional[datetime] = None) -> str:
    """Convenience function for formatting relative time"""
    return DateTimeFormatter.format_relative_time(dt, reference_time)


def format_time_remaining(dt: datetime, reference_time: Optional[datetime] = None) -> str:
    """Convenience function for formatting time remaining"""
    return DateTimeFormatter.format_time_remaining(dt, reference_time)


def is_recent(dt: datetime, hours: int = 24) -> bool:
    """Convenience function for checking if datetime is recent"""
    return DateTimeFormatter.is_recent(dt, hours)


def is_expired(dt: datetime, reference_time: Optional[datetime] = None) -> bool:
    """Convenience function for checking if datetime is expired"""
    return DateTimeFormatter.is_expired(dt, reference_time) 