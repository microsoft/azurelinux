# coding: utf-8

Gem::Specification.new do |s|
  s.name          = "hoe"
  s.version       = "4.0.4"
  s.authors       = ["Ryan Davis"]
  s.email         = ["ryand-ruby@zenspider.com"]

  s.summary       = "Rake/Rubygems helper for project Rakefiles"
  s.description   = "Hoe is a rake/rubygems helper for project Rakefiles. It helps you manage, maintain, and release your project and includes a dynamic plug-in system allowing for easy extensibility. Hoe ships with plug-ins for all your usual project tasks including rdoc generation, testing, packaging, deployment, and announcement."
  s.homepage      = "https://github.com/seattlerb/hoe"
  s.license       = "MIT"

  s.require_paths = %w[lib]
  s.files         = `git ls-files`.split($\)

  s.required_ruby_version = Gem::Requirement.new(">= 2.1")
end
