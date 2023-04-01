import unittest

from BlockAPI.CompositionObjects import Text, ConfirmationDialog, Option, OptionGroups, ConversationFilters, DispatchActionConfig
from BlockAPI.utils import PLAIN_TEXT, MRKDWN, DEFAULT, PRIMARY, DANGER


class TextTestCase(unittest.TestCase):
    def test_type(self):
        Text(type=PLAIN_TEXT, text="foo", verbatim=True)  # Should still work even with verbatim set to true
        Text(type=MRKDWN, text="foo", emoji=True)  # Should still work even with emoji set to true
        # Pass invalid type
        self.assertRaises(ValueError, Text, **{"type": "not_valid_type", "text": "foo"})

        _t = Text(type=PLAIN_TEXT, text="foo")
        _t.type = MRKDWN
        self.assertDictEqual(
            d1=_t.__dict__(),
            d2={"type": MRKDWN, "text": "foo", "verbatim": False},
            msg="Changing from plain_text to markdown should remove emoji and set verbatim."
        )

        _t.type = "plain_text"
        self.assertDictEqual(
            d1=_t.__dict__(),
            d2={"type": "plain_text", "text": "foo", "emoji": True},
            msg="Changing from markdown to plain_text should remove verbatim and set emoji."
        )

    def test_text(self):
        # Text.text must be between 1 and 3000 characters long by default
        self.assertRaises(ValueError, Text, **{"type": "plain_text", "text": "f" * 3001})
        self.assertRaises(ValueError, Text, **{"type": "plain_text", "text": ""})

        Text(type=PLAIN_TEXT, text="f" * 3000)
        Text(type=PLAIN_TEXT, text="f")

    def test_emoji(self):
        _t = Text(type=PLAIN_TEXT, text="foo")
        self.assertIn("emoji", _t._body)
        self.assertTrue(_t._body["emoji"])
        self.assertTrue(_t.emoji)

        _t.emoji = False
        self.assertFalse(_t.emoji)
        self.assertFalse(_t._body["emoji"])

        _t = Text(type=MRKDWN, text="foo")
        self.assertNotIn("emoji", _t._body)
        self.assertTrue(_t.emoji)

        _t.emoji = False
        self.assertFalse(_t.emoji)

    def test_verbatim(self):
        _t = Text(type=MRKDWN, text="foo")
        self.assertIn("verbatim", _t._body)
        self.assertFalse(_t._body["verbatim"])
        self.assertFalse(_t.verbatim)

        _t.verbatim = True
        self.assertTrue(_t.verbatim)
        self.assertTrue(_t._body["verbatim"])

        _t = Text(type=PLAIN_TEXT, text="foo")
        self.assertNotIn("verbatim", _t._body)
        self.assertFalse(_t.verbatim)

        _t.verbatim = True
        self.assertTrue(_t.verbatim)


class ConfirmationDialogTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._title = Text(type=PLAIN_TEXT, text="foo")
        self._text = Text(type=PLAIN_TEXT, text="foo")
        self._confirm = Text(type=PLAIN_TEXT, text="foo")
        self._deny = Text(type=PLAIN_TEXT, text="foo")
        self._c = ConfirmationDialog(self._title, self._text, self._confirm, self._deny)

    def test_title(self):
        # Title text type can only be plain text
        self._title.type = MRKDWN
        self.assertRaises(ValueError, ConfirmationDialog, self._title, self._text, self._confirm, self._deny)

        # Title text length must be in range [1, 100]
        self._title.type = PLAIN_TEXT
        self._title.text = "f" * 101
        self.assertRaises(ValueError, ConfirmationDialog, self._title, self._text, self._confirm, self._deny)

        _t = Text(type=MRKDWN, text="foo")
        try:
            self._c.title = _t
        except ValueError:
            assert True
        else:
            assert False

        _t = Text(type=PLAIN_TEXT, text="f" * 101)
        try:
            self._c.title = _t
        except ValueError:
            assert True
        else:
            assert False

    def test_text(self):
        self._text.type = MRKDWN
        ConfirmationDialog(self._title, self._text, self._confirm, self._deny)

        self._text.text = "f" * 301
        self.assertRaises(ValueError, ConfirmationDialog, self._title, self._text, self._confirm, self._deny)

        _t = Text(type=PLAIN_TEXT, text="f" * 301)
        try:
            self._c.text = _t
        except ValueError:
            assert True
        else:
            assert False

    def test_style(self):
        ConfirmationDialog(self._title, self._text, self._confirm, self._deny, DEFAULT)
        ConfirmationDialog(self._title, self._text, self._confirm, self._deny, PRIMARY)
        ConfirmationDialog(self._title, self._text, self._confirm, self._deny, DANGER)
        self.assertRaises(ValueError, ConfirmationDialog, self._title, self._text, self._confirm, self._deny, "foo")

    def test_confirm(self):
        # Confirm text type can only be plain text
        self._confirm.type = MRKDWN
        self.assertRaises(ValueError, ConfirmationDialog, self._title, self._text, self._confirm, self._deny)

        # Confirm text length must be in range [1, 30]
        self._confirm.type = PLAIN_TEXT
        self._confirm.text = "f" * 31
        self.assertRaises(ValueError, ConfirmationDialog, self._title, self._text, self._confirm, self._deny)

        _t = Text(type=MRKDWN, text="foo")
        try:
            self._c.confirm = _t
        except ValueError:
            assert True
        else:
            assert False

        _t = Text(type=PLAIN_TEXT, text="f" * 31)
        try:
            self._c.confirm = _t
        except ValueError:
            assert True
        else:
            assert False

    def test_deny(self):
        # Deny text type can only be plain text
        self._deny.type = MRKDWN
        self.assertRaises(ValueError, ConfirmationDialog, self._title, self._text, self._confirm, self._deny)

        # Deny text length must be in range [1, 30]
        self._deny.type = PLAIN_TEXT
        self._deny.text = "f" * 31
        self.assertRaises(ValueError, ConfirmationDialog, self._title, self._text, self._confirm, self._deny)

        _t = Text(type=MRKDWN, text="foo")
        try:
            self._c.deny = _t
        except ValueError:
            assert True
        else:
            assert False

        _t = Text(type=PLAIN_TEXT, text="f" * 31)
        try:
            self._c.deny = _t
        except ValueError:
            assert True
        else:
            assert False


