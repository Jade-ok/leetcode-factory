# LeetCode Notes

A standalone HTML site with two sections:

- **Problems**: an individual, freeform note for each problem.
- **Topics**: a master note for each topic, linked to the problems assigned to it.

The interface is in English and uses a neutral gray theme. Open `index.html` in a modern browser. No installation, account, server, or network connection is required.

## Writing

Each note has a title and one Markdown body. Write text, insert code blocks anywhere, and continue writing. Use **Insert code**, **Heading**, **Bold**, **List**, or **Link** in the toolbar, or paste Markdown directly. **Preview** shows the reading view. A note can contain multiple code blocks in different languages.

Problem numbers, topics, difficulty, tags, links, and dates are optional properties. Topic master notes start with editable concepts and Python templates; new topics start blank. Existing user-written content is preserved. Unedited built-in notes from older versions are updated to the English defaults.

- `Tab` / `Shift Tab`: indent / reduce the indentation at the start of a line.
- `Cmd B` / `Ctrl B`: bold the selection.
- `Cmd Enter` / `Ctrl Enter`: save the note.
- `Cmd K` / `Ctrl K`: search problems and topics.

## Saving and backup

Notes are saved in this browser using `localStorage`. The original HTML file is not modified automatically.

Open **Backup & export** to:

- **Download HTML**: export the site with all current notes embedded in one portable file.
- **Export JSON**: back up the data separately.
- **Import JSON**: validate a backup, review its counts, and replace the current data after confirmation.

Use HTML or JSON export to move notes between devices or browsers. There is no automatic synchronization. Each exported HTML file has its own storage identity. Edit a notebook in one tab at a time; concurrent writes are blocked to avoid overwriting another tab's changes.

Earlier structured backups and freeform backups are supported. User text and code are retained during migration. The editor displays raw HTML as text and does not run stored code.

Use **Print** on a problem note to print it or save it as a PDF through the browser.
