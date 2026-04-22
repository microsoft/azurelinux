require 'tmpdir'
require 'tempfile'
require 'fileutils'
# Available in Ruby upstream sources under tool/lib/envutil.rb
# Required for finding and setting up the built ruby binary.
require 'envutil'

module RPMTestHelper
  def setup
    @tmpdir = Dir.mktmpdir
    @tempfiles = []
  end

  def teardown
    @tempfiles.each do |file|
      file.close
      file.unlink
    end

    FileUtils.rmtree(@tmpdir)
  end

  GENERATOR_SCRIPT = ENV['GENERATOR_SCRIPT'].clone.freeze
  if GENERATOR_SCRIPT.nil? || GENERATOR_SCRIPT == ''
    raise "GENERATOR_SCRIPT is not specified." \
      "Specify the ENV variable with absolute path to the generator."
  end

  Dependency = Struct.new('Dependency', :name, :requirements) do
    def to_rpm_str
      "rubygem(#{self.name})"
    end
  end

  def make_gemspec(gem_info)
    file = Tempfile.new('req_gemspec', @tmpdir)
    # Fake gemspec with enough to pass most checks
    # Rubygems uses to validate the format.
    gemspec_contents = <<~EOF
      # -*- encoding: utf-8 -*-
      # stub: #{gem_info.name} #{gem_info.version} ruby lib

      Gem::Specification.new do |s|
        s.name = "#{gem_info.name}".freeze
        s.version = "#{gem_info.version}"

        s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
        s.require_paths = ["lib".freeze]
        s.authors = ["John Doe".freeze]
        s.bindir = "bin".freeze
        s.date = "2023-12-15"
        s.description = "Fake gemspec helper for testing Rubygem Generators".freeze
        s.email = ["example@example.com".freeze]
        s.files = ["LICENSE.txt".freeze, "lib/#{gem_info.name}.rb".freeze, "#{gem_info.name}.gemspec".freeze]
        s.homepage = "https://pkgs.fedoraproject.org/rpms/ruby".freeze
        s.licenses = ["MIT".freeze]
        s.required_ruby_version = Gem::Requirement.new(">= 2.5.0".freeze)
        s.rubygems_version = "3.3.5".freeze
        s.summary = "Fake gemspec for testing Rubygem Generators".freeze

        if s.respond_to? :specification_version then
          s.specification_version = 4
        end

        if s.respond_to? :add_runtime_dependency then
          #{gem_info.gemspec_runtime_dep_str}
        else
          #{gem_info.gemspec_dep_str}
        end
      end
    EOF

    file.write gemspec_contents
    file.rewind
    @tempfiles << file
    file
  end

  # Caller is expected to close subprocess stdin via #close_write
  # in order to let subprocess proceed if the process is reading
  # from STDIN in a loop.
  def rb_subprocess(*args)
    args = [GENERATOR_SCRIPT] if args.empty?
    ruby = EnvUtil.rubybin
    f = IO.popen([ruby] + args, 'r+') #, external_encoding: external_encoding)
    yield(f)
  ensure
    f.close unless !f || f.closed?
  end

  def run_generator_single_file(gem_info)
    lines = []
    gemspec_f = make_gemspec(gem_info)

    rb_subprocess do |io|
      io.write gemspec_f.path
      io.close_write
      lines = io.readlines
    end

    lines
  end

  def helper_rubygems_dependency
    "ruby(rubygems)"
  end

  class GemInfo
    attr_accessor :name, :version, :dependencies

    def initialize(name: 'foo', version: '1.2.3', dependencies: [])
      @name = name
      @version = version
      @dependencies = dependencies
    end

    def dependencies=(other)
      raise ArgumentError, "#{self.class.name}##{__method__.to_s}: Expected array of `Dependency' elements" \
        unless other.is_a?(Array) && other.all? { |elem| elem.respond_to?(:name) && elem.respond_to?(:requirements) }

      @dependencies = other
    end

    def to_rpm_str
      "rubygem(#{self.name})"
    end

    def gemspec_dep_str
      return '' if self.dependencies.nil? || self.dependencies.empty?
      @dependencies.inject("") do |memo, dep|
        memo += if dep.requirements && !dep.requirements.empty?
                  %Q|s.add_dependency(%q<#{dep.name}>.freeze, #{handle_dep_requirements(dep.requirements)})|
                else
                  %Q|s.add_dependency(%q<#{dep.name}>.freeze)|
                end

        memo += "\n"
      end
    end

    def gemspec_runtime_dep_str
      return '' if self.dependencies.nil? || self.dependencies.empty?

      @dependencies.inject("") do |memo, dep|
        memo += if dep.requirements && !dep.requirements.empty?
                  %Q|s.add_runtime_dependency(%q<#{dep.name}>.freeze, #{handle_dep_requirements(dep.requirements)})|
                else
                  %Q|s.add_runtime_dependency(%q<#{dep.name}>.freeze)|
                end

        memo += "\n"
      end
    end

    private

    def handle_dep_requirements(reqs)
      raise ArgumentError, "#{self.class.name}##{__method__.to_s}: Reqs must be an array." \
        unless reqs.is_a? Array
      raise ArgumentError, "#{self.class.name}##{__method__.to_s}: Reqs must not be empty for this method." \
        if reqs.empty?

      '[ "' + reqs.join('", "') + '" ]'
    end
  end
end
