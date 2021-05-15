from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=100)
    control_points = models.JSONField(default=list, unique=True)

    def __str__(self) -> str:
        return self.name


class Athlete(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Record(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    results = models.JSONField(default=list)

    def __str__(self) -> str:
        return f"{self.event.name} -> {self.athlete.name}"
