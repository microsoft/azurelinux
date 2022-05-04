%ruby_libdir %{_libdir}/%{name}
%ruby_libarchdir %{_libdir}/%{name}

# This is the local lib/arch and should not be used for packaging.
%ruby_sitedir site_ruby
%ruby_sitelibdir %{_prefix}/local/share/%{name}/%{ruby_sitedir}
%ruby_sitearchdir %{_prefix}/local/%{_lib}/%{name}/%{ruby_sitedir}

# This is the general location for libs/archs compatible with all
# or most of the Ruby versions available in the Fedora repositories.
%ruby_vendordir vendor_ruby
%ruby_vendorlibdir %(ruby -rrbconfig -e "puts RbConfig::CONFIG['vendorlibdir']")
%ruby_vendorarchdir %(ruby -rrbconfig -e "puts RbConfig::CONFIG['vendorarchdir']")

# For ruby packages we want to filter out any provides caused by private
# libs in %%{ruby_vendorarchdir}/%%{ruby_sitearchdir}.
#
# Note that this must be invoked in the spec file, preferably as
# "%{?ruby_default_filter}", before any %description block.
%ruby_default_filter %{expand: \
%global __provides_exclude_from %{?__provides_exclude_from:%{__provides_exclude_from}|}^(%{ruby_vendorarchdir}|%{ruby_sitearchdir})/.*\\\\.so$ \
}
