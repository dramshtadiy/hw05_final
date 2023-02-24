# import shutil
# import tempfile

# from django.conf import settings
# from django.core.files.uploadedfile import SimpleUploadedFile
# from django.test import Client, TestCase, override_settings
# from django.urls import reverse

# from ..models import Group, Post, User

# TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


# @override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
# class TaskPagesTests(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super(TaskPagesTests, cls).setUpClass()
#         cls.user = User.objects.create_user(username="HasNoName")
#         cls.group = Group.objects.create(
#             title="Test group",
#             slug="test_group_slug",
#             description="Test group description",
#         )
#         cls.small_gif = (
#             b"\x47\x49\x46\x38\x39\x61\x02\x00"
#             b"\x01\x00\x80\x00\x00\x00\x00\x00"
#             b"\xFF\xFF\xFF\x21\xF9\x04\x00\x00"
#             b"\x00\x00\x00\x2C\x00\x00\x00\x00"
#             b"\x02\x00\x01\x00\x00\x02\x02\x0C"
#             b"\x0A\x00\x3B"
#         )
#         cls.uploaded = SimpleUploadedFile(
#             name="small.gif", content=cls.small_gif, content_type="image/gif"
#         )
#         cls.post = Post.objects.create(
#             author=cls.user, text="Тестовый текст",
#             group=cls.group, image=cls.uploaded
#         )

#     @classmethod
#     def tearDownClass(cls):
#         super().tearDownClass()
#         shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

#     def setUp(self):
#         self.guest_client = Client()

#     def test_image_in_group_list_page(self):
#         """Картинка передается на страницу group_list."""
#         response = self.guest_client.get(
#             reverse("posts:group_list", kwargs={"slug": self.group.slug}),
#         )
#         obj = response.context["page_obj"][0]
#         self.assertEqual(obj.image, self.post.image)

#     def test_image_in_index_and_profile_page(self):
#         """Картинка передается на страницу index_and_profile."""
#         templates = (
#             reverse("posts:index"),
#             reverse("posts:profile", kwargs={"username": self.post.author}),
#         )
#         for url in templates:
#             with self.subTest(url):
#                 response = self.guest_client.get(url)
#                 obj = response.context["page_obj"][0]
#                 self.assertEqual(obj.image, self.post.image)

#     def test_image_in_post_detail_page(self):
#         """Картинка передается на страницу post_detail."""
#         response = self.guest_client.get(
#             reverse("posts:post_detail", kwargs={"post_id": self.post.id})
#         )
#         obj = response.context["post"]
#         self.assertEqual(obj.image, self.post.image)

#     def test_image_in_page(self):
#         """Проверяем что пост с картинкой создается в БД"""
#         self.assertTrue(
#             Post.objects.filter(text="Тестовый текст",
#                                 image="posts/small.gif").exists()
#         )
