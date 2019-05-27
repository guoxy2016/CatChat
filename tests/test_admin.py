from flask import url_for

from .base import BaseTestCase


class AdminTestCase(BaseTestCase):
    def test_delete_user(self):
        response = self.client.delete(url_for('admin.block_user', user_id='2'))
        self.assertIn("permission to access the requested resource", response.get_data(as_text=True))
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.delete(url_for('admin.block_user', user_id='20'))
        self.assertIn("sent a request that this server could not understand", response.get_data(as_text=True))
        self.assertEqual(response.status_code, 400)

        response = self.client.delete(url_for('admin.block_user', user_id='2'))
        data = response.get_data(as_text=True)
        self.assertEqual("", data)
        self.assertEqual(response.status_code, 204)
