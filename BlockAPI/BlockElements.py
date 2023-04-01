import datetime

from typing import Tuple

from BlockAPI.CompositionObjects import *


class Button(BlockInterface):
    def __init__(self, text: Text,
                 action_id: str,
                 url: str = None,
                 value: str = None,
                 style: str = DEFAULT,
                 confirm: ConfirmationDialog = None,
                 access_label: str = None):
        check_length(text.text, _min=1, _max=75)
        check_valid_type(text.type, _types=PLAIN_TEXT)
        check_length(action_id, _min=1, _max=255)

        self._body = {
            "type": "button",
            "text": text,
            "action_id": action_id
        }

        if value is not None:
            check_length(value, _min=1, _max=2000)
            self._body["value"] = value
        if url is not None:
            check_length(url, _min=1, _max=3000)
            self._body["url"] = url
        if style:
            check_style(style)
            self._body["style"] = style
        if confirm is not None:
            self._body["confirm"] = confirm
        if access_label is not None:
            check_length(access_label, _min=1, _max=75)
            self._body["accessibility_label"] = access_label

        self._text = text,
        self._action_id = action_id,
        self._url = url,
        self._value = value,
        self._style = style,
        self._confirm = confirm,
        self._access_label = access_label

    @property
    def text(self):
        return self._text

    @property
    def action_id(self):
        return self._action_id

    @property
    def url(self):
        return self._url

    @property
    def value(self):
        return self._value

    @property
    def style(self):
        return self._style

    @property
    def confirm(self):
        return self._confirm

    @property
    def access_label(self):
        return self._access_label

    @text.setter
    def text(self, _text):
        check_length(_text.text, _min=1, _max=75)
        check_valid_type(_text.type, _types=PLAIN_TEXT)
        self._text = _text
        self._body["text"] = _text

    @action_id.setter
    def action_id(self, _action_id):
        check_length(_action_id, _min=1, _max=255)
        self._action_id = _action_id
        self._body["action_id"] = _action_id

    @url.setter
    def url(self, _url: str):
        if _url is not None:
            check_length(_url, _min=1, _max=3000)
            self._body["url"] = _url
        else:
            self._body.pop("url", None)

        self._url = _url

    @value.setter
    def value(self, _value: str):
        if _value is not None:
            check_length(_value, _min=1, _max=2000)
            self._body["value"] = _value
        else:
            self._body.pop("value", None)

        self._value = _value

    @style.setter
    def style(self, _style):
        if _style == DEFAULT:
            self._body.pop("style", None)
        else:
            check_style(_style)
            self._body["style"] = _style

        self._style = _style

    @access_label.setter
    def access_label(self, _access_label):
        if _access_label is not None:
            check_length(_access_label, _min=1, _max=75)
            self._body["access_label"] = _access_label
        else:
            self._body.pop("access_label", None)

        self._access_label = _access_label

    @confirm.setter
    def confirm(self, _confirm):
        self._set_confirm(_confirm)


class CheckBoxGroup(BlockInterface):

    def __init__(self,
                 action_id: str,
                 options: List[Option],
                 init_options: List[Option] = None,
                 confirm: ConfirmationDialog = None,
                 focus_on_load: bool = False):
        check_options_no_url(options)
        check_length(action_id, _min=1, _max=255)
        check_length(options, _min=1, _max=10)

        self._body = {
            "type": "checkboxes",
            "action_id": action_id,
            "options": options
        }
        if init_options is not None:
            check_options_no_url(init_options)
            if not all(list(map(lambda x: x in options, init_options))):
                raise ValueError("Initial options must match the options list")
            self._body["initial_options"] = init_options
        if confirm:
            self._body["confirm"] = confirm
        self._body["focus_on_load"] = focus_on_load

        self._action_id = action_id
        self._options = options
        self._init_options = init_options
        self._confirm = confirm
        self._focus_on_load = focus_on_load

    @property
    def action_id(self):
        return self._action_id

    @action_id.setter
    def action_id(self, _action_id):
        self._set_action_id(_action_id)

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, _options):

        check_length(_options, _min=1, _max=10)
        if self._init_options:
            if not all(list(map(lambda x: x in self._options, self._init_options))):
                raise ValueError("Initial options must match the options list")

        self._options = _options
        self._body["options"] = _options

    @property
    def init_options(self):
        return self._init_options

    @init_options.setter
    def init_options(self, _init_options):
        if _init_options is not None:
            check_length(_init_options, _min=1, _max=10)
            if not all(list(map(lambda x: x in self._options, _init_options))):
                raise ValueError("Initial options must match the options list")
            else:
                self._body["initial_options"] = _init_options
        else:
            self._body.pop("initial_options", None)

        self._init_options = _init_options

    @property
    def confirm(self):
        return self._confirm

    @confirm.setter
    def confirm(self, _confirm):
        self._set_confirm(_confirm)

    @property
    def focus_on_load(self):
        return self._focus_on_load

    @focus_on_load.setter
    def focus_on_load(self, _focus_on_load):
        self._set_focus_on_load(_focus_on_load)


