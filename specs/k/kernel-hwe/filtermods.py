#!/usr/bin/env python3
"""
filter kmods into groups for packaging, see filtermods.adoc
"""

import argparse
import os
import re
import subprocess
import sys
import yaml
import unittest

from logging import getLogger, DEBUG, INFO, WARN, ERROR, CRITICAL, NOTSET, FileHandler, StreamHandler, Formatter, Logger
from typing import Optional

log = getLogger('filtermods')


def get_td(filename):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(script_dir, 'filtermods-testdata', filename)


def run_command(cmd, cwddir=None):
    p = subprocess.Popen(cmd, cwd=cwddir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    out_str = out.decode('utf-8')
    err_str = err.decode('utf-8')
    return p.returncode, out_str, err_str


def safe_run_command(cmd, cwddir=None):
    log.info('%s', cmd)
    retcode, out, err = run_command(cmd, cwddir)
    if retcode != 0:
        log.warning('Command failed: %s, ret_code: %d', cmd, retcode)
        log.warning(out)
        log.warning(err)
        raise Exception(err)
    log.info('  ^^[OK]')
    return retcode, out, err


def setup_logging(log_filename, stdout_log_level):
    log_format = '%(asctime)s %(levelname)7.7s %(funcName)20.20s:%(lineno)4s %(message)s'
    log = getLogger('filtermods')
    log.setLevel(DEBUG)

    handler = StreamHandler(sys.stdout)
    formatter = Formatter(log_format, '%H:%M:%S')
    handler.setFormatter(formatter)
    handler.setLevel(stdout_log_level)
    log.addHandler(handler)
    log.debug('stdout logging on')

    if log_filename:
        file_handler = FileHandler(log_filename, 'w')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(DEBUG)
        log.addHandler(file_handler)
        log.info('file logging on: %s', log_filename)

    return log


def canon_modname(kmod_pathname: str) -> str:
    name = os.path.basename(kmod_pathname)
    if name.endswith('.xz'):
        name = name[:-3]
    return name


class HierarchyObject:
    def __init__(self):
        self.depends_on = set()


def get_topo_order(obj_list: list[HierarchyObject], func_get_linked_objs=lambda x: x.depends_on) -> list[HierarchyObject]:
    topo_order = []
    objs_to_sort = set(obj_list)
    objs_sorted = set()

    while len(objs_to_sort) > 0:
        no_deps = set()
        for obj in objs_to_sort:
            linked = func_get_linked_objs(obj)
            if not linked:
                no_deps.add(obj)
            else:
                all_deps_sorted = True
                for dep in linked:
                    if dep not in objs_sorted:
                        all_deps_sorted = False
                        break
                if all_deps_sorted:
                    no_deps.add(obj)

        for obj in no_deps:
            topo_order.append(obj)
            objs_sorted.add(obj)
            objs_to_sort.remove(obj)

    return topo_order


class KMod(HierarchyObject):
    def __init__(self, kmod_pathname: str) -> None:
        super(KMod, self).__init__()
        self.name: str = canon_modname(kmod_pathname)
        self.kmod_pathname: str = kmod_pathname
        self.is_dependency_for: set[KMod] = set()
        self.assigned_to_pkg: Optional[KModPackage] = None
        self.preferred_pkg: Optional[KModPackage] = None
        self.rule_specifity: int = 0
        self.allowed_list: Optional[set[KModPackage]] = None
        self.err = 0

    def __str__(self):
        depends_on = ''
        for kmod in self.depends_on:
            depends_on = depends_on + ' ' + kmod.name
        return '%s {%s}' % (self.name, depends_on)


class KModList():
    def __init__(self) -> None:
        self.name_to_kmod_map: dict[str, KMod] = {}
        self.topo_order: Optional[list[KMod]] = None

    def get(self, kmod_pathname, create_if_missing=False):
        kmod_name = canon_modname(kmod_pathname)
        if kmod_name in self.name_to_kmod_map:
            return self.name_to_kmod_map[kmod_name]
        if not create_if_missing:
            return None

        kmod = KMod(kmod_pathname)
        # log.debug('Adding kmod %s (%s) to list', kmod.name, kmod.kmod_pathname)
        if kmod.kmod_pathname != kmod_pathname:
            raise Exception('Already have %s, but path changed? %s', kmod_name, kmod_pathname)
        if not kmod.name:
            raise Exception('Each kmod needs a name')
        self.name_to_kmod_map[kmod_name] = kmod
        return kmod

    def process_depmod_line(self, line):
        tmp = line.split(':')
        if len(tmp) != 2:
            raise Exception('Depmod line has unexpected format: %s', line)
        kmod_pathname = tmp[0].strip()
        dependencies_pathnames = tmp[1].strip()
        kmod = self.get(kmod_pathname, create_if_missing=True)

        if dependencies_pathnames:
            for dep_pathname in dependencies_pathnames.split(' '):
                dep_kmod = self.get(dep_pathname, create_if_missing=True)
                kmod.depends_on.add(dep_kmod)
                dep_kmod.is_dependency_for.add(kmod)

    def load_depmod_file(self, filepath):
        with open(filepath) as f:
            lines = f.readlines()
            for line in lines:
                if not line or line.startswith('#'):
                    continue
                self.process_depmod_line(line)
        log.info('depmod %s loaded, number of kmods: %s', filepath, len(self.name_to_kmod_map))

    def dump(self):
        for kmod in self.name_to_kmod_map.values():
            print(kmod)

    def get_topo_order(self):
        if self.topo_order is None:
            self.topo_order = get_topo_order(self.name_to_kmod_map.values())
        # TODO: what if we add something after?
        return self.topo_order

    def get_alphabetical_order(self):
        kmods = list(self.name_to_kmod_map.values())
        kmods.sort(key=lambda k: k.kmod_pathname)
        return kmods

    def load_kmods_from_dir(self, topdir):
        ret = []
        for root, dirs, files in os.walk(topdir):
            for filename in files:
                if filename.endswith('.xz'):
                    filename = filename[:-3]
                if filename.endswith('.ko'):
                    kmod_pathname = os.path.join(root, filename)
                    ret.append(kmod_pathname)

        return ret

    def check_depmod_has_all_kmods(self, dirpath):
        ret = self.load_kmods_from_dir(dirpath)
        for kmod_pathname in ret:
            kmod = self.get(kmod_pathname)
            if not kmod:
                raise Exception('Could not find kmod %s in depmod', kmod_pathname)
        log.debug('OK: all (%s) kmods from %s are known', len(ret), dirpath)


class KModPackage(HierarchyObject):
    def _get_depends_on(pkg):
        return pkg.depends_on

    def _get_deps_for(pkg):
        return pkg.is_dependency_for

    def __init__(self, name: str, depends_on=[]) -> None:
        self.name: str = name
        self.depends_on: set[KModPackage] = set(depends_on)
        self.is_dependency_for: set[KModPackage] = set()

        for pkg in self.depends_on:
            pkg.is_dependency_for.add(self)
        self.all_depends_on_list: list[KModPackage] = self._get_all_linked(KModPackage._get_depends_on)
        self.all_depends_on: set[KModPackage] = set(self.all_depends_on_list)
        self.all_deps_for: Optional[set[KModPackage]] = None
        self.default = False
        log.debug('KModPackage created %s, depends_on: %s', name, [pkg.name for pkg in depends_on])

    def __repr__(self):
        return self.name

    def get_all_deps_for(self):
        if self.all_deps_for is None:
            self.all_deps_for = set(self._get_all_linked(KModPackage._get_deps_for))
        return self.all_deps_for

    def _get_all_linked(self, func_get_links):
        ret = []
        explore = func_get_links(self)

        while len(explore) > 0:
            new_explore = set()
            for pkg in explore:
                if pkg not in ret:
                    ret.append(pkg)
                    for dep in func_get_links(pkg):
                        new_explore.add(dep)
            explore = new_explore
        return ret


class KModPackageList(HierarchyObject):
    def __init__(self) -> None:
        self.name_to_obj: dict[str, KModPackage] = {}
        self.kmod_pkg_list: list[KModPackage] = []
        self.rules: list[tuple[str, str, str]] = []

    def get(self, pkgname):
        if pkgname in self.name_to_obj:
            return self.name_to_obj[pkgname]
        return None

    def add_kmod_pkg(self, pkg):
        self.name_to_obj[pkg.name] = pkg
        self.kmod_pkg_list.append(pkg)

    def __iter__(self):
        return iter(self.kmod_pkg_list)


def get_kmods_matching_re(kmod_list: KModList, param_re: str) -> list[KMod]:
    ret = []
    # first subdir can be anything - this is because during build everything
    # goes to kernel, but subpackages can move it (e.g. to extra)
    param_re = '[^/]+/' + param_re
    pattern = re.compile(param_re)

    for kmod in kmod_list.get_topo_order():
        m = pattern.match(kmod.kmod_pathname)
        if m:
            ret.append(kmod)
    return ret


def walk_kmod_chain(kmod, myfunc):
    visited = set()

    def visit_kmod(kmod, parent_kmod, func_to_call):
        func_to_call(kmod, parent_kmod)
        visited.add(kmod)
        for dep in kmod.depends_on:
            if dep not in visited:
                visit_kmod(dep, kmod, func_to_call)

    visit_kmod(kmod, None, myfunc)
    return visited


# is pkg a parent to any pkg from "alist"
def is_pkg_parent_to_any(pkg: KModPackage, alist: set[KModPackage]) -> bool:
    if pkg in alist:
        return True

    for some_pkg in alist:
        if some_pkg in pkg.all_depends_on:
            return True
    return False


# is pkg a child to any pkg from "alist"
def is_pkg_child_to_any(pkg: KModPackage, alist: set[KModPackage]) -> bool:
    if pkg in alist:
        return True

    for some_pkg in alist:
        if pkg in some_pkg.all_depends_on:
            return True
    return False


def update_allowed(kmod: KMod, visited: set[KMod], update_linked: bool = False) -> int:
    num_updated = 0
    init = False
    to_remove = set()

    if kmod in visited:
        return num_updated
    visited.add(kmod)

    # if we have nothing, try to initialise based on parents and children
    if kmod.allowed_list is None:
        init_allowed_list: set[KModPackage] = set()

        # init from children
        for kmod_dep in kmod.depends_on:
            if kmod_dep.allowed_list:
                init_allowed_list.update(kmod_dep.allowed_list)
                init = True

        if init:
            # also add any pkgs that pkgs from list could depend on
            deps_for = set()
            for pkg in init_allowed_list:
                deps_for.update(pkg.get_all_deps_for())
            init_allowed_list.update(deps_for)

        # init from parents
        if not init:
            for kmod_par in kmod.is_dependency_for:
                if kmod_par.allowed_list:
                    init_allowed_list.update(kmod_par.allowed_list)
                    # also add any pkgs that depend on pkgs from list
                    for pkg in kmod_par.allowed_list:
                        init_allowed_list.update(pkg.all_depends_on)
                        init = True

        if init:
            kmod.allowed_list = init_allowed_list
            log.debug('%s: init to %s', kmod.name, [x.name for x in kmod.allowed_list])

    kmod_allowed_list = kmod.allowed_list or set()
    # log.debug('%s: update to %s', kmod.name, [x.name for x in kmod_allowed_list])

    # each allowed is parent to at least one child allowed [for _all_ children]
    for pkg in kmod_allowed_list:
        for kmod_dep in kmod.depends_on:
            if kmod_dep.allowed_list is None or kmod_dep.err:
                continue
            if not is_pkg_parent_to_any(pkg, kmod_dep.allowed_list):
                to_remove.add(pkg)
                log.debug('%s: remove %s from allowed, child: %s [%s]',
                          kmod.name, [pkg.name], kmod_dep.name, [x.name for x in kmod_dep.allowed_list])

    # each allowed is child to at least one parent allowed [for _all_ parents]
    for pkg in kmod_allowed_list:
        for kmod_par in kmod.is_dependency_for:
            if kmod_par.allowed_list is None or kmod_par.err:
                continue

            if not is_pkg_child_to_any(pkg, kmod_par.allowed_list):
                to_remove.add(pkg)
                log.debug('%s: remove %s from allowed, parent: %s %s',
                          kmod.name, [pkg.name], kmod_par.name, [x.name for x in kmod_par.allowed_list])

    for pkg in to_remove:
        kmod_allowed_list.remove(pkg)
        num_updated = num_updated + 1
        if len(kmod_allowed_list) == 0:
            log.error('%s: cleared entire allow list', kmod.name)
            kmod.err = 1

    if init or to_remove or update_linked:
        if to_remove:
            log.debug('%s: updated to %s', kmod.name, [x.name for x in kmod_allowed_list])

        for kmod_dep in kmod.depends_on:
            num_updated = num_updated + update_allowed(kmod_dep, visited)

        for kmod_dep in kmod.is_dependency_for:
            num_updated = num_updated + update_allowed(kmod_dep, visited)

    return num_updated


def apply_initial_labels(pkg_list: KModPackageList, kmod_list: KModList, treat_default_as_wants=False):
    log.debug('')
    for cur_rule in ['needs', 'wants', 'default']:
        for package_name, rule_type, rule in pkg_list.rules:
            pkg_obj = pkg_list.get(package_name)

            if not pkg_obj:
                log.error('no package with name %s', package_name)

            if cur_rule != rule_type:
                continue

            if rule_type == 'default' and treat_default_as_wants:
                rule_type = 'wants'

            if 'needs' == rule_type:
                # kmod_matching is already in topo_order
                kmod_matching = get_kmods_matching_re(kmod_list, rule)
                for kmod in kmod_matching:
                    if kmod.assigned_to_pkg and kmod.assigned_to_pkg != pkg_obj:
                        log.error('%s: can not be required by 2 pkgs %s %s', kmod.name, kmod.assigned_to_pkg, pkg_obj.name)
                    else:
                        kmod.assigned_to_pkg = pkg_obj
                        kmod.allowed_list = set([pkg_obj])
                        kmod.rule_specifity = len(kmod_matching)
                        log.debug('%s: needed by %s', kmod.name, [pkg_obj.name])

            if 'wants' == rule_type:
                # kmod_matching is already in topo_order
                kmod_matching = get_kmods_matching_re(kmod_list, rule)
                for kmod in kmod_matching:
                    if kmod.allowed_list is None:
                        kmod.allowed_list = set(pkg_obj.all_depends_on)
                        kmod.allowed_list.add(pkg_obj)
                        kmod.preferred_pkg = pkg_obj
                        kmod.rule_specifity = len(kmod_matching)
                        log.debug('%s: wanted by %s, init allowed to %s', kmod.name, [pkg_obj.name], [pkg.name for pkg in kmod.allowed_list])
                    else:
                        if kmod.assigned_to_pkg:
                            log.debug('%s: ignoring wants by %s, already assigned to %s', kmod.name, pkg_obj.name, kmod.assigned_to_pkg.name)
                        else:
                            # rule specifity may not be good idea, so just log it
                            # e.g. .*test.* may not be more specific than arch/x86/.*
                            log.debug('already have wants for %s %s, new rule: %s', kmod.name, kmod.preferred_pkg, rule)

            if 'default' == rule_type:
                pkg_obj.default = True


def settle(kmod_list: KModList) -> None:
    kmod_topo_order = list(kmod_list.get_topo_order())

    for i in range(0, 25):
        log.debug('settle start %s', i)

        ret = 0
        for kmod in kmod_topo_order:
            visited: set[KMod] = set()
            ret = ret + update_allowed(kmod, visited)
        log.debug('settle %s updated nodes: %s', i, ret)

        if ret == 0:
            break

        kmod_topo_order.reverse()


# phase 1 - propagate initial labels
def propagate_labels_1(pkg_list: KModPackageList, kmod_list: KModList):
    log.info('')
    settle(kmod_list)


def pick_closest_to_preffered(preferred_pkg: KModPackage, allowed_set: set[KModPackage]):
    for child in preferred_pkg.all_depends_on_list:
        if child in allowed_set:
            return child
    return None


# phase 2 - if some kmods allow more than one pkg, pick wanted package
def propagate_labels_2(pkg_list: KModPackageList, kmod_list: KModList):
    log.info('')
    ret = 0
    for kmod in kmod_list.get_topo_order():
        update_linked = False

        if kmod.allowed_list is None and kmod.preferred_pkg:
            log.error('%s: has no allowed list but has preferred_pkg %s', kmod.name, kmod.preferred_pkg.name)
            kmod.err = 1

        if kmod.allowed_list and kmod.preferred_pkg:
            chosen_pkg = None
            if kmod.preferred_pkg in kmod.allowed_list:
                chosen_pkg = kmod.preferred_pkg
            else:
                chosen_pkg = pick_closest_to_preffered(kmod.preferred_pkg, kmod.allowed_list)

            if chosen_pkg is not None:
                kmod.allowed_list = set([chosen_pkg])
                log.debug('%s: making to prefer %s (preffered is %s), allowed: %s', kmod.name, chosen_pkg.name,
                          kmod.preferred_pkg.name, [pkg.name for pkg in kmod.allowed_list])
                update_linked = True

        visited: set[KMod] = set()
        ret = ret + update_allowed(kmod, visited, update_linked)

    log.debug('updated nodes: %s', ret)
    settle(kmod_list)


# Is this the best pick? ¯\_(ツ)_/¯
def pick_topmost_allowed(allowed_set: set[KModPackage]) -> KModPackage:
    topmost = next(iter(allowed_set))
    for pkg in allowed_set:
        if len(pkg.all_depends_on) > len(topmost.all_depends_on):
            topmost = pkg

    return topmost


# phase 3 - assign everything else that remained
def propagate_labels_3(pkg_list: KModPackageList, kmod_list: KModList):
    log.info('')
    ret = 0
    kmod_topo_order = list(kmod_list.get_topo_order())
    # do reverse topo order to cover children faster
    kmod_topo_order.reverse()

    default_pkg = None
    default_name = ''
    for pkg_obj in pkg_list:
        if pkg_obj.default:
            if default_pkg:
                log.error('Already have default pkg: %s / %s', default_pkg.name, pkg_obj.name)
            else:
                default_pkg = pkg_obj
                default_name = default_pkg.name

    for kmod in kmod_topo_order:
        update_linked = False
        chosen_pkg = None

        if kmod.allowed_list is None:
            if default_pkg:
                chosen_pkg = default_pkg
            else:
                log.error('%s not assigned and there is no default', kmod.name)
        elif len(kmod.allowed_list) > 1:
            if default_pkg:
                if default_pkg in kmod.allowed_list:
                    chosen_pkg = default_pkg
                else:
                    chosen_pkg = pick_closest_to_preffered(default_pkg, kmod.allowed_list)
                    if chosen_pkg:
                        log.debug('closest is %s', chosen_pkg.name)
            if not chosen_pkg:
                # multiple pkgs are allowed, but none is preferred or default
                chosen_pkg = pick_topmost_allowed(kmod.allowed_list)
                log.debug('topmost is %s', chosen_pkg.name)

        if chosen_pkg:
            kmod.allowed_list = set([chosen_pkg])
            log.debug('%s: making to prefer %s (default: %s)', kmod.name, [chosen_pkg.name], default_name)
            update_linked = True

        visited: set[KMod] = set()
        ret = ret + update_allowed(kmod, visited, update_linked)

    log.debug('updated nodes: %s', ret)
    settle(kmod_list)


def load_config(config_pathname: str, kmod_list: KModList, variants=[]):
    kmod_pkg_list = KModPackageList()

    with open(config_pathname, 'r') as file:
        yobj = yaml.safe_load(file)

    for pkg_dict in yobj['packages']:
        pkg_name = pkg_dict['name']
        depends_on = pkg_dict.get('depends-on', [])
        if_variant_in = pkg_dict.get('if_variant_in')

        if if_variant_in is not None:
            if not (set(variants) & set(if_variant_in)):
                log.debug('Skipping %s for variants %s', pkg_name, variants)
                continue

        pkg_dep_list = []
        for pkg_dep_name in depends_on:
            pkg_dep = kmod_pkg_list.get(pkg_dep_name)
            pkg_dep_list.append(pkg_dep)

        pkg_obj = kmod_pkg_list.get(pkg_name)
        if not pkg_obj:
            pkg_obj = KModPackage(pkg_name, pkg_dep_list)
            kmod_pkg_list.add_kmod_pkg(pkg_obj)
        else:
            log.error('package %s already exists?', pkg_name)

    rules_list = yobj.get('rules', [])
    for rule_dict in rules_list:
        if_variant_in = rule_dict.get('if_variant_in')
        exact_pkg = rule_dict.get('exact_pkg')

        for key, value in rule_dict.items():
            if key in ['if_variant_in', 'exact_pkg']:
                continue

            if if_variant_in is not None:
                if not (set(variants) & set(if_variant_in)):
                    continue

            rule = key
            package_name = value

            if not kmod_pkg_list.get(package_name):
                raise Exception('Unknown package ' + package_name)

            rule_type = 'wants'
            if exact_pkg is True:
                rule_type = 'needs'
            elif key == 'default':
                rule_type = 'default'
                rule = '.*'

            log.debug('found rule: %s', (package_name, rule_type, rule))
            kmod_pkg_list.rules.append((package_name, rule_type, rule))

    log.info('loaded config, rules: %s', len(kmod_pkg_list.rules))
    return kmod_pkg_list


def make_pictures(pkg_list: KModPackageList, kmod_list: KModList, filename: str, print_allowed=True):
    f = open(filename + '.dot', 'w')

    f.write('digraph {\n')
    f.write('node [style=filled fillcolor="#f8f8f8"]\n')
    f.write('  subgraph kmods {\n')
    f.write('  "Legend" [shape=note label="kmod name\\n{desired package}\\nresulting package(s)"]\n')

    for kmod in kmod_list.get_topo_order():
        pkg_name = ''
        attr = ''
        if kmod.assigned_to_pkg:
            attr = 'fillcolor="#eddad5" color="#b22800"'
            pkg_name = kmod.assigned_to_pkg.name + "!"
        if kmod.preferred_pkg:
            attr = 'fillcolor="#ddddf5" color="#b268fe"'
            pkg_name = kmod.preferred_pkg.name + "?"
        allowed = ''
        if kmod.allowed_list and print_allowed:
            allowed = '=' + ' '.join([pkg.name for pkg in kmod.allowed_list])
        f.write(' "%s" [label="%s\\n%s\\n%s" shape=box %s] \n' % (kmod.name, kmod.name, pkg_name, allowed, attr))

    for kmod in kmod_list.get_topo_order():
        for kmod_dep in kmod.depends_on:
            f.write('    "%s" -> "%s";\n' % (kmod.name, kmod_dep.name))
    f.write('  }\n')

    f.write('  subgraph packages {\n')
    for pkg in pkg_list:
        desc = ''
        if pkg.default:
            desc = '/default'
        f.write(' "%s" [label="%s\\n%s"] \n' % (pkg.name, pkg.name, desc))
        for pkg_dep in pkg.depends_on:
            f.write('    "%s" -> "%s";\n' % (pkg.name, pkg_dep.name))
    f.write('  }\n')
    f.write('}\n')

    f.close()

    # safe_run_command('dot -Tpng -Gdpi=150 %s.dot > %s.png' % (filename, filename))
    safe_run_command('dot -Tsvg %s.dot > %s.svg' % (filename, filename))


def sort_kmods(depmod_pathname: str, config_str: str, variants=[], do_pictures=''):
    log.info('%s %s', depmod_pathname, config_str)
    kmod_list = KModList()
    kmod_list.load_depmod_file(depmod_pathname)

    pkg_list = load_config(config_str, kmod_list, variants)

    basename = os.path.splitext(config_str)[0]

    apply_initial_labels(pkg_list, kmod_list)
    if '0' in do_pictures:
        make_pictures(pkg_list, kmod_list, basename + "_0", print_allowed=False)

    try:

        propagate_labels_1(pkg_list, kmod_list)
        if '1' in do_pictures:
            make_pictures(pkg_list, kmod_list, basename + "_1")
        propagate_labels_2(pkg_list, kmod_list)
        propagate_labels_3(pkg_list, kmod_list)
    finally:
        if 'f' in do_pictures:
            make_pictures(pkg_list, kmod_list, basename + "_f")

    return pkg_list, kmod_list


def abbrev_list_for_report(alist: list[KMod]) -> str:
    tmp_str = []
    for kmod in alist:
        if kmod.allowed_list:
            tmp_str.append('%s(%s)' % (kmod.name, ' '.join([x.name for x in kmod.allowed_list])))
    ret = ', '.join(tmp_str)
    return ret


def print_report(pkg_list: KModPackageList, kmod_list: KModList):
    log.info('*'*26 + ' REPORT ' + '*'*26)

    kmods_err = 0
    kmods_moved = 0
    kmods_good = 0
    for kmod in kmod_list.get_topo_order():
        if not kmod.allowed_list:
            log.error('%s: not assigned to any package! Please check the full log for details', kmod.name)
            kmods_err = kmods_err + 1
            continue

        if len(kmod.allowed_list) > 1:
            log.error('%s: assigned to more than one package! Please check the full log for details', kmod.name)
            kmods_err = kmods_err + 1
            continue

        if not kmod.preferred_pkg:
            # config doesn't care where it ended up
            kmods_good = kmods_good + 1
            continue

        if kmod.preferred_pkg in kmod.allowed_list:
            # it ended up where it needs to be
            kmods_good = kmods_good + 1
            continue

        bad_parent_list = []
        for kmod_parent in kmod.is_dependency_for:
            if not is_pkg_child_to_any(kmod.preferred_pkg, kmod_parent.allowed_list):
                bad_parent_list.append(kmod_parent)

        bad_child_list = []
        for kmod_child in kmod.depends_on:
            if not is_pkg_parent_to_any(kmod.preferred_pkg, kmod_child.allowed_list):
                bad_child_list.append(kmod_parent)

        log.info('%s: wanted by %s but ended up in %s', kmod.name, [kmod.preferred_pkg.name], [pkg.name for pkg in kmod.allowed_list])
        if bad_parent_list:
            log.info('\thas conflicting parent: %s', abbrev_list_for_report(bad_parent_list))
        if bad_child_list:
            log.info('\thas conflicting children: %s', abbrev_list_for_report(bad_child_list))

        kmods_moved = kmods_moved + 1

    log.info('No. of kmod(s) assigned to preferred package: %s', kmods_good)
    log.info('No. of kmod(s) moved to a related package: %s', kmods_moved)
    log.info('No. of kmod(s) which could not be assigned: %s', kmods_err)
    log.info('*'*60)

    return kmods_err


def write_modules_lists(path_prefix: str, pkg_list: KModPackageList, kmod_list: KModList):
    kmod_list_alphabetical = sorted(kmod_list.get_topo_order(), key=lambda x: x.kmod_pathname)
    for pkg in pkg_list:
        output_path = os.path.join(path_prefix, pkg.name + '.list')
        i = 0
        with open(output_path, "w") as file:
            for kmod in kmod_list_alphabetical:
                if kmod.allowed_list and pkg in kmod.allowed_list:
                    file.write(kmod.kmod_pathname)
                    file.write('\n')
                    i = i + 1
        log.info('Module list %s created with %s kmods', output_path, i)


class FiltermodTests(unittest.TestCase):
    do_pictures = ''

    def setUp(self):
        self.pkg_list = None
        self.kmod_list = None

    def _is_kmod_pkg(self, kmodname, pkgnames):
        self.assertIsNotNone(self.pkg_list)
        self.assertIsNotNone(self.kmod_list)

        if type(pkgnames) is str:
            pkgnames = [pkgnames]

        expected_pkgs = []
        for pkgname in pkgnames:
            pkg = self.pkg_list.get(pkgname)
            self.assertIsNotNone(pkg)
            expected_pkgs.append(pkg)

        kmod = self.kmod_list.get(kmodname)
        self.assertIsNotNone(kmod)

        if expected_pkgs:
            self.assertTrue(len(kmod.allowed_list) == 1)
            self.assertIn(next(iter(kmod.allowed_list)), expected_pkgs)
        else:
            self.assertEqual(kmod.allowed_list, set())

    def test1a(self):
        self.pkg_list, self.kmod_list = sort_kmods(get_td('test1.dep'), get_td('test1.yaml'),
                                                   do_pictures=FiltermodTests.do_pictures)

        self._is_kmod_pkg('kmod1', 'modules-core')
        self._is_kmod_pkg('kmod2', 'modules-core')
        self._is_kmod_pkg('kmod3', 'modules')
        self._is_kmod_pkg('kmod4', 'modules')

    def test1b(self):
        self.pkg_list, self.kmod_list = sort_kmods(get_td('test1.dep'), get_td('test1.yaml'),
                                                   do_pictures=FiltermodTests.do_pictures,
                                                   variants=['rt'])

        self.assertIsNotNone(self.pkg_list.get('modules-other'))
        self._is_kmod_pkg('kmod1', 'modules-core')
        self._is_kmod_pkg('kmod2', 'modules-core')
        self._is_kmod_pkg('kmod3', 'modules')
        self._is_kmod_pkg('kmod4', 'modules-other')


    def test2(self):
        self.pkg_list, self.kmod_list = sort_kmods(get_td('test2.dep'), get_td('test2.yaml'),
                                                   do_pictures=FiltermodTests.do_pictures)

        self._is_kmod_pkg('kmod1', 'modules-extra')
        self._is_kmod_pkg('kmod2', 'modules')
        self._is_kmod_pkg('kmod3', 'modules-core')
        self._is_kmod_pkg('kmod4', 'modules-core')
        self._is_kmod_pkg('kmod5', 'modules-core')
        self._is_kmod_pkg('kmod6', 'modules-extra')
        self._is_kmod_pkg('kmod8', 'modules')

    def test3(self):
        self.pkg_list, self.kmod_list = sort_kmods(get_td('test3.dep'), get_td('test3.yaml'),
                                                   do_pictures=FiltermodTests.do_pictures)

        self._is_kmod_pkg('kmod2', ['modules-core', 'modules'])
        self._is_kmod_pkg('kmod4', ['modules-core', 'modules-extra'])
        self._is_kmod_pkg('kmod5', 'modules-core')
        self._is_kmod_pkg('kmod6', 'modules-core')

    def test4(self):
        self.pkg_list, self.kmod_list = sort_kmods(get_td('test4.dep'), get_td('test4.yaml'),
                                                   do_pictures=FiltermodTests.do_pictures)

        self._is_kmod_pkg('kmod0', 'modules')
        self._is_kmod_pkg('kmod1', 'modules')
        self._is_kmod_pkg('kmod2', 'modules')
        self._is_kmod_pkg('kmod3', 'modules')
        self._is_kmod_pkg('kmod4', 'modules')
        self._is_kmod_pkg('kmod5', 'modules')
        self._is_kmod_pkg('kmod6', 'modules')
        self._is_kmod_pkg('kmod7', 'modules-partner2')
        self._is_kmod_pkg('kmod8', 'modules-partner')
        self._is_kmod_pkg('kmod9', 'modules-partner')

    def _check_preffered_pkg(self, kmodname, pkgname):
        kmod = self.kmod_list.get(kmodname)
        self.assertIsNotNone(kmod)
        self.assertEqual(kmod.preferred_pkg.name, pkgname)

    def test5(self):
        self.pkg_list, self.kmod_list = sort_kmods(get_td('test5.dep'), get_td('test5.yaml'),
                                                   do_pictures=FiltermodTests.do_pictures)

        self._check_preffered_pkg('kmod2', 'modules')
        self._check_preffered_pkg('kmod3', 'modules-partner')
        self._check_preffered_pkg('kmod4', 'modules-partner')

    def test6(self):
        self.pkg_list, self.kmod_list = sort_kmods(get_td('test6.dep'), get_td('test6.yaml'),
                                                   do_pictures=FiltermodTests.do_pictures)

        self._is_kmod_pkg('kmod2', 'modules-core')
        self._is_kmod_pkg('kmod3', 'modules')
        self._is_kmod_pkg('kmod4', 'modules')
        self._is_kmod_pkg('kmod1', [])

    def test7(self):
        self.pkg_list, self.kmod_list = sort_kmods(get_td('test7.dep'), get_td('test7.yaml'),
                                                   do_pictures=FiltermodTests.do_pictures)

        self._is_kmod_pkg('kmod1', 'modules-core')
        self._is_kmod_pkg('kmod2', 'modules-core')
        self._is_kmod_pkg('kmod3', 'modules-other')
        self._is_kmod_pkg('kmod4', 'modules')


def do_rpm_mapping_test(config_pathname, kmod_rpms):
    kmod_dict = {}

    def get_kmods_matching_re(pkgname, param_re):
        matched = []
        param_re = '^kernel/' + param_re
        pattern = re.compile(param_re)

        for kmod_pathname, kmod_rec in kmod_dict.items():
            m = pattern.match(kmod_pathname)
            if m:
                matched.append(kmod_pathname)

        return matched

    for kmod_rpm in kmod_rpms.split():
        filename = os.path.basename(kmod_rpm)

        m = re.match(r'.*-modules-([^-]+)', filename)
        if not m:
            raise Exception('Unrecognized rpm ' + kmod_rpm + ', expected a kernel-modules* rpm')
        pkgname = 'modules-' + m.group(1)
        m = re.match(r'modules-([0-9.]+)', pkgname)
        if m:
            pkgname = 'modules'

        tmpdir = os.path.join('tmp.filtermods', filename, pkgname)
        if not os.path.exists(tmpdir):
            log.info('creating tmp dir %s', tmpdir)
            os.makedirs(tmpdir)
            safe_run_command('rpm2cpio %s | cpio -id' % (os.path.abspath(kmod_rpm)), cwddir=tmpdir)
        else:
            log.info('using cached content of tmp dir: %s', tmpdir)

        for path, subdirs, files in os.walk(tmpdir):
            for name in files:
                ret = re.match(r'.*/'+pkgname+'/lib/modules/[^/]+/[^/]+/(.*)', os.path.join(path, name))
                if not ret:
                    continue

                kmod_pathname = 'kernel/' + ret.group(1)
                if not kmod_pathname.endswith('.xz') and not kmod_pathname.endswith('.ko'):
                    continue
                if kmod_pathname in kmod_dict:
                    if pkgname not in kmod_dict[kmod_pathname]['target_pkgs']:
                        kmod_dict[kmod_pathname]['target_pkgs'].append(pkgname)
                else:
                    kmod_dict[kmod_pathname] = {}
                    kmod_dict[kmod_pathname]['target_pkgs'] = [pkgname]
                    kmod_dict[kmod_pathname]['pkg'] = None
                    kmod_dict[kmod_pathname]['matched'] = False

    kmod_pkg_list = load_config(config_pathname, None)

    for package_name, rule_type, rule in kmod_pkg_list.rules:
        kmod_names = get_kmods_matching_re(package_name, rule)

        for kmod_pathname in kmod_names:
            kmod_rec = kmod_dict[kmod_pathname]

            if not kmod_rec['matched']:
                kmod_rec['matched'] = True
                kmod_rec['pkg'] = package_name
    for kmod_pathname, kmod_rec in kmod_dict.items():
        if kmod_rec['pkg'] not in kmod_rec['target_pkgs']:
            log.warning('kmod %s wanted by config in %s, in tree it is: %s', kmod_pathname, [kmod_rec['pkg']], kmod_rec['target_pkgs'])
        elif len(kmod_rec['target_pkgs']) > 1:
            # if set(kmod_rec['target_pkgs']) != set(['modules', 'modules-core']):
            log.warning('kmod %s multiple matches in tree: %s/%s', kmod_pathname, [kmod_rec['pkg']], kmod_rec['target_pkgs'])


def cmd_sort(options):
    do_pictures = ''
    if options.graphviz:
        do_pictures = '0f'

    pkg_list, kmod_list = sort_kmods(options.depmod, options.config,
                                     options.variants, do_pictures)
    ret = print_report(pkg_list, kmod_list)
    if options.output:
        write_modules_lists(options.output, pkg_list, kmod_list)

    return ret


def cmd_print_rule_map(options):
    kmod_list = KModList()
    kmod_list.load_depmod_file(options.depmod)
    pkg_list = load_config(options.config, kmod_list, options.variants)
    apply_initial_labels(pkg_list, kmod_list, treat_default_as_wants=True)

    for kmod in kmod_list.get_alphabetical_order():
        print('%-20s %s' % (kmod.preferred_pkg, kmod.kmod_pathname))


def cmd_selftest(options):
    if options.graphviz:
        FiltermodTests.do_pictures = '0f'

    for arg in ['selftest', '-g', '--graphviz']:
        if arg in sys.argv:
            sys.argv.remove(arg)

    unittest.main()
    sys.exit(0)


def cmd_cmp2rpm(options):
    do_rpm_mapping_test(options.config, options.kmod_rpms)


def main():
    global log

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', dest='verbose',
                        help='be more verbose', action='count', default=4)
    parser.add_argument('-q', '--quiet', dest='quiet',
                        help='be more quiet', action='count', default=0)
    parser.add_argument('-l', '--log-filename', dest='log_filename',
                        help='log filename', default='filtermods.log')

    subparsers = parser.add_subparsers(dest='cmd')

    def add_graphviz_arg(p):
        p.add_argument('-g', '--graphviz', dest='graphviz',
                       help='generate graphviz visualizations',
                       action='store_true', default=False)

    def add_config_arg(p):
        p.add_argument('-c', '--config', dest='config', required=True,
                       help='path to yaml config with rules')

    def add_depmod_arg(p):
        p.add_argument('-d', '--depmod', dest='depmod', required=True,
                       help='path to modules.dep file')

    def add_output_arg(p):
        p.add_argument('-o', '--output', dest='output', default=None,
                       help='output $module_name.list files to directory specified by this parameter')

    def add_variants_arg(p):
        p.add_argument('-r', '--variants', dest='variants', action='append', default=[],
                       help='variants to enable in config')

    def add_kmod_rpms_arg(p):
        p.add_argument('-k', '--kmod-rpms', dest='kmod_rpms', required=True,
                       help='compare content of specified rpm(s) against yaml config rules')

    parser_sort = subparsers.add_parser('sort', help='assign kmods specified by modules.dep using rules from yaml config')
    add_config_arg(parser_sort)
    add_depmod_arg(parser_sort)
    add_output_arg(parser_sort)
    add_variants_arg(parser_sort)
    add_graphviz_arg(parser_sort)

    parser_rule_map = subparsers.add_parser('rulemap', help='print how yaml config maps to kmods')
    add_config_arg(parser_rule_map)
    add_depmod_arg(parser_rule_map)
    add_variants_arg(parser_rule_map)

    parser_test = subparsers.add_parser('selftest', help='runs a self-test')
    add_graphviz_arg(parser_test)

    parser_cmp2rpm = subparsers.add_parser('cmp2rpm', help='compare ruleset against RPM(s)')
    add_config_arg(parser_cmp2rpm)
    add_kmod_rpms_arg(parser_cmp2rpm)

    options = parser.parse_args()

    if options.cmd == "selftest":
        options.verbose = options.verbose - 2
    options.verbose = max(options.verbose - options.quiet, 0)
    levels = [NOTSET, CRITICAL, ERROR, WARN, INFO, DEBUG]
    stdout_log_level = levels[min(options.verbose, len(levels) - 1)]

    log = setup_logging(options.log_filename, stdout_log_level)

    ret = 0
    if options.cmd == "sort":
        ret = cmd_sort(options)
    elif options.cmd == "rulemap":
        cmd_print_rule_map(options)
    elif options.cmd == "selftest":
        cmd_selftest(options)
    elif options.cmd == "cmp2rpm":
        cmd_cmp2rpm(options)
    else:
        parser.print_help()

    return ret


if __name__ == '__main__':
    # import profile
    # profile.run('main()', sort=1)
    sys.exit(main())
