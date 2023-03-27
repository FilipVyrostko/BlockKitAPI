from BlockAPI.BlockElements import *
from .utils import *


class ActionBlock(BlockInterface):
    __restricted_types = [StaticOptions, ExternalDataOptions,
                          UserListOptions, ConversationOptions,
                          PublicChannelOptions]

    def __init__(self,
                 elements: List[Union[Button, CheckBoxGroup, DatePicker,
                                DateTimePicker, OverFlowMenu, RadioButtonGroup,
                                StaticOptions, ExternalDataOptions, UserListOptions,
                                ConversationOptions, PublicChannelOptions, TimePicker]],
                 block_id: str = None):
        check_length(elements, _min=1, _max=25)
        for _e in elements:
            if type(_e) in self.__restricted_types and _e.type.startswith("multi"):
                raise ValueError("Only single type options can be used with Action Block.")

        self._body = {
            "type": "actions",
            "elements": elements
        }

        if block_id:
            check_length(block_id, _min=1, _max=255)
            self._body["block_id"] = block_id

        self._elements = elements
        self._block_id = block_id

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, _elements):
        check_length(_elements, _min=1, _max=25)
        for _e in _elements:
            if type(_e) in self.__restricted_types and _e.type.startswith("multi"):
                raise ValueError("Only single type options can be used with Action Block.")
        self._body["elements"] = _elements
        self._elements = _elements

    @property
    def block_id(self):
        return self._block_id

    @block_id.setter
    def block_id(self, _block_id):
        self._set_block_id(_block_id)


class ContextBlock(BlockInterface):

    def __init__(self,
                 elements: List[Union[Image, Text]],
                 block_id: str = None):

        check_length(elements, _min=1, _max=10)

        self._body = {
            "type": "context",
            "elements": elements
        }

        if block_id:
            check_length(block_id, _min=1, _max=255)
            self._body["block_id"] = block_id

        self._elements = elements
        self._block_id = block_id

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, _elements):
        check_length(_elements, _min=1, _max=10)
        self._body["elements"] = _elements
        self._elements = _elements

    @property
    def block_id(self):
        return self._block_id

    @block_id.setter
    def block_id(self, _block_id):
        self._set_block_id(_block_id)


class DividerBlock(BlockInterface):

    def __init__(self, block_id: str = None):
        self._body = {
            "type": "divider"
        }
        if block_id:
            check_length(block_id, _min=1, _max=255)
            self._body["block_id"] = block_id

        self._block_id = block_id

    @property
    def block_id(self):
        return self._block_id

    @block_id.setter
    def block_id(self, _block_id):
        self._set_block_id(_block_id)


class FileBlock(BlockInterface):

    def __init__(self,
                 external_id: str,
                 # source: str,
                 block_id: str = None):

        self._body = {
            "type": "file",
            "external_id": external_id,
            "source": "remote"
        }
        if block_id:
            check_length(block_id, _min=1, _max=255)
            self._body["block_id"] = block_id

        self._block_id = block_id
        self._external_id = external_id

    @property
    def external_id(self):
        return self._external_id

    @external_id.setter
    def external_id(self, _external_id):
        self._body["external_id"] = _external_id
        self._external_id = _external_id

    @property
    def block_id(self):
        return self._block_id

    @block_id.setter
    def block_id(self, _block_id):
        self._set_block_id(_block_id)


class HeaderBlock(BlockInterface):

    def __init__(self,
                 text: Text,
                 block_id: str = None):
        check_length(text.text, _min=1, _max=150)
        check_valid_type(text.type, _types=PLAIN_TEXT)

        self._body = {
            "type": "header",
            "text": text
        }

        if block_id:
            check_length(block_id, _min=1, _max=255)
            self._body["block_id"] = block_id

        self._block_id = block_id
        self._text = text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, _text):
        check_length(_text.text, _min=1, _max=150)
        check_valid_type(_text.type, _types=PLAIN_TEXT)
        self._body["text"] = _text
        self._text = _text

    @property
    def block_id(self):
        return self._block_id

    @block_id.setter
    def block_id(self, _block_id):
        self._set_block_id(_block_id)


