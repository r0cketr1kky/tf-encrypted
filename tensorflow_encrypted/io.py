from __future__ import absolute_import
from typing import Optional, Callable, Union, List

import tensorflow as tf

from .player import Player
from .config import get_config


Data = Union[tf.Tensor, List[tf.Tensor]]
InputFunc = Callable[[], Data]
OutputFunc = Callable[[Data], tf.Operation]


class InputProvider(object):

    def __init__(self, player: Union[str, Player], input_fn: Optional[InputFunc] = None) -> None:
        if isinstance(player, str):
            self.player = get_config().get_player(player)
        else:
            self.player = player
        self.input_fn = input_fn

    def provide_input(self) -> Data:
        if self.input_fn is None:
            raise NotImplementedError()
        return self.input_fn()


class OutputReceiver(object):

    def __init__(self, player: Union[str, Player], output_fn: Optional[OutputFunc] = None) -> None:
        if isinstance(player, str):
            self.player = get_config().get_player(player)
        else:
            self.player = player
        self.output_fn = output_fn

    def receive_output(self, tensor: Data) -> tf.Operation:
        if self.output_fn is None:
            raise NotImplementedError()
        return self.output_fn(tensor)
