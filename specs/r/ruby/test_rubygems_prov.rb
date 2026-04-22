# frozen_string_literal: true

require 'test/unit'
require 'rpm_test_helper'

class TestRubyGemsProv < Test::Unit::TestCase
  include RPMTestHelper

  def test_provides_the_gem_version
    gem_i = GemInfo.new(version: '1.2')

    lines = run_generator_single_file(gem_i)

    assert_equal(1, lines.size)
    assert_equal("#{gem_i.to_rpm_str} = #{gem_i.version}\n", lines.first)

    gem_i = GemInfo.new(name: 'somegem_foo', version: '4.5.6')

    lines = run_generator_single_file(gem_i)

    assert_equal(1, lines.size)
    assert_equal("#{gem_i.to_rpm_str} = #{gem_i.version}\n", lines.first)

    deps = [
      Dependency.new('bar'),
      Dependency.new('baq', [">= 1.2"]),
      Dependency.new('quz', ["!= 3.2"])
    ]
    gem_i = GemInfo.new(dependencies: deps)

    lines = run_generator_single_file(gem_i)

    assert_equal(1, lines.size)
    assert_equal("#{gem_i.to_rpm_str} = #{gem_i.version}\n", lines.first)
  end

  def test_translates_prelease_version_provides_from_rubygems_to_rpm
    gem_i = GemInfo.new(version: '1.2.3.dev')

    lines = run_generator_single_file(gem_i)

    assert_equal(1, lines.size)
    assert_equal("#{gem_i.to_rpm_str} = 1.2.3~dev\n", lines.first)

    gem_i = GemInfo.new(name: 'foo2', version: '1.2.3.dev.2')

    lines = run_generator_single_file(gem_i)

    assert_equal(1, lines.size)
    assert_equal("#{gem_i.to_rpm_str} = 1.2.3~dev.2\n", lines.first)
  end
end
