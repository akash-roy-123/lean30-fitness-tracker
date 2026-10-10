# LEAN / 30 — Personal Fitness Tracker

A clean, responsive and **offline-first** 30-day fitness tracker for muscle recomposition. Built with plain HTML, CSS and vanilla JavaScript. No build step, frameworks, accounts or external dependencies.

## Features

- Daily tracker for **30 days** with automatically saved entries
- Tracks **protein, calories, water, sleep, daily steps, weight, waist, training, walking and notes**
- Push / Pull / Legs × 2 training schedule with recovery day
- Budget-friendly Indian meal framework using **regular curd**
- Interactive graphs of logged weight and waist measurements
- Weekly rollups for logged days, average protein, weight, latest waist and completed workouts
- Customizable challenge start date, protein, calorie and step targets
- CSV export, JSON backup/restore and printable layout
- Browser-only `localStorage` — data stays on your device

## Run locally

Open `index.html` in a browser. The app needs no dependencies and no server.

## Publish to GitHub Pages

1. Create a GitHub repository named `lean30-fitness-tracker` on your account.
2. Add the files at the **repository root**: `index.html`, `styles.css`, `app.js`, `favicon.svg`, `README.md`.
3. Open repository **Settings → Pages → Build and deployment**.
4. Choose **Deploy from a branch**, select `main` and `/ (root)`, and save.
5. GitHub Pages will provide a URL such as `https://akash-roy-123.github.io/lean30-fitness-tracker/` after deployment.

Or upload locally with Git once the empty repository has been created:

```bash
git init
git add .
git commit -m "feat: add offline 30-day fitness tracker"
git branch -M main
git remote add origin https://github.com/akash-roy-123/lean30-fitness-tracker.git
git push -u origin main
```

## Data & privacy

Tracking data is stored on **each browser and device separately**, not in the GitHub repo. GitHub Pages is static hosting and does **not** sync or persist logs across devices. Use **Backup** to download a JSON file and **Restore JSON backup** on another browser or device. Export CSV for spreadsheet analysis.

## Health and fitness disclaimer

The sample targets are provisional estimates, not medical advice. Individual calorie needs vary with height, age, daily movement, body composition and training intensity. Adjust using multi-week trends and professional advice where appropriate. Nutrition figures are approximate and differ by brand and portion size. Creatine content differs between whey formulations; verify the supplement's label.