class DatePicker(BlockInterface):

    def __init__(self,
                 action_id: str,
                 placeholder: Text = None,
                 init_date: datetime.date = None,
                 confirm: ConfirmationDialog = None,
                 focus_on_load: bool = False):
        check_length(action_id, _min=1, _max=255)

        self._body = {
            "type": "datepicker",
            "action_id": action_id,
        }
        if placeholder:
            check_length(placeholder.text, _min=1, _max=255)
            check_valid_type(placeholder.type, _types=PLAIN_TEXT)
            self._body["placeholder"] = placeholder
        if init_date:
            self._body["initial_date"] = init_date.__str__()
        if confirm:
            self._body["confirm"] = confirm
        self._body["focus_on_load"] = focus_on_load

        self._action_id = action_id
        self._placeholder = placeholder
        self._init_date = init_date
        self._confirm = confirm
        self._focus_on_load = focus_on_load

    @property
    def action_id(self):
        return self._action_id

    @action_id.setter
    def action_id(self, _action_id):
        self._set_action_id(_action_id)

    @property
    def placeholder(self):
        return self._placeholder

    @placeholder.setter
    def placeholder(self, _placeholder):
        self._set_placeholder(_placeholder)

    @property
    def init_date(self):
        return self._init_date

    @init_date.setter
    def init_date(self, _init_date):
        self._body["initial_date"] = _init_date.__str__()
        self._init_date = _init_date

    @property
    def confirm(self):
        return self._confirm

    @confirm.setter
    def confirm(self, _confirm):
        self._set_confirm(_confirm)

    @property
    def focus_on_load(self):
        return self._focus_on_load

    @focus_on_load.setter
    def focus_on_load(self, _focus_on_load):
        self._set_focus_on_load(_focus_on_load)


class DateTimePicker(BlockInterface):

    def __init__(self,
                 action_id: str,
                 initial_date_time: datetime.datetime = None,
                 confirm: ConfirmationDialog = None,
                 focus_on_load: bool = False):
        check_length(action_id, _min=1, _max=255)

        self._body = {
            "type": "datetimepicker",
            "action_id": action_id,
        }

        if initial_date_time:
            self._body["initial_date_time"] = int(initial_date_time.timestamp()).__str__()

        if confirm:
            self._body["confirm"] = confirm
        self._body["focus_on_load"] = focus_on_load

        self._action_id = action_id
        self._initial_date_time = initial_date_time
        self._confirm = confirm
        self._focus_on_load = focus_on_load

    @property
    def action_id(self):
        return self._action_id

    @action_id.setter
    def action_id(self, _action_id):
        self._set_action_id(_action_id)

    @property
    def initial_date_time(self):
        return self._initial_date_time

    @initial_date_time.setter
    def initial_date_time(self, _initial_date_time):
        if _initial_date_time:
            self._body["initial_date_time"] = int(_initial_date_time.time()).__str__()
        else:
            self._body.pop("initial_date_time", None)

        self._initial_date_time = _initial_date_time

    @property
    def confirm(self):
        return self.confirm

    @confirm.setter
    def confirm(self, _confirm):
        self._set_confirm(_confirm)

    @property
    def focus_on_load(self):
        return self._focus_on_load

    @focus_on_load.setter
    def focus_on_load(self, _focus_on_load):
        self._set_focus_on_load(_focus_on_load)


class EmailInput(BlockInterface):

    def __init__(self,
                 action_id: str,
                 placeholder: Text = None,
                 initial_value: str = None,
                 dispatch_action_config: DispatchActionConfig = None,
                 focus_on_load: bool = False):

        check_length(action_id, _min=1, _max=255)

        self._body = {
            "type": "email_text_input",
            "action_id": action_id
        }

        if initial_value is not None:
            self._body["initial_value"] = initial_value

        if placeholder:
            check_length(placeholder.text, _min=1, _max=150)
            check_valid_type(placeholder.type, _types=PLAIN_TEXT)
            self._body["placeholder"] = placeholder

        if dispatch_action_config:
            self._body["dispatch_action_config"] = dispatch_action_config

        self._body["focus_on_load"] = focus_on_load

        self._action_id = action_id
        self._placeholder = placeholder
        self._initial_value = initial_value
        self._dispatch_action_config = dispatch_action_config
        self._focus_on_load = focus_on_load

    @property
    def action_id(self):
        return self._action_id

    @action_id.setter
    def action_id(self, _action_id):
        self._set_action_id(_action_id)

    @property
    def placeholder(self):
        return self._placeholder

    @placeholder.setter
    def placeholder(self, _placeholder):
        self._set_placeholder(_placeholder)

    @property
    def initial_value(self):
        return self._initial_value

    @initial_value.setter
    def initial_value(self, _initial_value):
        if _initial_value is not None:
            self._body["initial_value"] = _initial_value
        else:
            self._body.pop("initial_value", None)

        self._initial_value = _initial_value

    @property
    def dispatch_action_config(self):
        return self._dispatch_action_config

    @dispatch_action_config.setter
    def dispatch_action_config(self, _dispatch_action_config):
        if _dispatch_action_config:
            self._body["dispatch_action_config"] = _dispatch_action_config
        else:
            self._body.pop("dispatch_action_config", None)
        self._dispatch_action_config = _dispatch_action_config

    @property
    def focus_on_load(self):
        return self._focus_on_load

    @focus_on_load.setter
    def focus_on_load(self, _focus_on_load):
        self._set_focus_on_load(_focus_on_load)


class Image(BlockInterface):

    def __init__(self, image_url: str, alt_text: str):
        check_length(image_url, _min=1, _max=3000)
        check_length(alt_text, _min=1, _max=255)

        self._body = {
            "type": "image",
            "image_url": image_url,
            "alt_text": alt_text
        }

        self._image_url = image_url
        self._alt_text = alt_text

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
        check_length(_alt_text, _min=1, _max=255)
        self._body["alt_text"] = _alt_text
        self._alt_text = _alt_text


