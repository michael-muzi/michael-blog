from users.models import Profile

def check_and_enable_profile(user, **kw):
    screenname = kw.get('screen_name', None)
    gender = kw.get('gender', None)
    if gender:
        gender = gender.upper()
        kw['gender'] = gender
    description = kw.get('description', '')
    location = kw.get('location', '')
    figurephoto = kw.get('figurephoto', '')
    profile, created = Profile.objects.get_or_create(user=user, defaults=kw)
    
    return user
