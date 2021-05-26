from django.db import models
from django.core.exceptions import ValidationError
from jsonfield import JSONField
from rest_framework.exceptions import NotAcceptable


def validate_control_points(val) -> bool:
    cp_objs = set(ControlPoint.objects.filter(
        name__in=val).values_list("name", flat=True))
    val_set = set(val)
    diff = list(val_set.difference(cp_objs))
    if diff:
        raise ValidationError([f"Bilinmeyen Kontrol Noktaları: {diff}"])


class ControlPoint(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Adı")
    desc = models.TextField(null=True, blank=True, verbose_name="Açıklama")

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Kontrol Noktası"
        verbose_name_plural = "Kontrol Noktaları"


class Event(models.Model):
    date = models.DateField(unique=True, verbose_name="Tarih")
    name = models.CharField(max_length=100, verbose_name="Etkinlik Adı")

    def __str__(self) -> str:
        return self.name

    def check_has_records(self):
        record_count = Record.objects.filter(
            athlete__category__event=self).count()
        if record_count:
            raise NotAcceptable("Bu etkinliğe ait kayıtlar var!")

    def save(self, *args, **kwargs):
        if self.pk:
            self.check_has_records()
        super(Event, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.check_has_records()
        super(Event, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "Etkinlik"
        verbose_name_plural = "Etkinlikler"


class Category(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, verbose_name="Etkinlik")
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    control_points = JSONField(
        default=list, validators=[validate_control_points], verbose_name="Kontrol Noktaları")

    def check_has_records(self):
        record_count = Record.objects.filter(athlete__category=self).count()
        if record_count:
            raise NotAcceptable("Bu kategoriye ait kayıtlar var!")

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if self.pk:
            self.check_has_records()
        super(Category, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.check_has_records()
        super(Category, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
        unique_together = [["event", "name"], ["event", "control_points"]]


class Athlete(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Kategori")
    card_id = models.IntegerField(verbose_name="Kart NO")
    name = models.CharField(max_length=100, blank=True,
                            null=True, verbose_name="Ad Soyad")

    def __str__(self) -> str:
        return self.name if self.name else self.card_id

    def check_has_records(self):
        record_count = Record.objects.filter(athlete=self).count()
        if record_count:
            raise NotAcceptable("Bu sporcuya ait kayıtlar var!")

    def save(self, *args, **kwargs):
        if self.pk:
            self.check_has_records()
        super(Athlete, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.check_has_records()
        super(Athlete, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = "Sporcu"
        verbose_name_plural = "Sporcular"
        unique_together = ["category", "card_id"]


class Record(models.Model):
    athlete = models.OneToOneField(
        Athlete, on_delete=models.CASCADE, verbose_name="Sporcu", unique=True)
    results = JSONField(default=list, verbose_name="Sonuçlar")

    def __str__(self) -> str:
        return f"{self.athlete.name} -> {self.athlete.category.event.name} - {self.athlete.category.name}"

    class Meta:
        verbose_name = "Kayıt"
        verbose_name_plural = "Kayıtlar"
