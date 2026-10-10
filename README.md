# LEAN / 30 — Fitness Dashboard

A responsive 30-day strength, nutrition and body-recomposition tracker. Built with **plain HTML, CSS and JavaScript**. No accounts, build step, third-party libraries, ads or trackers.

## What it does

- Interactive home dashboard with a **today-at-a-glance** protein and steps summary.
- Thirty-day log for protein, calories, water, sleep, steps, body weight, waist, RPE, supplement and walking checkboxes, and notes.
- Six-day **Push / Pull / Legs × 2** strength plan plus weekly recovery day.
- Indian nutrition guide that swaps costly Greek yogurt for regular curd.
- Weight and waist charts, weekly averages, and 30-day consistency indicators.
- Customize challenge start date and daily protein, calories, and step targets; labels and nutrition macro estimates update immediately.
- Mobile-friendly **bottom navigation** and improved layouts down to a 320px-wide screen.
- Local browser storage, CSV export, JSON backup/restore, and reset with confirmation.

## Run

Open `index.html` in a modern browser, or serve this directory as a static website (`python -m http.server 8000`). No npm install needed.

## GitHub Pages

Repository: [`akash-roy-123/lean30-fitness-tracker`](https://github.com/akash-roy-123/lean30-fitness-tracker)

If your account and repository are eligible for Pages: **Settings → Pages → Deploy from a branch → `main` → `/ (root)` → Save**.

Expected published address once deployment succeeds:
`https://akash-roy-123.github.io/lean30-fitness-tracker/`

> Repository visibility and plan eligibility affect Pages availability. The URL is not live until GitHub completes deployment.

## Browser testing

The source includes a smoke suite that checks five routes across 1440px, 768px, 390px and 320px viewports, form validation, persisted logs, customized targets, export, reset, restore, and chart generation.

```bash
pip install playwright
playwright install chromium
python tests/browser_smoke.py
```

The automated smoke suite uses a localStorage shim and inlines resources to make it runnable without a local server. Standard-browser localStorage must be tested on your actual browser/device, since browser privacy settings can vary.

## Privacy and backup

Your logs reside in **browser localStorage**, not in the GitHub repository. They do **not** sync across devices and may be lost if browser data is cleared or your device is reset. Use **Backup** regularly and **Restore JSON backup** on another device. CSV export is for analysis. Avoid logging sensitive information in a browser profile shared with others.

## Nutrition note

The initial 2,300 kcal, 160 g protein and 7,000 steps are working targets, not personalized medical prescriptions. Macros are estimates. A protein shake is optional; check your supplement packaging for serving size and creatine content.
