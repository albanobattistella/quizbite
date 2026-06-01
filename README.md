<p align="center">
  <img src="data/icons/hicolor/scalable/apps/dev.mohfy.quizbite.svg" alt="Quizbite Logo" height="128">
</p>
<h1 align="center">Quizbite</h1>
<p align="center"><em>Informative quizzes, bite sized.</em></p>



<div align="center">
  <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 1em;">
    <a href="https://flathub.org/apps/dev.mohfy.quizbite">
      <img width="190" alt="Download on Flathub" src="https://flathub.org/api/badge?locale=en" />
    </a>
  </div>
</div>

## Features:
- Create quizzes with multiple choice questions.
- add images to question.
- Import and export `.quiz` files.
- Import Flashcards and play them.
- Export a quiz or flashcards to PDF.

## Screenshots
<div align="center" style="display: flex; justify-content: center; align-items: center; gap: 5%;">
  <img src="data/screenshots/Quiz Library.png" alt="Quiz Library" style="height:300px; object-fit: contain;">
  <img src="data/screenshots/Quiz Player.png" alt="Quiz Player" style="height:300px; object-fit: contain;">
</div>


## Build And Run

Open the project in GNOME Builder and run it there.

GNOME Builder handles the build automatically for this project.

## Flatpak

The Flatpak manifest is `dev.mohfy.quizbite.json`.

```bash
flatpak-builder builddir dev.mohfy.quizbite.json --user --install --force-clean
flatpak run dev.mohfy.quizbite
```

## Translations
- Add `po/<lang>.po`
- Add `<lang>` to `po/LINGUAS`

