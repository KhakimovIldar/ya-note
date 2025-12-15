from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client

from notes.forms import NoteForm
from notes.models import Note
from notes.tests.urls import UrlMixin

User = get_user_model()


class BaseClass(TestCase, UrlMixin):
    @classmethod
    def setUpTestData(cls):

        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)

        cls.not_author = User.objects.create(username='Не автор')
        cls.not_author_client = Client()
        cls.not_author_client.force_login(cls.not_author)

        cls.note = Note.objects.create(
            title='Заголовок заметки',
            text='Просто текст.',
            slug=UrlMixin.NOTE_SLUG_AUTHOR,
            author=cls.author,
        )

        cls.urls = [
            cls.NOTES_ADD_URL,
            cls.NOTES_EDIT_URL
        ]


class TestContent(BaseClass):
    """
    П.1 отдельная заметка передаётся на страницу со списком заметок.
    В object_list в словаре context.
    П.2 В список заметок одного пользователя не попадают заметки другого.
    """

    def test_note_in_object_list(self):
        response = self.author_client.get(self.NOTES_LIST_URL)
        notes = response.context['object_list']
        note_in_list = notes.get(id=self.note.id)

        self.assertIn(self.note, notes)
        self.assertEqual(self.note.title, note_in_list.title)
        self.assertEqual(self.note.text, note_in_list.text)
        self.assertEqual(self.note.slug, note_in_list.slug)
        self.assertEqual(self.note.author, note_in_list.author)

    def test_notes_of_differernt_users_dont_across(self):
        note_from_not_author = Note.objects.create(
            title='Заголовок заметки не автора.',
            text='Просто текст.',
            slug='test-note-slug',
            author=self.not_author,
        )
        response = self.author_client.get(self.NOTES_LIST_URL)
        notes = response.context['object_list']

        self.assertNotIn(note_from_not_author, notes)


class TestNotesAccesRights(BaseClass):
    """На страницы создания и редактирования заметки передаются формы."""
    # urls = [
    #     UrlMixin.NOTES_ADD_URL,
    #     UrlMixin.NOTES_EDIT_URL
    # ]

    # def test_anonymous_client_has_no_form(self):
    #     # for url in self.urls:
    #     #     response = self.client.get(url)
    #     #     self.assertNotIn('form', response.context)
    #     url = reverse('notes:add')
    #     response = self.client.get(url)
    #     self.assertNotIn('form', response.context)

    def test_authorized_client_has_form(self):
        for url in self.urls:
            with self.subTest(url=url):
                self.assertIsInstance(
                    self.author_client.get(url).context.get('form'), NoteForm
                )
