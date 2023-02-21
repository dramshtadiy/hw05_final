# from django.urls import reverse

# from ..models import Post


# def test_check_cache(self):
#     """Тесты кеширования через пост/индекс."""
#     response = self.guest_client.get(reverse("posts:index"))
#     key1 = response.content
#     Post.objects.get(id=1).delete()
#     response2 = self.guest_client.get(reverse("posts:index"))
#     key2 = response2.content
#     self.assertEqual(key1, key2)
