#!/usr/bin/env python

# Try to determine how much RAM is currently being used per program.
# Note per _program_, not per process. So for example this script
# will report RAM used by all httpd process together. In detail it reports:
# sum(private RAM for program processes) + sum(Shared RAM for program processes)
# The shared RAM is problematic to calculate, and this script automatically
# selects the most accurate method available for your kernel.

# Licence: LGPLv2
# Author:  P@draigBrady.com
# Source:  https://www.pixelbeat.org/scripts/ps_mem.py

# V1.0      06 Jul 2005     Initial release
# V1.1      11 Aug 2006     root permission required for accuracy
# V1.2      08 Nov 2006     Add total to output
#                           Use KiB,MiB,... for units rather than K,M,...
# V1.3      22 Nov 2006     Ignore shared col from /proc/$pid/statm for
#                           2.6 kernels up to and including 2.6.9.
#                           There it represented the total file backed extent
# V1.4      23 Nov 2006     Remove total from output as it's meaningless
#                           (the shared values overlap with other programs).
#                           Display the shared column. This extra info is
#                           useful, especially as it overlaps between programs.
# V1.5      26 Mar 2007     Remove redundant recursion from human()
# V1.6      05 Jun 2007     Also report number of processes with a given name.
#                           Patch from riccardo.murri@gmail.com
# V1.7      20 Sep 2007     Use PSS from /proc/$pid/smaps if available, which
#                           fixes some over-estimation and allows totalling.
#                           Enumerate the PIDs directly rather than using ps,
#                           which fixes the possible race between reading
#                           RSS with ps, and shared memory with this program.
#                           Also we can show non truncated command names.
# V1.8      28 Sep 2007     More accurate matching for stats in /proc/$pid/smaps
#                           as otherwise could match libraries causing a crash.
#                           Patch from patrice.bouchand.fedora@gmail.com
# V1.9      20 Feb 2008     Fix invalid values reported when PSS is available.
#                           Reported by Andrey Borzenkov <arvidjaar@mail.ru>
# V3.14     28 May 2022
#   https://github.com/pixelb/ps_mem/commits/master/ps_mem.py

# Notes:
#
# All interpreted programs where the interpreter is started
# by the shell or with env, will be merged to the interpreter
# (as that's what's given to exec). For e.g. all python programs
# starting with "#!/usr/bin/env python" will be grouped under python.
# You can change this by using the full command line but that will
# have the undesirable affect of splitting up programs started with
# differing parameters (for e.g. mingetty tty[1-6]).
#
# For 2.6 kernels up to and including 2.6.13 and later 2.4 redhat kernels
# (rmap vm without smaps) it can not be accurately determined how many pages
# are shared between processes in general or within a program in our case:
# http://lkml.org/lkml/2005/7/6/250
# A warning is printed if overestimation is possible.
# In addition for 2.6 kernels up to 2.6.9 inclusive, the shared
# value in /proc/$pid/statm is the total file-backed extent of a process.
# We ignore that, introducing more overestimation, again printing a warning.
# Since kernel 2.6.23-rc8-mm1 PSS is available in smaps, which allows
# us to calculate a more accurate value for the total RAM used by programs.
#
# Programs that use CLONE_VM without CLONE_THREAD are discounted by assuming
# they're the only programs that have the same /proc/$PID/smaps file for
# each instance.  This will fail if there are multiple real instances of a
# program that then use CLONE_VM without CLONE_THREAD, or if a clone changes
# its memory map while we're checksumming each /proc/$PID/smaps.
#
# I don't take account of memory allocated for a program
# by other programs. For e.g. memory used in the X server for
# a program could be determined, but is not.
#
# FreeBSD is supported if linprocfs is mounted at /compat/linux/proc/
# FreeBSD 8.0 supports up to a level of Linux 2.6.16

import argparse
import errno
import os
import sys
import time
import io

# The following exits cleanly on Ctrl-C or EPIPE
# while treating other exceptions as before.
def std_exceptions(etype, value, tb):
    sys.excepthook = sys.__excepthook__
    if issubclass(etype, KeyboardInterrupt):
        pass
    elif issubclass(etype, IOError) and value.errno == errno.EPIPE:
        pass
    else:
        sys.__excepthook__(etype, value, tb)
sys.excepthook = std_exceptions

#
#   Define some global variables
#

PAGESIZE = os.sysconf("SC_PAGE_SIZE") / 1024 #KiB
our_pid = os.getpid()

have_pss = 0
have_swap_pss = 0

class Unbuffered(io.TextIOBase):
   def __init__(self, stream):
       super(Unbuffered, self).__init__()
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def close(self):
       self.stream.close()

