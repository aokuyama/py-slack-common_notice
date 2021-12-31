import requests
import json


class SlackNotice:
    def __init__(self, content={}) -> None:
        self.set(**content)

    def set(self, url=None, level=None, title=None, text=None):
        self.url = url
        self.level = level
        self.title = title
        self.text = text
        return self

    def send(self):
        if not self.url:
            raise
        level = self.getLevel(self.level)
        color = self.getColor(level)
        text = self.toText(self.text)
        main_text = ''
        if level > 1:
            main_text = '<!channel>'
        data = {
            "text": main_text,
            "attachments": [
                {
                    "title": self.title,
                    "text": text,
                    "color": color,
                }
            ]
        }
        return requests.post(self.url, json.dumps(data))

    def getLevel(self, var):
        if var == None:
            return 0
        if type(var) == int:
            return var
        if type(var) != str:
            return 9
        if var == 'notice':
            return 1
        if var == 'warn':
            return 2
        if var == 'error':
            return 3
        return 9

    def getColor(self, level):
        if level == 0:
            return None
        if level == 1:
            return "good"
        if level == 2:
            return "warning"
        if level == 3:
            return "danger"
        return "danger"

    def toText(self, var):
        if type(var) == str:
            return var
        return str(var)


if __name__ == '__main__':
    import unittest

    class SlackNoticeTest(unittest.TestCase):
        def setUp(self):
            self.s = SlackNotice()

        def test通知レベル(self):
            self.assertEqual(1, self.s.getLevel(1))
            self.assertEqual(3, self.s.getLevel(3))
            self.assertEqual(1, self.s.getLevel("notice"))
            self.assertEqual(2, self.s.getLevel("warn"))
            self.assertEqual(3, self.s.getLevel("error"))
            self.assertEqual(0, self.s.getLevel(None))

        def test色(self):
            self.assertEqual("good", self.s.getColor(1))
            self.assertEqual("danger", self.s.getColor(99))
            self.assertEqual("warning", self.s.getColor(2))
            self.assertIsNone(self.s.getColor(0))

        def testDict(self):
            self.s.set(**{"url": "example.com"})
            self.assertEqual("example.com", self.s.url)
            self.assertIsNone(self.s.level)

        def testText(self):
            self.assertEqual("abc", self.s.toText("abc"))
            self.assertEqual("['a']", self.s.toText(["a"]))
            self.assertEqual("{'b': 1}", self.s.toText({"b":1}))

    unittest.main()
