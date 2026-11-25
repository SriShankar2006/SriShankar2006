# Profile setup

## Repository

The profile repository is `SriShankar2006/SriShankar2006`. Push this repository to its `main` branch.

```powershell
cd C:\Users\Admin\Desktop\ReadMe\SriShankar2006
git add .
git commit -m "feat: create premium GitHub profile"
git push origin main
```

## Automatic visuals

Enable GitHub Actions in repository **Settings > Actions > General**.

- `contribution-grid.yml` uses the built-in `GITHUB_TOKEN` GraphQL permission to generate actual one-year contribution data.
- `profile-3d.yml` generates the separate 3D calendar.
- `contribution-snake.yml` publishes SVG output to the `output` branch.
- `profile-metrics.yml` generates a metrics asset in `assets/generated/`.

No personal access token is required for normal repository features. The built-in `GITHUB_TOKEN` is rotated automatically and must not be copied into files or README content.

## Initial generation

Open **Actions**, run each workflow manually with **Run workflow**, then wait for success. If workflow writes are rejected, set **Settings > Actions > General > Workflow permissions** to **Read and write permissions**.

The snake workflow needs the target `output` branch. It creates and publishes it through the GitHub Pages action.

## Validation

```powershell
python scripts\validate_readme.py
python -m py_compile scripts\generate_contributions.py scripts\validate_readme.py
```

For a local contribution-grid test, provide a fine-grained token with read access to public profile contribution data:

```powershell
$env:GITHUB_TOKEN="replace-in-shell-only"
python scripts\generate_contributions.py
```

Never commit the token. Delete it from the shell after testing.

## Troubleshooting

- **Empty or missing 3D asset:** Run `profile-3d.yml`, then verify `profile-3d-contrib/profile-night.svg` exists.
- **Snake image missing:** Verify the `output` branch contains `github-contribution-grid-snake.svg`; workflow permissions must permit branch pushes.
- **Statistics unavailable:** GitHub Readme Stats and activity services may have temporary outages. Refresh later; no local secret is needed.
- **External image blocked:** The README includes direct public URLs and a local project/banner fallback structure. Replace unavailable project thumbnails locally only after confirming their source.
- **Workflow validation:** Review the Actions log for exact action or permission failures. Workflow YAML is valid with the GitHub Actions interpreter; third-party action success depends on maintained upstream compatibility.
