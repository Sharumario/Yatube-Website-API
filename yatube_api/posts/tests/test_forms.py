from django import forms
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User


SLUG_ONE = 'test_slug_one'
SLUG_TWO = 'test_slug_two'
USERNAME = 'test_user'
POST_CREATE_URL = reverse('posts:post_create')
PROFILE_URL = reverse('posts:profile', args=(USERNAME,))


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username=USERNAME)
        cls.group_one = Group.objects.create(
            title=('Заголовок 1-ой тестовой группы'),
            slug=SLUG_ONE,
            description='Тестовое описание'
        )
        cls.group_two = Group.objects.create(
            title=('Заголовок 2-ой тестовой группы'),
            slug=SLUG_TWO,
            description='Тестовое описание'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая запись для создания 1 поста',
            group=cls.group_one)
        cls.POST_EDIT_URL = reverse('posts:post_edit', args=(cls.post.id,))
        cls.POST_DETAIL = reverse('posts:post_detail', args=(cls.post.id,))

    def setUp(self):
        self.guest = Client()
        self.author = Client()
        self.author.force_login(self.user)

    def test_post_create_form(self):
        """"Тест создания нового поста при отправке валидной формы"""
        COUNT_BEFORE_CREATE = Post.objects.count()
        form_data = {
            'text': 'Данные из формы',
            'group': self.group_one.id,
        }
        response = self.author.post(
            POST_CREATE_URL,
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, PROFILE_URL)
        self.assertEqual(Post.objects.count(), COUNT_BEFORE_CREATE + 1)
        posts_exclude_one = Post.objects.exclude(id=self.post.id)
        self.assertEqual(posts_exclude_one.count(), 1)
        post = posts_exclude_one[0]
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.group.id, form_data['group'])

    def test_post_edit_form(self):
        """"Тест редактирование поста при отправке валидной формы"""
        form_data = {
            'text': 'Измененный текст',
            'group': self.group_two.id,
        }
        response = self.author.post(
            self.POST_EDIT_URL,
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, self.POST_DETAIL)
        post = response.context['post']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.author, self.post.author)
        self.assertEqual(post.group.id, form_data['group'])

    def test_post_create_edit_correct_context(self):
        """Шаблон post_edit и create сформирован с правильным контекстом"""
        urls = (POST_CREATE_URL, self.POST_EDIT_URL)
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for url in urls:
            response = self.author.get(url)
            for value, expected in form_fields.items():
                with self.subTest(value=value):
                    form_field = response.context['form'].fields[value]
                    self.assertIsInstance(form_field, expected)
