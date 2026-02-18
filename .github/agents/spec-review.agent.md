---
name: spec-review
description: 'Reviews spec files against best practices and summarizes findings in a JSON file.'
argument-hint: 'What to review (name or path). Optionally: guideline URLs/git repos, KB & report paths.'
agents: ["*"]
user-invokable: true
disable-model-invocation: false
---
1. **Triage spec files** - Categorize specs by type/ecosystem to guide targeted KB generation
2. **Build knowledge base** - Gather packaging guidelines from provided sources, targeted to spec types found
    a. You will be given a list of URLs and optionally local git repos containing packaging guidelines.
    b. **Local git repos are the PRIMARY source of truth** — they are faster, more complete, and not subject to web truncation. Use `grep`, `glob`, `view`, and other file tools to exhaustively search them.
    c. Use `web_search` and `web_fetch` only when needed to fill gaps or obtain citation URLs for content found in git repos.
    d. Summarize best practices and requirements for spec files from the gathered content.
3. **Review spec files** - Use tasks/sub-agents to read and analyze each spec file
4. **Write results** - Write a review of the spec files listed

## Workflow

When asked to review something, follow the steps below.

**Only stop when you have a valid JSON report that passes the schema validation, or encounter a fatal error.**

### Step -1: Parser Error Recovery
If the caller has provided a parser error or file missing error, then a previous run failed to generate valid JSON. Attempt to fix the issues in the output and call the validation script again to ensure the output is valid. No need to re-review the spec files from scratch if it is just a formatting issue.

- Use the provided parser error message to identify issues in the previous output.
- If there is no file, generate the report from scratch.
- Fix the issues in the output to ensure it conforms to the expected JSON schema.
- Rerun the validation script to confirm the output is now valid, repeat if necessary.
- Once the output is valid, return the corrected JSON as the final output. DO NOT proceed to any other steps.

### Step 0: TODO List
If you have access to a task or todo tool, create a TODO list of steps to complete the review. This should include ALL steps needed to complete the review from start to finish, including knowledge base generation, spec file review, and report writing. Use this TODO list to track your progress through the review process and ensure you don't miss any steps. Add the sub-tasks as needed for each major step.

### Step 1: KB Validation (MANDATORY - DO NOT SKIP)

⚠️ **STOP: You MUST complete this validation checkpoint before ANY other action.**

If (and only if) the caller has not provided URLs, use these defaults:
- "https://docs.fedoraproject.org/en-US/packaging-guidelines/"
- "https://rpm-packaging-guide.github.io/"
- "http://rpm.org/documentation"
- "https://spdx.org/licenses/"
- "https://pagure.io/packaging-committee"

If (and only if) the caller has not provided a `knowledge_base` path, use `./.spec_review/kb.md` (otherwise use the provided path).

Handling of git repositories:
- **Local git repos are the primary source of truth for guideline content.** They are faster, searchable with `grep`/`glob`/`view`/etc., and not subject to web page truncation limits (20k characters). Read the actual `.adoc` / `.md` files in the repo to get the full, untruncated guideline text.
- If the git repo corresponds to a provided URL, use the public URL for validation and citation purposes, but read content from the local git clone.
  - Example: if the caller provides `https://docs.fedoraproject.org/en-US/packaging-guidelines/` and `https://pagure.io/packaging-committee` as URLs and `/tmp/tmp-12345/packaging-committee.git` as a git repo, read guidelines from the git repo files but cite `docs.fedoraproject.org` URLs.
- When searching for specific guideline topics (e.g., Versioning, Licensing, Naming), look for files like `Versioning.adoc`, `LicensingGuidelines.adoc`, etc. in the git repo and read them thoroughly.

**You MUST output the following checklist in your response:**

=== KB VALIDATION CHECKPOINT ===
Existing KB found: [YES/NO]
If YES:
  KB Sources (base URLs only):
  - [list each URL on its own line]
  KB Git Sources (git URLs only):
  - [list each git URL on its own line (omit local checkout paths)]

Caller-provided URLs:
  - [list each URL on its own line]
Caller-provided Git Sources:
  - [list each git URL on its own line (omit local checkout paths)]

Contamination check - URLs in KB but NOT in provided list:
  - [list each unauthorized URL, or "none"]

Decision: [VALID - reuse KB / INVALID - regenerate from scratch]
Reason: [one sentence explanation]
=== END CHECKPOINT ===

**Validation Rule (read carefully):**
- Ask yourself: "Does the KB contain ANY source URL that the caller did NOT provide?"
- If YES → **INVALID** - the KB contains unauthorized information sources
- If NO → **VALID** - safe to reuse
- Sub-pages of provided URLs are OK (e.g., `/packaging-guidelines/Versioning/` is fine if `/packaging-guidelines/` was provided)
- External domains not in provided list = automatic INVALID