class ImageBlock(BlockInterface):

    def __init__(self,
                 image_url: str,
                 alt_text: str,
                 title: Text = None,
                 block_id: str = None):
        check_length(image_url, _min=1, _max=3000)
        check_length(alt_text, _min=1, _max=2000)

        self._body = {
            "type": "image",
            "image_url": image_url,
            "alt_text": alt_text
        }

        if title:
            check_length(title.text, _min=1, _max=2000)
            check_valid_type(title.type, _types=PLAIN_TEXT)
            self._body["title"] = title
        if block_id:
            check_length(block_id, _min=1, _max=255)
            self._body["block_id"] = block_id

        self._block_id = block_id
        self._image_url = image_url
        self._alt_text = alt_text
        self._title = title

    @property
    def image_url(self):
        return self._image_url

    @image_url.setter
    def image_url(self, _image_url):
        check_length(_image_url, _min=1, _max=3000)
        self._body["image_url"] = _image_url
        self._image_url = _image_url

    @property
    def alt_text(self):
        return self._alt_text

    @alt_text.setter
    def alt_text(self, _alt_text):
        check_length(_alt_text, _min=1, _max=2000)
        self._body["alt_text"] = _alt_text
        self._alt_text = _alt_text

    @property
    def title(self):
        return self.title

    @title.setter
    def title(self, _title):
        if _title:
            check_length(_title.text, _min=1, _max=2000)
            check_valid_type(_title.type, _types=PLAIN_TEXT)
            self._body["title"] = _title
        else:
            self._body.pop("title", None)
        self._title = _title

    @property
    def block_id(self):
        return self._block_id

    @block_id.setter
    def block_id(self, _block_id):
        self._set_block_id(_block_id)


class InputBlock(BlockInterface):

    def __init__(self,
                 label: Text,
                 element: Union[CheckBoxGroup, DatePicker, DateTimePicker,
                                EmailInput, StaticOptions, ExternalDataOptions,
                                UserListOptions, ConversationOptions, PublicChannelOptions,
                                NumberInput, PlainTextInput, RadioButtonGroup,
                                TimePicker, UrlInput],
                 dispatcher_action: bool = False,
                 block_id: str = None,
                 hint: Text = None,
                 optional: bool = False):

        check_length(label.text, _min=1, _max=2000)
        check_valid_type(label.type, _types=PLAIN_TEXT)

        self._body = {
            "type": "input",
            "label": label,
            "element": element,
        }

        if block_id:
            check_length(block_id, _min=1, _max=255)
            self._body["block_id"] = block_id
        if hint:
            check_length(hint.text, _min=1, _max=2000)
            check_valid_type(hint.type, _types=PLAIN_TEXT)
            self._body["hint"] = hint
        if dispatcher_action:
            self._body["dispatcher_action"] = dispatcher_action
        self._body["optional"] = optional

        self._label = label
        self._element = element
        self._dispatcher_action = dispatcher_action
        self._block_id = block_id
        self._hint = hint
        self._optional = optional

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, _label):
        check_length(_label.text, _min=1, _max=2000)
        check_valid_type(_label.type, _types=PLAIN_TEXT)
        self._body["label"] = _label
        self._label = _label

    @property
    def element(self):
        return self._element

    @element.setter
    def element(self, _element):
        self._body["element"] = _element
        self._element = _element

    @property
    def dispatcher_action(self):
        return self._dispatcher_action

    @dispatcher_action.setter
    def dispatcher_action(self, _dispatcher_action):
        self._body["dispatcher_action"] = _dispatcher_action
        self._dispatcher_action = _dispatcher_action

    @property
    def hint(self):
        return self._hint

    @hint.setter
    def hint(self, _hint):
        if _hint:
            check_length(_hint.text, _min=1, _max=2000)
            check_valid_type(_hint.type, _types=PLAIN_TEXT)
            self._body["hint"] = _hint
        else:
            self._body.pop("hint", None)
        self._hint = _hint

    @property
    def optional(self):
        return self._optional

    @optional.setter
    def optional(self, _optional):
        self._body["optional"] = _optional
        self._optional = _optional

    @property
    def block_id(self):
        return self._block_id

    @block_id.setter
    def block_id(self, _block_id):
        self._set_block_id(_block_id)


class SectionBlock(BlockInterface):

    def __init__(self,
                 text: Text = None,
                 block_id: str = None,
                 fields: List[Text] = None,
                 accessory: Union[Button, CheckBoxGroup, DatePicker,
                                  ImageBlock, StaticOptions, ExternalDataOptions,
                                  UserListOptions, ConversationOptions, PublicChannelOptions,
                                  OverFlowMenu, RadioButtonGroup, TimePicker] = None):

        if not text and not fields:
            raise ValueError("Either text or fields must be specified.")

        self._body = {
            "type": "section",
        }

        if text:
            check_length(text.text, _min=1, _max=3000)
            self._body["text"] = text
        if block_id:
            check_length(block_id, _min=1, _max=255)
            self._body["block_id"] = block_id
        if fields:
            check_length(fields, _min=1, _max=10)
            for _f in fields:
                check_length(_f.text, _min=1, _max=2000)
            self._body["fields"] = fields

        if accessory:
            self._body["accessory"] = accessory

        self._text = text,
        self._block_id = block_id
        self._fields = fields
        self._accessory = accessory

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, _text):
        if _text:
            check_length(_text.text, _min=1, _max=3000)
            self._body["text"] = _text
        else:
            if not self._fields:
                raise ValueError("Removing text but fields is not set. Either text or fields must be specified.")
            self._body.pop("text", None)
        self._text = _text

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, _fields):
        if _fields:
            check_length(_fields, _min=1, _max=10)
            for _f in _fields:
                check_length(_f.text, _min=1, _max=2000)
            self._body["fields"] = _fields
        else:
            if not self._text:
                raise ValueError("Removing fields but text is not set. Either text or fields must be specified.")
            self._body.pop("fields", None)
        self._fields = _fields


