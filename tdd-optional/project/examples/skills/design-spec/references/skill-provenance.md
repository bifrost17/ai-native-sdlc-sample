# Applied skill source and version

Use this when filling `Skills applied`. Record only skills whose bodies you actually read and
used, with their real source. A version lookup does not substitute for reading or applying the skill.

- For a tracked file, use `git log -1 --format=%h -- <path-relative-to-its-repository>` in that
  skill's own repository. Check local changes; label changed/new content `uncommitted` with the
  known base SHA. Do not borrow the consuming project's revision for a plugin elsewhere.
- If Git history cannot be accessed, use the actual plugin's `.claude-plugin/plugin.json` or
  installation metadata: `namespace:skill@<manifest-or-installed-version>` and its source path.
  For a directory-loaded checkout, say it is the manifest version and note unverified Git/local state.
- A cache without `.git` is not automatically uncommitted. If no version can be verified, record
  `version-unverified` and why. An absent policy skill is a limitation, not a claim of policy compliance.

Keep detailed selection/provenance notes compact or in the versioned PR record if they would hide
the design. Preserve the applicable skill's policy procedure and the material decisions in the spec.
No source directory is an instruction to install a plugin, and no example creates a new team policy.
