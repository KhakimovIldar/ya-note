from django.urls import reverse


class UrlMixin:
    # Полные константы.
    NOTES_HOME_URL = reverse('notes:home')
    NOTES_LIST_URL = reverse('notes:list')
    NOTES_ADD_URL = reverse('notes:add')
    NOTES_SUCCESS_URL = reverse('notes:success')
    USER_SIGNUP_URL = reverse('users:signup')
    USER_LOGIN_URL = reverse('users:login')
    USER_LOGOUT_URL = reverse('users:logout')

    # Константы для параметров
    NOTE_SLUG_AUTHOR = 'notes_slug_author'

    # Зависят от константных тестовых данных.
    NOTES_EDIT_AUTH_URL = reverse('notes:edit', args=[NOTE_SLUG_AUTHOR])
    NOTES_DELETE_AUTH_URL = reverse('notes:delete', args=[NOTE_SLUG_AUTHOR])
    NOTES_DETAIL_AUTH_URL = reverse('notes:detail', args=[NOTE_SLUG_AUTHOR])
