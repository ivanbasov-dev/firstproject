import unittest
from app import app


class MovieCatalogTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_and_styles(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Касабланка', response.get_data(as_text=True))
        self.assertNotIn('poster.jpg', response.get_data(as_text=True))
        with self.client.get('/static/style.css') as stylesheet:
            self.assertEqual(stylesheet.status_code, 200)

    def test_search(self):
        for title, status in [('Касабланка', 200), ('', 400), ('   ', 400)]:
            with self.subTest(title=title):
                self.assertEqual(self.client.get('/search', query_string={'title': title}).status_code, status)
        self.assertEqual(self.client.get('/search').status_code, 400)

    def test_review_validation(self):
        for rating, status in [('1', 200), ('5', 200), ('0', 400), ('6', 400), ('2.5', 400), ('abc', 400), ('', 400)]:
            with self.subTest(rating=rating):
                result = self.client.post('/review', data={'title': 'Касабланка', 'rating': rating, 'review': 'Отличный фильм'})
                self.assertEqual(result.status_code, status)
                if status == 200:
                    self.assertIn(f'Оценка: {rating}/5.', result.get_data(as_text=True))
        for data in [{}, {'title': ' ', 'rating': '5', 'review': 'Текст'}, {'title': 'Фильм', 'rating': '5', 'review': ' '}]:
            self.assertEqual(self.client.post('/review', data=data).status_code, 400)
        self.assertEqual(self.client.get('/review').status_code, 405)

    def test_user_content_is_escaped(self):
        payload = '<script>alert(1)</script>'
        for response in [self.client.get('/search', query_string={'title': payload}), self.client.post('/review', data={'title': payload, 'rating': '5', 'review': 'Текст'})]:
            html = response.get_data(as_text=True)
            self.assertNotIn(payload, html)
            self.assertIn('&lt;script&gt;', html)


if __name__ == '__main__':
    unittest.main()
