import unittest

from rag_bot.auth import authenticate, get_login_config


class AuthTests(unittest.TestCase):
    def test_get_login_config_uses_local_defaults_when_env_missing(self):
        config = get_login_config({})

        self.assertEqual(config.username, "admin")
        self.assertEqual(config.password, "ragbot")
        self.assertTrue(config.uses_default_password)

    def test_get_login_config_uses_environment_values(self):
        config = get_login_config(
            {
                "RAG_BOT_USERNAME": "tester",
                "RAG_BOT_PASSWORD": "strong-password",
            }
        )

        self.assertEqual(config.username, "tester")
        self.assertEqual(config.password, "strong-password")
        self.assertFalse(config.uses_default_password)

    def test_authenticate_requires_exact_username_and_password(self):
        config = get_login_config(
            {
                "RAG_BOT_USERNAME": "tester",
                "RAG_BOT_PASSWORD": "strong-password",
            }
        )

        self.assertTrue(authenticate("tester", "strong-password", config))
        self.assertFalse(authenticate("tester", "wrong", config))
        self.assertFalse(authenticate(" tester ", "strong-password", config))


if __name__ == "__main__":
    unittest.main()
