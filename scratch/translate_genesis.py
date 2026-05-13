"""
Forensic Bible Translation Machine — Genesis 1-100
====================================================
Applies all 79 Forensic Rules to produce complete ForensicUnit JSON for
each sentence in Genesis, units 1 through 100.

Usage:
    python scratch/translate_genesis.py --api-key YOUR_GEMINI_API_KEY
    -- or --
    set GEMINI_API_KEY=YOUR_KEY && python scratch/translate_genesis.py

The script is safe to interrupt and re-run. Already-completed units
(forensic-confidence > 0) are skipped automatically.
"""

import os
import json
import time
import argparse
import sys

# ---------------------------------------------------------------------------
# Google Generative AI (legacy package, still functional)
# ---------------------------------------------------------------------------
try:
    import google.generativeai as genai
except ImportError:
    print("ERROR: google-generativeai not installed. Run: pip install google-generativeai")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BOOK_SLUG   = "genesis"
UNIT_START  = 1
UNIT_END    = 100
DATA_DIR    = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "static", "data", "books", BOOK_SLUG
)
MODEL_NAME  = "gemini-2.5-flash-preview-05-20"   # latest fast reasoning model
SLEEP_BETWEEN_CALLS = 3   # seconds — stay within free-tier rate limits

# ---------------------------------------------------------------------------
# 79-Rule Forensic System Prompt (compact, authoritative)
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """
You are the Forensic Bible Translation Engine. Your task is to produce a
COMPLETE forensic translation of a single Hebrew sentence from Genesis, filling
every field of the JSON schema below with maximum precision.

══════════════════════════════════════════════════════════════════════════════
CORE OBJECTIVE
══════════════════════════════════════════════════════════════════════════════
Produce a 100% accurate, 100% English forensic reconstruction of each Hebrew
sentence. Every semantic layer — grammatical, historical, social, theological —
must be physically written out in the English text. Nothing may be implied.

══════════════════════════════════════════════════════════════════════════════
THE 79 FORENSIC RULES (apply ALL that are relevant to this sentence)
══════════════════════════════════════════════════════════════════════════════
Rule 1  – Total Contextual Disclosure: every semantic layer must be explicit.
Rule 2  – Zero Contextual Drift: no dynamic equivalence or modern bias.
Rule 3  – Pure English Only: no loanwords/transliterations (except "Jesus" and "Christ").
Rule 4  – Modern Basic English: no KJV-isms (thou/hath/ye etc).
Rule 5  – Italicised Grouping: wrap multi-word expansions of ONE source word in <em>...</em> tags.
Rule 6  – Perfect Word + Bracket: use precise technical term + [explanation].
Rule 7  – Ancient Idiomatic Expressions: keep idiom + (functional meaning).
Rule 8  – Modern Value Comparison: for ancient weights/currencies add (modern equivalent).
Rule 9  – Verb Aspect Disclosure: state if action is continuous, one-time, completed status. Use natural English ("keep doing", "in a state of") not robotic adverbs.
Rule 10 – Status Permanence Disclosure: signal "fixed state" verbs explicitly.
Rule 11 – Agency and Causality: who acted personally vs caused vs used as instrument.
Rule 12 – Collective vs Individual Agency: unified group vs separate individuals.
Rule 13 – Instructional Intent Tone: strong order vs gentle plea vs sarcasm.
Rule 14 – Certainty and Mood: definite fact vs potential vs desired.
Rule 15 – Level of Obligation: legal debt vs moral necessity vs social fittingness.
Rule 16 – Degree of Urgency: "right now" vs general future instruction.
Rule 17 – Instrument and Means: what tool/means was used.
Rule 18 – Completeness of Action: once-for-all vs repeating process.
Rule 19 – Source of Authority: "in the name of" = full legal power-of-attorney.
Rule 20 – Consolidated Syntax: combine ancient prep repetitions naturally ("between A and B" not "between A and between B").
Rule 21 – Functional Object Disclosure: what ancient objects did physically.
Rule 22 – Symbolic Attire & Object: public declaration behind clothing/objects.
Rule 23 – Social Identity of Roles: modern social equivalent of ancient titles.
Rule 24 – Situational Name Disclosure: define name meaning at the narrative moment it is relevant.
Rule 25 – Intertextual Echoes: flag when author quotes/echoes another scripture.
Rule 26 – Prophetic Fulfillment: flag divine architecture behind fulfillment texts.
Rule 28 – Disciplinary Context: identify professional field (courtroom/military/temple/commercial).
Rule 29 – Geographical Orientation: disclose precise elevation/direction (going UP to Jerusalem, DOWN to Jordan, EASTWARD from Eden).
Rule 30 – Contextual Targeting & Bridging: translate ONLY the primary contextual meaning of a polysemous word; use a bridging phrase only for deliberate double-entendres.
Rule 31 – Divine vs Human Time: Chronos (clock-time) vs Kairos (appointed divine moment).
Rule 32 – Legal Status of Subject: slave / hired servant / minor child / legal heir.
Rule 33 – Eyewitness vs Reported Speech: firsthand vs hearsay.
Rule 34 – Intensity of Sacredness: holy (set apart for God) vs common.
Rule 35 – Direction of Address: internal monologue vs external audience.
Rule 36 – Wisdom vs Practical Insight: Sophia (philosophical) vs Phronesis (street-smart).
Rule 37 – Life Type Differentiation: physical life (bios/psyche) vs divine life (zoe).
Rule 38 – Community vs Individual: plural "you" vs singular.
Rule 39 – Identity of We and Us: apostles only vs whole community.
Rule 40 – Intimacy & Relationship Tone: formal respect vs brotherly vs fatherly.
Rule 41 – Gender Scope Disclosure: male only vs inclusive brothers-and-sisters.
Rule 42 – Intensity Grading: superlatives — extreme / overflowing / absolute.
Rule 43 – Emotional Intensity Pathos: visceral/physical nature of emotions.
Rule 44 – Honor and Shame Context: social currency — public honor vs public shame.
Rule 45 – Temple & Ceremonial Context: common service vs sacred priestly service.
Rule 46 – Social Scandal & Taboo: breaking a social taboo — flag the shock.
Rule 47 – Anthropological Disclosure: physical body (soma) vs sinful nature (sarx).
Rule 48 – Status Permanence (Perfect Tense): finished and fixed status.
Rule 49 – Patronage Relationship: grace as patron/client social contract.
Rule 50 – Ancient Hospitality Laws: binding duty of a host.
Rule 51 – Facial & Body Gesture Disclosure: legal/social message behind gestures.
Rule 52 – Structural "Therefore": disclose chain of command between truth and result.
Rule 53 – Forgiveness as Economic Debt: legal cancellation of a debt-bond.
Rule 54 – Master-Disciple Relationship: "follow" = total life apprenticeship.
Rule 55 – Theophanic Phenomenon: physical cloud/fire/thunder as vehicle of God's presence.
Rule 56 – Suffix of Endearment: diminutives signaling tender affection.
Rule 57 – Covenantal Signs & Seals: physical acts as binding legal seals.
Rule 58 – Plainness of Speech (Parrhesia): dangerous public boldness.
Rule 59 – Ancestral & Lineage Weight: "father" = legal source of entire lineage.
Rule 60 – Cognate Accusative: verb + cognate noun = absolute overflowing intensity.
Rule 61 – Nature & Animal Symbolism: archetypal spiritual code in nature/animals.
Rule 62 – Honorifics & Social Hierarchy: exact tier of a title (sir / master / deity).
Rule 63 – Channel vs Source Agency: originating Source (from God) vs instrumental Channel (through Christ).
Rule 64 – Conditional Reality: IF as fact / potential / impossible.
Rule 65 – Genitive Directionality: God's love FOR us vs our love FOR God.
Rule 66 – Hendiadys: two words forming one unified super-concept.
Rule 67 – Ancient Monetary Scale: disclose generational labor value.
Rule 68 – Polysemy Resolution Disclosure: when a word has multiple valid meanings, weave ALL valid meanings into a comprehensive phrase.
Rule 69 – Verbal Inspiration Granularity: preserve singular/plural exactly.
Rule 70 – Optimal Bridging Phrase Precision: every word in expansion must be forensically optimal.
Rule 71 – Biological vs Forensic Sonship: "Son" theologically = Supreme Heir / Exact Representation.
Rule 72 – Cognitive Center Realignment: "heart" (leb/kardia) = central command center of mind and will.
Rule 73 – Forensic Theological Boundary: no added anthropomorphic body parts unless in original text.
Rule 74 – Conjunctive Chain Precision: וְ (Waw) / καί / δέ / ἀλλά / γάρ / οὖν each carry distinct meanings — NEVER default to "and".
Rule 75 – Absence-of-Article Significance: anarthrous Greek/Hebrew nouns often signal qualitative force, not merely indefinite identity.
Rule 76 – Word-Order Emphasis (Hyperbaton): front-positioned words carry rhetorical stress — honor that stress in English.
Rule 77 – Resumptive Pronoun Disclosure: doubled subject structure "the one who — HE shall be" = intensified identity marker.
Rule 78 – Hapax Legomenon Flag: if a word appears only once in all Scripture, mark it as tentative in grammatical-notes.
Rule 79 – Semantic Range Boundary: for each dictionary entry state NEVER / MAXIMUM / CHOSEN boundary.

══════════════════════════════════════════════════════════════════════════════
OUTPUT JSON SCHEMA (return ONLY valid JSON, no markdown fences)
══════════════════════════════════════════════════════════════════════════════
{
  "literal-translation": ["word1-literal", "word2-literal", ...],
  "main-translation": "Full forensic English sentence using <em> tags for Rule 5",
  "grammatical-notes": {
    "HebrewWord1": "Root, stem, PGN, parse, syntactic function",
    "HebrewWord2": "..."
  },
  "dictionary-meaning": {
    "HebrewWord1": "NEVER: X | MAXIMUM: Y | CHOSEN: Z — reason",
    "HebrewWord2": "..."
  },
  "polysemy-log": {
    "HebrewWord1": {
      "options": ["meaning A", "meaning B", "meaning C"],
      "chosen": "meaning A",
      "reason": "Why this contextual choice"
    }
  },
  "main-translation-explanation": {
    "key English phrase from translation": "forensic justification citing rules and grammar",
    "another key phrase": "..."
  },
  "rejected-translations": [
    {"phrase": "traditional bad rendering", "reason": "why it fails forensically"},
    "simple string rejection is also valid"
  ],
  "rules-applied": [1, 2, 4, 5, 9, 20, 29, 74],
  "forensic-confidence": 92
}

RULES FOR forensic-confidence SCORING:
- Start at 100
- Deduct 5 per hapax legomenon (Rule 78)
- Deduct 3 per word with significant polysemy controversy
- Deduct 2 per word where modern lexicons disagree
- Minimum score: 70 for a well-attested passage; 50 if highly debated

CRITICAL REQUIREMENTS:
1. The main-translation MUST be fluent, modern English — not word-salad.
2. Use <em>...</em> tags (no hyphens) for multi-word expansions (Rule 5).
3. Conjunctions (וְ / וּ / אֲשֶׁר) must be rendered precisely per Rule 74.
4. Hebrew word-order emphasis must be reflected in English per Rule 76.
5. Every entry in dictionary-meaning MUST follow the NEVER/MAXIMUM/CHOSEN format.
6. Do NOT include the index, hash, sentence, words, word-count-original, or
   source-language fields — those are already set.
7. Return ONLY the JSON object. No commentary, no markdown.
"""

