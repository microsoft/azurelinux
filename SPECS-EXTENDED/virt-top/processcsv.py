#!/usr/bin/python3
#
# https://bugzilla.redhat.com/show_bug.cgi?id=665817
#
# Usage:
#
#   virt-top --csv data.csv
#   processcsv.py < data.csv
#
# Note this OVERWRITES the following files in the current directory:
#
#   global.csv         # all the global data
#   domain<NN>.csv     # data for domain ID <NN> (multiple files)

import sys
import csv

rows = csv.reader (sys.stdin)

# Get the header row.
header = next(rows)

# Find the index of the 'Hostname' and 'Time' cols (usually first two).
hostname_i = header.index ("Hostname")
time_i = header.index ("Time")

# Find the index of the 'Domain ID' column (i) and the number of
# columns per domain (w).
i = header.index ("Domain ID")
w = len (header) - i

dom_header = header[i:i+w]
dom_header.insert (0, "Hostname")
dom_header.insert (1, "Time")

gfile = open ("global.csv", "w")
gfile_writer = csv.writer (gfile)
gfile_writer.writerow (header[0:i])

dfiles = dict()

# Process all the remaining data rows.
for data in rows:
    # Global data is columns 0..i-1
    gfile_writer.writerow (data[0:i])

    hostname = data[hostname_i]
    time = data[time_i]

    # For each domain ...
    for j in range(i,len(data),w):
        dom = data[j:j+w]
        domid = dom[0]

        if domid in dfiles:
            dfile_writer = dfiles[domid]
        else:
            dfile = open ("domain%s.csv" % domid, "w")
            dfile_writer = csv.writer (dfile)
            dfile_writer.writerow (dom_header)
            dfiles[domid] = dfile_writer

        dom.insert (0, hostname)
        dom.insert (1, time)
        dfile_writer.writerow (dom)
