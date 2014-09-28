import sys

sys.path.insert(0, '../leap')

import time
from argparse import ArgumentParser
from pykeyboard import PyKeyboard
import Leap


class SwitchManager(object):
    def __init__(self, toggle_interval):
        self._toggle_interval = toggle_interval
        self._active = False
        self._keyboard = PyKeyboard()
        self._last_toggle = time.time()

    def _activate(self):
        print 'activate'
        self._active = True
        self._keyboard.press_key(self._keyboard.super_l_key)
        self._keyboard.tap_key('w')
        self._keyboard.release_key(self._keyboard.super_l_key)

    def _deactivate(self):
        print 'deactivate'
        self._active = False
        self._keyboard.tap_key(self._keyboard.enter_key)

    def toggle(self):
        if self._last_toggle + self._toggle_interval > time.time():
            print 'toggle interval'
            return

        print 'toggle'
        self._last_toggle = time.time()
        if self._active:
            self._deactivate()
        else:
            self._activate()

    def _move(self, key):
        print 'move', key
        if self._active:
            self._last_toggle = time.time()
            self._keyboard.tap_key(key)

    left = lambda self: self._move(self._keyboard.left_key)
    right = lambda self: self._move(self._keyboard.right_key)
    up = lambda self: self._move(self._keyboard.up_key)
    down = lambda self: self._move(self._keyboard.down_key)


class Listener(Leap.Listener):
    def __init__(self, switch_manager, swipe_threshold):
        """
        :type switch_manager: SwitchManager
        """
        super(Listener, self).__init__()
        self._swipe_threshold = swipe_threshold
        self._switch_manger = switch_manager
        self._last_xyz = None

    def on_connect(self, controller):
        """
        :type controller: Leap.Controller
        """
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
        controller.config.save()

    def on_frame(self, controller):
        """
        :type controller: Leap.Controller
        """
        handled = []
        for gesture in controller.frame().gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE and \
                            gesture.state == Leap.Gesture.STATE_STOP:
                if not 'circle' in handled:
                    handled.append('circle')
                    self._switch_manger.toggle()
            elif gesture.type == Leap.Gesture.TYPE_SWIPE and \
                            gesture.state == Leap.Gesture.STATE_STOP:
                swipe = Leap.SwipeGesture(gesture)
                if swipe.direction.x > self._swipe_threshold and \
                        not 'x' in handled:
                    handled.append('x')
                    self._switch_manger.right()
                if swipe.direction.x < self._swipe_threshold and \
                        not 'x' in handled:
                    handled.append('x')
                    self._switch_manger.left()
                if swipe.direction.y > self._swipe_threshold and \
                        not 'y' in handled:
                    handled.append('y')
                    self._switch_manger.up()
                if swipe.direction.y < self._swipe_threshold and \
                        not 'y' in handled:
                    handled.append('y')
                    self._switch_manger.down()


def get_args():
    parser = ArgumentParser()
    parser.add_argument('--swipe-threshold', type=float, default=0.1,
                        help='Threshold for swipe gestures.')
    parser.add_argument('--toggle-interval', type=int, default=3,
                        help='Interval between open/close switch window'
                             'actions.')
    return parser.parse_args()


def main():
    args = get_args()
    manager = SwitchManager(args.toggle_interval)
    listener = Listener(manager, args.swipe_threshold)
    controller = Leap.Controller()
    controller.add_listener(listener)
    raw_input()
