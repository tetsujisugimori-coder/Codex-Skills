---
name: pull-main
description: Safely update the local main branch of the current Git repository from its remote. Use when asked to pull, update, or sync local main; before starting work from the latest main; or when the user asks for the standard local-main update procedure.
---

# Safely Update Local Main

Update only the repository that contains the current working directory. Treat the remote as the source of truth, but never discard local work.

## Workflow

1. Identify the repository root with `git rev-parse --show-toplevel`, and stop if the current directory is not in a Git repository.
2. Inspect `git status --short` and the current branch. If the worktree has changes, stop before switching branches. Summarize the affected files and ask whether to stash, commit, or preserve the changes in another way. Do not run `git reset`, `git checkout --`, or a destructive clean.
3. Fetch the default remote with `git fetch origin main`. If `origin` or `main` does not exist, stop and report the available remotes and branches.
4. Switch to `main` with `git switch main`. If it cannot switch cleanly, stop and explain why.
5. Update with `git pull --ff-only origin main`. Use fast-forward only; never create a merge commit automatically.
6. Confirm the final branch, commit, and worktree state using `git status --short --branch` and `git log -1 --oneline`. Report whether new commits were received or main was already current.

## Failure Handling

- If the pull is rejected because local and remote history diverged, stop. Explain that a merge or rebase decision is required and ask the user which route they want.
- If authentication or network access fails, leave the worktree unchanged and report the failed command's meaning without exposing credentials.
- Do not push, change remotes, install dependencies, run application tests, or modify source files unless the user separately asks.

## Completion Standard

Finish only after `main` is checked out, its update has either succeeded or been shown unnecessary, and the resulting Git state has been displayed. Keep the handoff concise.
