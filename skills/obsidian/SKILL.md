---
name: obsidian
description: "Read, search, create, append to, and edit notes in an Obsidian vault using plain file operations on its markdown files, with [[wikilinks]] between notes. Use when the user asks to find, open, write, update, or link notes in their Obsidian vault. Not for generic markdown docs in a code repo (codebase-documentation-generator) or for Word/PDF files (docx, pdf)."
version: 1.0.0
author: Pixis
license: MIT
platforms: [linux, macos, windows]
metadata:
  pixis:
    category: Note-taking
    tags: [obsidian, notes, markdown, vault, wikilinks]
    related_skills: [docx, codebase-documentation-generator]
---

# Obsidian

An Obsidian vault is a folder of `.md` files, so no plugin or API is needed: use the normal read, search, write, and edit tools on the files directly.

## When to use

- Find or open a note in the user's vault.
- Create a new note or append to an existing one.
- Edit part of a note, or connect notes with links.

## Vault path

1. Use the `OBSIDIAN_VAULT_PATH` environment variable if it is set.
2. Otherwise default to `~/Documents/Obsidian Vault`.
3. File tools do not expand `~` or `$VARS`, so never pass `$OBSIDIAN_VAULT_PATH` to them. Resolve a concrete absolute path first; running a shell command is fine for that (for example `echo "$OBSIDIAN_VAULT_PATH"`, or checking that the default folder exists). Then go back to file tools.
4. Vault paths often contain spaces, another reason to prefer file tools over shell commands once the path is known.
5. If the folder does not exist, ask the user for the vault location rather than creating one.

## Operations

| Task | How |
|---|---|
| Read a note | File-read tool on the absolute path (gives line numbers and paging; better than `cat`) |
| List notes | File search, target files, pattern `*.md` under the vault; for a subfolder, search under its absolute path |
| Find by name | File search, target files, filename pattern (better than `find`/`ls`) |
| Find by content | File search, target content, regex pattern, restricted to `*.md` (better than `grep`) |
| Create | Write the file with its complete markdown content (avoids heredoc and quoting problems) |
| Append | Read the note first, then a targeted edit anchored on a stable heading or trailing block: replace the anchor with the anchor plus the new content |
| Edit part | Targeted edit (find and replace) on the exact passage |
| Full rewrite | Write the whole file, when a targeted edit would be fragile |

If rewriting the whole note is clearer than a fragile edit, write the full file. For a plain append with no stable anchor, a shell append (`>>`) is acceptable when it is the clearest safe option.

## Linking

Connect related notes with `[[Note Name]]` wikilinks. Use the existing note's exact filename (without `.md`); for a heading or alias use `[[Note Name#Heading]]` or `[[Note Name|label]]`.

## Pitfalls

- Never create a note or rewrite a file without reading it first if it might already exist; overwriting loses the user's content.
- Do not touch the `.obsidian/` folder (settings and plugins).
- Keep existing frontmatter and formatting when editing.

## Completion criteria

- The path used was absolute and inside the vault.
- A new or changed note was read back to confirm the content.
- Appends and edits kept the rest of the note unchanged.
- Any `[[links]]` point to notes that exist, or the user was told they are new.
