#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# cleanup
rm -rf /usr/share/misc
rm -rf /usr/share/man
rm -rf /usr/share/doc
rm -rf /usr/share/locale/[a-d]*
rm -rf /usr/share/locale/[f-k]*
rm -rf /usr/share/locale/[m-z]*
rm -rf /usr/share/espeak-ng-data/[a-d]*_dict
rm -rf /usr/share/espeak-ng-data/[f-z]*_dict
rm -rf /var/cache
rm -rf /usr/share/fonts/FreeMon*.ttf
