#!/usr/bin/env python
# -*- coding: utf8 -*-
# Created by Xavier Yin on 2015/3/1

import json
import os


class ConfBase(object):
    def __init__(self, conf):
        self._conf = {}
        if isinstance(conf, dict):
            self._conf = conf

    def __repr__(self):
        return str(self.__dict__)


class Config(ConfBase):

    def __init__(self, config_file):
        self.conf = {
            "mailer": {},
            "mail": {},
            "commit": {}
        }

        if os.path.isfile(str(config_file)):
            with open(config_file) as fp:
                self.conf = json.load(fp)

        self.mail = ConfMail(self.conf.get("mail", {}))
        self.mailer = ConfMailer(self.conf.get("mailer", {}))
        self.commit = ConfCommit(self.conf.get("commit", {}))


class ConfMailer(ConfBase):

    def __init__(self, conf):
        super(ConfMailer, self).__init__(conf)
        self.smtp = ConfSMTP(self._conf.get("smtp", {}))


class ConfMail(ConfBase):

    def __init__(self, conf):
        super(ConfMail, self).__init__(conf)
        self.from_ = self._conf.get("from", "xavier@git.ring")
        self.recipients = self._conf.get("recipients", [])
        self.subtype = self._conf.get("subtype", "html")
        self.charset = self._conf.get("charset", "utf8")
        self.to = self._conf.get("to", [])
        self.sc = self._conf.get("sc", [])
        self.subject = self._conf.get("subject", "Git Ring Says Hi")
        self.msg = self._conf.get("msg", "")


class ConfSMTP(ConfBase):

    def __init__(self, conf):
        super(ConfSMTP, self).__init__(conf)
        self.server = self._conf.get("server", 'localhost')
        self.user = self._conf.get("user", '')
        self.pw = self._conf.get("pw", '')
        self.sender = self._conf.get("sender", '')


class ConfCommit(ConfBase):

    def __init__(self, conf):
        super(ConfCommit, self).__init__(conf)
        self.new = self._conf.get("new", "")
        self.old = self._conf.get("old", "")
        self.ref = self._conf.get("ref", "")
        self.sha1 = self._conf.get("sha1", "")


if __name__ == "__main__":
    pass