class StaticOptions(BlockInterface):

    def __init__(self,
                 type: str,
                 action_id: str,
                 placeholder: Text = None,
                 options: List[Option] = None,
                 option_groups: List[OptionGroups] = None,
                 init_options: List[Option] = None,
                 confirm: ConfirmationDialog = None,
                 max_selected_items: int = 1,
                 focus_on_load: bool = False):

        check_length(action_id, _min=1, _max=255)

        if type != "multi_static_select" or type != "static_select":
            raise ValueError(f"This option type must be either static_select or multi_static_select.")

        if options is None and option_groups is None:
            raise ValueError("Options and option groups are both None, exactly 1 must be specified.")

        if options is not None and option_groups is not None:
            raise ValueError("Options and option groups are both specified, exactly 1 must be specified")

        if not 1 <= max_selected_items <= 100:
            raise ValueError("Maximum selected items value must be in range [1, 100].")

        self._body = {
            "type": type,
            "action_id": action_id,
        }

        if placeholder:
            check_length(placeholder.text, _min=1, _max=150)
            check_valid_type(placeholder.type, _types=PLAIN_TEXT)
            self._body["placeholder"] = placeholder

        if options is not None:
            check_options_no_url(options)
            check_length(options, _min=1, _max=100)
            self._body["options"] = options
        elif option_groups is not None:
            for _og in option_groups:
                check_options_no_url(_og.options)
            check_length(option_groups, _min=1, _max=100)
            self._body["option_groups"] = option_groups

        if init_options is not None:
            check_options_no_url(init_options)
            check_length(init_options, _min=1, _max=100)
            if options:
                if not all(list(map(lambda x: x in options, init_options))):
                    raise ValueError("Initial options must match the options list.")
            if option_groups:
                _l = [all(list(map(lambda x: x in _og.options, init_options))) for _og in option_groups]
                if _l.count(True) != 1:
                    raise ValueError("Initial options must match exactly on of the option groups ")

            if type == "static_select":
                self._body["initial_option"] = init_options[0]
            else:
                self._body["initial_options"] = init_options
                self._body["max_selected_items"] = max_selected_items

        if confirm:
            self._body["confirm"] = confirm

        self._body["focus_on_load"] = focus_on_load

        self._type = type
        self._placeholder = placeholder
        self._action_id = action_id
        self._options = options
        self._option_groups = option_groups
        self._init_options = init_options
        self._confirm = confirm
        self._max_selected_items = max_selected_items
        self.focus_on_load = focus_on_load

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, _type):
        self._set_select_type(_type, "option")

    @property
    def placeholder(self):
        return self._placeholder

    @placeholder.setter
    def placeholder(self, _placeholder):
        self._set_placeholder(_placeholder)

    @property
    def action_id(self):
        return self._action_id

    @action_id.setter
    def action_id(self, _action_id):
        self._set_action_id(_action_id)

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, _options: Optional[Union[List[Option], Tuple[List[Option], bool]]]):
        if _options is None:
            if self._option_groups is None:
                raise ValueError("Can not remove options when option_groups is not specified.")
            else:
                self._body.pop("options", None)
                self._body["option_groups"] = self._option_groups

        elif isinstance(_options, List):
            if self._option_groups:
                raise ValueError("Can not specify options when option_groups is also specified. "
                                 "To replace option_groups, with options supply a tuple with second argument "
                                 "True. To simply update options property without replacing option_groups, "
                                 "supply a tuple with second argument False.")

            else:
                check_length(_options, _min=1, _max=100)
                check_options_no_url(_options)
                self._body["options"] = _options
        else:
            _options, _replace = _options   # Unpack values
            check_length(_options, _min=1, _max=100)
            check_options_no_url(_options)
            if _replace:
                self._body.pop("option_groups", None)
                self._body["options"] = _options

        if self._init_options and _options:
            if not all(list(map(lambda x: x in _options, self._init_options))):
                raise ValueError("Initial options must match the options list.")

        self._option_groups = _options

    @property
    def option_groups(self):
        return self._option_groups

    @option_groups.setter
    def option_groups(self, _option_groups: Optional[Union[List[OptionGroups], Tuple[List[OptionGroups]], bool]]):
        if _option_groups is None:
            if self._options is None:
                raise ValueError("Can not remove option_groups when options is not specified.")
            else:
                self._body.pop("option_groups", None)
                self._body["options"] = self._options

        elif isinstance(_option_groups, List):
            if self._options:
                raise ValueError("Can not specify option_groups when options is also specified. To replace options,"
                                 "with option_groups supply a tuple with second argument True. To simply update"
                                 "option_groups property without replacing options, supply a tuple with second"
                                 "argument False.")

            else:
                check_length(_option_groups, _min=1, _max=100)
                for _og in _option_groups:
                    check_options_no_url(_og.options)
                self._body["option_groups"] = _option_groups
        else:
            _option_groups, _replace = _option_groups   # Unpack values
            check_length(_option_groups, _min=1, _max=100)
            for _og in _option_groups:
                check_options_no_url(_og.options)
            if _replace:
                self._body.pop("options", None)
                self._body["option_groups"] = _option_groups

        if self._init_options and _option_groups:
            _l = [all(list(map(lambda x: x in _og.options, self._init_options))) for _og in _option_groups]
            if _l.count(True) != 1:
                raise ValueError("Initial options must match exactly on of the option groups ")

        self._option_groups = _option_groups

    @property
    def init_options(self):
        return self._init_options

    @init_options.setter
    def init_options(self, _init_options):
        self._set_init_options(_init_options, "option")

    @property
    def confirm(self):
        return self.confirm

    @confirm.setter
    def confirm(self, _confirm):
        self._set_confirm(_confirm)

    @property
    def max_selected_items(self):
        return self._max_selected_items

    @max_selected_items.setter
    def max_selected_items(self, _max_selected_items):
        self._set_max_selected_items(_max_selected_items)

    @property
    def focus_on_load(self):
        return self._focus_on_load

    @focus_on_load.setter
    def focus_on_load(self, _focus_on_load):
        self._set_focus_on_load(_focus_on_load)