class Proc:
    def __init__(self):
        uname = os.uname()
        if uname[0] == "FreeBSD":
            self.proc = '/compat/linux/proc'
        else:
            self.proc = '/proc'

    def path(self, *args):
        return os.path.join(self.proc, *(str(a) for a in args))

    def open(self, *args):
        try:
            if sys.version_info < (3,):
                return open(self.path(*args))
            else:
                return open(self.path(*args), errors='ignore')
        except (IOError, OSError):
            if type(args[0]) is not int:
                raise
            val = sys.exc_info()[1]
            if (val.errno == errno.ENOENT or # kernel thread or process gone
                val.errno == errno.EPERM or
                val.errno == errno.EACCES):
                raise LookupError
            raise

proc = Proc()


#
#   Functions
#

def parse_options():
    help_msg = 'Show program core memory usage.'
    parser = argparse.ArgumentParser(prog='ps_mem', description=help_msg)
    parser.add_argument('--version', action='version', version='3.14')
    parser.add_argument(
        '-s', '--split-args',
        action='store_true',
        help='Show and separate by, all command line arguments',
    )
    parser.add_argument(
        '-t', '--total',
        dest='only_total',
        action='store_true',
        help='Show only the total value',
    )
    parser.add_argument(
        '-d', '--discriminate-by-pid',
        action='store_true',
        help='Show by process rather than by program',
    )
    parser.add_argument(
        '-S', '--swap',
        dest='show_swap',
        action='store_true',
        help='Show swap information',
    )
    parser.add_argument(
        '-p',
        dest='pids',
        metavar='<pid>[,pid2,...pidN]',
        help='Only show memory usage PIDs in the specified list',
    )
    parser.add_argument(
        '-w',
        dest='watch',
        metavar='<N>',
        type=int,
        help='Measure and show process memory every N seconds',
    )
    args = parser.parse_args()

    args.pids_to_show = []
    if args.pids:
        try:
            args.pids_to_show = [int(x) for x in args.pids.split(',')]
        except ValueError:
            parser.error('Invalid PID(s): %s' % args.pids)

    if args.watch is not None:
        if args.watch <= 0:
            parser.error('Seconds must be positive! (%s)' % args.watch)

    return (
        args.split_args,
        args.pids_to_show,
        args.watch,
        args.only_total,
        args.discriminate_by_pid,
        args.show_swap,
    )


# (major,minor,release)
def kernel_ver():
    kv = proc.open('sys/kernel/osrelease').readline().split(".")[:3]
    last = len(kv)
    if last == 2:
        kv.append('0')
    last -= 1
    while last > 0:
        for char in "-_":
            kv[last] = kv[last].split(char)[0]
        try:
            int(kv[last])
        except:
            kv[last] = 0
        last -= 1
    return (int(kv[0]), int(kv[1]), int(kv[2]))


#return Private,Shared,Swap(Pss),unique_id
#Note shared is always a subset of rss (trs is not always)
def getMemStats(pid):
    global have_pss
    global have_swap_pss
    mem_id = pid #unique
    Private_lines = []
    Shared_lines = []
    Private_huge_lines = []
    Shared_huge_lines = []
    Pss_lines = []
    Rss = (int(proc.open(pid, 'statm').readline().split()[1])
           * PAGESIZE)
    Swap_lines = []
    Swap_pss_lines = []

    Swap = 0

    if os.path.exists(proc.path(pid, 'smaps')):  # stat
        smaps = 'smaps'
        if os.path.exists(proc.path(pid, 'smaps_rollup')):
            smaps = 'smaps_rollup' # faster to process
        lines = proc.open(pid, smaps).readlines()  # open
        # Note we checksum smaps as maps is usually but
        # not always different for separate processes.
        mem_id = hash(''.join(lines))
        for line in lines:
            # {Private,Shared}_Hugetlb is not included in Pss (why?)
            # so we need to account for separately.
            if line.startswith("Private_Hugetlb:"):
                Private_huge_lines.append(line)
            elif line.startswith("Shared_Hugetlb:"):
                Shared_huge_lines.append(line)
            elif line.startswith("Shared"):
                Shared_lines.append(line)
            elif line.startswith("Private"):
                Private_lines.append(line)
            elif line.startswith("Pss:"):
                have_pss = 1
                Pss_lines.append(line)
            elif line.startswith("Swap:"):
                Swap_lines.append(line)
            elif line.startswith("SwapPss:"):
                have_swap_pss = 1
                Swap_pss_lines.append(line)
        Shared = sum([int(line.split()[1]) for line in Shared_lines])
        Private = sum([int(line.split()[1]) for line in Private_lines])
        Shared_huge = sum([int(line.split()[1]) for line in Shared_huge_lines])
        Private_huge = sum([int(line.split()[1]) for line in Private_huge_lines])
        #Note Shared + Private = Rss above
        #The Rss in smaps includes video card mem etc.
        if have_pss:
            pss_adjust = 0.5 # add 0.5KiB as this avg error due to truncation
            Pss = sum([float(line.split()[1])+pss_adjust for line in Pss_lines])
            Shared = Pss - Private
        Private += Private_huge  # Add after as PSS doesn't a/c for huge pages
        if have_swap_pss:
            # The kernel supports SwapPss, that shows proportional swap share.
            # Note that Swap - SwapPss is not Private Swap.
            Swap = sum([int(line.split()[1]) for line in Swap_pss_lines])
        else:
            # Note that Swap = Private swap + Shared swap.
            Swap = sum([int(line.split()[1]) for line in Swap_lines])
    elif (2,6,1) <= kernel_ver() <= (2,6,9):
        Shared = 0 #lots of overestimation, but what can we do?
        Shared_huge = 0
        Private = Rss
    else:
        Shared = int(proc.open(pid, 'statm').readline().split()[2])
        Shared *= PAGESIZE
        Shared_huge = 0
        Private = Rss - Shared
    return (Private, Shared, Shared_huge, Swap, mem_id)


