# Simulation de trajectoire d'une boule de pétanque

Projet Python pour un exposé d'enseignement scientifique de Première autour de la problématique :

> Comment les lois du mouvement permettent-elles d'expliquer et d'optimiser la trajectoire d'une boule de pétanque pour atteindre précisément le but ?

## Objectif

Le script `petanque_simulation.py` compare plusieurs angles de lancer d'une boule de pétanque avec un modèle simple de projectile. Il calcule :

- le temps de vol ;
- la hauteur maximale ;
- la distance d'impact ;
- l'écart avec le but ;
- la distance de roulement après impact ;
- la distance finale totale ;
- l'angle le plus précis.

## Hypothèses du modèle

Pour garder un niveau adapté à la classe de Première, le modèle utilise les simplifications suivantes :

- les frottements de l'air sont négligés pendant le vol ;
- la pesanteur est constante avec `g = 9,81 m/s²` ;
- la boule part d'une hauteur initiale de `1 m` ;
- la vitesse initiale est fixée à `7 m/s` ;
- le but est placé à `6 m` ;
- après l'impact, la boule roule avec une décélération constante de `1,5 m/s²`.

## Installation

```bash
python -m pip install -r requirements.txt
```

## Exécution

```bash
python petanque_simulation.py
```

Le programme affiche un tableau dans la console et ouvre un graphique `matplotlib` avec les trajectoires pour les angles `20°`, `35°`, `45°`, `55°` et `65°`.
