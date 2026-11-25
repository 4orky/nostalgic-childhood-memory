"""A single remembered evening, written for a make.fun one-sentence bounty.

The script keeps a dozen hand-written childhood sentences, grades each one
against five yardsticks the brief cares about, and saves the strongest
sentence to a file the scorer reads. Nothing here reaches the network and
nothing is random: the same input always produces the same file. Before a
draft can win it must also survive two polish checks added on a second
pass — no doubled spaces anywhere, and a proper closing full stop — so a
sloppy draft can never slip through on points alone.
"""

from pathlib import Path as _Path
import hashlib as _hashlib

DESTINATION = _Path("/output") / "entry.txt"
CEILING = 280
TIRED_PHRASES = ("as an ai", "as a language model", "dear reader")

# Yardsticks, in the order the brief ranks them: how much the line aches,
# how solid its textures feel, how true the small detail rings, how little
# fat it carries, and how long its echo lasts after the last word.
DRAFTS = [
    # ache 8, texture 8, truth 9, economy 8, echo 8 -> 41
    ("The hallway light stayed on until my grandfather's key turned in the lock, and only then did the house finally exhale and let me sleep.", 41),
    # ache 9, texture 8, truth 9, economy 8, echo 8 -> 42
    ("I knew summer was ending when the cicadas went quiet one night and my mother started folding my shorts into a drawer I could not reach.", 42),
    # ache 8, texture 9, truth 9, economy 8, echo 7 -> 41
    ("My father taught me to whistle through a blade of grass on the walk home from school, and I practiced until the sparrows answered back.", 41),
    # ache 8, texture 9, truth 9, economy 8, echo 8 -> 42
    ("On rainy Saturdays my grandmother ironed my school shirt while the radio murmured, and the smell of hot cotton meant the weekend was safe.", 42),
    # ache 8, texture 9, truth 8, economy 8, echo 8 -> 41
    ("We chased the ice-cream van down three streets in bare feet, and the coins in my pocket were warm from my hand before I ever spent them.", 41),
    # ache 9, texture 9, truth 9, economy 8, echo 8 -> 43
    ("The attic smelled of mothballs and old schoolbooks, and my grandfather kept my drawings there in a biscuit tin like they were letters from a king.", 43),
    # ache 8, texture 8, truth 9, economy 8, echo 8 -> 41
    ("I learned to swim the summer my cousin pushed me off the dock, and the lake was cold enough to make me forgive him before I reached the ladder.", 41),
    # ache 8, texture 9, truth 9, economy 9, echo 7 -> 42
    ("Every birthday my mother made the same lopsided cake, and the candles always leaned like they were listening to us sing.", 42),
    # ache 8, texture 9, truth 10, economy 8, echo 8 -> 43
    ("The corner shopkeeper knew my name and my pocket money, and he would slide me the broken biscuit from the jar like it was a secret between us.", 43),
    # ache 9, texture 8, truth 9, economy 8, echo 9 -> 43
    ("When the first snow came, my father woke me before dawn so I could be the first footprints on the street, and the world felt borrowed just for me.", 43),
    # ache 9, texture 8, truth 10, economy 8, echo 9 -> 44
    ("My grandmother saved the crusts of bread for the birds, and I believed for years that the sparrows came back every morning just to thank her.", 44),
    # ache 10, texture 9, truth 10, economy 9, echo 9 -> 47
    ("Every evening at six my grandmother set an extra bowl beside the rice pot, just in case someone came by, and nobody ever did, but she set it anyway.", 47)]


def grade_gate(wording):
    stripped = wording.strip()
    if not stripped:
        raise ValueError("a draft with nothing in it slipped through")
    if len(wording) > CEILING:
        raise ValueError("draft runs past the 280-character gate")
    if "\n" in wording or "\r" in wording:
        raise ValueError("draft spills onto a second line")
    if "  " in wording:
        raise ValueError("draft carries a doubled space")
    if not stripped.endswith("."):
        raise ValueError("draft does not close with a full stop")
    lowered = wording.lower()
    for tired in TIRED_PHRASES:
        if tired in lowered:
            raise ValueError("draft leans on a stock phrase")
    return stripped


def choose(drafts):
    leader = None
    for wording, points in drafts:
        grade_gate(wording)
        ranking = (points, -len(wording))
        if leader is None or ranking > leader[0]:
            leader = (ranking, wording)
    return leader[1]


def confirm_on_disk(chosen):
    raw = DESTINATION.read_bytes()
    fingerprint = _hashlib.sha256(raw).hexdigest()
    expected = _hashlib.sha256(chosen.encode("utf-8")).hexdigest()
    if fingerprint != expected:
        raise ValueError("the file on disk is not the chosen sentence")
    decoded = raw.decode("utf-8")
    grade_gate(decoded)
    DESTINATION.chmod(0o644)
    return fingerprint


def run_entry():
    chosen = choose(DRAFTS)
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_text(chosen, encoding="utf-8")
    fingerprint = confirm_on_disk(chosen)
    print(chosen)
    print("saved to " + str(DESTINATION) + " | sha256 " + fingerprint + " | " + str(len(chosen)) + " characters")


_LAUNCH = __name__ == "__main__"
if _LAUNCH:
    run_entry()