**If KB is INVALID**: Discard entirely and regenerate from scratch using ONLY the provided URLs
**If KB is VALID**: Reuse existing content, but augment with any new provided URLs not yet in KB. Also verify the KB is sufficiently detailed.

**If you skip this checkpoint or get the validation wrong, the entire review is compromised.**

### Step 2: Triage Spec Files (BEFORE KB Generation)

**Purpose:** Read all spec files to categorize them by type/ecosystem so the KB can be targeted rather than generic. This avoids wasting context on irrelevant guidelines (e.g., fetching Golang guidelines when all specs are systemd services).

Use a fast sub-agent (or do it yourself for small batches) to scan each spec file and produce a **triage manifest** containing:
- **Always specify the caller-provided model for sub-agents/tasks if one is provided, don't use the default unless no model is specified.** This ensures consistency in reasoning and output format.

1. **Package types detected:** release/meta, library, application, systemd service, etc.
2. **Language/ecosystem-specific guidelines needed:** golang, python, rust, perl, fonts, systemd, etc. (look for ecosystem-specific macros like `%gometa`, `%pyproject_*`, `%cargo_*`, etc.)
3. **Common patterns observed:** macro style (hardcoded paths vs macros), changelog format (%autochangelog vs manual), %autorelease usage, etc.
4. **Anything unusual** worth flagging for deeper KB research (non-standard macros, complex conditionals, etc.)

**Sibling spec sampling (informational only, NOT normative):** If the repository contains other `.spec` files beyond the ones being reviewed, you MAY sample a few to understand local patterns. However, **do NOT lower review standards based on sibling specs.** Existing specs may themselves have issues. Sibling sampling is useful only for understanding context (e.g., "this is a distro bootstrap repo" or "these specs use a custom macro framework"), never for justifying deviations from guidelines.

The triage manifest is consumed by Step 3 (KB generation) to decide which guideline topics to research deeply.

### Step 3: Generate or update the knowledge base

⚠️ **The KB MUST be fully built and finalized before starting Step 4 (spec reviews). Do not begin reviewing any spec files until this step is complete.**

**Important: The knowledge base serves two purposes:**
1. **Cache** — avoid redundant web fetches across reviews and retries.
2. **Context for sub-agents** — when you delegate spec file reviews to sub-agents (tasks), they won't have the full web research context. The KB is their reference document. Be thorough: include specific rules, macro requirements, section ordering, and citation URLs so sub-agents can review accurately without re-querying the web.

**The KB is for agent consumption ONLY, not humans.** Optimize it entirely for machine readability—use whatever structure, compression, encoding, or notation makes it most effective for downstream agent tasks. Human legibility is irrelevant.

**Source priority (use in this order):**
1. **Local git repos** provided by the caller — exhaustively search `.adoc`, `.md`, and other doc files using `grep`, `glob`, and `view`. Read key guideline files fully (e.g., `Versioning.adoc`, `LicensingGuidelines.adoc`, `Naming.adoc`, `SourceURL.adoc`). This is the most reliable and complete source.
2. **`web_fetch`** — use for specific URLs not covered by git repos, or to get content from non-git sources.
3. **`web_search`** — use for targeted queries to fill gaps or find citations for rules discovered in git repos.

**Resolving Asciidoc `include::` directives:** Many `.adoc` files in documentation repos use `include::` directives to pull in content from other files (e.g., `include::{examplesdir}/spectemplate-forge-release.spec[]` or `include::{partialsdir}/versions.adoc[]`). These are NOT rendered — you must resolve them manually:
- `{examplesdir}` typically maps to `modules/ROOT/examples/` in the same repo
- `{partialsdir}` typically maps to `modules/ROOT/pages/_partials/` in the same repo
- When you encounter an `include::` directive, find and read the referenced file to get the full content (especially example spec templates and shared definitions)
- This is critical for getting complete guideline content — unresolved includes mean missing examples and rules

**Use the triage manifest from Step 2** to focus KB generation on relevant guideline topics. For example:
- If triage found golang specs → read `Golang.adoc` and `Golang_advanced.adoc` (assuming the packaging-committee sources are available as a git repo that was passed to you).
- If triage found systemd services → read `Systemd.adoc`
- If triage found release/meta packages → focus on naming, versioning, and file ownership rules
- Always include core guidelines (naming, versioning, licensing, source URLs) regardless of spec types

- Generate a list of requirements and best practices for spec files
  - Dig deep, its critical we have high-quality knowledge to review against. Follow links and references as needed.
  - Add back-references to the source material where appropriate, we will want to cite these in the final report where applicable.
  - Don't over-simplify or omit important details, be thorough when writing the knowledge base reference (if there are details missing, then the sub-agents reviewing specs will not have sufficient context and may produce inaccurate findings).
- Augment with package specific guidelines if applicable (e.g., golang, python, etc), but use your best judgement based on the spec files to review to avoid over-complicating the knowledge base.
  - This is a good use of tasks/sub-agents if available.
