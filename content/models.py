from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils.timezone import now
from django.conf import settings

User = get_user_model()

class Post(models.Model):
    author_id = models.CharField(max_length=255, default="nul") 
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    # author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    media = models.ImageField(upload_to='post_media/', null=True, blank=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure slug uniqueness by appending an identifier if needed
            if Post.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{self.pk or 'new'}"
        super().save(*args, **kwargs)

    
    def __str__(self):
        return f"{self.title} by {self.author_id}"

    class Meta:
        ordering = ['-created_at']  
        
        
        
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_like')
        ]
        
        
        
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"

    class Meta:
        ordering = ['created_at'] 
        
        
        
class Share(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shares')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="shares")
    shared_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name='unique_share')
        ]