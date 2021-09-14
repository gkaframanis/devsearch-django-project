from django.db import models
import uuid


class Project(models.Model):
    title = models.CharField(max_length=200)
    # Not a required field, can be empty to the database (null=True), we can leave in a form this field empty (blank=True)
    description = models.TextField(null=True, blank=True)
    # If the folder wasn't called images, we should add it the path of the default image.
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    # Many to many relationship for tags | We put Tag in "" because we create the model below the Project.
    tags = models.ManyToManyField("Tag", blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    # Automatically create a timestamp
    created = models.DateTimeField(auto_now_add=True)
    # 16 characters of string with letters and numbers
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        # When we access the Project object we see the title, instead of the Project object.
        return self.title


class Review(models.Model):
    VOTE_TYPE = (
        ("up", "Up Vote"),
        ("down", "Down Vote"),
    )
    # owner =
    # Delete all the reviews if the project is deleted | one to many relationship
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    # choices is gonna be a dropdown list and the user selects up or down vote.
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name
