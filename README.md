# Sweet-Butters.github.io

Personal portfolio, served at **https://sweet-butters.github.io/**.

A single static `index.html` (no build step). The featured project is written by hand; the
repository list is fetched live from the GitHub API, so new public repositories show up automatically.

Edit `index.html` and push to `main` — GitHub Pages redeploys in about a minute.

## English and Korean pages

`/work/` and `/jev/` are English by default; `/ko/work/` and `/ko/jev/` are the Korean pages to share in Korea.
The Korean pages are generated: edit `work/index.html` or `jev/index.html` (they hold both languages), then run
`python tools/make_ko.py` and commit the regenerated files under `ko/`.
