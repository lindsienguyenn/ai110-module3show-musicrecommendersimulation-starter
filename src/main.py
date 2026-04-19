"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from typing import Dict, List
from src.recommender import load_songs, recommend_songs


def run_recommendations(user_prefs: Dict, songs: List[Dict], k: int = 5) -> None:
    """Run and display recommendations for a given user profile."""
    recommendations = recommend_songs(user_prefs, songs, k=k)

    print("\n" + "=" * 60)
    print("🎧 TOP RECOMMENDATIONS FOR YOU")
    print("=" * 60)
    print(f"Profile: {user_prefs['favorite_genre'].title()} | {user_prefs['favorite_mood'].title()} | Energy: {user_prefs['target_energy']} | Tempo: {user_prefs['target_tempo']} BPM")
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


def main() -> None:
    from typing import Dict, List
    
    songs = load_songs("data/songs.csv") 

    # ─────────────────────────────────────────────
    # USER PROFILES FOR TESTING
    # ─────────────────────────────────────────────
    
    # Profile 1: High-Energy Pop
    profile_pop = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.9,
        "target_tempo": 130
    }
    
    # Profile 2: Chill Lofi
    profile_lofi = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.4,
        "target_tempo": 80
    }
    
    # Profile 3: Deep Intense Rock
    profile_rock = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.95,
        "target_tempo": 150
    }
    
    # ─────────────────────────────────────────────
    # ADVERSARIAL / EDGE CASE PROFILES
    # ─────────────────────────────────────────────
    
    # Edge Case 1: Conflicting preferences (high energy + sad mood)
    profile_conflicting = {
        "favorite_genre": "metal",
        "favorite_mood": "sad",
        "target_energy": 0.95,
        "target_tempo": 160
    }
    
    # Edge Case 2: Genre that doesn't exist in dataset
    profile_nonexistent = {
        "favorite_genre": "country",
        "favorite_mood": "happy",
        "target_energy": 0.7,
        "target_tempo": 100
    }
    
    # Edge Case 3: Extreme energy values (very low)
    profile_extreme_low = {
        "favorite_genre": "classical",
        "favorite_mood": "focused",
        "target_energy": 0.1,
        "target_tempo": 60
    }
    
    # Edge Case 4: Extreme tempo (very high)
    profile_extreme_high = {
        "favorite_genre": "electronic",
        "favorite_mood": "energetic",
        "target_energy": 1.0,
        "target_tempo": 200
    }

    # Run all profiles
    print("\n" + "=" * 60)
    print("🎵 MUSIC RECOMMENDER - SYSTEM EVALUATION")
    print("=" * 60)
    
    print("\n>>> PROFILE 1: High-Energy Pop")
    run_recommendations(profile_pop, songs)
    
    print("\n>>> PROFILE 2: Chill Lofi")
    run_recommendations(profile_lofi, songs)
    
    print("\n>>> PROFILE 3: Deep Intense Rock")
    run_recommendations(profile_rock, songs)
    
    print("\n>>> EDGE CASE 1: Conflicting (Metal + Sad + High Energy)")
    run_recommendations(profile_conflicting, songs)
    
    print("\n>>> EDGE CASE 2: Nonexistent Genre (Country)")
    run_recommendations(profile_nonexistent, songs)
    
    print("\n>>> EDGE CASE 3: Extreme Low Energy (0.1)")
    run_recommendations(profile_extreme_low, songs)
    
    print("\n>>> EDGE CASE 4: Extreme High Tempo (200 BPM)")
    run_recommendations(profile_extreme_high, songs)


if __name__ == "__main__":
    main()