class ExternalDataOptions(BlockInterface):

    def __init__(self,
                 type: str,
                 action_id: str,
                 placeholder: Text = None,
                 min_query_length: int = 3,
                 init_options: List[Option] = None,
                 confirm: ConfirmationDialog = None,
                 max_selected_items: int = 1,
                 focus_on_load: bool = False):
        check_length(action_id, _min=1, _max=255)

        if type != "multi_external_select" and type != "external_select":
            raise ValueError("Type must be either multi_external_select or external_select.")

        if min_query_length < 1:
            raise ValueError("Minimum query length can not be less than 1.")
        if not 1 <= max_selected_items <= 100:
            raise ValueError("Maximum selected items value must be in range [1, 100].")

        self.body = {
            "type": type,
            "action_id": action_id,
            "min_query_length": min_query_length,
        }

        if placeholder:
            check_length(placeholder.text, _min=1, _max=150)
            check_valid_type(placeholder.type, _types=PLAIN_TEXT)
            self._body["placeholder"] = placeholder

        if type == "multi_external_select":
            if init_options is not None:
                check_options_no_url(init_options)
                check_length(init_options, _min=1, _max=2 ** 32)
                self.body["initial_options"] = init_options
            self.body["max_selected_items"] = max_selected_items
        else:
            if init_options is not None:
                check_options_no_url(init_options)
                check_length(init_options, _min=1, _max=2 ** 32)
                self.body["initial_option"] = init_options[0]

        if confirm:
            self.body["confirm"] = confirm
        self.body["focus_on_load"] = focus_on_load

        self._type = type
        self._placeholder = placeholder
        self._action_id = action_id
        self._init_options = init_options
        self._confirm = confirm
        self._max_selected_items = max_selected_items
        self._min_query_length = min_query_length
        self.focus_on_load = focus_on_load

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, _type):
        self._set_select_type(_type, "option")

    @property
    def placeholder(self):
        return self._placeholder

    @placeholder.setter
    def placeholder(self, _placeholder):
        self._set_placeholder(_placeholder)

    @property
    def action_id(self):
        return self._action_id

    @action_id.setter
    def action_id(self, _action_id):
        self._set_action_id(_action_id)

    @property
    def init_options(self):
        return self._init_options

    @init_options.setter
    def init_options(self, _init_options):
        self._set_init_options(_init_options, "option")

    @property
    def confirm(self):
        return self.confirm

    @confirm.setter
    def confirm(self, _confirm):
        self._set_confirm(_confirm)

    @property
    def max_selected_items(self):
        return self._max_selected_items

    @max_selected_items.setter
    def max_selected_items(self, _max_selected_items):
        self._set_max_selected_items(_max_selected_items)

    @property
    def focus_on_load(self):
        return self._focus_on_load

    @focus_on_load.setter
    def focus_on_load(self, _focus_on_load):
        self._set_focus_on_load(_focus_on_load)


class UserListOptions(BlockInterface):

    def __init__(self,
                 type: str,
                 action_id: str,
                 placeholder: Text = None,
                 init_users: List[str] = None,
                 confirm: ConfirmationDialog = None,
                 max_selected_items: int = 1,
                 focus_on_load: bool = False):

        check_none(placeholder)
        check_length(action_id, _min=1, _max=255)

        if type != "multi_users_select" or type != "users_select":
            raise ValueError(f"This option type must be either users_select or multi_users_select.")

        if not 1 <= max_selected_items <= 100:
            raise ValueError("Maximum selected items value must be in range [1, 100].")

        self.body = {
            "type": type,
            "action_id": action_id
        }

        if placeholder:
            check_length(placeholder.text, _min=1, _max=150)
            check_valid_type(placeholder.type, _types=PLAIN_TEXT)
            self._body["placeholder"] = placeholder

        if type == "multi_users_select":
            if init_users is not None:
                check_length(init_users, _min=1, _max=2 ** 32)
                self.body["initial_users"] = init_users
            self.body["max_selected_items"] = max_selected_items
        else:
            if init_users is not None:
                check_length(init_users, _min=1, _max=2 ** 32)
                self.body["initial_user"] = init_users[0]
        if confirm:
            self.body["confirm"] = confirm
        self.body["focus_on_load"] = focus_on_load

        self._type = type
        self._placeholder = placeholder
        self._action_id = action_id
        self._confirm = confirm
        self._max_selected_items = max_selected_items
        self.init_users = init_users
        self.focus_on_load = focus_on_load

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, _type):
        self._set_select_type(_type, "user")

    @property
    def placeholder(self):
        return self._placeholder

    @placeholder.setter
    def placeholder(self, _placeholder):
        self._set_placeholder(_placeholder)

    @property
    def action_id(self):
        return self._action_id

    @action_id.setter
    def action_id(self, _action_id):
        self._set_action_id(_action_id)

    @property
    def init_users(self):
        return self._init_options

    @init_users.setter
    def init_users(self, _init_users):
        self._set_init_options(_init_users, "user")

    @property
    def confirm(self):
        return self.confirm

    @confirm.setter
    def confirm(self, _confirm):
        self._set_confirm(_confirm)

    @property
    def max_selected_items(self):
        return self._max_selected_items

    @max_selected_items.setter
    def max_selected_items(self, _max_selected_items):
        self._set_max_selected_items(_max_selected_items)

    @property
    def focus_on_load(self):
        return self._focus_on_load

    @focus_on_load.setter
    def focus_on_load(self, _focus_on_load):
        self._set_focus_on_load(_focus_on_load)


