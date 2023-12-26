from .default_profile import Profile
from .dj_mouse_profile import DjMouseProfile
from .spoty_mouse_profile import SpotyMouseProfile

REGISTERED_PROFILES = {
    'DEFAULT_PROFILE': Profile,
    'MOUSE_DJ_PROFILE': DjMouseProfile,
    'MOUSE_SPOTY_PROFILE': SpotyMouseProfile,
}
