from django.urls import reverse


class UrlMixin:
    # Константы для параметров
    NOTE_SLUG_AUTHOR = 'notes_slug_author'

    # Зависят от константных текстовых данных.
    NOTES_EDIT_AUTH_URL = reverse('notes:edit', args=[NOTE_SLUG_AUTHOR])
    NOTES_DELETE_AUTH_URL = reverse('notes:delete', args=[NOTE_SLUG_AUTHOR])
    NOTES_DETAIL_AUTH_URL = reverse('notes:detail', args=[NOTE_SLUG_AUTHOR])

    # Полные константы.
    NOTES_HOME_URL = reverse('notes:home')
    NOTES_LIST_URL = reverse('notes:list')
    NOTES_ADD_URL = reverse('notes:add')
    NOTES_SUCCESS_URL = reverse('notes:success')
    USER_SIGNUP_URL = reverse('users:signup')
    USER_LOGIN_URL = reverse('users:login')
    USER_LOGOUT_URL = reverse('users:logout')
    NOTES_LIST_REDIRECT_URL = f'{USER_LOGIN_URL}?next={NOTES_LIST_URL}'
    NOTES_SUCCESS_REDIRECT_URL = f'{USER_LOGIN_URL}?next={NOTES_SUCCESS_URL}'
    NOTES_ADD_REDIRECT_URL = f'{USER_LOGIN_URL}?next={NOTES_ADD_URL}'
    NOTES_DETAIL_AUTH_REDIRECT_URL = f'{USER_LOGIN_URL}?next={
        NOTES_DETAIL_AUTH_URL}'
    NOTES_EDIT_AUTH_REDIRECT_URL = f'{USER_LOGIN_URL}?next={
        NOTES_EDIT_AUTH_URL}'
