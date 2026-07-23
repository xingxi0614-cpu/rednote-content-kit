# Release Procedure

1. Complete the patent decision in `PATENT-AND-LICENSING.md`; MIT is already selected and must not be changed without a documented decision.
2. Verify ownership and redistribution rights for every tracked file.
3. Verify that `LICENSE` is the unmodified MIT text with the intended generic copyright holder.
4. Verify that `.codex-plugin/plugin.json` contains the SPDX identifier `MIT`.
5. Replace installation placeholders only after the final GitHub owner and repository name are known.
6. Remove `RELEASE-HOLD.md` only after every checkbox is satisfied.
7. Run:

   ```bash
   python3 -m unittest discover -s tests -v
   python3 tools/audit_release.py . --release
   ```

8. Review the complete staged file list and diff.
9. Before the first commit, configure a public-safe Git author identity and a GitHub-provided `noreply` email. Existing commit metadata cannot be made private merely by changing the setting later.
10. Create a private GitHub repository first; enable secret scanning, push protection, and private vulnerability reporting.
11. Never bypass a secret-scanning or push-protection alert merely to finish the release.
12. Show the exact repository, visibility, README, license, commit identity, and release contents to the owner.
13. Obtain current explicit approval before changing visibility to public or publishing a release.
14. Tag the verified commit as `v0.1.0`; attach only artifacts built from that commit.

Never rewrite history to hide a leaked secret. Revoke or rotate the secret first, then remove it from history and verify the remediation.
