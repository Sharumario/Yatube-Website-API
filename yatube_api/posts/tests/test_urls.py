from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User


USER = 'test_user'
AUTHOR = 'test_author'
SLUG = 'test_slug'
LOGIN_URL = reverse('users:login')
INDEX_URL = reverse('posts:index')
CREATE_URL = reverse('posts:post_create')
GROUP_URL = reverse('posts:group_list', args=(SLUG,))
PROFILE_URL = reverse('posts:profile', args=(AUTHOR,))
UNEXISTING_URL = '/unexisting_page/'
LOGIN_CREATE_URL = f'{LOGIN_URL}?next={CREATE_URL}'


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_author = User.objects.create_user(username=AUTHOR)
        cls.user = User.objects.create_user(username=USER)
        cls.post_author = Post.objects.create(
            author=cls.user_author,
            text='Тестовая запись поста автора',)

        cls.group = Group.objects.create(
            title=('Заголовок для тестовой группы'),
            slug=SLUG
        )
        cls.POST_DETAIL_URL = reverse(
            'posts:post_detail', args=(cls.post_author.id,)
        )
        cls.POST_EDIT_URL = reverse(
            'posts:post_edit', args=(cls.post_author.id,)
        )
        cls.LOGIN_EDIT_URL = f'{LOGIN_URL}?next={cls.POST_EDIT_URL}'

    def setUp(self):
        """"SetUp создаём объекты класса Client():
        гостевой не авторизированный пользователь,
        авторизованый пользователь,
        авторизованный автор поста."""
        self.guest = Client()
        self.another = Client()
        self.author = Client()
        self.author.force_login(self.user_author)
        self.another.force_login(self.user)

    def test_client_pages(self):
        """Тест доступа на все страницы.
        Тест несуществующей страницы."""
        url_names = [
            [INDEX_URL, self.guest, 200],
            [GROUP_URL, self.guest, 200],
            [PROFILE_URL, self.guest, 200],
            [self.POST_DETAIL_URL, self.guest, 200],
            [self.POST_EDIT_URL, self.guest, 302],
            [self.POST_EDIT_URL, self.another, 302],
            [self.POST_EDIT_URL, self.author, 200],
            [CREATE_URL, self.guest, 302],
            [CREATE_URL, self.author, 200],
            [UNEXISTING_URL, self.guest, 404]
        ]
        for url, user, status in url_names:
            with self.subTest(url=url, user=user, status=status):
                self.assertEqual((user).get(url).status_code, status)

    def test_urls_uses_correct_template(self):
        """Тест URL-адреса используют соответствующие шаблоны."""
        templates_url_names = [
            [INDEX_URL, self.guest, 'posts/index.html'],
            [GROUP_URL, self.guest, 'posts/group_list.html'],
            [PROFILE_URL, self.guest, 'posts/profile.html'],
            [self.POST_DETAIL_URL, self.guest, 'posts/post_detail.html'],
            [CREATE_URL, self.another, 'posts/create_post.html'],
            [self.POST_EDIT_URL, self.author, 'posts/create_post.html'],
        ]
        for url, user, template in templates_url_names:
            with self.subTest(url=url):
                self.assertTemplateUsed((user).get(url), template)

    def test_urls_authorized_author_template(self):
        """Тест редиректов на другие страницы,
        неавторизированого пользователя и авторизованого пользователя."""
        templates_url_names = [
            [CREATE_URL, self.guest, LOGIN_CREATE_URL],
            [self.POST_EDIT_URL, self.guest, self.LOGIN_EDIT_URL],
            [self.POST_EDIT_URL, self.another, self.POST_DETAIL_URL],
        ]
        for url, user, redirect_url in templates_url_names:
            with self.subTest(url=url, redirect_url=redirect_url):
                response = (user).get(url, follow=True)
                self.assertRedirects(response, redirect_url)
