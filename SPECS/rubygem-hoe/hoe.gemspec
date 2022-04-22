# coding: utf-8

Gem::Specification.new do |s|
  s.name          = "hoe"
  s.version       = "3.18.0"
  s.authors       = ["Ryan Davis"]
  s.email         = ["ryand-ruby@zenspider.com"]

  s.summary       = "Rake/Rubygems helper for project Rakefiles"
  s.description   = "Hoe is a rake/rubygems helper for project Rakefiles. It helps you manage, maintain, and release your project and includes a dynamic plug-in system allowing for easy extensibility. Hoe ships with plug-ins for all your usual project tasks including rdoc generation, testing, packaging, deployment, and announcement."
  s.homepage      = "https://github.com/seattlerb/hoe"
  s.license       = "MIT"

  s.require_paths = %w[lib]
  s.files         = %w[
    hoe.gemspec
    History.rdoc
    Hoe.pdf
    Manifest.txt
    README.rdoc
    Rakefile
    bin/sow
    lib/hoe.rb
    lib/hoe/clean.rb
    lib/hoe/compiler.rb
    lib/hoe/debug.rb
    lib/hoe/deps.rb
    lib/hoe/flay.rb
    lib/hoe/flog.rb
    lib/hoe/gem_prelude_sucks.rb
    lib/hoe/gemcutter.rb
    lib/hoe/inline.rb
    lib/hoe/newb.rb
    lib/hoe/package.rb
    lib/hoe/publish.rb
    lib/hoe/racc.rb
    lib/hoe/rake.rb
    lib/hoe/rcov.rb
    lib/hoe/rdoc.rb
    lib/hoe/signing.rb
    lib/hoe/test.rb
    lib/minitest/test_task.rb
    template/.autotest.erb
    template/History.txt.erb
    template/Manifest.txt.erb
    template/README.txt.erb
    template/Rakefile.erb
    template/bin/file_name.erb
    template/lib/file_name.rb.erb
    template/test/test_file_name.rb.erb
    test/test_hoe.rb
    test/test_hoe_debug.rb
    test/test_hoe_gemcutter.rb
    test/test_hoe_package.rb
    test/test_hoe_publish.rb
    test/test_hoe_test.rb
  ]

  s.required_ruby_version = Gem::Requirement.new(">= 2.1")
end
