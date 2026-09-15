# frozen_string_literal: true

require 'facter'
require 'facter/resolvers/os_release'
require 'facter/facts/rhel/os/name'

resolver = Facter::Resolvers::OsRelease
file_helper = Facter::Util::FileHelper
original_readlines = file_helper.method(:safe_readlines)

expected_names = {
  'Azure Linux' => 'AzureLinux',
  'Microsoft Azure Linux' => 'AzureLinux',
  'Red Hat Enterprise Linux' => 'RedHat',
  'Oracle Linux Server' => 'OracleLinux',
  'Fedora Linux' => 'Fedora',
  'CBL-Mariner' => 'CBL-Mariner'
}

begin
  expected_names.each do |os_name, expected|
    file_helper.define_singleton_method(:safe_readlines) do |path, *args|
      if path == '/etc/os-release'
        ["NAME=\"#{os_name}\"\n", "VERSION_ID=\"4.0\"\n"]
      else
        original_readlines.call(path, *args)
      end
    end
    resolver.invalidate_cache

    actual = Facts::Rhel::Os::Name.new.call_the_resolver.to_h { |fact| [fact.name, fact.value] }
    expected_facts = { 'os.name' => expected, 'operatingsystem' => expected }
    raise "#{os_name}: expected #{expected_facts.inspect}, got #{actual.inspect}" unless actual == expected_facts

    release = resolver.resolve(:version_id)
    raise "#{os_name}: expected release 4.0, got #{release.inspect}" unless release == '4.0'

    puts "#{os_name}: os.name and operatingsystem are #{expected}"
  end
ensure
  file_helper.define_singleton_method(:safe_readlines, original_readlines)
  resolver.invalidate_cache
end
