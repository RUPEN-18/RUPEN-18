# Profile animation assets

These banners are custom graphics for Rupendran's GitHub profile. They are decorative illustrations, not photographs or recordings of a physical robot. They contain no third-party image assets and make no runtime network requests.

| File | Animation |
| --- | --- |
| `hero.gif` | Radar sweep, rover wheels, arm motion, and a progress signal |
| `workbench.gif` | Rotating typed focus statements |
| `signal.gif` | Moving circuit-style divider |
| `build-loop.gif` | Build, test, learn, repeat sequence |

Each animation has a matching `-still.png` first frame, used by the profile's reduced-motion picture sources. All animation text has a static equivalent or descriptive alt text in the profile README.

## Regenerate

From the repository root:

```bash
python -m pip install -r scripts/requirements-profile.txt
python scripts/render_profile.py
```

The renderer uses DejaVu Sans on Linux, Arial on Windows/macOS where available, and Pillow's default font as a fallback. Font changes can affect layout, so review the resulting banners before committing.

The contribution snake is generated separately by the existing `.github/workflows/snake.yml` workflow and published to the `output` branch.
