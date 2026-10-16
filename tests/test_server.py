import unittest

import server


class SchemeSaathiTests(unittest.TestCase):
    def test_catalog_has_schemes(self):
        schemes = server.load_schemes()
        self.assertGreaterEqual(len(schemes), 5)

    def test_search_by_category(self):
        result = server.search_catalog(category="agriculture")
        self.assertGreaterEqual(len(result), 3)
        self.assertTrue(all(item["category"] == "agriculture" for item in result))

    def test_find_scheme_by_id(self):
        scheme = server.find_scheme("pm-kisan")
        self.assertIsNotNone(scheme)
        self.assertEqual(scheme["name"], "PM-KISAN Samman Nidhi")

    def test_unknown_scheme(self):
        self.assertIsNone(server.find_scheme("not-a-real-scheme"))

    def test_documents_exist(self):
        for scheme in server.load_schemes():
            self.assertTrue(scheme["documents_to_check"])
            self.assertTrue(scheme["official_url"].startswith("https://"))


if __name__ == "__main__":
    unittest.main()
