# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder 1.0 is a rule-based music recommender designed to suggest
songs that match a listener's personal taste profile. Given a user's
preferred genre, mood, energy level, and tempo, it scans a catalog of
songs and returns the top 5 best matches with an explanation of why
each song was chosen.

- It generates ranked song recommendations from a fixed CSV catalog
- It assumes the user already knows their preferences well enough to
  describe them (favorite genre, mood, a number for energy, a BPM
  target)
- This is a classroom simulation — it is not connected to real
  streaming data, user history, or live music APIs. It is designed
  for learning how recommendation logic works under the hood.

---

## 3. How the Model Works

VibeFinder scores every song in the catalog against the user's taste
profile, then returns the highest-scoring ones.

Each song is judged on four things:

- **Genre** — does the song's genre exactly match what the user wants?
  This is worth the most points (40 out of 100) because a genre
  mismatch is usually a dealbreaker. A jazz song recommended to a
  metal fan is a bad recommendation no matter how good the energy
  match is.
- **Mood** — does the song's mood label match the user's preferred
  mood (e.g. "happy", "chill", "intense")? This is worth 25 points.
- **Energy** — how close is the song's energy level to what the user
  wants? Energy is a number between 0 and 1. A song with energy 0.75
  scores almost perfectly for a user who wants 0.8, while a song with
  energy 0.2 scores much lower. This is worth 20 points.
- **Tempo** — how close is the song's speed (in beats per minute) to
  the user's target tempo? This is worth 15 points and works the same
  way as energy — closeness is rewarded, not just high or low values.

All four scores are added together for a total out of 100. The system
then sorts all songs from highest to lowest score and recommends the
top 5. Each recommendation comes with a plain-English reason breakdown
showing exactly how many points each feature contributed.

The main change from the starter logic was adding the "reasons" system
so users can see *why* a song was recommended, not just that it was.

---

## 4. Data

The catalog is a hand-curated CSV file (`data/songs.csv`) containing
songs across several genres and moods. Each song includes:
genre, mood, energy (0–1), tempo in BPM, valence, danceability,
and acousticness.

- The catalog covers genres including **pop, rock, lofi, electronic,
  classical, metal, and indie**
- Moods represented include **happy, chill, intense, sad, angry,
  energetic, hopeful, and focused**
- No songs were added or removed from the original starter dataset
- Missing from the dataset: country, R&B, hip-hop, jazz, and folk —
  meaning users who prefer those genres will never get a genre match
  and will always score lower than users whose genre is represented
- The dataset also does not capture context (time of day, activity,
  listening history), which real platforms like Spotify use heavily

---

## 5. Strengths

VibeFinder works well when the user's preferences align with what the
catalog actually contains:

- **High-energy pop** profile → top result scored 97.50/100 with
  correct genre and mood match
- **Chill lofi** profile → top result scored 99.45/100, nearly
  perfect across all four features
- **Deep intense rock** profile → top result scored 99.05/100

In these cases the system behaved exactly as expected — the right
songs rose to the top, and the reason breakdowns were honest and
readable. The scoring correctly captures the intuition that a song
which matches genre *and* mood *and* has close energy/tempo should
rank much higher than one that only partially matches.

The explanation feature is also a genuine strength — instead of a
black-box result, every recommendation tells the user exactly which
features matched and how many points each one contributed.

---

## 6. Limitations and Bias

Several weaknesses were discovered during testing:

**Genre dominates everything.** At 40 points, genre match is so
heavily weighted that a song can rank in the top 5 even when its mood
is completely wrong. In the conflicting profile test (metal + sad),
the top result was a metal song with an "angry" mood — not sad — but
it still ranked highly because genre alone contributed 40 points.

**No semantic understanding of mood.** The system treats "sad" and
"angry" as completely different, even though both are negative/dark
moods and a user who wants sad music might enjoy a melancholic angry
song. All mood mismatches are penalised equally, regardless of how
related the moods actually are.

**Nonexistent genres produce weak results.** A user who wants
"country" music will never receive a genre match because country is
not in the catalog. Their top results are chosen purely by mood,
energy, and tempo, which produces recommendations that feel arbitrary.
The system gives no warning that the genre was not found.

**Extreme tempo values find no good matches.** A user who wants 200
BPM can only receive partial tempo proximity scores because no song
in the catalog reaches that speed. The highest-tempo songs are around
150–160 BPM, leaving a permanent gap.

**No diversity enforcement.** The top 5 results can all be very
similar songs — the system does not try to spread recommendations
across different artists or sub-genres.

**No listening history.** The system treats every session identically.
It does not remember what the user has already heard or disliked.

---

## 7. Evaluation

Seven user profiles were tested — three normal and four edge cases:

| Profile | Key finding |
|---|---|
| High-energy pop | ✅ Perfect results, scores 95–97 |
| Chill lofi | ✅ Perfect results, scores 97–99 |
| Deep intense rock | ✅ Perfect results, scores 97–99 |
| Conflicting (metal + sad) | ⚠️ Genre dominated, mood ignored |
| Nonexistent genre (country) | ⚠️ Fell back to mood/energy only |
| Extreme low energy (0.1) | ⚠️ Mood mismatch still ranked high |
| Extreme high tempo (200 BPM) | ⚠️ No songs close enough to score well |

The most surprising finding was how strongly genre dominates the
results. Even when a profile was designed to create a conflict (high
energy + sad mood), the genre weight was large enough to push
genre-matching songs to the top regardless of mood. This revealed
that the 40-point genre weight may be too high for edge cases, even
if it makes sense for typical users.

The nonexistent genre test was also illuminating — the system
produced results silently without any warning that the genre was
missing from the catalog entirely, which would confuse a real user.

---

## 8. Future Work

Several improvements would make VibeFinder more robust:

- **Semantic mood grouping** — cluster moods into families
  (e.g. dark: sad/angry/melancholic, bright: happy/euphoric/upbeat)
  so partial mood matches receive partial credit instead of zero
- **Genre similarity scoring** — treat "indie rock" and "rock" as
  closer than "rock" and "lofi", rather than binary match/no-match
- **Fallback warning** — detect when a genre is not in the catalog
  and tell the user, rather than silently returning weak results
- **Diversity rule** — prevent the top 5 from being all the same
  artist or extremely similar songs by adding a penalty for
  repetition
- **User history** — track previously recommended songs and down-rank
  ones the user has already seen
- **Adjustable weights** — let the user choose whether genre or mood
  matters more to them personally, making the algorithm recipe
  customisable per session

---

## 9. Personal Reflection

Building VibeFinder made the logic behind apps like Spotify feel much
less magical. What looks like "the algorithm knows me" is really just
a set of weighted comparisons running at massive scale — the same
pattern we implemented here, just with millions of songs and years of
listening history instead of a CSV file and four features.

The most unexpected discovery was how a single design choice — the
genre weight being 40 points — shaped almost every result. Small
decisions about weights have outsized consequences on what users
actually see, which is something that is easy to overlook when the
math seems straightforward.

It also changed how I think about fairness in recommendation systems.
A user who likes country music gets a worse experience than a user
who likes pop, not because of anything they did, but simply because
of what data was included in the catalog. That gap between
"the algorithm is neutral" and "the algorithm reflects its data"
is one of the most important things to understand about AI systems.