class ConversationOptions(BlockInterface):

    def __init__(self,
                 type: str,
                 action_id: str,
                 placeholder: Text = None,
                 init_conversations: List[str] = None,
                 default_to_current_conversation: bool = False,
                 confirm: ConfirmationDialog = None,
                 max_selected_items: int = 1,
                 filter: ConversationFilters = None,
                 response_url_enabled: bool = False,
                 focus_on_load: bool = False):

        check_length(action_id, _min=1, _max=255)

        if type != "multi_conversations_select" or type != "conversations_select":
            raise ValueError(f"This option type must be either conversations_select or multi_conversations_select.")

        if not 1 <= max_selected_items <= 100:
            raise ValueError("Maximum selected items value must be in range [1, 100].")

        self._body = {
            "type": type,
            "action_id": action_id,
        }

        if placeholder:
            check_length(placeholder.text, _min=1, _max=150)
            check_valid_type(placeholder.type, _types=PLAIN_TEXT)
            self._body["placeholder"] = placeholder

        if type == "multi_conversations_select":
            if init_conversations is not None:
                check_length(init_conversations, _min=1, _max=2 ** 32)
                self._body["initial_conversations"] = init_conversations
            self._body["max_selected_items"] = max_selected_items
        else:
            if init_conversations is not None:
                check_length(init_conversations, _min=1, _max=2 ** 32)
                self._body["initial_conversation"] = init_conversations[0]
            self._body["response_url_enabled"] = response_url_enabled
        self._body["default_to_current_conversation"] = default_to_current_conversation
        if confirm:
            self._body["confirm"]: confirm
        if filter:
            self._body["filter"]: filter
        self._body["focus_on_load"] = focus_on_load

        self._type = type
        self._placeholder = placeholder
        self._action_id = action_id
        self._confirm = confirm
        self._max_selected_items = max_selected_items
        self._init_conversations = init_conversations
        self._default_to_current_conversation = default_to_current_conversation
        self.focus_on_load = focus_on_load
        self._response_url_enabled = response_url_enabled
        self._filter = filter

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, _type):
        self._set_select_type(_type, "conversation")

    @property
    def placeholder(self):
        return self._placeholder

    @placeholder.setter
    def placeholder(self, _placeholder):
        self._set_placeholder(_placeholder)

    @property
    def action_id(self):
        return self._action_id

    @action_id.setter
    def action_id(self, _action_id):
        self._set_action_id(_action_id)

    @property
    def init_conversations(self):
        return self._init_conversations

    @init_conversations.setter
    def init_conversations(self, _init_conversations):
        self._set_init_options(_init_conversations, "conversation")

    @property
    def confirm(self):
        return self.confirm

    @confirm.setter
    def confirm(self, _confirm):
        self._set_confirm(_confirm)

    @property
    def max_selected_items(self):
        return self._max_selected_items

    @max_selected_items.setter
    def max_selected_items(self, _max_selected_items):
        self._set_max_selected_items(_max_selected_items)

    @property
    def focus_on_load(self):
        return self._focus_on_load

    @focus_on_load.setter
    def focus_on_load(self, _focus_on_load):
        self._set_focus_on_load(_focus_on_load)

    @property
    def default_to_current_conversation(self):
        return self._default_to_current_conversation

    @default_to_current_conversation.setter
    def default_to_current_conversation(self, _default_to_current_conversation):
        self._body["default_to_current_conversation"] = _default_to_current_conversation
        self._default_to_current_conversation = _default_to_current_conversation

    @property
    def response_url_enabled(self):
        return self._response_url_enabled

    @response_url_enabled.setter
    def response_url_enabled(self, _response_url_enabled):
        if not self._type.startswith("multi"):
            self._body["response_url_enabled"] = _response_url_enabled
        self._response_url_enabled = _response_url_enabled

    @property
    def filter(self):
        return self._filter

    @filter.setter
    def filter(self, _filter):
        if _filter:
            self._body["filter"] = _filter
        else:
            self._body.pop("filter", None)

        self._filter = _filter


class PublicChannelOptions(BlockInterface):

    def __init__(self,
                 type: str,
                 action_id: str,
                 placeholder: Text = None,
                 init_channels: List[str] = None,
                 confirm: ConfirmationDialog = None,
                 max_selected_items: int = 1,
                 response_url_enabled: bool = False,
                 focus_on_load: bool = False):

        check_length(action_id, _min=1, _max=255)

        if type != "multi_channels_select" or type != "channels_select":
            raise ValueError(f"This option type must be either channels_select or multi_channels_select.")

        if not 1 <= max_selected_items <= 100:
            raise ValueError("Maximum selected items value must be in range [1, 100].")

        self.body = {
            "type": type,
            "action_id": action_id,
            "focus_on_load": focus_on_load
        }

        if placeholder:
            check_length(placeholder.text, _min=1, _max=150)
            check_valid_type(placeholder.type, _types=PLAIN_TEXT)
            self._body["placeholder"] = placeholder

        if type == "multi_channels_select":
            if init_channels is not None:
                check_length(init_channels, _min=1, _max=2 ** 32)
                self.body["initial_channels"] = init_channels
            self.body["max_selected_items"] = max_selected_items
        else:
            if init_channels is not None:
                check_length(init_channels, _min=1, _max=2 ** 32)
                self.body["initial_channel"] = init_channels[0]
            self._body["response_url_enabled"] = response_url_enabled
        if confirm:
            self.body["confirm"] = confirm

        self._type = type
        self._placeholder = placeholder
        self._action_id = action_id
        self._confirm = confirm
        self._max_selected_items = max_selected_items
        self._init_channels = init_channels
        self._focus_on_load = focus_on_load
        self._response_url_enabled = response_url_enabled

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, _type):
        self._set_select_type(_type, "channel")

    @property
    def placeholder(self):
        return self._placeholder

    @placeholder.setter
    def placeholder(self, _placeholder):
        self._set_placeholder(_placeholder)

    @property
    def action_id(self):
        return self._action_id

    @action_id.setter
    def action_id(self, _action_id):
        self._set_action_id(_action_id)

    @property
    def init_channels(self):
        return self._init_channels

    @init_channels.setter
    def init_channels(self, _init_channels):
        self._set_init_options(_init_channels, "channel")

    @property
    def confirm(self):
        return self.confirm

    @confirm.setter
    def confirm(self, _confirm):
        self._set_confirm(_confirm)

    @property
    def max_selected_items(self):
        return self._max_selected_items

    @max_selected_items.setter
    def max_selected_items(self, _max_selected_items):
        self._set_max_selected_items(_max_selected_items)

    @property
    def focus_on_load(self):
        return self._focus_on_load

    @focus_on_load.setter
    def focus_on_load(self, _focus_on_load):
        self._set_focus_on_load(_focus_on_load)

    @property
    def response_url_enabled(self):
        return self._response_url_enabled

    @response_url_enabled.setter
    def response_url_enabled(self, _response_url_enabled):
        if not self._type.startswith("multi"):
            self._body["response_url_enabled"] = _response_url_enabled
        self._response_url_enabled = _response_url_enabled


