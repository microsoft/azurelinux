# -*- encoding: utf-8 -*-
# stub: minitest 5.15.0 ruby lib

Gem::Specification.new do |s|
  s.name = "minitest".freeze
  s.version = "5.15.0"

  s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
  s.require_paths = ["lib".freeze]
  s.authors = ["Ryan Davis".freeze]
  s.date = "2019-10-30"
  s.description = "minitest provides a complete suite of testing facilities supporting\nTDD, BDD, mocking, and benchmarking.\n\n    \"I had a class with Jim Weirich on testing last week and we were\n     allowed to choose our testing frameworks. Kirk Haines and I were\n     paired up and we cracked open the code for a few test\n     frameworks...\n\n     I MUST say that minitest is *very* readable / understandable\n     compared to the 'other two' options we looked at. Nicely done and\n     thank you for helping us keep our mental sanity.\"\n\n    -- Wayne E. Seguin\n\nminitest/test is a small and incredibly fast unit testing framework.\nIt provides a rich set of assertions to make your tests clean and\nreadable.\n\nminitest/spec is a functionally complete spec engine. It hooks onto\nminitest/test and seamlessly bridges test assertions over to spec\nexpectations.\n\nminitest/benchmark is an awesome way to assert the performance of your\nalgorithms in a repeatable manner. Now you can assert that your newb\nco-worker doesn't replace your linear algorithm with an exponential\none!\n\nminitest/mock by Steven Baker, is a beautifully tiny mock (and stub)\nobject framework.\n\nminitest/pride shows pride in testing and adds coloring to your test\noutput. I guess it is an example of how to write IO pipes too. :P\n\nminitest/test is meant to have a clean implementation for language\nimplementors that need a minimal set of methods to bootstrap a working\ntest suite. For example, there is no magic involved for test-case\ndiscovery.\n\n    \"Again, I can't praise enough the idea of a testing/specing\n     framework that I can actually read in full in one sitting!\"\n\n    -- Piotr Szotkowski\n\nComparing to rspec:\n\n    rspec is a testing DSL. minitest is ruby.\n\n    -- Adam Hawkins, \"Bow Before MiniTest\"\n\nminitest doesn't reinvent anything that ruby already provides, like:\nclasses, modules, inheritance, methods. This means you only have to\nlearn ruby to use minitest and all of your regular OO practices like\nextract-method refactorings still apply.".freeze
  s.email = ["ryand-ruby@zenspider.com".freeze]
  s.extra_rdoc_files = ["History.rdoc".freeze, "Manifest.txt".freeze, "README.rdoc".freeze]
  s.files = [".autotest".freeze, "History.rdoc".freeze, "Manifest.txt".freeze, "README.rdoc".freeze, "Rakefile".freeze, "design_rationale.rb".freeze, "lib/hoe/minitest.rb".freeze, "lib/minitest.rb".freeze, "lib/minitest/assertions.rb".freeze, "lib/minitest/autorun.rb".freeze, "lib/minitest/benchmark.rb".freeze, "lib/minitest/expectations.rb".freeze, "lib/minitest/hell.rb".freeze, "lib/minitest/mock.rb".freeze, "lib/minitest/parallel.rb".freeze, "lib/minitest/pride.rb".freeze, "lib/minitest/pride_plugin.rb".freeze, "lib/minitest/spec.rb".freeze, "lib/minitest/test.rb".freeze, "lib/minitest/unit.rb".freeze, "test/minitest/metametameta.rb".freeze, "test/minitest/test_minitest_assertions.rb".freeze, "test/minitest/test_minitest_benchmark.rb".freeze, "test/minitest/test_minitest_mock.rb".freeze, "test/minitest/test_minitest_reporter.rb".freeze, "test/minitest/test_minitest_spec.rb".freeze, "test/minitest/test_minitest_test.rb".freeze]
  s.homepage = "https://github.com/seattlerb/minitest".freeze
  s.licenses = ["MIT".freeze]
  s.rdoc_options = ["--main".freeze, "README.rdoc".freeze]
  s.required_ruby_version = Gem::Requirement.new(">= 2.2".freeze)
  s.rubygems_version = "3.1.2".freeze
  s.summary = "minitest provides a complete suite of testing facilities supporting TDD, BDD, mocking, and benchmarking".freeze

  if s.respond_to? :specification_version then
    s.specification_version = 4
  end

  if s.respond_to? :add_runtime_dependency then
    s.add_development_dependency(%q<rdoc>.freeze, [">= 4.0", "< 7"])
    s.add_development_dependency(%q<hoe>.freeze, ["~> 3.22"])
  else
    s.add_dependency(%q<rdoc>.freeze, [">= 4.0", "< 7"])
    s.add_dependency(%q<hoe>.freeze, ["~> 3.22"])
  end
end
