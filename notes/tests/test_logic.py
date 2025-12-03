from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.forms import WARNING
from notes.models import Note

User = get_user_model()


class TestNoteCreation(TestCase):
    """Тест создания заметки"""
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

    def test_user_can_create_comment(self):
        response = self.auth_client.post(self.url, data=self.form_data)
        self.assertRedirects(response, '/done/')
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)
        note = Note.objects.get()
        self.assertEqual(note.text, self.NOTE_TEXT)
        self.assertEqual(note.author, self.user)


class TestNoteEditDelete(TestCase):
    """Тест ужаления и редактирования """

    NOTE_TITLE = 'Заголовок 1'
    NOTE_TEXT = 'Текст заметки'
    NEW_NOTE_TEXT = 'Обновлённый текст заметки'

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
            slug='slug1'
        )
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.form_data = {'text': cls.NEW_NOTE_TEXT}

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
        print(self.edit_url)
        print(response)
        # Проверяем успешность запроса (редирект)
        # self.assertRedirects(response, reverse('notes:success'))
        # Обновляем объект из базы данных
        self.note.refresh_from_db()
        # Проверяем, что текст изменился
        print(self.note.text)
        print(self.NEW_NOTE_TEXT)
        self.assertEqual(self.note.text, self.NEW_NOTE_TEXT)

    # def test_user_cant_edit_comment_of_another_user(self):
    #     response = self.reader_client.post(self.edit_url, data=self.form_data)
    #     self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
    #     self.comment.refresh_from_db()
    #     self.assertEqual(self.comment.text, self.COMMENT_TEXT) 