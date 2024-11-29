from django import forms
from .models import UserProfile,Post

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']

    def clean_profile_picture(self):
      profile_picture = self.cleaned_data.get('profile_picture')
      if not profile_picture:
          return None  # Allow no profile picture to be set
      return profile_picture


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']