#!/usr/bin/env python
# -*- coding: utf8 -*-
# Created by Xavier Yin on 2015/2/28


from email.mime.text import MIMEText
import abc
import smtplib


class Mailer(object):

    @abc.abstractmethod
    def send_mail(self, to_addresses, msg):
        pass


class SMTPMailer(Mailer):

    def __init__(self, sender, smtp_server):
        self.sender = sender
        self.server = smtp_server
        self.smtp = smtplib.SMTP(self.server)
        self._subject = self._from = self._to = self._charset = self._subtype = None

    def login(self, user, pw):
        self.smtp.login(user, pw)

    @property
    def mail_subject(self):
        return self._subject or ''

    @mail_subject.setter
    def mail_subject(self, other):
        self._subject = other

    @property
    def mail_from(self):
        return self._from or self.sender

    @mail_from.setter
    def mail_from(self, other):
        self._from = other

    @property
    def mail_to(self):
        return self._to

    @mail_to.setter
    def mail_to(self, other):
        if isinstance(other, list):
            other = ";".join(set(other))
        self._to = other

    @property
    def mail_charset(self):
        return self._charset or "utf8"

    @mail_charset.setter
    def mail_charset(self, other):
        self._charset = other

    @property
    def mail_subtype(self):
        return self._subtype or "html"

    @mail_subtype.setter
    def mail_subtype(self, other):
        self._subtype = other

    def set_mail_headers(self, subject=None, from_addr=None, to_addrs=None):
        if subject:
            self.mail_subject = subject
        if from_addr:
            self.mail_from = from_addr
        if to_addrs:
            self.mail_to = to_addrs

    def send_mail(self, msg, to_addresses, subtype=None, charset=None):
        if subtype:
            self.mail_subtype = subtype
        if charset:
            self.mail_charset = charset
        if isinstance(to_addresses, str):
            to_addresses = to_addresses.split(";")
        to_addresses = list(set(to_addresses))

        m = MIMEText(msg, self.mail_subtype, self.mail_charset)
        m['Subject'] = self.mail_subject
        m['From'] = self.mail_from
        m['To'] = self.mail_to

        self.smtp.sendmail(self.sender, to_addresses, m.as_string())
        self.smtp.close()


def send_mail(config, subject=None, sender=None, recipients=None, from_=None,
              to=None, msg=None, subtype=None, server=None, user=None, pw=None):
    subject = subject or config.mail.subject
    sender = sender or config.mailer.smtp.sender
    recipients = recipients or config.mail.recipients
    from_ = from_ or config.mail.from_
    to = to or config.mail.to
    msg = msg or config.mail.msg
    subtype = subtype or config.mail.subtype
    server = server or config.mailer.smtp.server
    user = user or config.mailer.smtp.user
    pw = pw or config.mailer.smtp.pw

    mailer = SMTPMailer(sender, server)
    mailer.set_mail_headers(subject, from_, to)
    if user and pw:
        mailer.login(user, pw)
    mailer.send_mail(msg, recipients, subtype)


def send_mail2(msg, to_addrs, subject=None, subtype=None, charset=None, from_addr=None):
    # todo: remove this method.
    if isinstance(to_addrs, list):
        to_addrs = ';'.join(to_addrs)

    smtp = SMTPMailer("test_08@qq.com", "smtp.qq.com")
    smtp.login("test_08", "Abc12345")
    smtp.mail_subject = "Test W"
    smtp.set_mail_headers(to_addrs=to_addrs, subject=subject, from_addr=from_addr)
    smtp.send_mail(msg, to_addrs, subtype=subtype, charset=charset)

if __name__ == "__main__":
    pass
