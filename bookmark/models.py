from django.contrib.auth.models import User
from django.db import models
from broadcasting.models import Broadcast  # Import Broadcast model from the other app


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookmarks")
    broadcast = models.ForeignKey(
        Broadcast, on_delete=models.CASCADE, related_name="bookmarked_by"
    )
    date_bookmarked = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bookmarked {self.broadcast.title}"

    def save(self, *args, **kwargs):
        if self.user.bookmarks.count() >= 50:
            raise ValueError("You can only bookmark up to 50 broadcasts.")
        super().save(*args, **kwargs)
