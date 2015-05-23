#!/usr/bin/env python
# -*- coding: utf8 -*-
# Created by Xavier Yin on 2015/2/28

from core import GitCore
import inspect
import sys


class TemplateBase(object):

    def __init__(self, config):
        self.config = config
        self.new = self.config.commit.new
        self.old = self.config.commit.old

    def commit_summary(self, sha1=None):
        if sha1 is None:
            sha1 = self.new
        summary_heads = GitCore.get_summary_heads(sha1)
        summary_body = GitCore.get_full_summary_body(sha1)
        changed_text = '\n'.join(('<li>%s</li>' % path for path in GitCore.get_changed_files(sha1)))
        changed_text = "<ol>%s</ol>" % changed_text

        heads = summary_heads.items()
        heads.sort(key=lambda x: x[0])
        tpl = """<tr><td class="thick">%(head)s</td><td>%(value)s</td></tr>"""
        head_html = ""
        for head in heads:
            head_html += tpl % {'head': head[0], 'value': head[1]}

        html = """\
<table>
    %(head)s
    <tr>
        <td class="align-left" colspan="2"><pre>%(body)s</pre></td>
    </tr>
</table>

<p><b>本次修改文件: </b></p>
%(foot)s
""" % {"head": head_html, "body": summary_body, "foot": changed_text}
        return html

    def commit_summary_join(self, depth=20):
        html = ""
        g = GitCore.next_short_summary(self.new)
        i = 0
        for sha1, comment in g:
            if self.old.startswith(sha1):
                break
            html += "<div>%s</div><br><hr>\n" % self.commit_summary(sha1)
            i += 1
            if i >= depth:
                break
        return html

    def render(self, **kwargs):
        return self.html()

    def css(self):
        return """\
<style>
table{
    border-collapse: collapse;
    border: 1px solid;
    text-align: center;
}

th, td{
    border: 1px solid;
    font-size: medium;
    margin-left: auto;
    margin-right: auto;
}

td.thick {font-weight: bold;}

td.align-left { text-align: left; }

th{
    background: dodgerblue;
}

td ul{
    font-size: small;
}


li {
    list-style-type: none;
    text-align: left;
}

</style>
        """

    def head(self):
        return "<head>%(css)s</head>" % {'css': self.css()}

    def body(self):
        return "<body></body>"

    def html(self):
        html = """<!DOCTYPE html>
<html>
%(head)s
%(body)s
</html>
""" % {'head': self.head(), 'body': self.body()}
        return html


class TemplateTo(TemplateBase):

    def body(self):
        return """\
<body>
%(summary)s
</body>
""" % {'summary': self.commit_summary_join()}


class TemplateReview(TemplateTo):
    pass


class TemplateSc(TemplateTo):
    pass


def _get_all_template_objects():
    klasses = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    tpls = {}
    for k, v in klasses:
        if k.startswith("Template") and len(k) > 8:
            tpls[k] = v
    return tpls

TEMPLATES = _get_all_template_objects()


if __name__ == "__main__":
    pass