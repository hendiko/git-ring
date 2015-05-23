#!/usr/bin/env python
# -*- coding: utf8 -*-
# Created by Xavier Yin on 2015/2/11


import subprocess


class Core(object):
    pass


class GitCore(object):

    @staticmethod
    def exec_(cmd, input_=None, **kwargs):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, **kwargs)
        out = p.communicate(input_)[0].strip()
        code = p.wait()
        if code:
            raise GitCommandError(cmd, code)
        return out

    @classmethod
    def git(cls, args, input_=None, **kwargs):
        cmd = ['git'] + args
        return cls.exec_(cmd, input_, **kwargs)

    @classmethod
    def get_changed_files(cls, sha1='HEAD'):
        """Get files which have been changed."""
        out = cls.git(['log', '--name-only', '--oneline', '--no-walk', sha1])
        return out.split("\n")[1:]

    @classmethod
    def get_git_object_type(cls, sha1='HEAD'):
        """Identify git object type according to sha1, possible type is commit or tag."""
        return cls.git(['cat-file', '-t', sha1])

    @classmethod
    def get_short_sha1(cls, sha1='HEAD'):
        """Return a 7 chars long string."""
        return cls.git(['rev-parse', '--short', sha1])

    @classmethod
    def get_short_summary(cls, sha1='HEAD'):
        sha1, comment = cls.git(['log', '--abbrev', '--format=%h %s', '--no-walk', sha1]).split(' ', 1)
        return sha1, comment

    @classmethod
    def get_full_summary(cls, sha1='HEAD'):
        # todo: split full summary into different parts with regexp.
        return cls.git(['log', '--no-walk', sha1])

    @classmethod
    def get_full_summary_heads(cls, sha1='HEAD'):
        out = cls.get_full_summary(sha1)
        return out.split("\n\n", 1)[0]

    @classmethod
    def get_full_summary_body(cls, sha1='HEAD'):
        out = cls.get_full_summary(sha1)
        return out.split("\n\n", 1)[1]

    @classmethod
    def get_summary_heads(cls, sha1='HEAD'):
        out = cls.get_full_summary(sha1)
        heads = out.split("\n\n", 1)[0].split("\n")
        head_dict = {}
        for head in heads[1:]:
            k, v = head.split(":", 1)
            head_dict.setdefault(k.lower(), v.strip())
        head_dict.update((heads[0].split(),))
        return head_dict

    @classmethod
    def next_short_summary(cls, sha1='HEAD'):
        """A generator to traverse all commits."""
        while True:
            try:
                sha1, comment = cls.get_short_summary(sha1)
                yield (sha1, comment)
                sha1 = "%s^" % sha1
            except GitCommandError:
                break


class GitCommandError(Exception):
    """Git Command Error."""
    pass


if __name__ == "__main__":
    pass