class OverFlowMenu(BlockInterface):

    def __init__(self,
                 action_id: str,
                 options: List[Option],
                 confirm: ConfirmationDialog = None):
        check_length(action_id, _min=1, _max=255)
        check_length(options, _min=1, _max=5)

        self._body = {
            "type": "overflow",
            "options": options,
        }

        if confirm:
            self._body["confirm"] = confirm

        self._action_id = action_id
        self._options = options
        self._confirm = confirm

    @property
    def action_id(self):
        return self._action_id

    @action_id.setter
    def action_id(self, _action_id):
        self._set_action_id(_action_id)

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, _options: List[Option]):
        check_length(_options, _min=1, _max=5)
        self._body["options"] = _options
        self._options = _options

    @property
    def confirm(self):
        return self._confirm

    @confirm.setter
    def confirm(self, _confirm):
        self._set_confirm(_confirm)


class NumberInput(BlockInterface):

    def __init__(self,
                 is_decimal_allowed: bool,
                 action_id: str = None,
                 initial_value: str = None,
                 min_value: str = None,
                 max_value: str = None,
                 dispatch_action_config: DispatchActionConfig = None,
                 focus_on_load: bool = False,
                 placeholder: Text = None):

        self._body = {
            "type": "number_input",
            "is_decimal_allowed": is_decimal_allowed
        }

        if action_id is not None:
            check_length(action_id, _min=1, _max=255)
            self._body["action_id"] = action_id

        if initial_value is not None:
            check_is_number(initial_value, is_decimal_allowed)
            self._body["initial_value"] = initial_value

        if min_value is not None:
            check_is_number(min_value, is_decimal_allowed)
            self._body["min_value"] = min_value

        if max_value is not None:
            check_is_number(max_value, is_decimal_allowed)
            self._body["max_value"] = max_value

        if min_value and max_value:
            _min_v = get_number_from_string(min_value)
            _max_v = get_number_from_string(max_value)
            if _min_v > _max_v:
                raise ValueError("min_value must be less or equal to max_value.")

        if dispatch_action_config:
            self._body["dispatch_action_config"] = dispatch_action_config

        if placeholder:
            check_length(placeholder.text, _min=1, _max=150)
            check_valid_type(placeholder.type, _types=PLAIN_TEXT)
            self._body["placeholder"] = placeholder

        self._body["focus_on_load"] = focus_on_load

        self._is_decimal_allowed = is_decimal_allowed
        self._action_id = action_id
        self._init_value = initial_value
        self._max_value = max_value
        self._min_value = min_value
        self._dispatch_action_config = dispatch_action_config
        self._focus_on_load = focus_on_load
        self._placeholder = placeholder

    @property
    def is_decimal_allowed(self):
        return self._is_decimal_allowed

    @is_decimal_allowed.setter
    def is_decimal_allowed(self, _is_decimal_allowed):
        if not _is_decimal_allowed:
            # Round down the max and min values if they are decimal
            self._max_value = str(int(float(self._max_value)))
            self._min_value = str(int(float(self._min_value)))

        self._body["is_decimal_allowed"] = _is_decimal_allowed
        self._is_decimal_allowed = _is_decimal_allowed

    @property
    def action_id(self):
        return self._action_id

    @action_id.setter
    def action_id(self, _action_id):
        if _action_id is not None:
            self._body["action_id"] = _action_id
        else:
            self._body.pop("action_id", None)
        self._action_id = _action_id

    @property
    def init_value(self):
        return self._init_value

    @init_value.setter
    def init_value(self, _init_value):
        if _init_value is not None:
            check_is_number(_init_value, self._is_decimal_allowed)
            self._body["initial_value"] = _init_value
        else:
            self._body.pop("initial_value", None)
        self._init_value = _init_value

    @property
    def max_value(self):
        return self._max_value

    @max_value.setter
    def max_value(self, _max_value):
        if _max_value is not None:
            check_is_number(_max_value, self._is_decimal_allowed)
            if self._min_value:
                _min_v = get_number_from_string(self._min_value)
                _max_v = get_number_from_string(_max_value)
                if _min_v > _max_v:
                    raise ValueError("min_value must be less or equal to max_value.")
            self._body["max_value"] = _max_value
        else:
            self._body.pop("max_value", None)

        self._max_value = _max_value

    @property
    def min_value(self):
        return self._min_value

    @min_value.setter
    def min_value(self, _min_value):
        if _min_value is not None:
            check_is_number(_min_value, self._is_decimal_allowed)
            if self._max_value:
                _min_v = get_number_from_string(_min_value)
                _max_v = get_number_from_string(self._max_value)
                if _min_v > _max_v:
                    raise ValueError("min_value must be less or equal to max_value.")

            self._body["min_value"] = _min_value
        else:
            self._body.pop("min_value", None)
        self._min_value = _min_value

    @property
    def dispatch_action_config(self):
        return self._dispatch_action_config

    @dispatch_action_config.setter
    def dispatch_action_config(self, _dispatch_action_config):
        if _dispatch_action_config:
            self._body["dispatch_action_config"] = _dispatch_action_config
        else:
            self._body.pop("dispatch_action_config", None)
        self._dispatch_action_config = _dispatch_action_config

    @property
    def focus_on_load(self):
        return self._focus_on_load

    @focus_on_load.setter
    def focus_on_load(self, _focus_on_load):
        self._set_focus_on_load(_focus_on_load)

    @property
    def placeholder(self):
        return self._placeholder

    @placeholder.setter
    def placeholder(self, _placeholder):
        self._set_placeholder(_placeholder)


