"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "target_tempo": 120  # default BPM for pop
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 60)
    print("🎧 TOP RECOMMENDATIONS FOR YOU")
    print("=" * 60)
    print(f"Profile: {user_prefs['favorite_genre'].title()} | {user_prefs['favorite_mood'].title()} | Energy: {user_prefs['target_energy']}")
    print("-" * 60)
    
    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        print(f"\n#{i} {song['title']}")
        print(f"   Artist: {song['artist']}")
        print(f"   Genre: {song['genre']} | Mood: {song['mood']}")
        print(f"   ─────────────────────────────────")
        print(f"   ★ SCORE: {score:.2f} / 100")
        print(f"   Reasons:")
        for reason in explanation.split(" | "):
            print(f"      • {reason}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
