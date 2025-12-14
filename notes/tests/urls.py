#urls.py
from django.urls import reverse


class UrlMixin:
    # Полные константы.
    NOTES_LIST_URL = reverse('notes:list')
    NOTES_ADD_URL = reverse('notes:add')

    # Константы для параметров
    NOTE_SLUG_AUTHOR = 'notes_slug_author'
    NOTE_SLUG_NOT_AUTHOR = 'notes_slug_not_author'

    # Зависят от константных тестовых данных.
    NOTES_EDIT_URL = reverse('notes:edit', args=[NOTE_SLUG_AUTHOR])

