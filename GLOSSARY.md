# TowerDefence

A 2D grid-based tower defence game built with Pygame where players defend against waves of enemies, earn currency, and upgrade towers and global research.

## Language

### Currencies

**Money**:
The in-game currency earned during a battle by defeating enemies and spent to place or upgrade towers within that session.
_Avoid_: Coin, Gold, Cash

**Coin**:
The persistent meta-currency awarded at the end of battles and saved to disk, spent in the Research laboratory on permanent talent upgrades.
_Avoid_: Money, Currency

### Systems

**Research**:
The out-of-battle meta-progression laboratory where players spend Coin to permanently upgrade global stats.
_Avoid_: Tech Tree, Upgrades

**Bonus**:
The passive stat multiplier or flat buff derived from Research levels, applied to gameplay variables such as tower damage, attack speed, range, or initial resources.
_Avoid_: Buff, Perk, Modifier

**Wave**:
A timed sequence of enemy spawns within a battle level that must be cleared to progress.
_Avoid_: Round, Stage

**World**:
The runtime match state managing the grid map, enemy pathing, wave progression, and in-game Money/Health for an active level.
_Avoid_: Level Manager, Game Map