def getCmdName(pid, split_args, discriminate_by_pid, exe_only=False):
    cmdline = proc.open(pid, 'cmdline').read().split("\0")
    while cmdline[-1] == '' and len(cmdline) > 1:
        cmdline = cmdline[:-1]

    path = proc.path(pid, 'exe')
    try:
        path = os.readlink(path)
        # Some symlink targets were seen to contain NULs on RHEL 5 at least
        # https://github.com/pixelb/scripts/pull/10, so take string up to NUL
        path = path.split('\0')[0]
    except OSError:
        val = sys.exc_info()[1]
        if (val.errno == errno.ENOENT or # either kernel thread or process gone
            val.errno == errno.EPERM or
            val.errno == errno.EACCES):
            raise LookupError
        raise

    if split_args:
        return ' '.join(cmdline).replace('\n', ' ')
    if path.endswith(" (deleted)"):
        path = path[:-10]
        if os.path.exists(path):
            path += " [updated]"
        else:
            #The path could be have prelink stuff so try cmdline
            #which might have the full path present. This helped for:
            #/usr/libexec/notification-area-applet.#prelink#.fX7LCT (deleted)
            if os.path.exists(cmdline[0]):
                path = cmdline[0] + " [updated]"
            else:
                path += " [deleted]"
    exe = os.path.basename(path)
    if exe_only: return exe

    proc_status = proc.open(pid, 'status').readlines()
    cmd = proc_status[0][6:-1]
    if exe.startswith(cmd):
        cmd = exe #show non truncated version
        #Note because we show the non truncated name
        #one can have separated programs as follows:
        #584.0 KiB +   1.0 MiB =   1.6 MiB    mozilla-thunder (exe -> bash)
        # 56.0 MiB +  22.2 MiB =  78.2 MiB    mozilla-thunderbird-bin
    else:
        #Lookup the parent's exe and use that if matching
        #which will merge "Web Content" with "firefox" for example
        ppid = 0
        for l in range(10):
            ps_line = proc_status[l]
            if ps_line.startswith('PPid:'):
                ppid = int(ps_line[6:-1])
                break
        if ppid:
            try:
                p_exe = getCmdName(ppid, False, False, exe_only=True)
            except LookupError:
                pass
            else:
                if exe == p_exe:
                    cmd = exe
    if sys.version_info >= (3,):
        cmd = cmd.encode(errors='replace').decode()
    if discriminate_by_pid:
        cmd = '%s [%d]' % (cmd, pid)
    return cmd


#The following matches "du -h" output
#see also human.py
def human(num, power="Ki", units=None):
    if units is None:
        powers = ["Ki", "Mi", "Gi", "Ti"]
        while num >= 1000: #4 digits
            num /= 1024.0
            power = powers[powers.index(power)+1]
        return "%.1f %sB" % (num, power)
    else:
        return "%.f" % ((num * 1024) / units)


def cmd_with_count(cmd, count):
    if count > 1:
        return "%s (%u)" % (cmd, count)
    else:
        return cmd

