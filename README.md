# animacie-a-ine

Manim animations, organized as `src/<subject>/<lesson>.py` (e.g. `src/inf/zaklady_pythonu.py`).
Requires [Manim](https://www.manim.community/) and LaTeX.

## Quick start

```sh
make new FILE=src/inf/rekurzia.py  # start a new lesson from the template
make preview                       # quick 480p render of the file you last edited
make open                          # final 4K render, then open it
```

Run `make` on its own to see every command.

## Commands

| Command          | What it does                                          |
| ---------------- | ----------------------------------------------------- |
| `make preview`   | Fast low-quality render (480p mp4), then open it      |
| `make open`      | Render at full quality, then open it                  |
| `make render`    | Render without opening                                |
| `make still`     | Render only the last frame as a PNG, then open it     |
| `make list`      | List animations and their scenes                      |
| `make new`       | Create a new lesson file from the template            |
| `make all`       | Render every animation                                |
| `make clean`     | Delete caches (`make clean-all` also deletes renders) |

## Options

Add them after the command, e.g. `make open FILE=zaklady_pythonu SCENE=FunctionsAsPrograms Q=h`.

| Option   | Meaning                                                       | Default            |
| -------- | ------------------------------------------------------------- | ------------------ |
| `FILE`   | Lesson path or just its name (`src/` and `.py` optional)      | last edited file   |
| `SCENE`  | Scene class to render                                         | all scenes in file |
| `Q`      | Quality: `l` 480p · `m` 720p · `h` 1080p · `p` 1440p · `k` 4K | `k`                |
| `FORMAT` | `mov`, `mp4`, `gif` or `webm`                                 | `mov`              |
| `ARGS`   | Extra flags passed to manim, e.g. `ARGS="-n 3,5"`             | none               |

## Output

Finished files go to `renders/<subject>/<lesson>/<quality>/`, for example
`renders/inf/zaklady_pythonu/2160p60/FunctionsAsPrograms.mov`.

## Tips

- Don't use spaces in file names: Make can't handle them.
- Don't set the resolution or frame rate inside a scene file, because it overrides `Q`.
