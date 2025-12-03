from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):
    """Тестирование маршрутов."""

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(
            title='Ildar',
            text='Текст',
            author=cls.author,
        )

    def test_home_page(self):
        """
        Тест Главная страница доступна анонимному пользователю.
        Страницы регистрации и входа в доступны анонимным пользователям.
        """
        urls = (
            'notes:home',
            'users:login',
            'users:signup',
        )
        for name in urls:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_notes_list_page(self):
        """
        Тест страницы со списком и добавления заметки.
        Доступна авторизованному пользователю.
        """
        self.client.force_login(self.author)
        urls = (
            'notes:list',
            'notes:add',
        )
        for name in urls:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_in_application(self):
        """Страницы детализациии, удаления и редактирования доступны автору."""
        urls = (
            'notes:delete',
            'notes:detail',
            'notes:edit',
        )
        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name in urls:
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.note.slug,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_after_succesful_operation(self):
        """Тест редиректа после добавления, удаления и редактирования."""
        login_url = reverse('users:login')
        urls = (
            ('notes:add', None),
            ('notes:delete', (self.note.slug,)),
            ('notes:edit', (self.note.slug,)),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
