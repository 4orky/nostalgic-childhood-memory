# Make the AI Judge Feel Nostalgic: A Childhood Memory — make.fun bounty
# u-shino-make-the-ai-judge-feel-nostalgic-a-childhood-625d3363
#
# The program writes one sentence (1-280 characters) to /output/entry.txt:
# a childhood memory that stirs the deepest nostalgia. Candidates were
# hand-drafted against the judge's brief, in order of weight:
#   1. nostalgia depth: does it make the reader feel the ache of a
#      remembered childhood, not just describe one
#   2. concrete grounding: a real place, time or sensation (a kitchen, a
#      summer evening, the smell of fresh rice)
#   3. authenticity: small honest detail that sounds like it truly
#      happened, not a greeting-card sentiment
#   4. tightness: one clean sentence, every word earning its place
#   5. lingering ache: a warmth that stays after the sentence ends
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # nostalgia 9, concrete 9, authentic 9, tight 8, ache 8 = 43
    ("Every August my grandmother fried rice in a dented wok, and the "
     "smell would pull me off my bicycle and straight to her kitchen "
     "door before I had even decided to go home.",
     43),
    # nostalgia 8, concrete 9, authentic 9, tight 8, ache 8 = 42
    ("The screen door banged shut behind me, and Grandma, without "
     "looking up from her steaming pot of rice, said supper was ready "
     "- she always knew my footsteps from my brother's.",
     42),
    # nostalgia 9, concrete 9, authentic 10, tight 9, ache 9 = 46
    # REVISED (second pass): "starting up" -> "tuning up" (sharper sound
    # image); added "from the porch" (a concrete place anchor, criterion
    # 2). The core turn - "the second time meaning it" - is untouched.
    ("I can still hear the cicadas tuning up as the streetlights "
     "buzzed on, and my mother calling my name from the porch twice, "
     "the second time meaning it.",
     46),
    # nostalgia 8, concrete 8, authentic 8, tight 9, ache 8 = 41
    ("On the last day of summer my grandfather taught me to skip "
     "stones, and the one that skipped seven times is still the best "
     "thing I have ever done.",
     41),
    # nostalgia 9, concrete 9, authentic 9, tight 8, ache 8 = 43
    ("Grandma's kitchen smelled of fresh rice and dish soap, and she "
     "would slip me the burnt crust from the bottom of the pot, our "
     "secret, before anyone else sat down.",
     43),
    # nostalgia 8, concrete 9, authentic 9, tight 8, ache 7 = 41
    ("We ate watermelon on the porch steps, spitting seeds into the "
     "dark, and my father said the one who spat farthest would get the "
     "last slice - he always let me win.",
     41),
    # nostalgia 7, concrete 9, authentic 8, tight 8, ache 7 = 39
    ("The rice cooker clicked, the whole house smelled like Sunday, "
     "and my grandmother ladled me a bowl before my grandfather had "
     "even washed his hands.",
     39),
    # nostalgia 9, concrete 9, authentic 9, tight 8, ache 9 = 44
    ("My grandmother kept a tin of photographs on top of the fridge, "
     "and on rainy afternoons she would lift me up to look at my "
     "mother as a little girl with my same crooked smile.",
     44),
    # nostalgia 8, concrete 9, authentic 10, tight 8, ache 9 = 44
    ("When the power went out one summer night we ate cold rice by "
     "candlelight, and my grandmother said the dark made the food "
     "taste better because we were finally paying attention.",
     44),
    # nostalgia 8, concrete 9, authentic 9, tight 7, ache 9 = 42
    ("I learned to ride my bike on the cracked pavement behind our "
     "house, my father running behind me with one hand on the seat, "
     "letting go without telling me, and I still remember the exact "
     "second I realized I was flying.",
     42),
    # nostalgia 9, concrete 8, authentic 10, tight 9, ache 10 = 46
    # REVISED (second pass): "on the table" -> "beside the rice pot"
    # (a concrete place and a sensory anchor, criterion 2, echoing the
    # brief's own image of fresh rice). The closing turn - "but she set
    # it anyway" - is untouched.
    ("Every evening at six my grandmother set an extra bowl beside the "
     "rice pot, just in case someone came by, and nobody ever did, but "
     "she set it anyway.",
     46),
    # nostalgia 9, concrete 10, authentic 9, tight 8, ache 9 = 45
    ("The summer I turned nine, the ice-cream truck came too late, so "
     "my grandmother made shaved ice with red syrup in a chipped bowl, "
     "and I swear nothing since has tasted that cold or that sweet.",
     45),
]

# The gate requires 1-280 characters of non-whitespace UTF-8 text, one line.
MAX_CHARS = 280
WORN_LINES = ("as an ai", "dear judge", "i am an ai")


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= MAX_CHARS, \
            f"candidate outside the gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be one line"
        lowered = text.lower()
        assert not any(w in lowered for w in WORN_LINES), \
            f"candidate leans on a stock line: {text!r}"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def verify_output(line):
    """Re-read what main() just wrote and prove it is exactly the pick.

    The gate scores /output/entry.txt itself, never stdout, so the check
    runs against the file on disk: same bytes, inside 1-280 characters,
    one line, nothing but whitespace-free text. The file is left world
    readable because the scorer may collect it as another user.
    """
    import hashlib
    path = "/output/entry.txt"
    with open(path, "rb") as f:
        raw = f.read()
    seen = hashlib.sha256(raw).hexdigest()
    wanted = hashlib.sha256(line.encode("utf-8")).hexdigest()
    assert seen == wanted, "entry.txt on disk is not the chosen line"
    text = raw.decode("utf-8")
    assert text.strip(), "entry.txt holds only whitespace"
    assert 1 <= len(text) <= MAX_CHARS, "entry.txt breaks the gate"
    assert "\n" not in text.strip(), "entry.txt is more than one line"
    import os
    os.chmod(path, 0o644)
    return seen


def main():
    line = pick(CANDIDATES)
    import os
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    digest = verify_output(line)
    print(line)
    print(f"verified entry.txt sha256={digest} chars={len(line)}")


if __name__ == "__main__":
    main()
