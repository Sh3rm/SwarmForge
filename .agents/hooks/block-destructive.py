#!/usr/bin/env python3
# PreToolUse guard — deterministic enforcement layer of Rule 02 (Destructive Action Barrier).
# Antigravity hooks contract (antigravity.google/docs/hooks): the hook receives the tool-call
# JSON on stdin ({"toolCall": {"name": "run_command", "arguments": {...}}, ...}); responding
# with {"decision": "deny"} on stdout (and/or a non-zero exit code) hard-blocks the call.
import json
import re
import sys

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)  # not parseable -> do not block

tool_call = data.get("toolCall") or {}
if tool_call.get("name") not in (None, "run_command"):
    sys.exit(0)  # the hooks.json matcher already scopes us to run_command


def collect_strings(node):
    # run_command's exact argument key is not pinned by the docs, so scan every
    # string in the arguments payload instead of trusting a single key name.
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for value in node.values():
            yield from collect_strings(value)
    elif isinstance(node, list):
        for value in node:
            yield from collect_strings(value)


cmd = " ".join(collect_strings(tool_call.get("arguments") or {}))


def block(reason):
    print(
        json.dumps(
            {
                "decision": "deny",
                "reason": (
                    f"BLOCKED by Destructive Action Barrier (Rule 02): {reason}. "
                    "This operation requires explicit human approval — ask the operator instead."
                ),
            }
        )
    )
    sys.exit(2)


# rm with both recursive and force flags (any order, combined or separate, incl. long
# forms, absolute paths like /bin/rm, and rm reached via xargs)
for segment in re.split(r"[|;&]", cmd):
    tokens = segment.split()
    if any(t == "rm" or t.endswith("/rm") for t in tokens):
        flags = " ".join(t for t in tokens if t.startswith("-"))
        recursive = bool(re.search(r"-\w*[rR]|--recursive", flags))
        force = bool(re.search(r"-\w*f|--force", flags))
        if recursive and force:
            block("recursive force-delete (rm -rf)")

PATTERNS = [
    (r"\bmkfs(\.\w+)?\b", "filesystem format (mkfs)"),
    (r"\bdd\b[^|;&]*\bof=/dev/", "raw write to a block device (dd of=/dev/...)"),
    (r"\bgit\s+push\b[^|;&]*(\s--force\b|\s-f\b)", "force push (git push --force)"),
    (r"\bgit\s+push\b[^|;&]*\s\+\S+", "force push via refspec (git push origin +branch)"),
    (r"\bfind\b[^|;&]*\s-delete\b", "bulk delete (find ... -delete)"),
    (r"(?i)\bdrop\s+(database|table|tablespace|schema)\b", "SQL DROP statement"),
    (r"\bterraform\s+(destroy|apply\s+-destroy)\b", "terraform destroy"),
    (r"\bkubectl\s+delete\s+(namespace|ns)\b", "kubectl namespace deletion"),
    (r"\baws\s+\S+\s+(delete|terminate)-\S+", "AWS resource deletion"),
    (r"\bgcloud\b[^|;&]*\bdelete\b", "GCP resource deletion"),
]
for pattern, reason in PATTERNS:
    if re.search(pattern, cmd):
        block(reason)

sys.exit(0)
