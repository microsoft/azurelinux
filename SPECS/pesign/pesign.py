#!/usr/bin/python3
#
# Copyright 2017 Peter Jones <Peter Jones@random>
#
# Distributed under terms of the GPLv3 license.

"""
mock plugin to make sure pesign and mockbuild users have the right uid and
gid.
"""

from mockbuild.trace_decorator import getLog, traceLog
import mockbuild.util

requires_api_version = "1.1"

@traceLog()
def init(plugins, conf, buildroot):
    """ hello """
    Pesign(plugins, conf, buildroot)

def getuid(name):
    """ get a uid for a user name """
    output = mockbuild.util.do(["getent", "passwd", "%s" % (name,)],
                               returnOutput=1, printOutput=True)
    output = output.split(':')
    return output[2], output[3]

def getgid(name):
    """ get a gid for a group name """
    output = mockbuild.util.do(["getent", "group", "%s" % (name,)],
                               returnOutput=1, printOutput=True)
    return output.split(':')[2]

def newgroup(name, gid, rootdir):
    """ create a group with a gid """
    getLog().info("creating group %s with gid %s" % (name, gid))
    mockbuild.util.do(["groupadd",
                       "-g", "%s" % (gid,),
                       "-R", "%s" % (rootdir,),
                       "%s" % (name,),
                      ])

def newuser(name, uid, gid, rootdir):
    """ create a user with a uid """
    getLog().info("creating user %s with uid %s" % (name, uid))
    mockbuild.util.do(["useradd",
                       "-u", "%s" % (uid,),
                       "-g", "%s" % (gid,),
                       "-R", "%s" % (rootdir,),
                       "%s" % (name,)])

class Pesign(object):
    """ Creates some stuff in our mock root """
    # pylint: disable=too-few-public-methods
    @traceLog()
    def __init__(self, plugins, conf, buildroot):
        """ Effectively we're doing:
            getent group pesign >/dev/null || groupadd -r pesign
            getent passwd pesign >/dev/null || \
                    useradd -r -g pesign -d /var/run/pesign -s /sbin/nologin \
                    -c "Group for the pesign signing daemon" pesign
        """

        self.buildroot = buildroot
        self.pesign_opts = conf
        self.config = buildroot.config
        self.state = buildroot.state
        self.users = {}
        self.groups = {}
        plugins.add_hook("postinit", self._pesignPostInitHook)

    @traceLog()
    def _pesignPostInitHook(self):
        """ find our uid and gid lists """
        for user in self.pesign_opts['users']:
            uid, gid = getuid(user)
            self.users[user] = [user, uid, gid]
        for group in self.pesign_opts['groups']:
            gid = getgid(group)
            self.groups[group] = [group, gid]

        # create our users
        rootdir = self.buildroot.make_chroot_path()
        for name, gid in self.groups.values():
            newgroup(name, gid, rootdir)
        for name, uid, gid in self.users.values():
            newuser(name, uid, gid, rootdir)

# -*- coding: utf-8 -*-
# vim:fenc=utf-8:tw=75
