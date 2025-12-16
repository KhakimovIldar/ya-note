from http import HTTPStatus

from .base_class import BaseClass

OK = HTTPStatus.OK
NOT_FOUND = HTTPStatus.NOT_FOUND
METHOD_NOT_ALLOWED = HTTPStatus.METHOD_NOT_ALLOWED
FOUND = HTTPStatus.FOUND


class TestRoutes(BaseClass):
    """Тестирование маршрутов."""
    def test_control_of_all_return_codes(self):
        urls = (
            (self.NOTES_HOME_URL, self.client, OK),
            (self.NOTES_ADD_URL, self.reader_client, OK),
            (self.NOTES_SUCCESS_URL, self.reader_client, OK),
            (self.NOTES_LIST_URL, self.reader_client, OK),
            (self.NOTES_DETAIL_AUTH_URL, self.auth_client, OK),
            (self.NOTES_DELETE_AUTH_URL, self.auth_client, OK),
            (self.NOTES_EDIT_AUTH_URL, self.auth_client, OK),
            (self.NOTES_DETAIL_AUTH_URL, self.reader_client, NOT_FOUND),
            (self.NOTES_DELETE_AUTH_URL, self.reader_client, NOT_FOUND),
            (self.NOTES_EDIT_AUTH_URL, self.reader_client, NOT_FOUND),
            (self.USER_SIGNUP_URL, self.client, OK),
            (self.USER_LOGIN_URL, self.client, OK),
            (self.USER_LOGOUT_URL, self.client, METHOD_NOT_ALLOWED),
            (self.NOTES_LIST_URL, self.client, FOUND),
            (self.NOTES_SUCCESS_URL, self.client, FOUND),
            (self.NOTES_ADD_URL, self.client, FOUND),
            (self.NOTES_DETAIL_AUTH_URL, self.client, FOUND),
            (self.NOTES_DETAIL_AUTH_URL, self.client, FOUND),
            (self.NOTES_EDIT_AUTH_URL, self.client, FOUND),
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
            (self.NOTES_LIST_URL, self.NOTES_LIST_REDIRECT_URL),
            (self.NOTES_SUCCESS_URL, self.NOTES_SUCCESS_REDIRECT_URL),
            (self.NOTES_ADD_URL, self.NOTES_ADD_REDIRECT_URL),
            (self.NOTES_DETAIL_AUTH_URL, self.NOTES_DETAIL_AUTH_REDIRECT_URL),
            (self.NOTES_EDIT_AUTH_URL, self.NOTES_EDIT_AUTH_REDIRECT_URL)
        )
        for url, redirect_url in urls:
            with self.subTest(url=url):
                self.assertRedirects(self.client.get(url), redirect_url)
