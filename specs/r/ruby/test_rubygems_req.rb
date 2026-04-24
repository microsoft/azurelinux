# frozen_string_literal: true

require 'test/unit'
require 'rpm_test_helper'

class TestRubyGemsReq < Test::Unit::TestCase
  include RPMTestHelper

  def test_depends_on_rubygems
    gem_i = GemInfo.new

    lines = run_generator_single_file(gem_i)

    assert_equal(1, lines.size)
    assert_equal("#{helper_rubygems_dependency}\n", lines.first)
  end

  def test_requires_rubygems_and_dependency
    dep = Dependency.new('bar')
    gem_i = GemInfo.new(dependencies: [dep])

    lines = run_generator_single_file(gem_i)

    assert_equal(2, lines.size)
    assert_equal("#{helper_rubygems_dependency}\n", lines.first)
    assert_equal("#{dep.to_rpm_str}\n", lines[1])
  end

  def test_requires_multiple_dependencies_with_constraint
    constraints = [
      '>= 3.0',
      '>= 3.0.0',
      '>= 3',
      '= 1.0.2',
      '= 3.0',
      '< 3.2',
      '<= 3.4'
    ]

    dependencies = []
    constraints.each_with_index do |constraint, idx|
      dependencies << Dependency.new("bar#{idx}", [constraint])
    end

    gem_i = GemInfo.new(dependencies: dependencies)

    lines = run_generator_single_file(gem_i)
    # + 1 for the rubygems dependency
    assert_equal(constraints.size + 1, lines.size)
    dependencies.each_with_index do |dep, idx|
      rpm_dep_name = dep.to_rpm_str
      # Start indexing lines at 1, to jump over rubygems dependency
      assert_equal("#{rpm_dep_name} #{constraints[idx]}\n", lines[idx + 1])
    end
  end

  def test_expands_pessimistic_constraint_for_rpm
    dep = Dependency.new('bar', ['~> 1.2'])

    gem_i = GemInfo.new(dependencies: [dep])

    lines = run_generator_single_file(gem_i)

    assert_equal(2, lines.size)

    rpm_dep_name = dep.to_rpm_str
    left_constraint = "#{rpm_dep_name} >= 1.2"
    right_constraint = "#{rpm_dep_name} < 2"
    expected_constraint = "(#{left_constraint} with #{right_constraint})\n"
    assert_equal(expected_constraint, lines[1])
  end

  def test_multiple_pessimistically_constrained_dependencies
    dependencies = []
    dep_map = [
      {
        constraint:     '~> 1.2.3',
        expanded_left:  '>= 1.2.3',
        expanded_rigth: '< 1.3',
        gem_name: 'bar1'
      },
      {
        constraint:     '~> 1.2',
        expanded_left:  '>= 1.2',
        expanded_rigth: '< 2',
        gem_name: 'bar2'
      },
      {
        constraint:     '~> 3',
        expanded_left:  '>= 3',
        expanded_rigth: '< 4',
        gem_name: 'bar3'
      }
    ].each do |deps|
      dependencies << Dependency.new(deps[:gem_name], [deps[:constraint]])
    end

    gem_i = GemInfo.new(dependencies: dependencies)

    lines = run_generator_single_file(gem_i)

    assert_equal(dep_map.size + 1, lines.size)

    dep_map.each_with_index do |hash, idx|
      rpm_dep_name = dependencies[idx].to_rpm_str
      left_constraint = rpm_dep_name + ' ' + hash[:expanded_left]
      right_constraint = rpm_dep_name + ' ' + hash[:expanded_rigth]
      expected_constraint = "(#{left_constraint} with #{right_constraint})\n"
      assert_equal(expected_constraint, lines[idx + 1])
    end
  end

  def test_multiple_constraints_on_one_dependency_composes_constraints_for_RPM
    # The quoting here depends on how the constraint is expanded in the helpers.
    # right now the form is `["#{constraint}"]`, therefore we have to not specify
    # left and right quotes.
    constraints = ['>= 0.2.3', '<= 0.2.5']
    dep = Dependency.new('baz', constraints)

    gem_i = GemInfo.new(dependencies: [dep])

    lines = run_generator_single_file(gem_i)

    assert_equal(2, lines.size)
    rpm_dep_name = dep.to_rpm_str
    assert_equal("(#{rpm_dep_name} >= 0.2.3 with #{rpm_dep_name} <= 0.2.5)\n", lines[1])

    # Not sure who would compose a dependency like this, but it's possible
    # to do with the current generator
    constraints = ['> 0.4.5', '< 0.6.4', '>= 2.3', '<= 2.5.3']
    dep = Dependency.new('qux', constraints)

    gem_i = GemInfo.new(dependencies: [dep])

    lines = run_generator_single_file(gem_i)

    rpm_dep = dep.to_rpm_str
    expected_str = "(#{rpm_dep} > 0.4.5 with #{rpm_dep} < 0.6.4 with " \
                   "#{rpm_dep} >= 2.3 with #{rpm_dep} <= 2.5.3)\n"

    assert_equal(2, lines.size)
    assert_equal(expected_str, lines[1])
  end

  # https://bugzilla.redhat.com/show_bug.cgi?id=1561487
  def test_depends_on_gem_with_version_conflict
    dep = Dependency.new('baz', ['!= 0.4'])

    gem_i = GemInfo.new(dependencies: [dep])

    lines = run_generator_single_file(gem_i)

    assert_equal(2, lines.size)
    assert_equal("#{dep.to_rpm_str}\n", lines[1])
  end

  def test_filters_conflict_from_regular_version_constraints
    constraint = ['> 1.2.4', '!= 1.2.7']
    dep = Dependency.new('baq', constraint)

    gem_i = GemInfo.new(dependencies: [dep])

    lines = run_generator_single_file(gem_i)

    assert_equal(2, lines.size)
    assert_equal("#{dep.to_rpm_str} > 1.2.4\n", lines[1])
  end

  def test_filtering_conflicts_is_not_depending_on_contraint_ordering
    constraints = ['!= 1.2.7', '> 1.2.4']
    dep = Dependency.new('baq', constraints)

    gem_i = GemInfo.new(dependencies: [dep])

    lines = run_generator_single_file(gem_i)

    assert_equal(2, lines.size)
    assert_equal("#{dep.to_rpm_str} > 1.2.4\n", lines[1])
  end

  def test_filters_multiple_conflicts_from_dependency
    omit "Case not yet supported."
    constraints = ['!= 1.2.4', '!= 1.2.5', '!= 2.3', '!= 4.8']
    dep = Dependency.new('baf', constraints)

    gem_i = GemInfo.new(dependencies: [dep])

    lines = run_generator_single_file(gem_i)

    assert_equal(2, lines.size)
    assert_equal("#{dep.to_rpm_str}\n", lines[1])
  end

  def test_filters_multiple_conflicts_from_dependency_but_keeps_regular_constraint
    constraints = ['!= 1.2.4', '!= 1.2.5', '!= 2.3', '<= 4.8']
    dep = Dependency.new('bam', constraints)

    gem_i = GemInfo.new(dependencies: [dep])

    lines = run_generator_single_file(gem_i)

    assert_equal(2, lines.size)
    assert_equal("#{dep.to_rpm_str} <= 4.8\n", lines[1])
  end
end
