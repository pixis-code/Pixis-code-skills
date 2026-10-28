# House style (optional)

`--style` copyedits to a house style on top of the de-AI pass, which always runs. It is not a registry of guides: it applies **register** (voice directives) and removes AI tells on top of whatever **mechanics** you enforce. No style guides are bundled; the example configs are generic.

## Config file (preferred)

`--style ./house.json`, or a bare name matching `examples/<name>.json`, applies a JSON config and verifies the checkable subset of its mechanics:

```bash
node scripts/check-style.js <file> --config <config.json>
```

Exit 0 means clean, 1 a hard violation, 2 a tool error (including an unresolvable bare name). Name the resolved config in your reply ("Applying config examples/technical.json; checkable mechanics verified.") so the mode that ran is clear.

```json
{
  "name": "My house style",
  "genre": "technical documentation",
  "register": ["Second person, active voice, present tense.", "No hype."],
  "mechanics": {
    "quotes": "straight",
    "headings": "sentence",
    "emDash": "sparing",
    "latinAbbrev": "parentheses",
    "serialComma": true,
    "spellNumbersUpTo": 9
  }
}
```

- **`register`:** voice directives applied as written; judgment calls, not machine-checked.
- **`genre`:** what the config was written for. Do not apply a config to a genre it was not written for.
- **`mechanics`:**

| key | values | check |
|---|---|---|
| `quotes` | straight, curly | hard: flags the wrong mark in prose |
| `latinAbbrev` | never, parentheses, any | hard: never flags any e.g./i.e.; parentheses flags them outside parentheses |
| `headings` | sentence, title | advisory (proper nouns make it ambiguous) |
| `emDash` | sparing, deliberate | advisory: sparing flags over about 1 per 1,000 words |
| `spellNumbersUpTo` | number | advisory: flags numerals at or below it in prose |
| `serialComma` | true, false | model-applied only |

Unrecognized keys or values give warnings, not silence. The checker skips frontmatter, code, link destinations, HTML tags and comments, and escaped punctuation.

## How `--style` composes

Follow the editing contract's applicability and protection gates. A config's `mechanics` govern its typographic features in editable prose. An explicit `--voice` wins over a config's `register` where they conflict; otherwise use the config register. `--context` decides whether an AI-writing pattern applies, and source fidelity governs every axis. Example: `--voice blunt` with a warm config stays blunt, the config's `emDash: deliberate` still governs dashes, and a necessary technical hedge keeps its uncertainty. When a config's mechanics conflict with the pattern catalog, the config wins the mechanic (a prose config with `headings: title` keeps Title Case headings), but still flag the AI habit, such as em-dash stacking.

## Named guide fallback

If someone passes a name such as "APA" or "Chicago" with no config, apply it best-effort from general knowledge. Open with a status line like "Applying APA from general knowledge (not verified; no compliance claim).", make no compliance claim, do not reproduce the guide's copyrighted text, and note that your knowledge may reflect an older edition. For real enforcement point the user to a dedicated style linter or a custom config. A bare de-AI request with no `--style` is unchanged.

## Quote normalization

```bash
node scripts/normalize-quotes.js draft.md --reference original.md          # prints result
node scripts/normalize-quotes.js draft.md --reference original.md --write  # edits file
```

Default `--quotes auto` infers double quotes and single quotes/apostrophes independently from unprotected reference prose (majority wins, ties use the first seen, no evidence leaves a family unchanged); without `--reference`, it infers from the input. An explicit house style uses `--quotes straight` or `--quotes curly` with no `--reference`. It changes only quotation marks and apostrophes in prose, preserving protected source, whitespace, and line endings; dashes and heading case stay as written. Exit 0 on success, 2 on invalid arguments or file errors. Review leading elisions (`'twas`, `rock 'n' roll`) by hand. For a bare URL in single quotes, use an explicit link or `<autolink>` if punctuation is ambiguous. For rewrites, normalize only editable prose and keep quotations, tables, and attributed text untouched.
