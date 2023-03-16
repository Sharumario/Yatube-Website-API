from django.urls import reverse
from django.test import TestCase


AUTHOR = 'user_author'
SLUG = 'test_slug'
POST_ID = 1
URLS = [
    ['/', 'index', ()],
    [f'/group/{SLUG}/', 'group_list', (SLUG,)],
    [f'/profile/{AUTHOR}/', 'profile', (AUTHOR,)],
    [f'/posts/{POST_ID}/', 'post_detail', (POST_ID,)],
    ['/create/', 'post_create', ()],
    [f'/posts/{POST_ID}/edit/', 'post_edit', (POST_ID,)]
]


class RoutesTests(TestCase):
    def test_routes(self):
        """"Тест маршрутов."""
        for url, route, args in URLS:
            with self.subTest(url=url):
                self.assertEqual(url, reverse(f'posts:{route}', args=args))
