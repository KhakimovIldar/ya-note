from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from notes.models import Note
from .urls import UrlMixin

User = get_user_model()


class Base(TestCase, UrlMixin):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Читатель простой')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Ildar',
            text='Текст',
            author=cls.author,
            slug=f'{cls.NOTE_SLUG_AUTHOR}',
        )


class TestRoutes(Base):
    """Тестирование маршрутов."""
    def test_control_of_all_return_codes(self):
        """
        П.1 главная страница доступна анонимному пользователю.
        П.2 Аутентифицированному пользователю доступны страницы add|notes|done.
        П.3 Страницы детализациии, удаления и редактирования доступны автору.
        Другому пользователю — вернётся ошибка 404.
        П.5 Страницы регистрации , входа и выхода доступны всем пользователям.
        """
        urls = (
            (self.NOTES_HOME_URL, self.client, HTTPStatus.OK),
            (self.NOTES_ADD_URL, self.reader_client, HTTPStatus.OK),
            (self.NOTES_SUCCESS_URL, self.reader_client, HTTPStatus.OK),
            (self.NOTES_LIST_URL, self.reader_client, HTTPStatus.OK),
            (self.NOTES_DETAIL_AUTH_URL, self.author_client, HTTPStatus.OK),
            (self.NOTES_DELETE_AUTH_URL, self.author_client, HTTPStatus.OK),
            (self.NOTES_EDIT_AUTH_URL, self.author_client, HTTPStatus.OK),
            (self.NOTES_DETAIL_AUTH_URL, self.reader_client,
             HTTPStatus.NOT_FOUND),
            (self.NOTES_DELETE_AUTH_URL, self.reader_client,
             HTTPStatus.NOT_FOUND),
            (self.NOTES_EDIT_AUTH_URL, self.reader_client,
             HTTPStatus.NOT_FOUND),
            (self.USER_SIGNUP_URL, self.client, HTTPStatus.OK),
            (self.USER_LOGIN_URL, self.client, HTTPStatus.OK),
            (self.USER_LOGOUT_URL, self.client, HTTPStatus.METHOD_NOT_ALLOWED),
        )
        for url, client, expected_status in urls:
            with self.subTest(
                url=url, client=client, expected_status=expected_status
            ):
                self.assertEqual(client.get(url).status_code, expected_status)

    def test_redirect_anonymous_user(self):
        """
        П.4 Тест редиректа на страницу логина после попытки зайти на страницы.
        Списка, успешного добавления, добавления, отдельной заметки.
        Редактирования или удаления замекти анонимного пользователя.
        """
        urls = (
            self.NOTES_LIST_URL,
            self.NOTES_SUCCESS_URL,
            self.NOTES_ADD_URL,
            self.NOTES_DETAIL_AUTH_URL,
            self.NOTES_DETAIL_AUTH_URL,
            self.NOTES_EDIT_AUTH_URL,
        )
        for url in urls:
            with self.subTest(url=url):
                redirect_url = f'{self.USER_LOGIN_URL}?next={url}'
                self.assertRedirects(self.client.get(url), redirect_url)