#Warn of possible inaccuracies
#RAM:
#2 = accurate & can total
#1 = accurate only considering each process in isolation
#0 = some shared mem not reported
#-1= all shared mem not reported
#SWAP:
#2 = accurate & can total
#1 = accurate only considering each process in isolation
#-1= not available
def val_accuracy(show_swap):
    """http://wiki.apache.org/spamassassin/TopSharedMemoryBug"""
    kv = kernel_ver()
    pid = os.getpid()
    swap_accuracy = -1
    if kv[:2] == (2,4):
        if proc.open('meminfo').read().find("Inact_") == -1:
            return 1, swap_accuracy
        return 0, swap_accuracy
    elif kv[:2] == (2,6):
        if os.path.exists(proc.path(pid, 'smaps')):
            swap_accuracy = 1
            if proc.open(pid, 'smaps').read().find("Pss:")!=-1:
                return 2, swap_accuracy
            else:
                return 1, swap_accuracy
        if (2,6,1) <= kv <= (2,6,9):
            return -1, swap_accuracy
        return 0, swap_accuracy
    elif kv[0] > 2 and os.path.exists(proc.path(pid, 'smaps')):
        swap_accuracy = 1
        if show_swap and proc.open(pid, 'smaps').read().find("SwapPss:")!=-1:
            swap_accuracy = 2
        return 2, swap_accuracy
    else:
        return 1, swap_accuracy

def show_val_accuracy( ram_inacc, swap_inacc, only_total, show_swap ):
    level = ("Warning","Error")[only_total]

    # Only show significant warnings
    if not show_swap:
        swap_inacc = 2
    elif only_total:
        ram_inacc = 2

    if ram_inacc == -1:
        sys.stderr.write(
         "%s: Shared memory is not reported by this system.\n" % level
        )
        sys.stderr.write(
         "Values reported will be too large, and totals are not reported\n"
        )
    elif ram_inacc == 0:
        sys.stderr.write(
         "%s: Shared memory is not reported accurately by this system.\n" % level
        )
        sys.stderr.write(
         "Values reported could be too large, and totals are not reported\n"
        )
    elif ram_inacc == 1:
        sys.stderr.write(
         "%s: Shared memory is slightly over-estimated by this system\n"
         "for each program, so totals are not reported.\n" % level
        )

    if swap_inacc == -1:
        sys.stderr.write(
         "%s: Swap is not reported by this system.\n" % level
        )
    elif swap_inacc == 1:
        sys.stderr.write(
         "%s: Swap is over-estimated by this system for each program,\n"
         "so totals are not reported.\n" % level
        )

    sys.stderr.close()
    if only_total:
        if show_swap:
            accuracy = swap_inacc
        else:
            accuracy = ram_inacc
        if accuracy != 2:
            sys.exit(1)


def get_memory_usage(pids_to_show, split_args, discriminate_by_pid,
                     include_self=False, only_self=False):
    cmds = {}
    shareds = {}
    shared_huges = {}
    mem_ids = {}
    count = {}
    swaps = {}
    for pid in os.listdir(proc.path('')):
        if not pid.isdigit():
            continue
        pid = int(pid)

        # Some filters
        if only_self and pid != our_pid:
            continue
        if pid == our_pid and not include_self:
            continue
        if pids_to_show and pid not in pids_to_show:
            continue

        try:
            cmd = getCmdName(pid, split_args, discriminate_by_pid)
        except LookupError:
            #operation not permitted
            #kernel threads don't have exe links or
            #process gone
            continue

        try:
            private, shared, shared_huge, swap, mem_id = getMemStats(pid)
        except RuntimeError:
            continue #process gone
        if shareds.get(cmd):
            if have_pss: #add shared portion of PSS together
                shareds[cmd] += shared
            elif shareds[cmd] < shared: #just take largest shared val
                shareds[cmd] = shared
        else:
            shareds[cmd] = shared
        if shared_huges.get(cmd):
            if shared_huges[cmd] < shared_huge: #just take largest shared_huge
                shared_huges[cmd] = shared_huge
        else:
            shared_huges[cmd] = shared_huge
        cmds[cmd] = cmds.setdefault(cmd, 0) + private
        if cmd in count:
            count[cmd] += 1
        else:
            count[cmd] = 1
        mem_ids.setdefault(cmd, {}).update({mem_id: None})

        # Swap (overcounting for now...)
        swaps[cmd] = swaps.setdefault(cmd, 0) + swap

    # Total swaped mem for each program
    total_swap = 0

    # Add shared mem for each program
    total = 0

    for cmd in cmds:
        cmd_count = count[cmd]
        if len(mem_ids[cmd]) == 1 and cmd_count > 1:
            # Assume this program is using CLONE_VM without CLONE_THREAD
            # so only account for one of the processes
            cmds[cmd] /= cmd_count
            if have_pss:
                shareds[cmd] /= cmd_count
        # overestimation possible if shared_huges shared across commands
        shareds[cmd] += shared_huges[cmd]
        cmds[cmd] = cmds[cmd] + shareds[cmd]
        total += cmds[cmd]  # valid if PSS available
        total_swap += swaps[cmd]

    sorted_cmds = sorted(cmds.items(), key=lambda x:x[1])
    sorted_cmds = [x for x in sorted_cmds if x[1]]

    return sorted_cmds, shareds, count, total, swaps, total_swap

