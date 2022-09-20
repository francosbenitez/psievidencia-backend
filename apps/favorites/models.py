from django.db import models

#######


class Favorite(models.Model):

    user = models.ForeignKey(User, related_name="favorites", on_delete=models.CASCADE)
    psychologist = models.ForeignKey(
        Psychologist, related_name="favorites", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.psychologist
