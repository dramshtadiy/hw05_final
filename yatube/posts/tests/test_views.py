from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..forms import PostForm
from ..models import Group, Post, Comment, Follow

User = get_user_model()


class PostPageTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create(username='authtest1')
        cls.group = Group.objects.create(
            title='Тестовый заголовок группы',
            slug='test1slug',
            description='Тестовое описание',
        )
        cls.group_2 = Group.objects.create(
            title='Заголовок для тестовой группы2',
            slug='test_slug2',
            description='Тестовое описание2',
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text='Текст поста',
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.author = User.objects.get(username='authtest1')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={
                'slug': self.group.slug}): 'posts/group_list.html',
            reverse('posts:profile', kwargs={
                'username': self.author.username}): 'posts/profile.html',
            reverse('posts:post_detail', kwargs={
                'post_id': self.post.pk}): 'posts/post_detail.html',
            reverse('posts:post_edit', kwargs={
                'post_id': self.post.pk}): 'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def assert_post(self, first_object):
        """Сверка постов."""
        post_context = {
            first_object.text: self.post.text,
            first_object.author.username: self.post.author.username,
            first_object.author.pk: self.post.author.pk,
            first_object.group.title: self.group.title,
            first_object.group.pk: self.group.pk,
            first_object.pk: self.post.pk,
        }
        for key, value in post_context.items():
            with self.subTest(key=key):
                self.assertEqual(key, value)

    def test_index_pages_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        self.assert_post(first_object)

    def test_group_list_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
        )
        group_context = {
            'title': self.group.title,
            'description': self.group.description,
            'slug': self.group.slug,
            'pk': self.group.pk,
        }
        for key, value in group_context.items():
            with self.subTest(key=key):
                self.assertEqual(
                    getattr(response.context.get('group'), key), value
                )

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом"""
        response = (self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.author})))
        first_object = response.context['page_obj'][0]
        self.assert_post(first_object)

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом"""
        response = (self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.pk})))
        self.assertEqual(response.context.get('post').id, self.post.pk)

    def test_post_edit_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом"""
        response = self.authorized_client.get(reverse(
            'posts:post_edit', kwargs={'post_id': self.post.pk}))
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context.get('form'), PostForm)
        self.assertIs(type(response.context.get('is_edit')), bool)
        self.assertEqual(response.context.get('is_edit'), True)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_create_show_correct_context(self):
        """Шаблон create_post сформирован с правильным контекстом"""
        response = self.authorized_client.get(reverse('posts:post_create'))
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context.get('form'), PostForm)

    def test_post_another_group(self):
        """Пост не попал в другую группу"""
        response = self.guest_client.get(
            reverse("posts:group_list", kwargs={"slug": self.group_2.slug})
        )
        group_post_list_2 = response.context.get("page_obj").object_list
        self.assertNotIn(self.post, group_post_list_2)

    def test_404(self):
        """404='core/404.html'"""
        response = self.guest_client.get('/not_existing_page/')
        template = 'core/404.html'
        self.assertTemplateUsed(response, template)

    def test_cache(self):
        """Тест кеширования"""
        response = self.guest_client.get(reverse("posts:index"))
        key1 = response.content
        Post.objects.get(id=1).delete()
        response2 = self.guest_client.get(reverse("posts:index"))
        key2 = response2.content
        self.assertEqual(key1, key2)

    def test_comment(self):
        """Тест коммента."""
        comments_count = Comment.objects.count()
        form_data = {"text": "Тестовый коммент"}
        response = self.authorized_client.post(
            reverse("posts:add_comment", kwargs={"post_id": self.post.id}),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response, reverse("posts:post_detail",
                              kwargs={"post_id": self.post.id})
        )
        self.assertEqual(Comment.objects.count(), comments_count + 1)
        self.assertTrue(Comment.objects.filter(text="Тестовый коммент")
                        .exists())

    def test_follow(self):
        """Проверяю подписку на автора."""
        test_author = User.objects.create(username="skala")
        self.authorized_client.post(
            reverse("posts:profile_follow", kwargs={"username": test_author})
        )
        self.assertIs(
            Follow.objects.filter(user=self.author,
                                  author=test_author).exists(),
            True
        )

    def test_unfollow(self):
        """Проверяю отписку от автора."""
        test_author = User.objects.create(username="skala1")
        self.authorized_client.force_login(self.author)
        self.authorized_client.post(
            reverse("posts:profile_unfollow", kwargs={"username": test_author})
        )
        self.assertIs(
            Follow.objects.filter(user=self.author,
                                  author=test_author).exists(),
            False
        )

    def test_follow_function(self):
        test_author = User.objects.create(username="skala3")
        self.authorized_client.force_login(test_author)
        self.assertIs(
            Follow.objects.filter(user=test_author,
                                  author=test_author).exists(),
            False
        )


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(
            username='test_username',
            email='test@test.ru',
            password='Test1234',
        )
        cls.group = Group.objects.create(
            title=('Заголовок для тестовой группы'),
            slug='test_slug2',
            description='Тестовое описание')
        cls.posts = []
        for i in range(13):
            cls.posts.append(Post(
                text=f'Тестовый пост {i}',
                author=cls.author,
                group=cls.group
            )
            )
        Post.objects.bulk_create(cls.posts)

    def setUp(self):
        self.guest_client = Client()
        self.author = User.objects.get(username='test_username')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def test_paginator(self):
        """Проверяю пагинацию."""
        list_urls = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': self.group.slug}),
            reverse('posts:profile', kwargs={'username': self.author}),
        ]
        for tested_url in list_urls:
            response = self.client.get(tested_url)
            self.assertEqual(
                len(response.context.get('page_obj').object_list),
                settings.PAGINATION
            )
