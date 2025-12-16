#base_class
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client

from notes.models import Note
from notes.tests.urls import UrlMixin

User = get_user_model()


class BaseClass(TestCase, UrlMixin):
    @classmethod
    def setUpTestData(cls):
   
        cls.author = User.objects.create(username='Автор')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.author)

        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

        cls.form_data = {
            'title': 'Заголовок 2',
            'text': 'Текст 2',
            'slug': f'{cls.NOTE_SLUG_AUTHOR}'
        }
        
        cls.note = Note.objects.create(
            title='Заголовок',
            author=cls.author,
            text='Текст',
            slug=cls.NOTE_SLUG_AUTHOR,
        )

        cls.initial_notes = Note.objects.all()
