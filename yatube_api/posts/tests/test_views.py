from django.urls import reverse
from django.test import Client, TestCase

from ..views import QUANTITY_POSTS
from ..models import Group, Post, User

USER = 'authorized_client'
AUTHOR_1 = 'user_author_1'
AUTHOR_2 = 'user_author_2'
SLUG_1 = 'test_slug_1'
SLUG_2 = 'test_slug_2'
INDEX_URL = reverse('posts:index')
CREATE_URL = reverse('posts:post_create')
GROUP_ONE_URL = reverse('posts:group_list', args=(SLUG_1,))
GROUP_TWO_URL = reverse('posts:group_list', args=(SLUG_2,))
PROFILE_AUTHOR_1_URL = reverse('posts:profile', args=(AUTHOR_1,))


class PostViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user_author = User.objects.create_user(
            username=AUTHOR_1,
        )
        cls.user = User.objects.create_user(username=USER)
        cls.group_one = Group.objects.create(
            title='Заголовок для 1 тестовой группы',
            slug=SLUG_1
        )
        cls.group_two = Group.objects.create(
            title='Заголовок для 2 тестовой группы',
            slug=SLUG_2
        )
        cls.post_one = Post.objects.create(
            author=cls.user_author,
            text='Тестовая запись для создания 1 поста',
            group=cls.group_one)
        cls.POST_DETAIL_URL = reverse(
            'posts:post_detail', args=(cls.post_one.id,)
        )
        cls.POST_EDIT_URL = reverse(
            'posts:post_edit', args=(cls.post_one.id,)
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_author = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_author.force_login(self.user_author)

    def test_pages_context(self):
        """Пост self.post_two в шаблонах index, group, profile
        сформированы с правильным контекстом."""
        urls = [
            [INDEX_URL, 'page_obj'],
            [GROUP_ONE_URL, 'page_obj'],
            [PROFILE_AUTHOR_1_URL, 'page_obj'],
            [self.POST_DETAIL_URL, 'post']
        ]
        for url, context in urls:
            posts = self.authorized_author.get(url).context[context]
            with self.subTest(url=url):
                if context == 'page_obj':
                    self.assertEqual(len(posts), 1)
                    post = posts[0]
                else:
                    post = posts
                self.assertEqual(post.id, self.post_one.id)
                self.assertEqual(post.text, self.post_one.text)
                self.assertEqual(post.author, self.post_one.author)
                self.assertEqual(post.group, self.post_one.group)

    def test_group_pages_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_author.get(GROUP_ONE_URL)
        group = response.context['group']
        self.assertEqual(group.title, self.group_one.title)
        self.assertEqual(group.slug, self.group_one.slug)
        self.assertEqual(group.description, self.group_one.description)
        self.assertEqual(group.id, self.group_one.id)

    def test_profile_pages_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_author.get(PROFILE_AUTHOR_1_URL)
        self.assertEqual(response.context['author'], self.user_author)

    def test_post_another_group(self):
        """"Пост post_one не попал в другую группу."""
        self.assertNotIn(
            self.post_one,
            self.authorized_author.get(GROUP_TWO_URL).context.get('page_obj')
        )

    def test_paginator(self):
        """Paginator правильно отображает 1-ую и 2-ую страницы с постами"""
        Post.objects.bulk_create(
            Post(
                text=f'Тестовый пост {i}',
                author=self.user_author,
                group=self.group_one
            ) for i in range(QUANTITY_POSTS + 1)
        )
        count_posts_index = (
            Post.objects.all().count() - QUANTITY_POSTS
        )
        count_posts_group = (
            Group.objects.filter(slug=SLUG_1).get().posts.count()
            - QUANTITY_POSTS
        )
        count_posts_profile = (
            User.objects.filter(username=AUTHOR_1).get().posts.count()
            - QUANTITY_POSTS
        )
        list_urls = {
            INDEX_URL: QUANTITY_POSTS,
            GROUP_ONE_URL: QUANTITY_POSTS,
            PROFILE_AUTHOR_1_URL: QUANTITY_POSTS,
            INDEX_URL + "?page=2": count_posts_index,
            GROUP_ONE_URL + "?page=2": count_posts_group,
            PROFILE_AUTHOR_1_URL + "?page=2": count_posts_profile,
        }
        for url, quantity_posts in list_urls.items():
            self.assertEqual(
                len(self.client.get(url).context.get('page_obj').object_list),
                quantity_posts
            )