class PlainTextInput(BlockInterface):

    def __init__(self,
                 action_id: str,
                 placeholder: Text = None,
                 init_value: str = None,
                 multiline: bool = False,
                 min_length: int = None,
                 max_length: int = None,
                 focus_on_load: bool = False,
                 dispatch_action_config: DispatchActionConfig = None,
                 ):

        check_length(action_id, _min=1, _max=255)

        self._body = {
            "type": "plain_text_input",
            "action_id": action_id
        }

        if placeholder:
            check_length(placeholder.text, _min=1, _max=150)
            check_valid_type(placeholder.type, _types=PLAIN_TEXT)
            self._body["placeholder"] = placeholder

        if init_value is not None:
            self._body["initial_value"] = init_value

        self._body["multiline"] = multiline

        if min_length:
            if not 1 <= min_length <= 3000:
                raise ValueError("min_length must be in range [1, 3000].")
            self._body["min_length"] = min_length

        if max_length:
            self._body["max_length"] = max_length

        if min_length and max_length:
            if min_length > max_length:
                raise ValueError("min_length must be less or equal to max_length.")

        self._body["focus_on_load"] = focus_on_load

        if dispatch_action_config:
            self._body["dispatch_action_config"] = dispatch_action_config

        self._action_id = action_id
        self._placeholder = placeholder
        self._init_value = init_value
        self._multiline = multiline
        self._min_length = min_length
        self._max_length = max_length
        self._dispatch_action_config = dispatch_action_config
        self._focus_on_load = focus_on_load

    @property
    def placeholder(self):
        return self._placeholder

    @placeholder.setter
    def placeholder(self, _placeholder):
        self._set_placeholder(_placeholder)

    @property
    def action_id(self):
        return self._action_id

    @action_id.setter
    def action_id(self, _action_id):
        self._set_action_id(_action_id)

    @property
    def dispatch_action_config(self):
        return self._dispatch_action_config

    @dispatch_action_config.setter
    def dispatch_action_config(self, _dispatch_action_config):
        if _dispatch_action_config:
            self._body["dispatch_action_config"] = _dispatch_action_config
        else:
            self._body.pop("dispatch_action_config", None)
        self._dispatch_action_config = _dispatch_action_config

    @property
    def focus_on_load(self):
        return self._focus_on_load

    @focus_on_load.setter
    def focus_on_load(self, _focus_on_load):
        self._set_focus_on_load(_focus_on_load)

    @property
    def init_value(self):
        return self._init_value

    @init_value.setter
    def init_value(self, _init_value):
        if _init_value is not None:
            check_length(_init_value, _min=1, _max=2 ** 32)
            self._body["initial_value"] = _init_value
        else:
            self._body.pop("initial_value", None)
        self._init_value = _init_value

    @property
    def multiline(self):
        return

    @multiline.setter
    def multiline(self, _multiline):
        self._body["multiline"] = _multiline
        self._multiline = _multiline

    @property
    def max_length(self):
        return self._max_length

    @max_length.setter
    def max_length(self, _max_length):
        if _max_length:
            if self._min_length and self._min_length > _max_length:
                raise ValueError("min_length must be less or equal to max_length.")
            self._body["max_length"] = _max_length
        else:
            self._body.pop("max_length", None)
        self._max_length = _max_length

    @property
    def min_length(self):
        return self._min_length

    @min_length.setter
    def min_length(self, _min_length):
        if _min_length:
            if self._max_length and self._max_length < _min_length:
                raise ValueError("min_length must be less or equal to max_length.")
            self._body["_min_length"] = _min_length
        else:
            self._body.pop("_min_length", None)
        self._min_length = _min_length


