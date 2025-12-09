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
        П.1 главная страница доступна анонимному пользователю.
        П.5 Страницы регистрации пользователей, входа и выходав учётную запись.
        Доступны всем пользователям.
        """
        urls = (
            'notes:home',
            'users:signup',
            'users:login',
            # 'users:logout',
        )
        for name in urls:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_add_sseccuss_list_notes(self):
        """
        П.2 плана сестов. Аутентифицированному пользователю доступны страницы.
        Со списком заметок notes/, страница успешного добавления заметки done/.
        Cтраница добавления новой заметки add/.
        """
        self.client.force_login(self.author)
        urls = (
            'notes:add',
            'notes:success',
            'notes:list',
        )
        for name in urls:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_delete_detail_edit_notes(self):
        """
        П.3 Страницы детализациии, удаления и редактирования доступны автору.
        Другому пользователю — вернётся ошибка 404.
        """
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

    def test_redirect_anonymous_user(self):
        """
        П.4 Тест редиректа на страницу логина после попытки зайти на странмцы.
        Списка, успешного добавления, добавления, отдельной заметки.
        Редактирования или удаления замекти анонимного пользователя.
        """
        login_url = reverse('users:login')
        urls = (
            ('notes:list', None),
            ('notes:success', None),
            ('notes:add', None),
            ('notes:detail', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
            ('notes:edit', (self.note.slug,)),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)
