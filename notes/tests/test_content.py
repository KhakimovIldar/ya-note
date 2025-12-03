from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.forms import NoteForm
from notes.models import Note


User = get_user_model()


class TestNotesListPage(TestCase):
    """Тест контента на странице с заметками"""

    NOTES_LIST_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        all_notes = [
            Note(
                title=f'Заметка {index}',
                slug=f'note-{index}',
                text='Просто текст.',
                author=cls.author,
            )
            for index in range(100)
        ]
        Note.objects.bulk_create(all_notes)

    def test_notes_count(self):
        """Тест на то, что все заметки отображаются на главной странице."""
        self.client.force_login(self.author)
        response = self.client.get(self.NOTES_LIST_URL)
        object_list = response.context['object_list']
        notes_count = object_list.count()
        self.assertEqual(notes_count, 100)


class TestNotesAccesRights(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.note = Note.objects.create(
            title='Ildar',
            text='Текст',
            author=cls.author,
        )
        cls.urls = (
            ('notes:add', None),
            ('notes:edit', (cls.note.slug,)),
        )

    def test_anonymous_client_has_no_form(self):
        for name, args in self.urls:
            url = reverse(name, args=args)
            response = self.client.get(url)
            if response.context:
                self.assertNotIn('form', response.context)

    def test_authorized_client_has_form(self):
        self.client.force_login(self.author)
        for name, args in self.urls:
            url = reverse(name, args=args)
            response = self.client.get(url)
            self.assertIn('form', response.context)
            self.assertIsInstance(response.context['form'], NoteForm)
