from .base_class import BaseClass
from notes.forms import NoteForm


class TestContent(BaseClass):

    def test_note_in_object_list(self):

        response = self.auth_client.get(self.NOTES_LIST_URL)
        notes = response.context['object_list']
        note = notes.get(id=self.note.id)
        self.assertEqual(self.note.title, note.title)
        self.assertEqual(self.note.text, note.text)
        self.assertEqual(self.note.slug, note.slug)
        self.assertEqual(self.note.author, note.author)

    def test_notes_of_differernt_users_dont_across(self):
        response = self.reader_client.get(self.NOTES_LIST_URL)
        notes = response.context['object_list']
        self.assertNotIn(self.note, notes)

    def test_authorized_client_has_form(self):
        for url in [self.NOTES_ADD_URL, self.NOTES_EDIT_AUTH_URL]:
            with self.subTest(url=url):
                self.assertIsInstance(
                    self.auth_client.get(url).context.get('form'), NoteForm
                )