class RadioButtonGroup(BlockInterface):

    def __init__(self,
                 action_id: str,
                 options: List[Option],
                 init_option: Option = None,
                 confirm: ConfirmationDialog = None,
                 focus_on_load: bool = False):
        check_length(action_id, _min=1, _max=255)
        check_length(options, _min=1, _max=10)
        check_options_no_url(options)

        self._body = {
            "type": "radio_buttons",
            "action_id": action_id,
            "options": options
        }

        if init_option:
            check_options_no_url([init_option])
            if options.count(init_option) != 1:
                raise ValueError("Initial option must match exactly 1 option.")
            self._body["initial_option"] = init_option
        if confirm:
            self._body["confirm"] = confirm
        self._body["focus_on_load"] = focus_on_load

        self._action_id = action_id
        self._options = options
        self._init_option = init_option
        self._confirm = confirm
        self._focus_on_load = focus_on_load

    @property
    def action_id(self):
        return self._action_id

    @action_id.setter
    def action_id(self, _action_id):
        self._set_action_id(_action_id)

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, _options):
        check_length(_options, _min=1, _max=10)
        check_options_no_url(_options)
        if self._init_options:
            if _options.count(self._init_option) != 1:
                raise ValueError("Initial option must match exactly 1 option.")
        self._body["options"] = _options
        self._options = _options

    @property
    def init_option(self):
        return self._init_option

    @init_option.setter
    def init_option(self, _init_option):
        if _init_option:
            check_options_no_url([_init_option])
            if self._options.count(_init_option) != 1:
                raise ValueError("Initial option must match exactly 1 option.")
            self._body["initial_option"] = _init_option
        else:
            self._body.pop("initial_option", None)
        self._init_option = _init_option

    @property
    def focus_on_load(self):
        return self._focus_on_load

    @focus_on_load.setter
    def focus_on_load(self, _focus_on_load):
        self._set_focus_on_load(_focus_on_load)

    @property
    def confirm(self):
        return self.confirm

    @confirm.setter
    def confirm(self, _confirm):
        self._set_confirm(_confirm)


class TimePicker(BlockInterface):

    def __init__(self,
                 action_id: str,
                 init_time: datetime.time = None,
                 confirm: ConfirmationDialog = None,
                 placeholder: Text = None,
                 tz: datetime.datetime = None,
                 focus_on_load: bool = False):
        check_length(action_id, _min=1, _max=255)

        self._body = {
            "type": "timepicker",
            "action_id": action_id
        }

        if init_time:
            self._body["initial_time"] = init_time.strftime("%H:%M")

        if confirm:
            self._body["confirm"] = confirm

        if placeholder:
            check_length(placeholder.text, _min=1, _max=150)
            check_valid_type(placeholder.type, _types=PLAIN_TEXT)
            self._body["placeholder"] = placeholder

        if tz:
            self._body["timezone"] = tz.tzname()

        self._body["focus_on_load"] = focus_on_load

        self._action_id = action_id
        self._init_time = init_time
        self._confirm = confirm
        self._placeholder = placeholder
        self._tz = tz
        self._focus_on_load = focus_on_load

    @property
    def action_id(self):
        return self._action_id

    @action_id.setter
    def action_id(self, _action_id):
        self._set_action_id(_action_id)

    @property
    def init_time(self):
        return self._init_time

    @init_time.setter
    def init_time(self, _init_time):
        if _init_time:
            self._body["initial_time"] = _init_time.strftime("%H:%M")
        else:
            self._body.pop("initial_time", None)
        self._init_time = _init_time

    @property
    def tz(self):
        return self._tz

    @tz.setter
    def tz(self, _tz):
        if _tz:
            self._body["timezone"] = _tz.tzname()
        else:
            self._body.pop("timezone", None)
        self._tz = _tz

    @property
    def focus_on_load(self):
        return self._focus_on_load

    @focus_on_load.setter
    def focus_on_load(self, _focus_on_load):
        self._set_focus_on_load(_focus_on_load)

    @property
    def confirm(self):
        return self.confirm

    @confirm.setter
    def confirm(self, _confirm):
        self._set_confirm(_confirm)

    @property
    def placeholder(self):
        return self._placeholder

    @placeholder.setter
    def placeholder(self, _placeholder):
        self._set_placeholder(_placeholder)


class UrlInput(BlockInterface):

    def __init__(self,
                 action_id: str,
                 placeholder: Text = None,
                 initial_value: str = None,
                 dispatch_action_config: DispatchActionConfig = None,
                 focus_on_load: bool = False):
        check_length(action_id, _min=1, _max=255)

        self._body = {
            "type": "url_text_input",
            "action_id": action_id
        }

        if placeholder:
            check_length(placeholder.text, _min=1, _max=150)
            check_valid_type(placeholder.type, _types=PLAIN_TEXT)
            self._body["placeholder"] = placeholder

        if initial_value:
            self._body["initial_value"] = initial_value

        if dispatch_action_config:
            self._body["dispatch_action_config"] = dispatch_action_config

        self._body["focus_on_load"] = focus_on_load

        self._action_id = action_id
        self._init_value = initial_value
        self._dispatch_action_config = dispatch_action_config
        self._placeholder = placeholder
        self._focus_on_load = focus_on_load

    @property
    def action_id(self):
        return self._action_id

    @action_id.setter
    def action_id(self, _action_id):
        self._set_action_id(_action_id)

    @property
    def dispatch_action_config(self):
        return self._dispatch_action_config

    @dispatch_action_config.setter
    def dispatch_action_config(self, _dispatch_action_config):
        if _dispatch_action_config:
            self._body["dispatch_action_config"] = _dispatch_action_config
        else:
            self._body.pop("dispatch_action_config", None)
        self._dispatch_action_config = _dispatch_action_config

    @property
    def focus_on_load(self):
        return self._focus_on_load

    @focus_on_load.setter
    def focus_on_load(self, _focus_on_load):
        self._set_focus_on_load(_focus_on_load)

    @property
    def init_value(self):
        return self._init_value

    @init_value.setter
    def init_value(self, _init_value):
        if _init_value:
            self._body["initial_value"] = _init_value
        else:
            self._body.pop("initial_value", None)
        self._init_value = _init_value

    @property
    def placeholder(self):
        return self._placeholder

    @placeholder.setter
    def placeholder(self, _placeholder):
        self._set_placeholder(_placeholder)
