from copy import deepcopy, copy
from typing import Type

from BlockAPI.Blocks import *

# List of types supported by home surface and modals
_home_and_modal_types = Union[ActionBlock, ContextBlock, DividerBlock,
                              HeaderBlock, ImageBlock, InputBlock,
                              SectionBlock, VideoBlock]

_all_types = Union[_home_and_modal_types, FileBlock]  # File block is allowed only for message surfaces


def _add(self,
         item: _all_types,
         index: int = None):

    if index and index > len(self._blocks):
        raise IndexError

    if index is None:
        self._blocks.append(item)
    else:
        self._blocks.insert(index, item)


def _add_after(self,
               _block: _all_types,
               _type: Type[_all_types],
               _instance_num: int = 1,
               _strict: bool = False):
    if _instance_num == 0:
        raise ValueError("Instance number must be non-zero.")

    _step = 1 if _instance_num > 0 else -1
    _instance_num = abs(_instance_num)

    _last_index = None
    for _ix, _b in enumerate(self._blocks[::_step]):
        if isinstance(_b, _type):
            _instance_num -= 1
            _last_index = _ix
            if _instance_num == 0:
                if _step == 1:
                    self._blocks.insert(_ix + 1, _block)
                else:
                    self._blocks.insert(len(self._blocks) - _ix, _block)
                break
    else:
        if _last_index:
            if _step == 1:
                self._blocks.insert(_last_index + 1, _block)
            else:
                self._blocks.insert(len(self._blocks) - _last_index, _block)
        else:
            if _strict:
                raise ValueError(f"Could not find instance of {_type.__name__}.")
            self._blocks.append(_block)


def _add_before(self,
                _block: _all_types,
                _type: Type[_all_types],
                _instance_num: int = 1,
                _strict: bool = False):
    if _instance_num == 0:
        raise ValueError("Instance number must be non-zero.")

    _step = 1 if _instance_num > 0 else -1
    _instance_num = abs(_instance_num)

    _last_index = None
    for _ix, _b in enumerate(self._blocks[::_step]):
        if isinstance(_b, _type):
            _instance_num -= 1
            _last_index = _ix
            if _instance_num == 0:
                if _step == 1:
                    self._blocks.insert(_ix, _block)
                else:
                    self._blocks.insert(len(self._blocks) - _ix - 1, _block)
                break
    else:
        if _last_index:
            if _step == 1:
                self._blocks.insert(_last_index, _block)
            else:
                self._blocks.insert(len(self._blocks) - _last_index - 1, _block)
        else:
            if _strict:
                raise ValueError(f"Could not find instance of {_type.__name__}.")
            self._blocks.append(_block)


class HomeSurface(BlockInterface):

    def __init__(self, blocks: _home_and_modal_types = None):
        self._blocks = blocks if blocks else []
        self._body = {
            "type": "home",
            "blocks": self._blocks
        }

    def add(self,
            item: _home_and_modal_types,
            index: int = None):
        """
        Add block element to the surface.
        :param item: Block element to be added.
        :param index: Index at which to add the element. If none, append.
        :return: Self.
        """
        _add(self, item, index)
        return self

    def add_after(self,
                  _block: _home_and_modal_types,
                  _type: Type[_home_and_modal_types],
                  _instance_num: int = 1,
                  _strict: bool = False):
        """
        Add block element after specified instance occurrence of a block of type _type.
        :param _block: Block to be added.
        :param _type: Type of block to add the inserted _block after.
        :param _instance_num: Must be non-zero. Number of the instance of a block of type _type
        after which the _block is added. If number of the instance is larger than actual number of occurrences,
        add after the last instance. If the instance number 'i' is < 0, add after 'i-th' instance of block from the end.
        :param _strict: If True, raise ValueError if no occurrence of block of type _type found, else append
        the _block at the end.
        :return: Self.
        """
        _add_after(self, _block, _type, _instance_num, _strict)
        return self

    def add_before(self,
                   _block: _home_and_modal_types,
                   _type: Type[_home_and_modal_types],
                   _instance_num: int = 1,
                   _strict: bool = False):
        """
        Add block element before specified instance occurrence of a block of type _type.
        :param _block: Block to be added.
        :param _type: Type of block to add the inserted _block before.
        :param _instance_num: Must be non-zero. Number of the instance of blocks of type _type
        before which the _block is added. If number of the instance is larger than actual number of occurrences,
        add before the last instance. If instance number 'i' is < 0, add before 'i-th' instance of block from the end.
        :param _strict: If True, raise ValueError if no occurrence of block of type _type found, else add
        the _block at the beginning.
        :return: Self.
        """
        _add_before(self, _block, _type, _instance_num, _strict)
        return self

    def copy(self):
        temp = HomeSurface()
        temp._body = deepcopy(self._body)
        temp._blocks = temp._body["blocks"]
        return temp

    @property
    def blocks(self):
        return self._blocks

    @blocks.setter
    def blocks(self, _blocks):
        self._blocks = _blocks


