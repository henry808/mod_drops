
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect
from user_profile.models import UserProfile
from user_profile.forms import ProfileForm


@login_required
def profile(request):
    # photo_count = len(request.user.photos.all())
    # album_count = len(request.user.albums.all())
    # follower_count = len(UserProfile.objects.filter(
    #     following=request.user.profile))
    context = {'name': request.user, 'profileID': request.user.profile.id}
    #           'photo_count': photo_count, "album_count": album_count,
    #           "follower_count": follower_count}
    return render(request, 'profile.html', context)


@login_required
def profile_update_view(request, *args, **kwargs):
    profile = UserProfile.objects.get(pk=kwargs['pk'])
    user = profile.user
    # import pdb; pdb.set_trace()
    if request.method == 'POST':
        # For submission of form for updating information...
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()
            return HttpResponseRedirect(
                reverse(
                    'profile_detail',
                    kwargs={'pk': request.user.profile.pk}
                ))
    else:
        # For populating a form when a user navigates to page
        # using the edit link in the profile detail page...
        initial = {'first_name': user.first_name,
                   'last_name': user.last_name,
                   'email': user.email,
                   }

        form = ProfileForm(instance=profile, initial=initial)
    return render(request, 'profile_update.html', {'form': form})