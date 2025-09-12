# Chat History Storage (Local Only)

This repository intentionally does not version chat transcripts.

- Keep your transcripts under: `docs/chat-history/`
- The directory is ignored by `.gitignore` and won’t be committed.
- Maintain your own local backups; these files are important but non-source assets.

Notes after the cleanup:
- Repo history was rewritten to remove past commits of chat transcripts (including ones that briefly lived outside `docs/chat-history/`).
- Local files under `docs/chat-history/` are untouched by this policy; they remain on your disk but are untracked.
- If you had an older clone, run a hard reset against `origin/main` to avoid reintroducing removed content.

Please do not move chat transcripts outside `docs/chat-history/`, and do not change `.gitignore` rules that protect this directory.
