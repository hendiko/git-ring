#!/usr/bin/env python
# -*- coding: utf8 -*-
# Created by Xavier Yin on 2015/3/1

from mail import send_mail
from tpls import TEMPLATES
import abc
import inspect
import re
import shlex
import sys


class Hook(object):

    def __init__(self, arg, config):
        self.raw_arg = str(arg)
        self.args = shlex.split(self.raw_arg)
        self.config = config

    def get_template(self):
        name = "Template%s" % self.__class__.__name__.lstrip("Hook")
        klass = TEMPLATES.get(name, None)
        if klass is not None:
            return klass(self.config)

    @abc.abstractmethod
    def go(self):
        pass

    @abc.abstractmethod
    def prepare(self):
        pass

    def get_title_prefix(self):
        prefix = "[%(commit)s][%(ref)s][%(sha1)s]" % {
            "ref": self.config.commit.ref,
            "sha1": self.config.commit.sha1,
            "commit": self.config.commit.new[:7]
        }
        return prefix


class HookTo(Hook):

    def go(self):
        tpl = self.get_template()
        html = tpl.render() if tpl is not None else self.config.mail.msg
        subject = "[通知]%(prefix)s %(subject)s" % {
            "prefix": self.get_title_prefix(), "subject": self.config.mail.subject.encode('utf8')}
        send_mail(self.config, recipients=self.config.mail.to, msg=html, subject=subject)

    def prepare(self):
        self.config.mail.to += self.args


class HookReview(Hook):

    def go(self):
        tpl = self.get_template()
        html = tpl.render() if tpl is not None else self.config.mail.msg
        subject = "[审阅]%(prefix)s %(subject)s" % {
            "prefix": self.get_title_prefix(), "subject": self.config.mail.subject.encode('utf8')}
        send_mail(self.config, recipients=self.args, to=self.args, msg=html, subject=subject)

    def prepare(self):
        pass


class HookCc(Hook):

    def go(self):
        tpl = self.get_template()
        html = tpl.render() if tpl is not None else self.config.mail.msg
        subject = "[抄送]%(prefix)s %(subject)s" % {
            "prefix": self.get_title_prefix(), "subject": self.config.mail.subject.encode('utf8')}
        send_mail(self.config, recipients=self.args, to=self.args, msg=html, subject=subject)

    def prepare(self):
        pass


class Watch(Hook):
    def __init__(self, config):
        self.config = config

    def get_template(self):
        name = "Template%s" % self.__class__.__name__.lstrip("Watch")
        klass = TEMPLATES.get(name, None)
        if klass is not None:
            return klass(self.config)

    def go(self):
        pass

    def prepare(self):
        pass


class WatchSc(Watch):

    def go(self):
        tpl = self.get_template()
        html = tpl.render()
        subject = "[密送]%(prefix)s %(subject)s" % {
            "prefix": self.get_title_prefix(), "subject": self.config.mail.subject.encode('utf8')}
        send_mail(self.config, recipients=self.config.mail.sc, to=self.config.mail.sc,
                  msg=html, subject=subject)


class Parser(object):
    RE_HOOK_FIELD = r"\[\[(.*)\]\]"

    def __init__(self, msg, config):
        self.msg = str(msg)
        self.config = config
        self.fields = self._get_all_fields()
        self.hooks = self._get_all_hooks()

    def _get_all_fields(self):
        return re.findall(self.RE_HOOK_FIELD, self.msg)

    def _get_all_hooks(self):
        hooks = [x.split(":", 1) for x in self.fields]
        _hooks = {}
        for k, v in hooks:
            _hooks[k.strip()] = v.strip()
        return _hooks


def _get_all_hook_objects(prefix='Hook'):
    klasses = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    hooks = {}
    for k, v in klasses:
        if k.startswith(prefix) and len(k) > len(prefix):
            hooks[k] = v
    return hooks

HOOKS = _get_all_hook_objects()
WATCHES = _get_all_hook_objects('Watch')

if __name__ == "__main__":
    pass