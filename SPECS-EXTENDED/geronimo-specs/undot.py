#!/usr/bin/python

# remove dots from package names, as they are not allowed in SUSE
#
# Usage:
# cat geronimo-specs.spec | ./undot.py > geronimo-specs.new.spec
# gvimdiff geronimo-specs.spec geronimo-specs.new.spec # review

import re
import sys

regexp = re.compile(r'^(Requires|%package|%description|%post|%postun|%pre|%preun|%files|BuildRequires|PreReq|Provides).*')
oregexp = re.compile(r'[<=>]')

for line in sys.stdin:

    if regexp.search(line):
        m = oregexp.search(line)
        if m:
            line = line[:m.start()].replace('.', '_') + line[m.start():]
        else:
            line = line.replace('.', '_')
    
    sys.stdout.write(line)

