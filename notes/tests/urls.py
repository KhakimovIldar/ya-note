from django.urls import reverse


class UrlMixin:
    # Полные константы.
    NOTES_LIST_URL = reverse('notes:list')
    NOTES_ADD_URL = reverse('notes:add')
    NOTES_SUCCESS_URL = reverse('notes:success')

    # Константы для параметров
    NOTE_SLUG_AUTHOR = 'notes_slug_author'
    NOTE_SLUG_READER = 'notes_slug_reader'

    # Зависят от константных тестовых данных.
    NOTES_EDIT_URL = reverse('notes:edit', args=[NOTE_SLUG_AUTHOR])
    NOTES_DELETE_BY_AUTH_URL = reverse('notes:delete', args=[NOTE_SLUG_AUTHOR])
