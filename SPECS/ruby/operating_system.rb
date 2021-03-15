module Gem
  class << self

    ##
    # Returns full path of previous but one directory of dir in path
    # E.g. for '/usr/share/ruby', 'ruby', it returns '/usr'

    def previous_but_one_dir_to(path, dir)
      return unless path

      split_path = path.split(File::SEPARATOR)
      File.join(split_path.take_while { |one_dir| one_dir !~ /^#{dir}$/ }[0..-2])
    end
    private :previous_but_one_dir_to

    ##
    # Detects --install-dir option specified on command line.

    def opt_install_dir?
      @opt_install_dir ||= ARGV.include?('--install-dir') || ARGV.include?('-i')
    end
    private :opt_install_dir?

    ##
    # Detects --build-root option specified on command line.

    def opt_build_root?
      @opt_build_root ||= ARGV.include?('--build-root')
    end
    private :opt_build_root?

    ##
    # Tries to detect, if arguments and environment variables suggest that
    # 'gem install' is executed from rpmbuild.

    def rpmbuild?
      @rpmbuild ||= ENV['RPM_PACKAGE_NAME'] && (opt_install_dir? || opt_build_root?)
    end
    private :rpmbuild?

    ##
    # Default gems locations allowed on FHS system (/usr, /usr/share).
    # The locations are derived from directories specified during build
    # configuration.

    def default_locations
      @default_locations ||= {
        :system => previous_but_one_dir_to(RbConfig::CONFIG['vendordir'], RbConfig::CONFIG['RUBY_INSTALL_NAME']),
        :local => previous_but_one_dir_to(RbConfig::CONFIG['sitedir'], RbConfig::CONFIG['RUBY_INSTALL_NAME'])
      }
    end

    ##
    # For each location provides set of directories for binaries (:bin_dir)
    # platform independent (:gem_dir) and dependent (:ext_dir) files.

    def default_dirs
      @libdir ||= case RUBY_PLATFORM
      when 'java'
        RbConfig::CONFIG['datadir']
      else
        RbConfig::CONFIG['libdir']
      end

      @default_dirs ||= default_locations.inject(Hash.new) do |hash, location|
        destination, path = location

        hash[destination] = if path
          {
            :bin_dir => File.join(path, RbConfig::CONFIG['bindir'].split(File::SEPARATOR).last),
            :gem_dir => File.join(path, RbConfig::CONFIG['datadir'].split(File::SEPARATOR).last, 'gems'),
            :ext_dir => File.join(path, @libdir.split(File::SEPARATOR).last, 'gems')
          }
        else
          {
            :bin_dir => '',
            :gem_dir => '',
            :ext_dir => ''
          }
        end

        hash
      end
    end

    ##
    # Remove methods we are going to override. This avoids "method redefined;"
    # warnings otherwise issued by Ruby.

    remove_method :operating_system_defaults if method_defined? :operating_system_defaults
    remove_method :default_dir if method_defined? :default_dir
    remove_method :default_path if method_defined? :default_path
    remove_method :default_ext_dir_for if method_defined? :default_ext_dir_for

    ##
    # Regular user installs into user directory, root manages /usr/local.

    def operating_system_defaults
      unless opt_build_root?
        options = if Process.uid == 0
          "--install-dir=#{Gem.default_dirs[:local][:gem_dir]} --bindir #{Gem.default_dirs[:local][:bin_dir]}"
        else
          "--user-install --bindir #{File.join [Dir.home, 'bin']}"
        end

        {"gem" => options}
      else
        {}
      end
    end

    ##
    # RubyGems default overrides.

    def default_dir
      Gem.default_dirs[:system][:gem_dir]
    end

    def default_path
      path = default_dirs.collect {|location, paths| paths[:gem_dir]}
      path.unshift Gem.user_dir if File.exist? Gem.user_home
      path
    end

    def default_ext_dir_for base_dir
      dir = if rpmbuild?
        build_dir = base_dir.chomp Gem.default_dirs[:system][:gem_dir]
        if build_dir != base_dir
          File.join build_dir, Gem.default_dirs[:system][:ext_dir]
        end
      else
        dirs = Gem.default_dirs.detect {|location, paths| paths[:gem_dir] == base_dir}
        dirs && dirs.last[:ext_dir]
      end
      dir && File.join(dir, RbConfig::CONFIG['RUBY_INSTALL_NAME'])
    end

    # This method should be available since RubyGems 2.2 until RubyGems 3.0.
    # https://github.com/rubygems/rubygems/issues/749
    if method_defined? :install_extension_in_lib
      remove_method :install_extension_in_lib

      def install_extension_in_lib
        false
      end
    end
  end
end
