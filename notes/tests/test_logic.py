from http import HTTPStatus

import pytils.translit

from .base_class import BaseClass
from ..models import Note


class TestNoteCreation(BaseClass):
    def test_anonymous_user_cant_create_note(self):
        """П.1 Анонимный пользователь не может создать заметку."""
        self.client.post(self.NOTES_ADD_URL, data=self.form_data)
        self.assertQuerySetEqual(self.initial_notes, Note.objects.all())

    def test_user_can_create_note(self):  # Доработать
        """П.1 Залогиненный пользователь может создать заметку."""
        self.form_data['slug'] = 'new_note'
        notes_count = self.initial_notes.count()
        self.auth_client.post(self.NOTES_ADD_URL, data=self.form_data)
        self.assertEqual(Note.objects.count() - notes_count, 1)
        note = Note.objects.latest('id')
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.author)

    def test_duplicate_slug(self):
        """П.2 Невозможно создать две заметки с одинаковым slug."""
        self.form_data['slug'] = f'{self.note.slug}'
        self.assertIn('slug', self.auth_client.post(
            self.NOTES_ADD_URL, data=self.form_data).context['form'].errors)
        self.assertEqual(Note.objects.all().count(), 1)

    def test_translit_empty_slug(self):
        """П.3 Slug формируется автоматически, с помощью translit.slugify."""
        notes_count = self.initial_notes.count()
        self.form_data['slug'] = ''
        self.auth_client.post(self.NOTES_ADD_URL, data=self.form_data)
        self.assertEqual(Note.objects.count() - notes_count, 1)
        note = Note.objects.latest('id')
        self.assertEqual(note.slug, pytils.translit.slugify(
            self.form_data['title']))
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.author, self.author)

    def test_author_can_delete_note(self):
        """П.4 Пользователь может удалять свои заметки."""
        response = self.auth_client.delete(self.NOTES_DELETE_AUTH_URL)
        self.assertRedirects(response, self.NOTES_SUCCESS_URL)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Note.objects.count(), 0)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

    def test_user_cant_delete_note_of_another_user(self):
        """П.4 Пользователь не может удалять чужие заметки."""
        note_before_delete = Note.objects.get(id=self.note.id)
        response = self.reader_client.delete(self.NOTES_DELETE_AUTH_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertQuerySetEqual(self.initial_notes, Note.objects.all())
        self.assertEqual(note_before_delete.author, self.note.author)
        self.assertEqual(note_before_delete.slug, self.note.slug)
        self.assertEqual(note_before_delete.text, self.note.text)
        self.assertEqual(note_before_delete.title, self.note.title)

    def test_author_can_edit_note(self):
        """П.4 Пользователь может редактировать свои заметки."""
        note_id = self.note.id
        note_bofore_edit = self.note
        self.auth_client.post(self.NOTES_EDIT_AUTH_URL, data=self.form_data)
        note = Note.objects.get(id=note_id)
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note_bofore_edit.author, note.author)

    def test_user_cant_edit_comment_of_another_user(self):
        """П.4 Пользователь не может редактировать чужие заметки."""
        note_id = self.note.id
        response = self.reader_client.post(self.NOTES_EDIT_AUTH_URL,
                                           data=self.form_data)
        note = Note.objects.get(id=note_id)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.author, note.author)
        self.assertEqual(self.note.slug, note.slug)
