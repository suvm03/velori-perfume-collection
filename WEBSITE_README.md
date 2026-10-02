# VELORI website

A static HTML/CSS/JavaScript presentation of the complete perfume concept collection. No server-side application, build framework or account is required for visitors.

## Browse locally

Open `index.html` in a browser, or run `python -m http.server 8000` in the project directory and visit `http://localhost:8000`.

## Files

- `index.html`: complete landing page and detail-dialog markup.
- `styles.css`: responsive visual design.
- `app.js`: gallery, search, collection/category filters, views and deep links.
- `assets/collection-data.js`: all 24 specifications; generated from `Source_Files/concepts.json`.
- `assets/designs/`: lightweight WebP previews; original full-resolution PNGs remain downloadable.
- `downloads/`: 24 individual design packs and a complete collection ZIP.
- `.github/workflows/deploy.yml`: automatic GitHub Pages deployment from `main`.

## Regenerate

Run `python Source_Files/build_all.py` to regenerate the original design deliverables. Run `python Source_Files/build_website_assets.py` to regenerate browser previews and archives. These scripts require the Python packages in `Source_Files/requirements.txt`.

The optional browser verification script `Source_Files/check_website.py` uses Chrome on Windows and the `websocket-client` package. Results and desktop/mobile screenshots are stored in `Quality_Checks/` locally. Font loading uses Google Fonts with Arial/Georgia fallbacks.

## Deployment

Push to the `main` branch and configure GitHub Pages with GitHub Actions as the publishing source. The included workflow publishes this repository as a static site. All asset and download links are relative so the site works under a repository subpath.

The collection is conceptual vector design artwork. Engineering, testing, formula development, trademark clearance and printer-approved artwork remain separate development steps.
