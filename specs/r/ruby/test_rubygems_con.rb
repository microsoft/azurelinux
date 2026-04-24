# frozen_string_literal: true

require 'test/unit'
require 'rpm_test_helper'

class TestRubyGemsCon < Test::Unit::TestCase
  include RPMTestHelper

  def test_filter_out_regular_requirements
    gem_i = GemInfo.new

    lines = run_generator_single_file(gem_i)

    assert_equal(0, lines.size)

    deps = [ Dependency.new('bar') ]
    gem_i.dependencies = deps

    lines = run_generator_single_file(gem_i)

    assert_equal(0, lines.size)

    deps = [
      Dependency.new('bar'),
      Dependency.new('baq'),
      Dependency.new('quz')
    ]

    gem_i.dependencies = deps
    lines = run_generator_single_file(gem_i)

    assert_equal(0, lines.size)

    deps = [
      Dependency.new('bar', ['>= 4.1']),
      Dependency.new('baz', ['~> 3.2']),
      Dependency.new('quz', ['>= 5.6'])
    ]

    gem_i.dependencies = deps

    lines = run_generator_single_file(gem_i)

    assert_equal(0, lines.size)
  end

  def test_single_gem_single_version_conflict
    con = Dependency.new('bar', ['!= 0.4.4'])

    gem_i = GemInfo.new(dependencies: [ con ])
    lines = run_generator_single_file(gem_i)

    assert_equal(1, lines.size)
    assert_equal("#{con.to_rpm_str} = 0.4.4\n", lines.first)
  end

  def test_multiple_gems_with_single_conflict
    cons = [
      Dependency.new('bar', ['!= 1.1']),
      Dependency.new('baq', ['!= 1.2.2']),
      Dependency.new('quz', ['!= 1.3'])
    ]

    gem_i = GemInfo.new(dependencies: cons)

    lines = run_generator_single_file(gem_i)

    assert_equal(3, lines.size)

    assert_equal("#{cons[0].to_rpm_str} = 1.1\n"  , lines[0])
    assert_equal("#{cons[1].to_rpm_str} = 1.2.2\n", lines[1])
    assert_equal("#{cons[2].to_rpm_str} = 1.3\n"  , lines[2])
  end

  def test_multiple_conflicts_on_single_gem
    con = Dependency.new('bar', ['!= 2.3', '!= 2.4'])

    gem_i = GemInfo.new(dependencies: [con])

    lines = run_generator_single_file(gem_i)

    assert_equal(1, lines.size)
    rpm_name = con.to_rpm_str
    left_rpm_constraint = "(#{rpm_name} = 2.3 with "
    right_rpm_constraint = "#{rpm_name} = 2.4)\n"
    assert_equal((left_rpm_constraint + right_rpm_constraint), lines[0])

    con = Dependency.new('bar', ['!= 2.3', '!= 2.4', '!= 4.5'])

    gem_i = GemInfo.new(dependencies: [ con ])

    lines = run_generator_single_file(gem_i)

    assert_equal(1, lines.size)

    rpm_name = con.to_rpm_str
    left_rpm_constraint = "(#{rpm_name} = 2.3 with "
    middle_rpm_constraint = "#{rpm_name} = 2.4 with "
    right_rpm_constraint = "#{rpm_name} = 4.5)\n"

    assert_equal((left_rpm_constraint + middle_rpm_constraint + right_rpm_constraint), lines[0])
  end

  def test_generates_conflicts_while_ignoring_regular_requirements
    deps = [
      Dependency.new('bar', ['>= 2.3', '!= 2.4.2']),
      Dependency.new('quz', ['~> 3.0', '!= 3.2'])
    ]

    gem_i = GemInfo.new(dependencies: deps)

    lines = run_generator_single_file(gem_i)

    assert_equal(2, lines.size)

    rpm_name = deps[0].to_rpm_str
    rpm_constraint = "#{rpm_name} = 2.4.2\n"
    assert_equal(rpm_constraint, lines[0])

    rpm_name = deps[1].to_rpm_str
    rpm_constraint = "#{rpm_name} = 3.2\n"
    assert_equal(rpm_constraint, lines[1])
  end
end
