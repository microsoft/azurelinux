#!/bin/sh
# Copyright (C) 2008 Red Hat, Inc.
#
# All rights reserved. This copyrighted material is made available to anyone
# wishing to use, modify, copy, or redistribute it subject to the terms and
# conditions of the GNU General Public License version 2.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
if [ -z "$DBUS_SESSION_BUS_ADDRESS" ]; then
        eval `dbus-launch --sh-syntax --exit-with-session`
fi
