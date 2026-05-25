---
name: binary-license-scanner
description: Analyze compiled binary files to extract linked library dependencies, then search for each library's official website, GitHub repository, and open source license. Outputs a Markdown table with library name, homepage, and license. Use when the user wants to audit a binary's dependencies, check license compliance, or scan a .dylib/.so/.dll/executable for third-party libraries. Triggers on requests like "analyze this binary", "scan libraries", "check licenses", "what libraries does this binary use", or any binary/license auditing task.
---

# Binary License Scanner

Analyze a compiled binary and produce a license audit report for all linked libraries.

## Workflow

### 1. Extract linked libraries

```bash
python3 <skill_dir>/scripts/analyze_binary.py <path-to-binary>
```

The script auto-detects the platform and binary format, then outputs JSON with `platform` and `libraries` (each with `full_path` and `name`).

### 2. Look up each library

**Order of operations:**

1. Check [known-libraries.md](references/known-libraries.md) first — use cached info for any match.
2. For libraries NOT in the known list, use `WebSearch` to find the official homepage / GitHub repo and license.
3. System libraries (libc, libSystem, kernel32.dll, ntdll.dll, libpthread, libm, libdl, libstdc++, libc++, libgcc_s, libSystem.B.dylib) — mark as "System (OS vendor)" without searching.

**Search query template:** `"<library_name> open source license github"`

**Batch searches:** Group unknown libraries into parallel `WebSearch` calls (3-5 per batch).

### 3. Format output

Produce a Markdown table with columns: **Library**, **Homepage / GitHub**, **License**.

- Rows sorted alphabetically by library name
- URLs as Markdown links: `[repo](https://github.com/...)`
- Unknown license → `Unknown`
- System libraries → `System (OS vendor)` with no link

Print the table to terminal.

### Output template

```markdown
## License Audit: <binary-filename>

| Library | Homepage / GitHub | License |
|---------|-------------------|---------|
| libfoo.so | [github.com/foo/libfoo](https://github.com/foo/libfoo) | MIT |
| libbar.dll | [bar.dev](https://bar.dev) | Apache-2.0 |
| libc.so.6 | — | System (OS vendor) |
```
