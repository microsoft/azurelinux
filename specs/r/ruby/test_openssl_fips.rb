require 'openssl'

# Run openssl tests in OpenSSL FIPS. See the link below for how to test.
# https://github.com/ruby/openssl/blob/master/.github/workflows/test.yml
# - step name: test on fips module

# Listing the testing files by an array explicitly rather than the `Dir.glob`
# to prevent the test files from not loading unintentionally.
TEST_FILES = %w[
  test/openssl/test_fips.rb
  test/openssl/test_pkey.rb
].freeze

if ARGV.empty?
  puts 'ERROR: Argument base_dir required.'
  puts "Usage: #{__FILE__} base_dir [options]"
  exit false
end
BASE_DIR = ARGV[0]
abs_test_files = TEST_FILES.map { |file| File.join(BASE_DIR, file) }

# Set Fedora/RHEL downstream OpenSSL downstream environment variable to enable
# FIPS module in non-FIPS OS environment. It is available in Fedora 38 or later
# versions.
# https://src.fedoraproject.org/rpms/openssl/blob/rawhide/f/0009-Add-Kernel-FIPS-mode-flag-support.patch
ENV['OPENSSL_FORCE_FIPS_MODE'] = '1'
# A flag to tell the tests the current environment is FIPS enabled.
# https://github.com/ruby/openssl/blob/master/test/openssl/test_fips.rb
ENV['TEST_RUBY_OPENSSL_FIPS_ENABLED'] = 'true'

abs_test_files.each do |file|
  puts "INFO: Loading #{file}."
  require file
end