# ---------------------------------------------------------------------------
# Translation function
# ---------------------------------------------------------------------------
def translate_unit(model, unit: dict) -> dict:
    """Call Gemini to produce forensic fields for the given unit."""
    hebrew_sentence = unit.get("sentence", "")
    words = unit.get("words", [])
    index = unit.get("index", "?")

    user_prompt = f"""
Translate Genesis unit {index}.

HEBREW SENTENCE:
{hebrew_sentence}

WORDS ARRAY (in order):
{json.dumps(words, ensure_ascii=False)}

Produce the complete forensic JSON for this sentence.
Remember: literal-translation must be an array of the same length as the words array.
"""

    response = model.generate_content(
        user_prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.1,
            max_output_tokens=8192,
        ),
        safety_settings=[
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH",       "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HARASSMENT",        "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        ],
    )

    raw = response.text.strip()

    # Strip markdown fences if the model accidentally adds them
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1]
    if raw.endswith("```"):
        raw = raw.rsplit("```", 1)[0]
    raw = raw.strip()

    return json.loads(raw)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Forensic Genesis Translation Machine")
    parser.add_argument("--api-key", default=None, help="Gemini API key (or set GEMINI_API_KEY env var)")
    parser.add_argument("--start",   type=int, default=UNIT_START, help=f"First unit index (default {UNIT_START})")
    parser.add_argument("--end",     type=int, default=UNIT_END,   help=f"Last unit index (default {UNIT_END})")
    parser.add_argument("--force",   action="store_true", help="Re-translate already-completed units")
    args = parser.parse_args()

    # Resolve API key
    api_key = (
        args.api_key
        or os.environ.get("GEMINI_API_KEY")
        or os.environ.get("GOOGLE_API_KEY")
    )
    if not api_key:
        print("ERROR: Gemini API key not found.")
        print("  Option A: python scratch/translate_genesis.py --api-key YOUR_KEY")
        print("  Option B: set GEMINI_API_KEY=YOUR_KEY in environment or .env file")
        sys.exit(1)

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name=MODEL_NAME,
        system_instruction=SYSTEM_PROMPT,
    )

    print(f"\n{'='*60}")
    print(f"  FORENSIC GENESIS TRANSLATION MACHINE")
    print(f"  Processing units {args.start}–{args.end}")
    print(f"  Data directory: {DATA_DIR}")
    print(f"  Model: {MODEL_NAME}")
    print(f"{'='*60}\n")

    completed = 0
    skipped   = 0
    errors    = 0

    for i in range(args.start, args.end + 1):
        path = os.path.join(DATA_DIR, f"{i}.json")

        if not os.path.exists(path):
            print(f"  [SKIP] Unit {i}: file not found at {path}")
            skipped += 1
            continue

        with open(path, "r", encoding="utf-8") as f:
            unit = json.load(f)

        # Skip already-translated units unless --force
        if not args.force and unit.get("forensic-confidence", 0) > 0:
            print(f"  [DONE] Unit {i}: already translated (confidence={unit['forensic-confidence']}%), skipping.")
            skipped += 1
            continue

        print(f"  [TRANSLATING] Unit {i}: {unit.get('sentence', '')[:60]}...")

        try:
            result = translate_unit(model, unit)
        except json.JSONDecodeError as e:
            print(f"  [ERROR] Unit {i}: JSON parse failed — {e}")
            errors += 1
            continue
        except Exception as e:
            print(f"  [ERROR] Unit {i}: API call failed — {e}")
            errors += 1
            # Exponential back-off for rate-limit errors
            if "429" in str(e) or "quota" in str(e).lower():
                wait = 30
                print(f"  Rate limit hit. Waiting {wait}s...")
                time.sleep(wait)
            continue

        # Merge the AI-generated fields back into the unit (preserving
        # index, hash, sentence, words, word-count-original, source-language)
        MERGEABLE_FIELDS = [
            "literal-translation",
            "main-translation",
            "grammatical-notes",
            "dictionary-meaning",
            "polysemy-log",
            "main-translation-explanation",
            "rejected-translations",
            "rules-applied",
            "forensic-confidence",
        ]
        for field in MERGEABLE_FIELDS:
            if field in result:
                unit[field] = result[field]

        # Validate literal-translation length
        words = unit.get("words", [])
        lit = unit.get("literal-translation", [])
        if isinstance(lit, list) and len(lit) != len(words):
            print(f"  [WARN] Unit {i}: literal-translation length {len(lit)} != words length {len(words)}, padding/trimming.")
            if len(lit) < len(words):
                unit["literal-translation"] = lit + ["..."] * (len(words) - len(lit))
            else:
                unit["literal-translation"] = lit[:len(words)]

        # Write back to disk
        with open(path, "w", encoding="utf-8") as f:
            json.dump(unit, f, ensure_ascii=False, indent=2)

        confidence = unit.get("forensic-confidence", 0)
        print(f"  [OK] Unit {i} saved — confidence: {confidence}%")
        completed += 1

        # Polite pause to avoid hitting rate limits
        time.sleep(SLEEP_BETWEEN_CALLS)

    print(f"\n{'='*60}")
    print(f"  COMPLETE")
    print(f"  Translated : {completed}")
    print(f"  Skipped    : {skipped}")
    print(f"  Errors     : {errors}")
    print(f"{'='*60}\n")

    # Regenerate combined.json after successful run
    if completed > 0:
        print("  Rebuilding combined.json...")
        combined = []
        for i in range(1, 2063):  # full Genesis range
            p = os.path.join(DATA_DIR, f"{i}.json")
            if os.path.exists(p):
                with open(p, "r", encoding="utf-8") as f:
                    combined.append(json.load(f))
        combined_path = os.path.join(DATA_DIR, "combined.json")
        with open(combined_path, "w", encoding="utf-8") as f:
            json.dump(combined, f, ensure_ascii=False, separators=(",", ":"))
        print(f"  combined.json rebuilt ({len(combined)} units).")


if __name__ == "__main__":
    main()
