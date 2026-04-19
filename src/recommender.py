import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


# ─────────────────────────────────────────────
# WEIGHTS — your Algorithm Recipe from Phase 2
# ─────────────────────────────────────────────
WEIGHT_GENRE  = 40.0   # genre match is a dealbreaker → highest weight
WEIGHT_MOOD   = 25.0   # mood drives the feeling of a song
WEIGHT_ENERGY = 20.0   # proximity score (closeness to target_energy)
WEIGHT_TEMPO  = 15.0   # fine-tuner; less critical than mood/genre


# ─────────────────────────────────────────────
# Step 1 — Load songs from CSV
# ─────────────────────────────────────────────
def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file and returns a list of dicts.
    Numerical fields (energy, tempo_bpm, valence, danceability,
    acousticness) are converted to float; id is converted to int
    so math and comparisons work correctly later.

    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    songs = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = {
                "id":           int(row["id"]),
                "title":        row["title"].strip(),
                "artist":       row["artist"].strip(),
                "genre":        row["genre"].strip().lower(),
                "mood":         row["mood"].strip().lower(),
                # ↓ convert to float so scoring math works
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            }
            songs.append(song)

    print(f"  Loaded {len(songs)} songs.")
    return songs


# ─────────────────────────────────────────────
# Step 2 — Score a single song
# ─────────────────────────────────────────────
def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores one song against user preferences using a weighted formula.

    Scoring recipe (max 100 pts):
      Genre match  → 40 pts  (exact string match)
      Mood match   → 25 pts  (exact string match)
      Energy prox  → 20 pts  (1 - |song - user|) × 20
      Tempo prox   → 15 pts  (1 - |song - user| / 200) × 15

    Returns:
        (score, reasons) — score is a float 0–100;
        reasons is a list of human-readable strings explaining
        each component so the user understands the recommendation.
    """
    score   = 0.0
    reasons = []

    # ── Genre (0 or 40 pts) ──────────────────
    if song["genre"] == user_prefs["favorite_genre"].lower():
        score += WEIGHT_GENRE
        reasons.append(f"genre match (+{WEIGHT_GENRE})")
    else:
        reasons.append(f"genre mismatch: '{song['genre']}' ≠ '{user_prefs['favorite_genre']}' (+0)")

    # ── Mood (0 or 25 pts) ───────────────────
    if song["mood"] == user_prefs["favorite_mood"].lower():
        score += WEIGHT_MOOD
        reasons.append(f"mood match (+{WEIGHT_MOOD})")
    else:
        reasons.append(f"mood mismatch: '{song['mood']}' ≠ '{user_prefs['favorite_mood']}' (+0)")

    # ── Energy proximity (0–20 pts) ──────────
    # Rewards closeness to target_energy, not just high/low values.
    # Formula: (1 - |song_energy - target|) × weight
    energy_distance  = abs(song["energy"] - user_prefs["target_energy"])
    energy_proximity = max(0.0, 1.0 - energy_distance)          # clamp to [0, 1]
    energy_points    = round(energy_proximity * WEIGHT_ENERGY, 2)
    score           += energy_points
    reasons.append(f"energy proximity {song['energy']:.2f} vs {user_prefs['target_energy']:.2f} (+{energy_points})")

    # ── Tempo proximity (0–15 pts) ───────────
    # Tempo ranges ~60–200 BPM, so we normalise by 200 to keep
    # the distance in the same [0, 1] space as energy.
    tempo_distance  = abs(song["tempo_bpm"] - user_prefs["target_tempo"])
    tempo_proximity = max(0.0, 1.0 - tempo_distance / 200.0)    # clamp to [0, 1]
    tempo_points    = round(tempo_proximity * WEIGHT_TEMPO, 2)
    score          += tempo_points
    reasons.append(f"tempo proximity {song['tempo_bpm']:.0f} BPM vs {user_prefs['target_tempo']} BPM (+{tempo_points})")

    return round(score, 2), reasons


# ─────────────────────────────────────────────
# Step 3 — Rank all songs, return top-k
# ─────────────────────────────────────────────
def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5
) -> List[Tuple[Dict, float, str]]:
    """
    Scores every song in the catalog, sorts by score (highest first),
    and returns the top-k results.

    Why sorted() instead of .sort():
        .sort()  mutates the original list in-place (no return value).
        sorted() leaves the original list untouched and returns a
        brand-new sorted list — safer and more predictable when the
        catalog is used elsewhere in the program.

    Returns:
        List of (song_dict, score, explanation) tuples — one per
        top-k result. The explanation is a joined string of reasons
        so src/main.py can print it directly.
    """
    # Score every song (Scoring Rule — runs once per song)
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, reasons))

    # Ranking Rule — sort the full scored list, highest score first.
    # sorted() is used here so the original `songs` list is NOT mutated.
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)

    # Slice top-k and format the explanation string
    results = []
    for song, score, reasons in ranked[:k]:
        explanation = " | ".join(reasons)
        results.append((song, score, explanation))

    return results


# ─────────────────────────────────────────────
# OOP wrapper — required by test_recommender.py
# ─────────────────────────────────────────────
class Recommender:
    """
    Object-oriented interface around the functional helpers above.
    Required by tests/test_recommender.py
    """

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _song_to_dict(self, song: Song) -> Dict:
        """Converts a Song dataclass to the dict format score_song expects."""
        return {
            "id":           song.id,
            "title":        song.title,
            "artist":       song.artist,
            "genre":        song.genre,
            "mood":         song.mood,
            "energy":       song.energy,
            "tempo_bpm":    song.tempo_bpm,
            "valence":      song.valence,
            "danceability": song.danceability,
            "acousticness": song.acousticness,
        }

    def _profile_to_dict(self, user: UserProfile) -> Dict:
        """Converts a UserProfile dataclass to the dict format score_song expects."""
        # Estimate a target_tempo from likes_acoustic:
        # acoustic lovers tend to prefer slower tempos (~90 BPM),
        # non-acoustic listeners a more energetic ~130 BPM.
        target_tempo = 90 if user.likes_acoustic else 130
        return {
            "favorite_genre": user.favorite_genre,
            "favorite_mood":  user.favorite_mood,
            "target_energy":  user.target_energy,
            "target_tempo":   target_tempo,
        }

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top-k Song objects for this UserProfile."""
        user_dict  = self._profile_to_dict(user)
        song_dicts = [self._song_to_dict(s) for s in self.songs]

        results = recommend_songs(user_dict, song_dicts, k)

        # Map scored dicts back to the original Song dataclass objects
        id_to_song = {s.id: s for s in self.songs}
        return [id_to_song[song_dict["id"]] for song_dict, _, _ in results]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable explanation for why song was recommended."""
        user_dict = self._profile_to_dict(user)
        song_dict = self._song_to_dict(song)
        score, reasons = score_song(user_dict, song_dict)
        lines = [f'Why "{song.title}" was recommended (score: {score}/100):']
        for i, reason in enumerate(reasons, 1):
            lines.append(f"  {i}. {reason}")
        return "\n".join(lines)