#!/usr/bin/env python
# -*- coding: utf8 -*-
# Created by Xavier Yin on 2015/2/28

from modules.conf import Config
from modules import run_as_post_receive
import os
import sys


CURRENT_FILE_PATH = os.path.abspath(__file__)
CURRENT_WORK_DIR = os.path.dirname(CURRENT_FILE_PATH)
GIT_DIR = os.path.dirname(CURRENT_WORK_DIR)

config_file = os.path.join(CURRENT_WORK_DIR, "ring.json")
config = Config(config_file)


if __name__ == "__main__":
    old, new, ref = sys.stdin.read().split()
    head, body, foot = ref.split("/", 2)
    config.commit.new = new
    config.commit.old = old
    config.commit.ref = "branch" if body == "heads" else "tag"
    config.commit.sha1 = foot
    run_as_post_receive(config)