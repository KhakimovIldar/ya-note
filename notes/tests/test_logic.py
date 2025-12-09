
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import Client, TestCase
from django.urls import reverse

from ..forms import NoteForm
from ..models import Note

import pytils.translit

User = get_user_model()


class TestNoteCreation(TestCase):
    """П.1 Залогиненный пользователь может создать заметку, анонимный — нет."""
    NOTE_TITLE = 'Заголовок 1'
    NOTE_TEXT = 'Текст комментария'

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('notes:add')
        cls.user = User.objects.create(username='Пользователь')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.form_data = {
            'title': cls.NOTE_TITLE,
            'text': cls.NOTE_TEXT
        }

    def test_anonymous_user_cant_create_note(self):
        self.client.post(self.url, data=self.form_data)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 0)

    def test_user_can_create_note(self):
        response = self.auth_client.post(self.url, data=self.form_data)
        self.assertRedirects(response, '/done/')
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        note = Note.objects.get()
        self.assertEqual(note.text, self.NOTE_TEXT)
        self.assertEqual(note.author, self.user)


class TestSlugUniqueness(TestCase):
    """
    П.2 Невозможно создать две заметки с одинаковым slug.
    П.3 Slug формируется автоматически, с помощью функции translit.slugify.
    """
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Пользователь')
        cls.author_2 = User.objects.create(username='Пользователь_2')

    def test_duplicate_slug(self):
        Note.objects.create(
            title='Заголовок',
            author=self.author,
            text='Текст',
            slug='slug',
        )
        with self.assertRaises(IntegrityError):
            Note.objects.create(
                title='Заголовок_2',
                author=self.author_2,
                text='Текст_2',
                slug='slug',
            )

    def test_translit_empty_slug(self):
        form_data = {
            'title': 'Новая заметка через форму',
            'text': 'Текст',
        }
        form = NoteForm(data=form_data)
        note = form.save(commit=False)
        note.author = self.author
        note.save()
        self.assertEqual(note.slug, pytils.translit.slugify(
            form_data['title']
        ))


class TestNoteEditDelete(TestCase):
    """
    П.4 Пользователь может редактировать и удалять свои заметки.
    Но не может редактировать или удалять чужие.
    """
    NOTE_TITLE = 'Заголовок 1'
    NEW_NOTE_TITLE = 'Обновлённый заголовок'
    NOTE_TEXT = 'Текст заметки'
    NEW_NOTE_TEXT = 'Обновлённый текст заметки'
    NOTE_SLUG = 'slug'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title=cls.NOTE_TITLE,
            author=cls.author,
            text=cls.NOTE_TEXT,
            slug=cls.NOTE_SLUG,
        )
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.form_data = {
            'title': cls.NEW_NOTE_TITLE,
            'text': cls.NEW_NOTE_TEXT,
            'slug': cls.NOTE_SLUG,
        }

    def test_author_can_delete_note(self):
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, '/done/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        comments_count = Note.objects.count()
        self.assertEqual(comments_count, 0)

    def test_user_cant_delete_note_of_another_user(self):
        response = self.reader_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_author_can_edit_comment(self):
        response = self.author_client.post(self.edit_url, data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NEW_NOTE_TEXT)

    def test_user_cant_edit_comment_of_another_user(self):
        response = self.reader_client.post(self.edit_url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.note.text)
