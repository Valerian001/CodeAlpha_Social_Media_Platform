from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True, default='default_profile_picture.jpeg')
    # followers = models.ManyToManyField("self", symmetrical=False, related_name='following_set', blank=True)
    # following = models.ManyToManyField('self', symmetrical=False, related_name='followers_set', blank=True)

    def __str__(self):
        return self.user.username

    def followers_count(self):
        return self.user.followers.count()

    def following_count(self):
        return self.user.following.count()

class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return f"Post by {self.author.username} on {self.created_at}"
    
    def extract_hashtags(self):
        # Extract hashtags from the post content and save them
        hashtags = set(word[1:] for word in self.content.split() if word.startswith('#'))
        for tag in hashtags:
            hashtag, created = Hashtag.objects.get_or_create(name=tag)
            self.hashtags.add(hashtag)
        self.save()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post}"


# class Follow(models.Model):
#     follower = models.ForeignKey(User, related_name='follower_set', on_delete=models.CASCADE)
#     following = models.ForeignKey(User, related_name='following_set', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.follower.username} follows {self.following.username}"
    

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"
    





@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()