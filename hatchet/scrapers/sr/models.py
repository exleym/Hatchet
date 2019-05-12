from dataclasses import dataclass


@dataclass
class SRSchool:
    name: str
    games_played: int
    games_won: int
    games_lost: int
    games_tied: int
    win_loss_pct: float
    g_post: int
    wins_post: int
    losses_post: int
    ties_post: int
    win_loss_pct_post: float
    last_final_rank: int
    conf_champ_count: int
    simple_rating_score: float
    strength_of_schedule: float
    start_year: int
    last_year: int
    seasons_played: int
    notes: str
