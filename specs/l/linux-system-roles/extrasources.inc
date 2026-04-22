# Sources and related tags that are used only on RHEL and not on Fedora
# They are in a separate file that differs between RHEL and Fedora
# in order to avoid conditional Sources in the main spec file

# All uses of them in the main spec file must be wrapped in
# %%if 0%%{?rhel} ... %%endif
