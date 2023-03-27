from utils import *


def _build_list(_l: list):
    for ix, value in enumerate(_l):
        if isinstance(value, list):
            _l[ix] = _build_list(value)
        elif isinstance(value, dict):
            _l[ix] = _build_dict(value)
        elif isinstance(value, BlockInterface):
            _l[ix] = value.build()

    return _l


def _build_dict(_d: dict):
    for key, value in _d.items():
        if isinstance(value, list):
            _d[key] = _build_list(value)
        elif isinstance(value, dict):
            _d[key] = _build_dict(value)
        elif isinstance(value, BlockInterface):
            _d[key] = value.build()

    return _d


class BlockInterface:
    _body = {}

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        for k in self._body.keys():
            if other._body.get(k) is None or self._body.get(k) != other._body.get(k):
                return False
        return True

    def build(self) -> dict:
        for key, value in self._body.items():
            if isinstance(value, list):
                self._body[key] = _build_list(value)
            elif isinstance(value, dict):
                self._body[key] = _build_dict(value)
            elif isinstance(value, BlockInterface):
                self._body[key] = value.build()

        return self._body

    def __dict__(self) -> dict:
        return self.build()

    # _type_name can be option, user, conversation or channel, append with 's' if multi type
    def _set_select_type(self, _type: str, _type_name: str):
        # From single to multi
        if self._type.startswith("static") and _type.startswith("multi"):
            _option = self._body.pop(f"initial_{_type_name}")
            self._body[f"initial_{_type_name}s"] = [_option]

            if _type_name == "conversation" or _type_name == "channel":
                self._body.pop("response_url_enabled", None)

        # From multi to single
        elif self._type.startswith("multi") and _type.startswith("static"):
            _options = self._body.pop(f"initial_{_type_name}s")
            self._body[f"initial_{_type_name}"] = _options[0]
            self._body.pop("max_selected_items", None)

            if _type_name == "conversation" or _type_name == "channel":
                self._body["response_url_enabled"] = self._response_url_enabled

        self._type = _type

    def _set_select_options(self, _options):
        check_length(_options, _min=1, _max=10)
        if self._init_options:
            if not all(list(map(lambda x: x in self._options, self._init_options))):
                raise ValueError("Initial options must match the options list")

        self._options = _options
        self._body["options"] = _options

    def _set_action_id(self, _action_id):
        check_length(_action_id, _min=1, _max=255)
        self._action_id = _action_id
        self._body["action_id"] = _action_id

    def _set_confirm(self, _confirm):
        if not _confirm:
            self._body.pop("confirm", None)
        else:
            self._body["confirm"] = _confirm

        self._confirm = _confirm

    def _set_focus_on_load(self, _focus_on_load):
        self._body["focus_on_load"] = _focus_on_load
        self._focus_on_load = _focus_on_load

    def _set_placeholder(self, _placeholder):
        if _placeholder:
            check_length(_placeholder.text, _min=1, _max=150)
            check_valid_type(_placeholder.type, _types=PLAIN_TEXT)
            self._body["placeholder"] = _placeholder
        else:
            self._body.pop("placeholder", None)

        self._placeholder = _placeholder

    def _set_init_options(self, _init_options: List, _type_name: str):
        if self._type.startswith("multi"):
            self._body[f"initial_{_type_name}s"] = _init_options
        else:
            self._body["initial_{_type_name}"] = _init_options[0]

        self._init_options = _init_options

    def _set_max_selected_items(self, _max_selected_items):
        if not self._type.startswith("multi"):
            return  # Ignore if not multi

        if not 1 <= _max_selected_items <= 100:
            raise ValueError("Maximum selected items value must be in range [1, 100].")
        self._body["max_selected_items"] = _max_selected_items
        self._max_selected_items = _max_selected_items

    def _set_block_id(self, _block_id):
        check_length(_block_id, _min=1, _max=255)
        if _block_id:
            self._body["block_id"] = _block_id
        else:
            self._body.pop("_block_id", None)
        self._block_id = _block_id
