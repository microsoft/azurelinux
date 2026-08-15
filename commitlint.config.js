// Shared Conventional Commits rules for Azure Linux.
//
// This config is the single source of truth for commit-message validation. It
// is consumed both by the "Check Commit Messages" GitHub workflow and by
// contributors running commitlint locally, so CI and local checks stay in sync.
// See CONTRIBUTING.md for the human-readable description of these conventions.
//
// Validate locally (same rules as CI):
//   npx --yes @commitlint/cli@21 --config commitlint.config.js \
//     --from origin/4.0 --to HEAD
// or lint a single message:
//   echo "feat(demo): add capability" | npx --yes @commitlint/cli@21

/** @type {import('@commitlint/types').UserConfig} */
module.exports = {
  extends: ['@commitlint/config-conventional'],
  // Lint every commit. commitlint otherwise silently ignores fixup!/squash!
  // and merge commits, but CONTRIBUTING.md requires those to be cleaned up
  // (rebase-merge means merge commits never enter history), so we want them
  // reported as invalid rather than skipped.
  defaultIgnores: false,
  rules: {
    // Types documented in CONTRIBUTING.md. Anything else fails.
    'type-enum': [
      2,
      'always',
      ['feat', 'fix', 'docs', 'style', 'refactor', 'perf', 'test', 'build', 'ci', 'chore', 'revert'],
    ],
    // CONTRIBUTING.md recommends a lowercase summary but does not hard-enforce
    // it (proper nouns and acronyms are common), so surface it as a warning.
    'subject-case': [1, 'never', ['sentence-case', 'start-case', 'pascal-case', 'upper-case']],
    // Summary length is a soft guideline in CONTRIBUTING.md; warn, don't fail.
    'header-max-length': [1, 'always', 100],
    // Validation is header-focused: commit bodies may legitimately contain long
    // lines (URLs, pasted logs) and trailers (e.g. Co-authored-by) that exceed
    // the conventional 100-char limit, so do not fail on body/footer length.
    'body-max-line-length': [0],
    'footer-max-line-length': [0],
  },
};
