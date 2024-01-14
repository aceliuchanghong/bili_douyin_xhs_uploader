class UploadError(Exception):
    """Base class for exceptions in this module."""
    pass


class LoginError(UploadError):
    """Raised when login to the platform fails."""
    pass


class VideoUploadError(UploadError):
    """Raised when the video upload fails."""
    pass