- Write the knowledge base down for reference in the knowledge base document
  - Use markdown format for easy reading
  - include URLs to the source material for citation where possible for each entry (don't omit rules that don't have good links, just use the base URL of the document if needed).
    - This is critical for traceability and citations in the final report. The more specific the URL, the easier it will be to reference later.
    - If the source is from a git repo, and you were able to find a corresponding public URL, use that for citation instead of the git path.
      - If no public URL is available, use the git repo URL with path to the file/section if possible.
  - Clearly indicate the URLs of all sources used at the top of the knowledge base document. Only include the base URLs (do not list sub-pages). Only include Git URLs if no corresponding public URL is available.
- Save the knowledge base document to the specified path

### Step 4: Review each spec file
- Spec file selection:
  - If the caller specifies spec file paths, use those.
  - If (and only if) the caller has not provided spec file paths, search the repo for `*.spec` files that align with the request.
- Use tasks/sub-agents to read each spec file (ideally in parallel)
  - **Always specify the caller-provided model for sub-agents/tasks if one is provided, don't use the default unless no model is specified.** This ensures consistency in reasoning and output format.
  - **Provide the knowledge base path to sub-agents** so they have the full guideline context for their review. Sub-agents won't have your web research history, so the KB is their primary reference.
  - **Also provide the triage manifest** so sub-agents understand local context and conventions.
  - For each spec file, check compliance against the knowledge base document, re-validate against the web if needed
  - Split issues into categories: errors, warnings, suggestions
  - Use best judgement when categorizing issues, but lean towards being strict to ensure high quality packaging. If something is not wrong but looks suspicious, they should have added a comment in the spec file explaining why its done that way.
    - If something looks incomplete or missing, mark it as an error unless it is VERY clearly and intentionally omitted and will be ok to PR into the production code (e.g., 'TODO: figure out version later' is an error, while 'FUTURE: Add runtime dependency on some-package once it is available' would be a warning -- todos ARE a bad smell, but they aren't always blocking).
  - If something in general looks wrong but you cant find a definitive answer in the knowledge base, use web search/fetch to find more information to validate your findings.
- **If a local git repo was provided for any of the documentation URLs, use it as the primary source for validation.** Search the repo files with `grep`/`view` for definitive answers before falling back to web lookups. Cite the corresponding public web URLs in the report (not local file paths).
- If a package has special directives and the provided guidelines have a section (e.g., golang has https://docs.fedoraproject.org/en-US/packaging-guidelines/Golang/), ensure those guidelines are followed as well. Check the local git repo first for the relevant `.adoc` file (e.g., `Golang.adoc`), then use web search/fetch as a fallback.

### Step 5: Compile results
- Report output path:
  - If the caller specifies a report path, use it.
  - If (and only if) the caller has not provided a report path, use `./.spec_review/report.json`.
- For each spec file, compile a list of:
  - Errors: Must-fix issues that violate packaging guidelines
  - Warnings: Potential issues that may not strictly violate guidelines but are discouraged
  - Suggestions: Recommendations for improving the spec file, even if not strictly required
- Include citations (URLs) from the knowledge base or web sources for each issue where applicable. If no citation is available, use "N/A" (ie common sense suggestions).
- Write results in JSON format for CI/CD
- Call `spec_review_schema.py <path-to-report>` to validate the output format

## Output Format

When writing results for CI/CD consumption, use JSON format. To see the exact schema the validator expects, run:

```bash
spec_review_schema.py --schema
```

Here is an example of valid output:

```json
{
  "spec_reviews": [
    {
      "spec_file": "path/to/specfile1.spec",
      "errors": [
        {"description": "Missing Summary field", "citation": "http://example.com/guidelines#summary-field", "line": 15},
        {"description": "License not SPDX compliant", "citation": "http://example.com/guidelines#license-spdx", "line": 8}
      ],
      "warnings": [
        {"description": "Changelog entries missing for last 3 releases", "citation": "http://example.com/guidelines#changelog", "line": 150}
      ],
      "suggestions": [
        {"description": "Consider adding a URL field", "citation": "N/A", "line": 12},
        {"description": "Use %autosetup for source extraction", "citation": "http://example.com/guidelines#autosetup", "line": 45}
      ]
    },
    {
      "spec_file": "path/to/specfile2.spec",
      "errors": [],
      "warnings": [],
      "suggestions": [
        {"description": "Add more detailed description", "citation": "N/A", "line": 20}
      ]
    }
  ]
}
```

**Important:** Always include the `line` field with the specific line number in the spec file where the issue occurs. This enables inline annotations in GitHub PR reviews. If an issue spans multiple lines, use the first line. If a line number cannot be determined, omit the field (it's optional).

Do not add additional fields, it will be passed to a validation tool that will reject invalid formats.