class VideoBlock(BlockInterface):

    def __init__(self,
                 alt_text: str,
                 title: Text,
                 thumbnail_url: str,
                 video_url: str,
                 author_name: str = None,
                 block_id: str = None,
                 description: Text = None,
                 provider_icon_url: str = None,
                 provider_name: str = None,
                 title_url: str = None):
        check_length(title.text, _min=1, _max=200)
        check_valid_type(title.type, _types=PLAIN_TEXT)
        if not video_url.startswith("https"):
            raise ValueError("Video URL must be HTTPS.")

        self._body = {
            "type": "video",
            "alt_text": alt_text,
            "title": title,
            "thumbnail_url": thumbnail_url,
            "video_url": video_url
        }

        if block_id:
            check_length(block_id, _min=1, _max=255)
            self._body["block_id"] = block_id
        if author_name:
            self._body["author_name"] = author_name
        if description:
            check_valid_type(description.type, _types=PLAIN_TEXT)
            self._body["description"] = description
        if provider_name:
            self._body["provider_name"] = provider_name
        if provider_icon_url:
            self._body["provider_icon_url"] = provider_icon_url
        if title_url:
            if not title_url.startswith("https"):
                raise ValueError("Title URL must be HTTPS.")
            self._body["title_url"] = title_url

        self._alt_text = alt_text
        self._title = title
        self._thumbnail_url = thumbnail_url
        self._video_url = video_url
        self._author_name = author_name
        self._block_id = block_id
        self._description = description
        self._provider_icon_url = provider_icon_url
        self._provider_name = provider_name
        self._title_url = title_url

    @property
    def alt_text(self):
        return self._alt_text

    @alt_text.setter
    def alt_text(self, _alt_text):
        self._body["alt_text"] = _alt_text
        self._alt_text = _alt_text

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, _title):
        check_length(_title.text, _min=1, _max=200)
        check_valid_type(_title.type, _types=PLAIN_TEXT)
        self._body["title"] = _title
        self._title = _title

    @property
    def thumbnail_url(self):
        return self._thumbnail_url

    @thumbnail_url.setter
    def thumbnail_url(self, _thumbnail_url):
        self._body["thumbnail_url"] = _thumbnail_url
        self._thumbnail_url = _thumbnail_url

    @property
    def video_url(self):
        return self._video_url

    @video_url.setter
    def video_url(self, _video_url):
        if not _video_url.startswith("https"):
            raise ValueError("Video URL must be HTTPS.")
        self._body["video_url"] = _video_url
        self._video_url = _video_url

    @property
    def author_name(self):
        return self._author_name

    @author_name.setter
    def author_name(self, _author_name):
        if _author_name:
            self._body["author_name"] = _author_name
        else:
            self._body.pop("author_name", None)
        self._author_name = _author_name

    @property
    def block_id(self):
        return self._block_id

    @block_id.setter
    def block_id(self, _block_id):
        self._set_block_id(_block_id)

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, _description):
        if _description:
            check_valid_type(_description.type, _types=PLAIN_TEXT)
            self._body["description"] = _description
        else:
            self._body.pop("description", None)
        self._description = _description

    @property
    def provider_icon_url(self):
        return self._provider_icon_url

    @provider_icon_url.setter
    def provider_icon_url(self, _provider_icon_url):
        if _provider_icon_url:
            self._body["provider_icon_url"] = _provider_icon_url
        else:
            self._body.pop("provide_icon_url", None)
        self._provider_icon_url = _provider_icon_url

    @property
    def provider_name(self):
        return self._provider_name

    @provider_name.setter
    def provider_name(self, _provider_name):
        if _provider_name:
            self._body["provider_name"] = _provider_name
        else:
            self._body.pop("provider_name", None)
        self._provider_name = _provider_name

    @property
    def title_url(self):
        return self._title_url

    @title_url.setter
    def title_url(self, _title_url):
        if _title_url:
            if not _title_url.startswith("https"):
                raise ValueError("Title URL must be HTTPS.")
            self._body["title_url"] = _title_url
        else:
            self._body.pop("title_url", None)
        self._title_url = _title_url
