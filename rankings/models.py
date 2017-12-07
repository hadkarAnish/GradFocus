from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator


class City(models.Model):
    name = models.CharField(max_length=50, unique=True)
    livingExpense = models.PositiveIntegerField()
    minTemperature = models.FloatField(validators=[MaxValueValidator(212)])
    maxTemperature = models.FloatField(validators=[MaxValueValidator(212)])
    logo = models.FileField(default=None, null=True, blank=True)

    def get_absolute_url(self):
        # the return below states that go to this view,keyWord args: use the primary key of the current crated object,
        #  and go to detail using this pk
        return reverse('rankings:details', kwargs={'pk': self.pk})

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"


class University(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    UNIVERSITY_TYPE_CHOICES = (
        ('Private', 'Private'),
        ('Public', 'Public'),
    )
    type = models.CharField(
        max_length=50,
        choices=UNIVERSITY_TYPE_CHOICES,
        default='Private',
    )
    logo = models.FileField(default=None, null=True, blank=True)

    def get_absolute_url(self):
        return reverse('rankings:university_details', kwargs={'pk': self.pk})

    def __str__(self):
        return "%s, ID: %i" % (self.name, self.id)

    class Meta:
        verbose_name = "University"
        verbose_name_plural = "Universities"


class Program(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    pName = models.CharField(max_length=50)
    rank = models.PositiveIntegerField()
    acceptedGRE = models.PositiveIntegerField(null=True, blank=True, validators=[MaxValueValidator(340)])
    acceptedGMAT = models.PositiveIntegerField(null=True, blank=True, validators=[MaxValueValidator(800)])
    acceptedTOEFL = models.PositiveIntegerField(validators=[MaxValueValidator(120)])
    minCGPA = models.FloatField(null=True, blank=True)
    feePerCredit = models.PositiveIntegerField()
    avgWorkExp = models.FloatField(null=True, blank=True, validators=[MaxValueValidator(100)])

    def get_absolute_url(self):
        return reverse('rankings:program_details', kwargs={'pk': self.pk})

    def __str__(self):
        return "%s, %s, ID: %i" % (University.objects.get(program__id=self.id).name, self.pName, self.id)

    class Meta:
        verbose_name = "Program"
        verbose_name_plural = "Programs"


class Course(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    courseName = models.CharField(max_length=100)
    courseDescription = models.CharField(max_length=1000)

    def get_absolute_url(self):
        return reverse('rankings:course_details', kwargs={'pk': self.pk})

    def __str__(self):
        return "%s, %s, ID: %i" % (University.objects.get(program__course__id=self.id).name, self.courseName, self.id)


class Student(models.Model):
    sFirstName = models.CharField(max_length=50)
    sLastName = models.CharField(max_length=100)
    sDateOfBirth = models.DateField()
    sPhoneNumber = models.PositiveIntegerField(null=True, blank=True, )
    sEmailId = models.EmailField()
    sGRE = models.PositiveIntegerField(validators=[MaxValueValidator(340)], null=True, blank=True, )
    sGMAT = models.PositiveIntegerField(validators=[MaxValueValidator(800)], null=True, blank=True, )
    sTOEFL = models.PositiveIntegerField(validators=[MaxValueValidator(120)], null=True, blank=True, )
    sCGPA = models.FloatField()
    sWorkExp = models.FloatField(validators=[MaxValueValidator(100.0)], null=True, blank=True, )
    sUnderGradStream = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('rankings:student_details', kwargs={'pk': self.pk})

    def __str__(self):
        return "%s %s, ID: %i" % (self.sFirstName, self.sLastName, self.id)


class Matches(models.Model):
    student = models.ForeignKey(Student, related_name="student_matches")
    program = models.ForeignKey(Program, related_name="program_matches")

    class Meta:
        unique_together = (('student', 'program'),)
        verbose_name = "Matches"
        verbose_name_plural = "Matches"

    def get_absolute_url(self):
        return reverse('rankings:matches_details', kwargs={'pk': self.pk})

    def __str__(self):
        return "program id: %i, student ID: %i" % (self.program_id, self.student_id)
