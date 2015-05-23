#!/usr/bin/env python
# -*- coding: utf8 -*-
# Created by Me on 2015/2/11

from mail import SMTPMailer
from hooks import HOOKS, WATCHES, Parser
from core import GitCore
from threading import Thread
from Queue import Queue, Empty
import time


class CallHookError(Exception):
    pass


def _call_hook_action(name, arg, config, action="prepare"):
    klass = HOOKS.get("Hook%s" % name.capitalize(), None)
    if klass is not None:
        obj = klass(arg, config)
        if action == "prepare":
            obj.prepare()
        elif action == "go":
            obj.go()
        else:
            pass
    else:
        raise CallHookError("Can't find hook for tag '%s'." % name)


def run(q):
    while True:
        try:
            th = q.get(False)
            th.start()
            th.join()
            q.task_done()
            time.sleep(5)
        except Empty:
            break


def run_as_post_receive(config):
    parser = Parser(GitCore.get_full_summary_body(config.commit.new), config)

    # tasks = Queue()
    for k, v in parser.hooks.items():
        _call_hook_action(k, v, config, "prepare")
    for k, v in parser.hooks.items():
        # th = Thread(target=_call_hook_action, args=(k, v, config, "go"))
        # tasks.put(th)
        _call_hook_action(k, v, config, "go")
        time.sleep(3)

    for watch in WATCHES.values():
        # func = watch(config).go
        # th = Thread(target=func)
        # tasks.put(th)
        watch(config).go()

    # th = Thread(target=run, args=(tasks,))
    # th.start()


if __name__ == "__main__":
    pass