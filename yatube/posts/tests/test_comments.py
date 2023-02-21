# from django.urls import reverse

# from ..models import Comment


# def test_comment_correct_context(self):
#     """Тест коммента."""
#     comments_count = Comment.objects.count()
#     form_data = {"text": "Тестовый коммент"}
#     response = self.authorized_client.post(
#         reverse("posts:add_comment", kwargs={"post_id": self.post.id}),
#         data=form_data,
#         follow=True,
#     )
#     self.assertRedirects(
#         response, reverse("posts:post_detail",
#                           kwargs={"post_id": self.post.id})
#     )
#     self.assertEqual(Comment.objects.count(), comments_count + 1)
#     self.assertTrue(Comment.objects.filter(text="Тестовый коммент").exists())
