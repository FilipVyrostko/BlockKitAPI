from copy import deepcopy
from BlockAPI.Blocks import *

# List of types supported by home surface and modals
_home_and_modal_types = Union[ActionBlock, ContextBlock, DividerBlock,
                              HeaderBlock, ImageBlock, InputBlock,
                              SectionBlock, VideoBlock]


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

        if index and index > len(self._blocks):
            raise IndexError

        if index is None:
            self._blocks.append(item)
        else:
            self._blocks.insert(index, item)
        return self

    # Add block after specified instance of block of type _type
    # If _strict is True, raise ValueError if _type block is not found,
    # else append at the end of the list of blocks
    def add_after(self,
                  _block: _home_and_modal_types,
                  _type: _home_and_modal_types,
                  _instance_num: int = 1,
                  _strict: bool = False):
        pass

    # Add block before specified instance of block of type _type
    # If _strict is True, raise ValueError if _type block is not found,
    # else append at the end of the list of block
    def add_before(self,
                   _block: _home_and_modal_types,
                   _type: _home_and_modal_types,
                   _instance_num: int = 1,
                   _strict: bool = False):
        pass

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

    def __init__(self, blocks: Union[ActionBlock, ContextBlock, DividerBlock,
                                     HeaderBlock, ImageBlock, InputBlock,
                                     SectionBlock, VideoBlock, FileBlock] = None):
        self._blocks = blocks if blocks else []
        self._body = {
            "blocks": self._blocks
        }


class ModalSurface(BlockInterface):

    def __init__(self, title: Text, close: Text, blocks: List = None, submit: Text = None):

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
            item: Union[ActionBlock, ContextBlock, DividerBlock,
                        FileBlock, HeaderBlock, ImageBlock,
                        InputBlock, SectionBlock, VideoBlock],
            index: int = None):

        if index and index > len(self._blocks):
            raise IndexError

        if index is None:
            self._blocks.append(item)
        else:
            self._blocks.insert(index, item)

        return self

    def copy(self):
        temp = ModalSurface()
        temp._body = deepcopy(self._body)
        temp._blocks = temp._body["blocks"]
        return temp
