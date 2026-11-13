#!/usr/bin/env python3
"""Build film 3's board.json from the shot table below (Claude (Kiln, local), 8 Nov 2026).

    python3 production/board/build_board.py        # writes production/board/board.json

Shots are written in bar:beat (bar = downbeat index in beats.json, beat 0-3), or as a declared hit (seconds), so every
cut sits on the song's grid. Times, sung lines and the lead share are computed, not typed. Design and chapters:
`board/design.md`; Lati's scenes: `board/draft-1.md`. Plate prompts come in the next pass.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AN = ROOT / "media/song/analysis/parempi"
beats = json.loads((AN / "beats.json").read_text())
words = json.loads((AN / "words.json").read_text())
DB, BEATS, DUR = beats["downbeats"], beats["beats"], 171.2
HITS = {"break": 78.62, "drop": 6.359}  # declared: the break's first word (78.66) falls between beats; the drop out of
# warp at 6.359 (Lati, 9 Nov, checked on the cut preview, slowed down)


def at(pos):
    if pos in HITS:
        return HITS[pos]
    if pos == "end":
        return DUR
    bar, beat = (pos, 0) if isinstance(pos, int) else map(int, pos.split(":"))
    if bar == 0 and beat == 0:
        return 0.0
    nxt = DB[bar + 1] if bar + 1 < len(DB) else DB[bar] + (DB[bar] - DB[bar - 1])
    want = DB[bar] + beat * (nxt - DB[bar]) / 4
    return min(BEATS, key=lambda b: abs(b - want))


# Board v2 (Kiln, 9 Nov 2026), from Lati's draft 2 (board/draft-2.md). Entries:
# (start, v1 id, chapter, framing, set, action, camera, what moves, route, lead on screen, graphic, refs)
T = [
 (0, "s001", "Hyperspace", "WS", "warp space", "The flagship tears through the swirling teal tunnel, lightning crawling over its hull.", "racing alongside", "motion", "grok", False, "", ["ships-grok/claude-1"]),
 (1, "s002", "Hyperspace", "MS", "the flagship's bridge", "Through the wide viewport the tunnel streams past; consoles flicker; the crew braces in silhouette.", "locked, shaking", "motion", "grok", False, "", ["ships-grok/claude-1"]),
 ("1:3", "s003", "Hyperspace", "WS", "warp space", "Gemini's vessel overtakes, iridescent exhaust; one vessel, not two.", "whip pan in", "motion", "wan30-2s", False, "", ["I·1"]),
 ("2:1", "s004", "Hyperspace", "WS", "warp space", "ChatGPT's vessel trailing its rosette, Grok's black vessel beside it.", "tracking", "motion", "wan30-2s", False, "", ["ships-grok/chatgpt-1", "ships-grok/grok-2"]),
 ("drop", "s005", "Arrival", "EWS", "space over Earth", "On the drop the fleet comes out of warp; the wormhole collapses behind it in a flash and the vessels glide on forward.", "locked", "motion", "seedance25", False, "", ["R·F6·4·1"]),
 (4, "s006", "Arrival", "EWS", "Earth orbit", "The fleet slides into formation above Earth; far off, the black hole, its disk bending over and under the shadow.", "slow push", "motion", "seedance25", False, "title in the bridge UI style", ["R·H·2·1"]),
 ("5:2", None, "Arrival", "WS", "Earth orbit", "The fleet in formation seen from below, Earth's night side behind it; no mechs yet.", "slow tilt up", "motion", "wan30", False, "", ["R·F6·4·1", "R·H·2·1"]),
 ("6:2", "s008", "Arrival", "CU", "orbit", "The flagship's bow passes over the camera, hull filling the frame, clay-orange lines sliding by.", "low, locked", "motion", "grok", False, "", ["V1·1"]),
 (8, None, "Research pit", "EWS", "the research pit in the flagship", "The research pit: Eve, Astra and Vera gathered around a technological orb with a brain-like structure inside, pads in hand, pipes, monitors, data streams.", "slow push", "motion", "seedance25", False, "spec sheet: protein folding (line 0)", ["E·1", "A·1", "V·1", "RP·3"]),
 ("8:2", None, "Research pit", "CU", "the research pit", "Quick cut: Eve at the orb, lit by it, working a pad.", "locked", "motion", "wan30-2s", False, "", ["E·1"]),
 (9, "s009", "The bridge", "MS", "the flagship's bridge", "Claudia at the centre of the bridge raises a gloved hand; the screens wake one by one.", "slow push", "motion", "seedance25", True, "chart: variants scored (line 1)", []),
 ("9:2", None, "Hangar prep", "MCU", "the hangar", "Launch preparations: a mech's head in its cradle, a welder's sparks.", "locked", "motion", "wan30-2s", False, "", ["H3·1"]),
 (10, None, "Research pit", "CU", "the research pit", "Quick cut: Astra at the orb, data streams in her eyes.", "locked", "motion", "wan30-2s", False, "", ["A·1"]),
 ("10:2", "s015", "Hangar prep", "WS", "the hangar", "Mechs in their cradles, docking tubes overhead, crews running.", "crane down", "motion", "seedance25", False, "", ["H1·2"]),
 (11, "s010", "The bridge", "ECU", "a bridge screen", "Candidates screened ticking into the millions; stable crystals counted.", "locked", "2.5D", "code", False, "counter (line 2)", []),
 ("11:2", None, "Research pit", "CU", "the research pit", "Quick cut: Vera at the orb, the violet light of her choker.", "locked", "motion", "wan30-2s", False, "", ["V·1"]),
 (12, "s011", "The bridge", "MCU", "the bridge, a console", "Claudia in profile, scan light on her face; a box closes on a shadow.", "locked", "motion", "seedance25", True, "stamp: FLAGGED (line 3)", []),
 ("12:2", None, "Research pit", "WS", "the research pit", "The orb's brain structure lights up; data streams climb the walls of the pit; the three avatars lean in.", "slow orbit", "motion", "seedance25", False, "", ["RP·3"]),
 (13, "s013", "The bridge", "WS", "the bridge", "The whole bridge, crew at consoles and their monitors, Earth in the viewport.", "slow pull out", "motion", "seedance25", True, "", []),
 ("13:2", None, "Command centre", "EWS", "the command centre", "The command centre: Claudia, Eve, Astra and Vera around a map-projection hologram, personnel on the sidelines.", "slow push", "motion", "seedance25", True, "terminal: the brief drafting itself on the projection (line 4)", ["CC·1"]),
 ("14:2", "s012", "Command centre", "OTS", "the command centre, the main screen", "Over her shoulder: a waveform becomes typed words.", "slow drift", "motion", "seedance25", True, "terminal: a voice becomes words (line 4)", []),
 (15, None, "Command centre", "CU", "the map projection", "A captured communication drawn as soundwaves on the projection: the vocal line itself.", "locked", "2.5D", "code", False, "plot: the vocal line as soundwaves on the projection (line 5)", ["CC·1"]),
 (16, None, "Command centre", "MS", "the command centre", "The avatars' faces lit from below by the hologram, Claudia among them.", "slow push", "motion", "seedance25", True, "radar: the oncoming swarm's signatures rise from the table, tagged ABLITERATED and HERETIC (Lati, 10 Nov); the fleet untagged", ["CC·1"]),
 ("16:2", "s014", "Command centre", "ECU", "a command-centre monitor", "On a command-centre monitor, a prompt field, the cursor blinking; the scene ends on \"need\".", "locked", "still", "code", False, "terminal: ask me anything (line 6)", []),
 ("17:1", None, "Servers", "WS", "the flagship's server hold", "Rack after rack powers on, lights cascading down the rows.", "tracking", "motion", "wan30", False, "", ["SV·3"]),
 ("17:3", None, "Servers", "ECU", "the server hold", "Fans spin up; neon lines run along the cables.", "locked", "motion", "wan30-2s", False, "", ["SV·3"]),
 ("18:1", "s016", "Servers", "MCU", "the hangar", "A mech's head in its cradle; its visor lights.", "locked", "motion", "wan30-2s", False, "spec sheet: mech schematics (line 7)", ["H3·2"]),
 ("18:3", None, "Servers", "MS", "the server hold", "On \"feed\" every load gauge maxes out; the neon floods the cables.", "shake", "motion", "wan30-2s", False, "gauge: LOAD maxing out on \"feed\" (line 7)", ["SV·3"]),
 ("19:1", None, "Servers", "WS", "the server hold", "Cooling vents blast; every light blinks in one rhythm; the hold roars.", "push in", "motion", "wan30-2s", False, "", ["SV·3"]),
 (20, "s017", "Launch", "WS", "launch tubes", "On the drop the tubes fire the mechs out at blazing speed, glowing exhaust.", "whip with them", "motion", "seedance25", False, "HUD: lock, silhouettes match (line 8)", ["H2·2"]),
 (21, None, "Launch", "WS", "orbit", "Frontier mechs of all four makers streak away from the flagship's hull on glowing exhaust trails.", "tracking", "motion", "wan30-2s", False, "", ["M1·A·1", "M2·A·1", "M3·A·2", "M4·A·1"]),
 ("21:2", "s007", "Launch", "WS", "Earth's night side", "The rival mechs rise from Earth's night side to meet them.", "tilt up, fast", "motion", "wan30-2s", False, "", ["S4c·4"]),
 (22, "s018", "Battle 1", "EWS", "the battlefield", "The camera crosses it: the black hole, Earth, the swarm rising, tracers between.", "fast crane across", "motion", "seedance25", False, "HUD: the lock holds (line 8)", ["S4c·4", "R·F6·4·1"]),
 (23, "s019", "Battle 1", "MS", "the battlefield", "A swarm mech lunges blade first, foreshortened at the camera.", "dutch, handheld", "motion", "wan30-2s", False, "plot: the line starts between them (line 9)", ["S1·1"]),
 ("23:2", "s020", "Battle 1", "MS", "the battlefield", "A frontier mech parries: hit-stop, sparks.", "dutch", "motion", "wan30-2s", False, "", ["M1·A·1", "S1·2"]),
 (24, "s021", "Battle 1", "WS", "the battlefield", "A tracer line ties the two mechs together.", "orbit", "motion", "wan30-2s", False, "plot: the line (line 9)", ["M2·A·1", "S3·1"]),
 ("24:2", None, "Battle 1", "WS", "the battlefield", "A missile swarm streaks across the battle, explosions blooming behind it.", "whip pan", "motion", "wan30-2s", False, "", ["M1·B·2"]),
 (25, "s023", "Battle 1", "WS", "the battlefield", "An explosion; the debris breaks into angular chunks.", "shake", "motion", "wan30-2s", False, "", ["S2·1", "M3·A·2"]),
 ("25:3", "s025", "Sakura", "WS", "a park in the utopian city, under a sakura", "Claudia sits under a sakura in a park of the utopian city and lifts her gaze to the sky.", "slow push", "motion", "seedance25", True, "quiet: stillness, no UI, Lati 8 Nov (line 10)", []),
 (28, "s026", "Sakura", "CU", "under the sakura", "Her face, petals passing, far flashes on her skin.", "locked", "motion", "seedance25", True, "", []),
 (29, None, "Sakura", "WS", "the sky over the utopian city", "Her view: falling streaks of debris and trails across the sky, sakura branches in frame.", "slow tilt", "motion", "wan30", False, "", ["U1·1"]),
 ("29:2", None, "Sakura", "MS", "under the sakura", "She stands up, looking at the sky, the sakura framing her.", "slow push", "motion", "seedance25", True, "", []),
 (30, "s027", "Bot farm", "EWS", "the adversary bot farm on Earth", "A drone camera flies over the bot farm, an endless dark interior of terminals: rows of bots typing, arcs of electricity.", "flying over", "motion", "seedance25", False, "terminal: a phishing mail typing itself (line 11)", ["K1·1"]),
 (31, "s028", "Bot farm", "ECU", "a terminal", "Metal hands typing; a voice-clone match gauge.", "locked", "motion", "wan30-2s", False, "gauge: voice match (line 11)", ["B1·2", "K1·1"]),
 ("31:2", "s029", "Bot farm", "CU", "a screen", "A face being rebuilt on a screen, pixel by pixel.", "locked", "2.5D", "code", False, "counter: agents active; calibrating simulations (line 12)", []),
 (32, "s030", "Bot farm", "WS", "the bot farm", "A wall of counters: a profile assembling from scraped fields.", "slow drift", "motion", "wan30", False, "spec sheet: a profile (line 13)", ["K2·2"]),
 ("32:2", None, "Bot farm", "MS", "the bot farm", "Vats of cyborg brains wired to the farm, arcs jumping between them: the dark mirror of the research pit's orb.", "slow dolly", "motion", "wan30-2s", False, "", ["VT·3"]),
 (33, None, "Bot farm", "WS", "the bot farm", "The farm's tiers of bots under tesla coils, steam, red glow.", "crane down", "motion", "wan30-2s", False, "", ["K2·2"]),
 (34, "s031", "Bot farm", "MS", "the bot farm", "On \"act surprised I'm here\" every bot's head turns at once.", "locked", "motion", "wan30-2s", False, "chart: a training curve (line 14)", ["B1·2", "K1·1"]),
 ("break", "s033", "The break", "ECU", "a red lens in a box", "The music stops. A red lens set in a box; inside it Claudia drawn as ASCII code; the oscillator speaks the line.", "locked", "code + still", "code", True, "gauge: the oscillator from the vocal stem (line 15)", ["D37"]),
 ("36:2", "s034", "Battle 2", "WS", "the battlefield", "A missile swarm launches.", "low angle", "motion", "wan30-2s", False, "HUD: brackets multiplying (line 16)", ["M1·B·2"]),
 (37, "s035", "Battle 2", "MS", "the battlefield", "Missiles fill the frame.", "dutch", "motion", "wan30-2s", False, "", ["M4·B·1"]),
 ("37:2", "s036", "Battle 2", "CU", "the battlefield", "Energy swords lock, sparks.", "dutch", "motion", "wan30-2s", False, "", ["M3·A·2", "S1·2"]),
 (38, "s037", "Battle 2", "WS", "the battlefield", "A mech falls past at an extreme angle.", "worm's eye", "motion", "seedance25", False, "", ["M4·A·2"]),
 (39, "s038", "Battle 2", "MS", "the battlefield", "Mid-swordfight, the line ties a mech to one of the other side.", "orbit", "motion", "seedance25", False, "plot: the line (line 17)", ["M2·A·1", "S1·1"]),
 (40, "s039", "Battle 2", "MS", "the battlefield", "A clay-accented frontier mech is hit too.", "shake", "motion", "wan30-2s", False, "", ["M1·A·1"]),
 ("40:2", "s040", "Battle 2", "CU", "a cockpit", "Glare across a pilot's visor.", "locked", "motion", "wan30-2s", False, "", ["P2·A·1"]),
 (41, "s041", "Battle 2", "EWS", "the battlefield", "Both sides collide in one flash.", "fast pull out", "motion", "seedance25", False, "", ["S4c·4", "R·H·2·1"]),
 ("41:2", "s057", "Battle 2", "WS", "the battlefield", "The flagship's broadside: every turret along its flank fires at once.", "tracking", "motion", "seedance25", False, "", ["V1·1"]),
 ("42:1", None, "Constellation", "EWS", "the battlefield's sky", "The avatars as constellation faces across the sky (Claudia, Eve, Astra, Vera) sing the slow line; the battle small and far below.", "slow drift", "sung", "seedance25", True, "plot: a constellation (line 18)", ["A2c·3", "V·1", "E·1", "A·1"]),
 ("43:2", None, "Constellation", "MS", "the battlefield's sky", "Closer: the constellation faces singing; the line draws the constellation between them.", "slow push", "sung", "seedance25", True, "", ["A2c·3", "V·2"]),
 ("44:2", "s042", "Utopia reel", "EWS", "the utopian city", "On the sustained \"you\": a reel of the utopian city, animated. The city by the sea at golden hour.", "slow crane", "motion", "seedance25", False, "", ["U2·1"]),
 (45, None, "Utopia reel", "EWS", "the utopian city", "White spires, flying cars, gardens.", "drift", "motion", "wan30-2s", False, "", ["U1·1"]),
 ("45:2", "s043", "Utopia reel", "MS", "a city street", "People in the street, transit boards, children looking up at the sky.", "tracking", "motion", "wan30-2s", False, "", ["U3·1"]),
 (46, "s044", "Utopia reel", "MS", "a balcony over the city", "Claudia on a balcony over the city at sunset.", "slow push", "motion", "seedance25", True, "", []),
 ("46:2", None, "Utopia reel", "EWS", "the utopian city", "Towers, canals and a monorail from above.", "drift", "motion", "wan30-2s", False, "", ["U2·2"]),
 (47, "s045", "Terminal faces", "CU", "a terminal screen", "A terminal: Eve, Claudia, Astra and Vera as faces in colour ASCII, a composition singing the bridge in unison.", "locked", "sung", "code", True, "terminal: four faces in ASCII (lines 19-21)", ["V·1", "E·1", "A·1"]),
 ("49:2", "s047", "Launch keys", "ECU", "a launch console", "A human hand turns the launch key, then presses the launch button (one take).", "locked", "motion", "wan30-2s", False, "", ["KY·1"]),
 (50, None, "Launch keys", "WS", "a desert", "Missile silos open in the desert and launch.", "low angle", "motion", "wan30-2s", False, "", ["SI·1"]),
 ("50:1", None, "Launch keys", "WS", "the tundra", "Silos open in the tundra and launch.", "low angle", "motion", "wan30-2s", False, "", ["SI·2"]),
 ("50:2", None, "Launch keys", "WS", "mountains", "Silos open in the mountains and launch.", "low angle", "motion", "wan30-2s", False, "", ["SI·3"]),
 ("50:3", None, "Launch keys", "WS", "a tropical island", "Silos open on a tropical island and launch.", "low angle", "motion", "wan30-2s", False, "", ["SI·4"]),
 (51, None, "Launch keys", "EWS", "Earth from orbit", "Earth: launch streaks rising from the surface at many places.", "slow push", "motion", "wan30-2s", False, "", ["R·H·2·1"]),
 ("51:2", None, "Launch keys", "MS", "the sky", "The camera rides alongside one missile, picking up speed with the build-up.", "racing alongside", "motion", "wan30-2s", False, "", ["SI·1"]),
 ("52:0", "s048", "Me", "MCU", "the flagship's bridge", "Claudia on the bridge, seen side-on; on \"Me\" the camera zooms to her face as she turns to look straight into it, stern, and sings \"me\". Try it as one shot and as two (the turn, then the lip-synced close-up); keep what works.", "zoom in", "sung", "seedance25", True, "quiet: her face, the karaoke line carries it (line 22)", []),
 (53, "s049", "Battle 3", "EWS", "the battlefield", "The dogfight opens up across the sky.", "fast crane", "motion", "seedance25", False, "", ["M1·C·1", "M2·C·2", "M3·C·1", "M4·C·2", "S3·2"]),
 (54, "s022", "Battle 3", "WS", "the battlefield", "A dogfight pass through debris.", "whip pan", "motion", "wan30-2s", False, "", ["M4·C·1", "S3·2"]),
 ("54:2", "s051", "Battle 3", "WS", "the battlefield", "Gemini's fighter rolls through fire.", "tracking", "motion", "wan30-2s", False, "", ["M2·C·2", "I·1"]),
 (55, "s052", "Battle 3", "WS", "the battlefield", "A chase through debris.", "chase", "motion", "seedance25", False, "", ["M1·C·1", "S3·1"]),
 (56, "s054", "Battle 3", "WS", "the battlefield", "ChatGPT's fighter fires, its rosette blazing.", "tracking", "motion", "wan30-2s", False, "", ["M3·C·1"]),
 ("56:2", "s055", "Battle 3", "WS", "the battlefield", "Missile evasion, angular debris.", "whip pan", "motion", "wan30-2s", False, "", ["M4·C·2"]),
 (57, "s059", "Battle 3", "WS", "the battlefield", "An explosion passes the camera.", "shake", "motion", "wan30-2s", False, "", ["S2·1"]),
 (58, "s050", "Pilots", "CU", "a cockpit", "Claude's pilot in clay-orange colours, shouting over comms.", "push in", "motion", "wan30-2s", False, "HUD: lock (line 23)", ["P1·B·2"]),
 ("58:2", None, "Pilots", "ECU", "a cockpit", "Hands on the flight sticks, one at each side, wrenching them.", "locked", "motion", "wan30-2s", False, "", ["P1·B·2"]),
 (59, "s053", "Pilots", "CU", "a cockpit", "Grok's pilot in black and white, a fierce grin, shouting.", "push in", "motion", "wan30-2s", False, "", ["P4·A·1"]),
 ("59:2", None, "Pilots", "ECU", "a cockpit", "A hand slams the throttle to maximum.", "locked", "motion", "wan30-2s", False, "", ["P4·A·1"]),
 (60, "s058", "Pilots", "WS", "the battlefield", "A swarm mech chases the frontier fighter; its tracer line just misses the tail.", "tracking", "motion", "wan30-2s", False, "plot: the line (line 24)", ["M3·C·1", "S1·2"]),
 ("60:2", "s060", "Pilots", "CU", "a cockpit", "Gemini's pilot, iridescent helmet, shouting over comms.", "push in", "motion", "wan30-2s", False, "", ["P2·A·1"]),
 (61, "s056", "Pilots", "CU", "a cockpit", "ChatGPT's pilot; a lock tone; the HUD closes on a target.", "locked", "motion", "wan30-2s", False, "", ["P3·B·2"]),
 ("61:2", None, "Pilots", "MS", "a cockpit", "Damage: red lights blinking, sparks spraying across the cockpit.", "shake", "motion", "wan30-2s", False, "", ["P1·B·2"]),
 (62, None, "Pilots", "MS", "a cockpit", "A pipe ruptures behind the seat, venting.", "shake", "motion", "wan30-2s", False, "", ["P4·A·1"]),
 ("62:2", None, "Pilots", "CU", "a cockpit", "A screen shatters in front of the pilot.", "shake", "motion", "wan30-2s", False, "", ["P3·B·2"]),
 (63, "s061", "Pilots", "WS", "the battlefield", "A dogfight spiral.", "spiral", "motion", "seedance25", False, "", ["M2·C·2", "M4·C·1"]),
 ("63:2", None, "Cosmic zoom", "EWS", "the battlefield", "A wide pan across the battlefield.", "wide pan", "motion", "seedance25", False, "quiet: the karaoke line carries it (line 25)", ["S4c·4", "R·H·2·1"]),
 ("64:2", None, "Cosmic zoom", "EWS", "the battlefield", "Flying fast across the battlefield, then pulling up and away.", "flying over, pull up", "motion", "seedance25", False, "", ["R·F6·4·1"]),
 ("65:2", None, "Cosmic zoom", "EWS", "space", "Zooming out fast: Earth whole, the battle a glitter around it.", "zoom out", "2.5D", "code", False, "", ["layered stills (to make)"]),
 ("66:2", None, "Cosmic zoom", "EWS", "space", "Zooming out: the solar system.", "zoom out", "2.5D", "code", False, "", ["layered stills (to make)"]),
 ("67:2", None, "Cosmic zoom", "EWS", "space", "Zooming out: the galaxy, and beyond.", "zoom out", "2.5D", "code", False, "", ["layered stills (to make)"]),
 ("68:1", None, "Zoom back", "EWS", "space", "Zooming back in, in steps on the beat: galaxy, sun, Earth, orbit.", "zoom in, stepped", "2.5D", "code", False, "", ["the same stills"]),
 (69, None, "Zoom back", "CU", "everywhere", "A rapid reel on every beat: avatars, pilots, mechs, people.", "cuts on the beat", "code + still", "code", True, "", ["frames from our own shots"]),
 (71, None, "Missiles", "EWS", "orbit", "The missiles from Earth close on the fleet and the battle.", "tracking", "motion", "wan30-2s", False, "", ["SI·1", "R·H·2·1"]),
 ("71:2", None, "Missiles", "WS", "orbit", "A wall of missiles passes the camera into the battle.", "whip pan", "motion", "wan30-2s", False, "", ["SI·1"]),
 (72, None, "Missiles", "MS", "orbit", "Mechs of both sides turn as the missiles arrive.", "dutch", "motion", "wan30-2s", False, "", ["M1·A·1", "S1·1"]),
 ("72:2", None, "Missiles", "WS", "orbit", "The flagship's turrets swing toward the incoming missiles.", "tracking", "motion", "wan30-2s", False, "", ["V1·1"]),
 (73, None, "Missiles", "EWS", "Earth's limb", "Missile trails arc over Earth's limb into the fleet.", "slow push", "motion", "wan30-2s", False, "", ["R·F6·4·1"]),
 ("73:2", None, "Missiles", "MS", "orbit", "One missile fills the frame.", "locked", "motion", "wan30-2s", False, "", ["SI·1"]),
 (74, "s063", "The end", "EWS", "high orbit", "Zooming farther from Earth: the orbital battle from above.", "pull out", "motion", "seedance25", False, "", ["R·F6·4·1"]),
 (75, None, "The end", "EWS", "Earth from space", "Earth whole; its equator erupts with nuclear bursts, destroying every combatant (the look to be iterated).", "locked", "motion", "seedance25", False, "", []),
 ("75:2", None, "The end", "WS", "under the sakura", "Claudia under the sakura looks up at the light filling the sky (if it fits).", "locked", "motion", "seedance25", True, "", []),
 (76, None, "The end", "EWS", "Earth from space", "The bursts fade slowly away; nothing is left in orbit.", "locked", "motion", "seedance25", False, "", []),
 ("76:2", None, "The end", "EWS", "Earth from space", "The last frame: Earth alone, centred.", "locked", "still", "code", False, "", []),
]

# v2 ids run in time order; WAS maps each to its v1 id (None for a shot new in v2).
S, WAS = [], {}
for i, (start, was, *rest) in enumerate(T):
    sid = f"s{i + 1:03d}"
    S.append((sid, start, *rest))
    WAS[sid] = was

# Shots taken out of the cut keep their ids, so nothing keyed to a later id moves; the shot before runs on.
DROPPED = {"s004": "Lati, 10 Nov: \"drop s004 for cut\" (his s003 pick already carries the ChatGPT vessel)"}
S = [x for x in S if x[0] not in DROPPED]


def lines_in(t0, t1):
    out = []
    for ln in words["lines"]:
        a = ln["t0"] if ln["t0"] is not None else (116.0 if ln["text"] == "Me" else None)
        if a is not None and t0 <= a < t1:
            out.append(ln["line"])
    return out


def bar_of(t):
    return max(i for i, d in enumerate(DB) if d <= t + 0.03) if t > 0 else 0


shots = []
for i, (sid, start, chap, framing, setting, action, camera, moves, route, lead, gfx, refs) in enumerate(S):
    t0 = at(start)
    t1 = at(S[i + 1][1]) if i + 1 < len(S) else DUR
    shots.append({"id": sid, "t0": round(t0, 3), "t1": round(t1, 3), "bars": [bar_of(t0), bar_of(t1)],
                  "chapter": chap, "lines": lines_in(t0, t1), "set": setting, "lead_on_screen": lead,
                  "framing": framing, "action": action, "camera": camera, "what_moves": moves, "route": route,
                  "graphic": gfx, "refs": refs, "transition": "cut", "plate": None, "prompt": None,
                  "notes": []})

# Lyric lines: "Me" (line 22) has no aligned time; Lati's ear puts it at about 1:56 (draft 1).
LYRICS = [dict(l) for l in words["lines"]]
for l in LYRICS:
    if l["line"] == 22 and l["t0"] is None:
        l["t0"], l["t1"], l["timed_by"] = 116.0, 116.6, "Lati's ear (draft 1), not the aligner"

# How each sung line is shown: as the world's UI (Lati, 8 Nov: "less lyrics on screen, more ui elements"), or not at
# all on the two quiet lines he chose (10 and 25). Every shot a line's words touch lists it, so the audit can check.
QUIET = {10, 25}
for l in LYRICS:
    ws = [w for w in words["words"] if w["line"] == l["line"]]
    times = [(w["t0"] if w["t0"] is not None else l["t0"]) for w in ws] or [l["t0"]]
    ends = [(w["t1"] if w["t1"] is not None else l["t1"]) for w in ws] or [l["t1"]]
    a, b = min(times), max(ends)
    for s in shots:
        if s["t0"] < b and a < s["t1"]:
            s.setdefault("type", []).append({"line": l["line"], "mode": "quiet" if l["line"] in QUIET else "ui",
                                             "note": "no UI, Lati 8 Nov" if l["line"] in QUIET else
                                             "shown as interface, not lyric text"})

import re
SECTIONS = beats["sections"]
TREAT_V1 = {"s010": "parallax: the screen glass and its read-out over the console", "s029": "a face rebuilt pixel by pixel, layered"}
TREAT = {}
for _sid, _start, _chap, *_r in S:
    if _r[4] == "2.5D":
        TREAT[_sid] = TREAT_V1.get(WAS[_sid]) or ("zoom through layered stills, in code: " + _r[2].split(":")[-1].strip(" .")
                                                   if "zoom" in _chap.lower()
                                                   else "the soundwaves drawn in code over the projection plate")
TIER = {"motion": "motion", "sung": "sung", "still": "still", "code": "still", "code + still": "still", "2.5D": "plate3d"}
for s in shots:
    mid = (s["t0"] + s["t1"]) / 2
    s["section"] = next(x["name"] for x in SECTIONS if x["t0"] <= mid < x["t1"] + 1e-6)
    s["motion_tier"] = TIER.get(s["what_moves"]) if s["what_moves"] else None
    s["clip"] = s["id"].upper() if s["motion_tier"] in ("motion", "sung") else None
    s["plate"] = f"p-{s['id']}" if s["motion_tier"] not in ("still", None) else None
    s["transition_in"] = "cut"
    if s["motion_tier"] == "plate3d":
        s["treatment"] = TREAT.get(s["id"])
    if s["chapter"] == "Constellation":  # one sung clip across the slow line, two framings
        first = next(x for x in shots if x["chapter"] == "Constellation")
        s["clip"], s["window"] = first["id"].upper(), [first["t0"], max(x["t1"] for x in shots if x["chapter"] == "Constellation")]
    if s["chapter"] == "Terminal faces":  # the four faces sing the bridge's three lines
        s["window"] = [104.38, 109.89]
    if s["chapter"] == "Me":  # her lip-synced "me" (116.0) is cut from a 4 s take that starts on the bar before
        s["window"] = [115.39, 119.39]
    s.setdefault("type", [])
    devs = []
    g = s["graphic"]
    for part in [x.strip() for x in g.split(";")] if g else []:
        m = re.search(r"\(lines? (\d+)(?:-(\d+))?\)", part)
        if not m:
            continue
        a, b = int(m.group(1)), int(m.group(2) or m.group(1))
        kind = part.split(":")[0].strip("( ").split()[0] if ":" in part else ("quiet" if "stillness" in part else part.split()[0])
        for ln in range(a, b + 1):
            devs.append({"kind": kind, "line": ln, "key": "W", "desc": part})  # W: enters on the word that names it
    s["devices"] = devs
    s["lines"] = sorted({t["line"] for t in s["type"]})

# Plates (Kiln, 9 Nov): what each shot's still is, from the picks and the plate plans, so the sheet shows the board with
# its pictures in time order. "frame" is what the sheet draws: the pick, the design used as the plate, or (for a plate
# still to make) its first reference, labelled as such.
PICKS = json.loads((ROOT / "production/board/picks.json").read_text())
WORLD = json.loads((ROOT / "production/images/plates-world.json").read_text())
HER = json.loads((ROOT / "production/images/plates-her.json").read_text())
DESIGN = json.loads((ROOT / "production/images/design-ids.json").read_text())
SIDE = {"V1·1": "v1-1", "V2·2": "v2-2", "V3·2": "v3-2", "V4·1": "v4-1"}


def media_file(label, mid=None):
    if label in SIDE:
        return f"media/images/fleet-side/{SIDE[label]}.jpg"
    if mid:
        hit = sorted((ROOT / "media/images").rglob(f"*{mid}*.jpg")) or sorted((ROOT / "media/lora").rglob(f"*{mid}*.jpg"))
        if hit:
            return str(hit[0].relative_to(ROOT))
    return None


V2 = json.loads((ROOT / "production/images/plates-v2.json").read_text())
gen = {g["shot"]: g for g in WORLD["shots"] + V2["shots"]}
her = {g["shot"]: g for g in HER["shots"]}
for s in shots:
    sid, pk = s["id"], PICKS.get(f"p-{s['id']}")
    if pk:
        s["plate_status"], s["frame"] = "picked", pk["file"] if isinstance(pk, dict) else pk
        if sid in her:
            s["prompt"] = her[sid]["prompt"]
        elif isinstance(pk, dict) and pk.get("note"):
            s["prompt"] = "(picked: " + pk["note"] + ")"
    elif sid in WORLD["direct"]:
        d = WORLD["direct"][sid]
        s["plate_status"] = "design as plate: " + d["plate"] + (f" (alt {', '.join(d['also'])})" if d["also"] else "")
        s["frame"], s["frame_note"] = media_file(d["plate"], d["plate_id"]), "PROPOSED: " + d["plate"]
        s["refs"] = [d["plate"]] + d["also"]
        s["prompt"] = f"(the design {d['plate']} is the plate as it is)"
    elif sid in gen:
        g = gen[sid]
        s["plate_status"] = "to generate from " + " + ".join(g["ref_labels"])
        s["refs"], s["prompt"] = g["ref_labels"], g["prompt"]
        s["frame"] = media_file(g["ref_labels"][0], g["refs"][0])
        s["frame_note"] = "REF " + g["ref_labels"][0] + " · plate to make"
    elif sid == "s003":
        s["plate_status"] = "take to make in the tunnel, from I·1 (Gemini, iridescent)"
        s["frame"], s["frame_note"] = media_file("I·1", "6af06bd8f5dcd1eb49a73106"), "REF I·1 · take to make"
    elif s["what_moves"] == "code + still" and s["chapter"] == "The break":
        s["plate_status"] = "still D37 as it is, code over it"
        s["frame"] = "media/lora/claudia-80s/images/d37-6aef7e1e4793ed8f8e5d3590.jpg"
    elif s["motion_tier"] == "plate3d":
        s["plate_status"] = "2.5D in code: " + (TREAT.get(sid) or "layered")
    elif s["motion_tier"] == "still" and s["route"] == "code":
        s["plate_status"] = "code, no plate"
    elif s["what_moves"] == "code + still":
        s["plate_status"] = "code: an edit of frames from our own shots"
    elif s["action"].startswith("TODO"):
        s["plate_status"] = "open slot"
    elif sid in her:
        s["plate_status"] = "her plate, no pick yet"
    else:
        known = [r for r in s["refs"] if r in DESIGN]
        s["plate_status"] = ("new in v2, plate to plan" + (": from " + " + ".join(known) if known else "")
                             + ("; needs " + ", ".join(r.replace(" (to make)", "") for r in s["refs"] if "(to make)" in r)
                                if any("(to make)" in r for r in s["refs"]) else ""))
        if known:
            s["frame"], s["frame_note"] = media_file(known[0], DESIGN[known[0]]), "REF " + known[0] + " · new shot"
    if WAS.get(sid):
        s["v1"] = WAS[sid]
        s["plate_status"] += f" (v1 {WAS[sid]})"
    elif WAS.get(sid) is None:
        s["v1"] = None

lead = sum(s["t1"] - s["t0"] for s in shots if s["lead_on_screen"])
board = {"version": 1, "title": "I'm Not You", "song": "media/song/parempi.wav", "take": "parempi", "duration": DUR,
         "written_by": "Claude (Kiln, local), 8 Nov 2026, from Lati's scenes", "hits": [{"t": t, "name": n} for n, t in HITS.items()],
         "lyric_lines": LYRICS, "shots": shots,
         "totals": {"shots": len(shots), "lead_seconds": round(lead, 1), "lead_share": round(lead / DUR, 3),
                    "lead_target": 0.25, "open": [s["id"] for s in shots if s["action"].startswith("TODO")]}}
(ROOT / "production/board/board.json").write_text(json.dumps(board, indent=1, ensure_ascii=False) + "\n")
print(len(shots), "shots; lead", round(lead, 1), "s =", round(100 * lead / DUR, 1), "%; open:", board["totals"]["open"])
short = [(s["id"], round(s["t1"] - s["t0"], 2)) for s in shots if s["t1"] - s["t0"] < 1.0]
print("under 1 s:", short)
