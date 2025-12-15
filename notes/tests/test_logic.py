from http import HTTPStatus

import pytils.translit

from .base_class import BaseClass
from ..models import Note


class TestNoteCreation(BaseClass):
    def test_anonymous_user_cant_create_note(self):
        """П.1 Анонимный пользователь не может создать заметку."""
        self.client.post(self.NOTES_ADD_URL, data=self.form_data)
        self.assertEqual(self.initial_notes_count, Note.objects.count())

    def test_user_can_create_note(self):
        """П.1 Залогиненный пользователь может создать заметку."""
        response = self.auth_client.post(
            self.NOTES_ADD_URL, data=self.form_data
        )
        note = Note.objects.get(title=self.form_data['title'])
        self.assertRedirects(response, self.NOTES_SUCCESS_URL)
        self.assertEqual(self.initial_notes_count + 1, Note.objects.count())
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.author)

    def test_duplicate_slug(self):
        """П.2 Невозможно создать две заметки с одинаковым slug."""
        self.form_data['slug'] = f'{self.NOTE_SLUG_AUTHOR}'
        response = self.auth_client.post(
            self.NOTES_ADD_URL, data=self.form_data
        )
        form = response.context['form']
        self.assertIn('slug', form.errors)

    def test_translit_empty_slug(self):
        """П.3 Slug формируется автоматически, с помощью translit.slugify."""
        self.form_data['title'] = 'Новая заметка'
        self.form_data['slug'] = ''
        self.auth_client.post(self.NOTES_ADD_URL, data=self.form_data)
        note = Note.objects.get(title=self.form_data['title'])
        self.assertEqual(note.slug, pytils.translit.slugify(
            self.form_data['title']))

    def test_author_can_delete_note(self):
        """П.4 Пользователь может удалять свои заметки."""
        response = self.auth_client.delete(self.NOTES_DELETE_AUTH_URL)
        self.assertRedirects(response, self.NOTES_SUCCESS_URL)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Note.objects.count(), self.initial_notes_count - 1)

    def test_user_cant_delete_note_of_another_user(self):
        """П.4 Пользователь не может удалять чужие заметки."""
        response = self.reader_client.delete(self.NOTES_DELETE_AUTH_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), self.initial_notes_count)

    def test_author_can_edit_note(self):
        """П.4 Пользователь может редактировать свои заметки."""
        response = self.auth_client.post(self.NOTES_EDIT_AUTH_URL,
                                         data=self.form_data)
        note = Note.objects.get()
        self.assertRedirects(response, self.NOTES_SUCCESS_URL)
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])

    def test_user_cant_edit_comment_of_another_user(self):
        """П.4 Пользователь не может редактировать чужие заметки."""
        initial_note = Note.objects.get()
        print(initial_note)
        response = self.reader_client.post(self.NOTES_EDIT_AUTH_URL,
                                           data=self.form_data)
        note = Note.objects.get()
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(initial_note.title, note.title)
        self.assertEqual(initial_note.text, note.text)
        self.assertEqual(initial_note.author, note.author)
        self.assertEqual(initial_note.slug, note.slug)