def print_header(show_swap, discriminate_by_pid):
    output_string = " Private  +   Shared  =  RAM used"
    if show_swap:
        output_string += "   Swap used"
    output_string += "\tProgram"
    if discriminate_by_pid:
        output_string += "[pid]"
    output_string += "\n\n"
    sys.stdout.write(output_string)


def print_memory_usage(sorted_cmds, shareds, count, total, swaps, total_swap,
                       show_swap):
    for cmd in sorted_cmds:

        output_string = "%9s + %9s = %9s"
        output_data = (human(cmd[1]-shareds[cmd[0]]),
                       human(shareds[cmd[0]]), human(cmd[1]))
        if show_swap:
            output_string += "   %9s"
            output_data += (human(swaps[cmd[0]]),)
        output_string += "\t%s\n"
        output_data += (cmd_with_count(cmd[0], count[cmd[0]]),)

        sys.stdout.write(output_string % output_data)

    # Only show totals if appropriate
    if have_swap_pss and show_swap:  # kernel will have_pss
        sys.stdout.write("%s\n%s%9s%s%9s\n%s\n" %
                         ("-" * 45, " " * 24, human(total), " " * 3,
                          human(total_swap), "=" * 45))
    elif have_pss:
        sys.stdout.write("%s\n%s%9s\n%s\n" %
                         ("-" * 33, " " * 24, human(total), "=" * 33))


def verify_environment(pids_to_show):
    if os.geteuid() != 0 and not pids_to_show:
        sys.stderr.write("Sorry, root permission required, or specify pids with -p\n")
        sys.stderr.close()
        sys.exit(1)

    try:
        kernel_ver()
    except (IOError, OSError):
        val = sys.exc_info()[1]
        if val.errno == errno.ENOENT:
            sys.stderr.write(
              "Couldn't access " + proc.path('') + "\n"
              "Only GNU/Linux and FreeBSD (with linprocfs) are supported\n")
            sys.exit(2)
        else:
            raise

def main():
    # Force the stdout and stderr streams to be unbuffered
    sys.stdout = Unbuffered(sys.stdout)
    sys.stderr = Unbuffered(sys.stderr)

    split_args, pids_to_show, watch, only_total, discriminate_by_pid, \
    show_swap = parse_options()

    verify_environment(pids_to_show)

    if not only_total:
        print_header(show_swap, discriminate_by_pid)

    if watch is not None:
        try:
            sorted_cmds = True
            while sorted_cmds:
                sorted_cmds, shareds, count, total, swaps, total_swap = \
                    get_memory_usage(pids_to_show, split_args,
                                     discriminate_by_pid)
                if only_total and show_swap and have_swap_pss:
                    sys.stdout.write(human(total_swap, units=1)+'\n')
                elif only_total and not show_swap and have_pss:
                    sys.stdout.write(human(total, units=1)+'\n')
                elif not only_total:
                    print_memory_usage(sorted_cmds, shareds, count, total,
                                       swaps, total_swap, show_swap)

                sys.stdout.flush()
                time.sleep(watch)
            else:
                sys.stdout.write('Process does not exist anymore.\n')
        except KeyboardInterrupt:
            pass
    else:
        # This is the default behavior
        sorted_cmds, shareds, count, total, swaps, total_swap = \
            get_memory_usage(pids_to_show, split_args,
                             discriminate_by_pid)
        if only_total and show_swap and have_swap_pss:
            sys.stdout.write(human(total_swap, units=1)+'\n')
        elif only_total and not show_swap and have_pss:
            sys.stdout.write(human(total, units=1)+'\n')
        elif not only_total:
            print_memory_usage(sorted_cmds, shareds, count, total, swaps,
                               total_swap, show_swap)

    # We must close explicitly, so that any EPIPE exception
    # is handled by our excepthook, rather than the default
    # one which is reenabled after this script finishes.
    sys.stdout.close()

    ram_accuracy, swap_accuracy = val_accuracy( show_swap )
    show_val_accuracy( ram_accuracy, swap_accuracy, only_total, show_swap )

if __name__ == '__main__': main()
