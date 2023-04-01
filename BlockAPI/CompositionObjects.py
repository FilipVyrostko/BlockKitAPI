from typing import Optional

from BlockAPI.BlockInterface import BlockInterface
from BlockAPI.utils import *


class Text(BlockInterface):

    def __init__(self, type: str, text: str, emoji: bool = True, verbatim: bool = False):

        check_valid_type(type)
        check_length(text, _min=1, _max=3000)

        self._type = type
        self._text = text
        self._emoji = emoji
        self._verbatim = verbatim

        if type == PLAIN_TEXT:
            self._body = {
                "type": type,
                "text": text,
                "emoji": emoji
            }
        else:
            self._body = {
                "type": type,
                "text": text,
                "verbatim": verbatim
            }

    def __eq__(self, other):
        return isinstance(other, Text) and self._body == other._body

    @property
    def type(self) -> str:
        return self._type

    @property
    def text(self) -> str:
        return self._text

    @property
    def emoji(self) -> Optional[bool]:
        return self._emoji

    @property
    def verbatim(self) -> Optional[bool]:
        return self._verbatim

    @text.setter
    def text(self, text: str):
        check_length(text, _min=1, _max=3000)
        self._body["text"] = text
        self._text = text

    @type.setter
    def type(self, type: str):
        check_valid_type(type)

        if type == PLAIN_TEXT:
            self._body.pop("verbatim", None)
            self._body["emoji"] = self._emoji
        else:
            self._body.pop("emoji", None)
            self._body["verbatim"] = self._verbatim

        self._body["type"] = type
        self._type = type

    @emoji.setter
    def emoji(self, _emoji: bool):
        self._body["emoji"] = _emoji
        self._emoji = _emoji

    @verbatim.setter
    def verbatim(self, _verbatim: bool):
        self._body["verbatim"] = _verbatim
        self._verbatim = _verbatim


class ConfirmationDialog(BlockInterface):

    def __init__(self, title: Text, text: Text, confirm: Text, deny: Text, style: str = DEFAULT):
        check_length(title.text, _min=1, _max=100)
        check_valid_type(title.type, _types=PLAIN_TEXT)
        check_length(text.text, _min=1, _max=300)
        check_length(confirm.text, _min=1, _max=30)
        check_valid_type(confirm.type, _types=PLAIN_TEXT)
        check_length(deny.text, _min=1, _max=30)
        check_valid_type(deny.type, _types=PLAIN_TEXT)
        check_style(style)

        self._title = title
        self._text = text
        self._confirm = confirm
        self._deny = deny
        self._style = style

        self._body = {
            "title": title,
            "text": text,
            "confirm": confirm,
            "deny": deny,
        }

        if style != DEFAULT:
            self._body["style"] = style

    @property
    def title(self):
        return self._title

    @property
    def text(self):
        return self._text

    @property
    def style(self):
        return self._style

    @property
    def confirm(self):
        return self._confirm

    @property
    def deny(self):
        return self._deny

    @title.setter
    def title(self, _title: Text):
        check_length(_title.text, _min=1, _max=100)
        check_valid_type(_title.type, _types=PLAIN_TEXT)
        self._title = _title
        self._body["title"] = _title

    @text.setter
    def text(self, _text: Text):
        check_length(_text.text, _min=1, _max=300)
        self._text = _text
        self._body["text"] = _text

    @confirm.setter
    def confirm(self, _confirm: Text):
        check_length(_confirm.text, _min=1, _max=30)
        check_valid_type(_confirm.type, _types=PLAIN_TEXT)
        self._confirm = _confirm
        self._body["confirm"] = _confirm

    @deny.setter
    def deny(self, _deny: Text):
        check_length(_deny.text, _min=1, _max=30)
        check_valid_type(_deny.type, _types=PLAIN_TEXT)
        self._deny = _deny
        self._body["deny"] = _deny

    @style.setter
    def style(self, _style: str = DEFAULT):
        check_style(_style)
        if _style == DEFAULT:
            self._body.pop("style", None)
        else:
            self._body["style"] = _style
        self._style = _style