class MessageSurface(BlockInterface):

    def __init__(self, blocks: _all_types = None):
        self._blocks = blocks if blocks else []
        self._body = {
            "blocks": self._blocks
        }

    def add(self,
            item: _all_types,
            index: int = None):
        """
        Add block element to the surface.
        :param item: Block element to be added.
        :param index: Index at which to add the element. If none, append.
        :return: Self.
        """
        _add(self, item, index)
        return self

    def add_after(self,
                  _block: _all_types,
                  _type: Type[_all_types],
                  _instance_num: int = 1,
                  _strict: bool = False):
        """
        Add block element after specified instance occurrence of a block of type _type.
        :param _block: Block to be added.
        :param _type: Type of block to add the inserted _block after.
        :param _instance_num: Must be non-zero. Number of the instance of a block of type _type
        after which the _block is added. If number of the instance is larger than actual number of occurrences,
        add after the last instance. If the instance number 'i' is < 0, add after 'i-th' instance of block from the end.
        :param _strict: If True, raise ValueError if no occurrence of block of type _type found, else append
        the _block at the end.
        :return: Self.
        """
        _add_after(self, _block, _type, _instance_num, _strict)
        return self

    def add_before(self,
                   _block: _all_types,
                   _type: Type[_all_types],
                   _instance_num: int = 1,
                   _strict: bool = False):
        """
        Add block element before specified instance occurrence of a block of type _type.
        :param _block: Block to be added.
        :param _type: Type of block to add the inserted _block before.
        :param _instance_num: Must be non-zero. Number of the instance of blocks of type _type
        before which the _block is added. If number of the instance is larger than actual number of occurrences,
        add before the last instance. If instance number 'i' is < 0, add before 'i-th' instance of block from the end.
        :param _strict: If True, raise ValueError if no occurrence of block of type _type found, else add
        the _block at the beginning.
        :return: Self.
        """
        _add_before(self, _block, _type, _instance_num, _strict)
        return self

    def copy(self):
        temp = MessageSurface()
        temp._body = deepcopy(self._body)
        temp._blocks = temp._body["blocks"]
        return temp


class ModalSurface(BlockInterface):

    def __init__(self, title: Text, close: Text, blocks: List[_home_and_modal_types] = None, submit: Text = None):
        self._blocks = blocks if blocks else []
        self._title = title
        self._submit = submit
        self._close = close

        self._body = {
            "type": "modal",
            "title": title,
            "close": close,
            "blocks": blocks
        }

        if submit:
            self._body["submit"] = submit

    def add(self,
            item: _home_and_modal_types,
            index: int = None):
        """
        Add block element to the surface.
        :param item: Block element to be added.
        :param index: Index at which to add the element. If none, append.
        :return: Self.
        """
        _add(self, item, index)
        return self

    def add_after(self,
                  _block: _home_and_modal_types,
                  _type: Type[_home_and_modal_types],
                  _instance_num: int = 1,
                  _strict: bool = False):
        """
        Add block element after specified instance occurrence of a block of type _type.
        :param _block: Block to be added.
        :param _type: Type of block to add the inserted _block after.
        :param _instance_num: Must be non-zero. Number of the instance of a block of type _type
        after which the _block is added. If number of the instance is larger than actual number of occurrences,
        add after the last instance. If the instance number 'i' is < 0, add after 'i-th' instance of block from the end.
        :param _strict: If True, raise ValueError if no occurrence of block of type _type found, else append
        the _block at the end.
        :return: Self.
        """
        _add_after(self, _block, _type, _instance_num, _strict)
        return self

    def add_before(self,
                   _block: _home_and_modal_types,
                   _type: Type[_home_and_modal_types],
                   _instance_num: int = 1,
                   _strict: bool = False):
        """
        Add block element before specified instance occurrence of a block of type _type.
        :param _block: Block to be added.
        :param _type: Type of block to add the inserted _block before.
        :param _instance_num: Must be non-zero. Number of the instance of blocks of type _type
        before which the _block is added. If number of the instance is larger than actual number of occurrences,
        add before the last instance. If instance number 'i' is < 0, add before 'i-th' instance of block from the end.
        :param _strict: If True, raise ValueError if no occurrence of block of type _type found, else add
        the _block at the beginning.
        :return: Self.
        """
        _add_before(self, _block, _type, _instance_num, _strict)
        return self

    def copy(self):
        _title = copy(self._title)
        _close = copy(self._close)
        temp = ModalSurface(_title, _close)
        temp._body = deepcopy(self._body)
        temp._blocks = temp._body["blocks"]
        return temp

    @property
    def blocks(self):
        return self._blocks

    @blocks.setter
    def blocks(self, _blocks):
        self._blocks = _blocks
        self._body["blocks"] = _blocks

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, _title):
        self._title = _title
        self._body["title"] = _title

    @property
    def close(self):
        return self._close

    @close.setter
    def close(self, _close):
        self._close = _close
        self._body["close"] = _close

    @property
    def submit(self):
        return self._submit

    @submit.setter
    def submit(self, _submit):
        if _submit:
            self._body["submit"] = _submit
        else:
            self._body.pop("submit", None)
        self._submit = _submit