class OptionTestCase(unittest.TestCase):

    def setUp(self):
        self._text = Text(type=PLAIN_TEXT, text="foo")
        self._value = "foo"
        self._o = Option(self._text, self._value)

    def test_text(self):
        self._text.type = MRKDWN
        self.assertRaises(ValueError, Option, self._text, self._value)
        self._text.text = "f" * 76
        self.assertRaises(ValueError, Option, self._text, self._value)

        _t = Text(type=MRKDWN, text="foo")
        try:
            self._o.text = _t
        except ValueError:
            assert True
        else:
            assert False

        _t = Text(type=PLAIN_TEXT, text="f" * 76)
        try:
            self._o.text = _t
        except ValueError:
            assert True
        else:
            assert False

    def test_value(self):
        self._value = "f" * 76
        self.assertRaises(ValueError, Option, self._text, self._value)

        try:
            self._o.value = "f" * 76
        except ValueError:
            assert True
        else:
            assert False

    def test_description(self):
        _d = Text(type=PLAIN_TEXT, text="foo")
        _o = Option(self._text, self._value, _d)
        _d.type = MRKDWN
        self.assertRaises(ValueError, Option, self._text, self._value, _d)

        try:
            _o.description = _d
        except ValueError:
            assert True
        else:
            assert False

    def test_url(self):
        _url = "foo"
        _o = Option(self._text, self._value, url=_url)
        _url = "f"*3001
        self.assertRaises(ValueError, Option, self._text, self._value, None, _url)
        _url = ""
        self.assertRaises(ValueError, Option, self._text, self._value, None, _url)

        try:
            _o.url = "f"*3001
        except ValueError:
            assert True
        else:
            assert False

        try:
            _o.url = ""
        except ValueError:
            assert True
        else:
            assert False


class OptionGroupTestCase(unittest.TestCase):
    def setUp(self):
        self._label = Text(type=PLAIN_TEXT, text="foo")
        self._options = [
            Option(
                text=self._label,
                value="foo"
            )
        ]*100
        self._og = OptionGroups(self._label, self._options)

    def test_label(self):
        self._label.type = MRKDWN
        self.assertRaises(ValueError, OptionGroups, self._label, self._options)
        self._label.text = "f" * 76
        self.assertRaises(ValueError, OptionGroups, self._label, self._options)

        _t = Text(type=MRKDWN, text="foo")
        try:
            self._og.label = _t
        except ValueError:
            assert True
        else:
            assert False

        _t = Text(type=PLAIN_TEXT, text="f" * 76)
        try:
            self._og.label = _t
        except ValueError:
            assert True
        else:
            assert False

    def test_options(self):
        self._options = [self._options[0]]*101
        self.assertRaises(ValueError, OptionGroups, self._label, self._options)
        self._options = []
        self.assertRaises(ValueError, OptionGroups, self._label, self._options)


class ConversationFiltersTestCase(unittest.TestCase):
    def setUp(self):
        self._c = ConversationFilters()

    def test_include(self):
        _include = ["foo"]
        self.assertRaises(ValueError, ConversationFilters, _include)
        _include = []
        self.assertRaises(ValueError, ConversationFilters, _include)
        _include = ["im", "public"]
        ConversationFilters(_include)

        _include = ["foo"]
        try:
            self._c.include = _include
        except ValueError:
            assert True
        else:
            assert False

        _include = []
        try:
            self._c.include = _include
        except ValueError:
            assert True
        else:
            assert False

        self._c.include = None
        self.assertIsNone(self._c._body.get("include"))


class DispatchActionConfigTestCase(unittest.TestCase):
    def test_config(self):
        _config = ["on_enter_pressed", "on_character_entered"]
        _c = DispatchActionConfig(_config)

        _config = ["foo"]
        self.assertRaises(ValueError, DispatchActionConfig, _config)
        _config = ["on_enter_pressed", "foo"]
        self.assertRaises(ValueError, DispatchActionConfig, _config)
        _config = []
        self.assertRaises(ValueError, DispatchActionConfig, _config)


if __name__ == '__main__':
    unittest.main()

