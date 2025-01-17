Handling file uploads in Django involves creating forms to upload files, setting up the necessary configurations, and writing views to process the uploaded files. Here’s a step-by-step guide on how to handle file uploads in Django.

### 1. Setup

Ensure you have Django installed. If not, install it using pip:

```bash
pip install django
```

Create a new Django project and an app:

```bash
django-admin startproject myproject
cd myproject
django-admin startapp myapp
```

Add the app to your `INSTALLED_APPS` in `settings.py`:

```python
# settings.py
INSTALLED_APPS = [
    ...
    'myapp',
]
```

### 2. Configuring Media Settings

In your `settings.py`, configure the media settings:

```python
# settings.py
import os

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

Ensure your `urls.py` is configured to serve media files during development:

```python
# myproject/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 3. Creating the Model

Create a model to handle file uploads:

```python
# myapp/models.py
from django.db import models

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
```

Run the migrations to create the model in the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Creating the Form

Create a form to upload files:

```python
# myapp/forms.py
from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )
```

### 5. Writing the Views

Create views to handle the file upload process:

```python
# myapp/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms.py import DocumentForm
from .models import Document

def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('file_list')
    else:
        form = DocumentForm()
    return render(request, 'myapp/upload_file.html', {'form': form})

def file_list(request):
    documents = Document.objects.all()
    return render(request, 'myapp/file_list.html', {'documents': documents})
```

### 6. Creating the Templates

Create templates to render the file upload form and the list of uploaded files:

#### upload_file.html

```html
<!-- myapp/templates/myapp/upload_file.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Upload file</title>
</head>
<body>
    <h1>Upload file</h1>
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Upload</button>
    </form>
    <a href="{% url 'file_list' %}">View uploaded files</a>
</body>
</html>
```

#### file_list.html

```html
<!-- myapp/templates/myapp/file_list.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Uploaded files</title>
</head>
<body>
    <h1>Uploaded files</h1>
    <ul>
        {% for document in documents %}
            <li>
                <a href="{{ document.document.url }}">{{ document.description }}</a>
                (uploaded at {{ document.uploaded_at }})
            </li>
        {% endfor %}
    </ul>
    <a href="{% url 'upload_file' %}">Upload another file</a>
</body>
</html>
```

### 7. URL Configuration

Configure the URLs to access the views:

```python
# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('', views.file_list, name='file_list'),
]
```

### 8. Running the Application

Run the Django development server:

```bash
python manage.py runserver
```

Now you can upload files by navigating to [http://127.0.0.1:8000/upload/](http://127.0.0.1:8000/upload/) and view the uploaded files at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

### Summary

This guide covers the basics of handling file uploads in Django, including configuring media settings, creating a model to store files, creating a form for file uploads, writing views to process uploads, and creating templates to render the form and list of uploaded files.
