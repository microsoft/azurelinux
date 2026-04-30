# kmod-macros.inc — Framework for building kmod subpackages alongside the kernel
#
# Usage in kernel.spec (injected via comp.toml overlays):
#   %include %%{_sourcedir}/kmod-macros.inc    (in preamble, after genspec vars)
#
# Then at each phase point, the overlay injects:
#   %%global _kmod_phase <phase>
#   %%include %%{_sourcedir}/kmod-<name>.inc
#
# Each kmod .inc file uses %%if "%%{_kmod_phase}" == "<phase>" guards to
# activate only the relevant section for that phase.
#
# To add a new kmod: create kmod-<name>.inc, add overlays to register its
# sources and inject %%include lines at each phase point.
# To remove: delete those overlays.
#

# Master list of kmod subpackages (informational — used by .inc files if needed)
%global kmod_subpackages nvidia-open
