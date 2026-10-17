# A/D Battle Map

A live world-map screen for an attack-defense CTF run on the
[FAUST ctf-gameserver](https://github.com/fausecteam/ctf-gameserver).
Opening `index.html` with no settings runs the built-in demo: it simulates a FAUST server that
emits the same JSON and scores with FAUST's formula.

Files: `index.html` (the page), `world-geo.js` (map data, must sit next to the page),
`build-world-geo.mjs` (regenerates the map data).

## Data the page reads

| Endpoint | What it uses |
|---|---|
| `/competition/scoreboard.json` | `tick` (last scored tick), and for each team: `rank`, `name`, `offense`, `defense`, `sla`, `total`, `thumbnail`, plus each service's `status`, `offense`, `defense`, `sla` |
| `/competition/status.json` | `services` (service names; scoreboard.json does not include them) |

Status codes follow `StatusCheck.STATUSES`: 0 up, 1 down, 2 faulty, 3 flag not found, 4 recovering,
missing value or 5 = not checked.

FAUST does not publish who attacked whom. The map draws attacks from each tick's point changes:
teams that gained offense points become attackers, and teams that lost defense points become targets.
The pairs are plausible but not real, as the footer on the map says.

## Connecting to a real gameserver

1. Edit `CONFIG` near the top of the `<script>` in `index.html`:
   - `competition`: the event name shown in the header.
   - `faust.url`: the gameserver base URL. `""` means the same host as the page.
   - `faust.tickSeconds`, `faust.start`, `faust.end`: copy from *Game Control* in the gameserver
     admin. The JSON API does not expose them; the tick countdown needs them.
   - `locations`: team name → `[city, latitude, longitude]`. Unlisted teams get a free city
     automatically.
2. Serve the folder from the same origin as the gameserver, for example with nginx next to the
   Django site:

   ```nginx
   location /battlemap/ {
       alias /srv/battlemap/;
   }
   ```

   Then open `https://<gameserver>/battlemap/` with `faust.url` set to `""`.
   Browsers block cross-origin requests unless the gameserver sends CORS headers, so loading the
   page from another host only works if you add those headers.
3. To try a server without editing the file, add `?faust=https://<gameserver>` to the page address.

The page polls every `faust.pollSeconds` (default 15). FAUST caches the scoreboard JSON for a few
seconds, so polling faster gains nothing.