class Option(BlockInterface):

    def __init__(self, text: Text, value: str, description: Text = None, url: str = None):
        check_length(text.text, _min=1, _max=75)
        check_valid_type(text.type, _types=PLAIN_TEXT)
        check_length(value, _min=1, _max=75)

        self._text = text
        self._value = value
        self._description = description
        self._url = url

        self._body = {
            "text": text,
            "value": value,
        }

        if description is not None:
            check_length(description.text, _min=1, _max=75)
            check_valid_type(description.type, _types=PLAIN_TEXT)
            self._body["description"] = description
        if url is not None:
            check_length(url, _min=1, _max=3000)
            self._body["url"] = url
            
    def __eq__(self, other):
        return isinstance(other, Option) and self._body == other._body

    @property
    def text(self):
        return self._text

    @property
    def value(self):
        return self._value

    @property
    def description(self) -> Optional[Text]:
        return self._description

    @property
    def url(self) -> Optional[str]:
        return self._url

    @text.setter
    def text(self, _text: Text):
        check_length(_text.text, _min=1, _max=75)
        check_valid_type(_text.type, _types=PLAIN_TEXT)
        self._text = _text
        self._body["text"] = _text

    @value.setter
    def value(self, _value: str):
        check_length(_value, _min=1, _max=75)
        self._value = _value
        self._body["value"] = _value

    @description.setter
    def description(self, _description):
        check_length(_description.text, _min=1, _max=75)
        check_valid_type(_description.type, _types=PLAIN_TEXT)
        self._description = _description
        self._body["description"] = _description

    @url.setter
    def url(self, _url):
        check_length(_url, _min=1, _max=3000)
        self._url = _url
        self._body["url"] = _url


class OptionGroups(BlockInterface):

    def __init__(self, label: Text, options: List[Option]):
        check_length(label.text, _min=1, _max=75)
        check_valid_type(label.type, _types=PLAIN_TEXT)
        check_length(options, _min=1, _max=100)

        self._label = label
        self._options = options

        self._body = {
            "label": label,
            "options": options,
        }

    @property
    def label(self):
        return self._label

    @property
    def options(self):
        return self._options

    @label.setter
    def label(self, _label: Text):
        check_length(_label.text, _min=1, _max=75)
        check_valid_type(_label.type, _types=PLAIN_TEXT)
        self._label = _label
        self._body["label"] = _label

    @options.setter
    def options(self, _options: List[Option]):
        check_length(_options, _min=1, _max=100)
        self._options = _options
        self._body["options"] = _options


class ConversationFilters(BlockInterface):

    def __init__(self, include: List[str] = None, exclude_external: bool = False, exclude_bots: bool = False):
        self._body = {}

        if include is not None:
            check_filter_options(include)
            self._body["include"] = include

        self._include = include
        self._exclude_external = exclude_external
        self._body["exclude_external_shared_channels"] = exclude_external
        self._exclude_bots = exclude_bots
        self._body["exclude_bots"] = exclude_bots

    @property
    def include(self) -> Optional[List[str]]:
        return self._include

    @property
    def exclude_external(self) -> bool:
        return self._exclude_external

    @property
    def exclude_bots(self) -> bool:
        return self._exclude_bots

    @include.setter
    def include(self, _include: Optional[List[str]]):
        if _include is not None:
            check_filter_options(_include)
            self._body["include"] = _include
        else:
            self._body.pop("include", None)

        self._include = _include

    @exclude_external.setter
    def exclude_external(self, _exclude_external):
        self._exclude_external = _exclude_external
        self._body["exclude_external_shared_channels"] = _exclude_external

    @exclude_bots.setter
    def exclude_bots(self, _exclude_bots):
        self._exclude_bots = _exclude_bots
        self._body["exclude_bots"] = _exclude_bots


class DispatchActionConfig(BlockInterface):

    def __init__(self, config: List[str]):
        check_config_options(config)
        self._body = {"trigger_actions_on": config}
        self._config = config

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, _config: List[str]):
        check_config_options(_config)
        self._config = _config
        self._body["trigger_actions_on"] = _config
