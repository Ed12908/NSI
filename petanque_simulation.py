"""
Simulation pédagogique d'un lancer de boule de pétanque.

Problématique :
"Comment les lois du mouvement permettent-elles d'expliquer et d'optimiser
la trajectoire d'une boule de pétanque pour atteindre précisément le but ?"

Ce programme est volontairement simple pour être compréhensible par un élève
de Première. Il utilise le modèle du projectile : pendant le vol, on néglige
les frottements de l'air et on suppose que seule la pesanteur agit sur la boule.

Bonus : après le premier contact avec le sol, la boule continue à rouler avec
une décélération constante due aux frottements.
"""

import math

import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# 1. Paramètres physiques du problème
# ---------------------------------------------------------------------------

# Accélération de la pesanteur sur Terre, en m/s².
# Elle est dirigée vers le bas : c'est elle qui courbe la trajectoire.
G = 9.81

# Vitesse initiale de la boule au moment où elle quitte la main, en m/s.
VITESSE_INITIALE = 7.0

# Hauteur initiale du lancer, en mètre : la boule part environ de la main.
HAUTEUR_INITIALE = 1.0

# Distance horizontale entre le joueur et le but, en mètre.
DISTANCE_BUT = 6.0

# Angles de lancer que l'on veut comparer, en degrés.
ANGLES_DEGRES = [20, 35, 45, 55, 65]

# Bonus : décélération constante pendant le roulement, en m/s².
# Plus cette valeur est grande, plus la boule s'arrête rapidement.
DECELERATION_ROULEMENT = 1.5

# Pas de temps utilisé pour dessiner les trajectoires.
# Une petite valeur donne une courbe plus lisse.
PAS_TEMPS = 0.02


# ---------------------------------------------------------------------------
# 2. Fonctions de calcul
# ---------------------------------------------------------------------------

def calculer_temps_de_vol(vitesse_y_initiale):
    """Calcule le temps avant que la boule touche le sol.

    La hauteur de la boule pendant le vol est donnée par :
        y(t) = h0 + v0y * t - 1/2 * g * t²

    L'impact avec le sol a lieu lorsque y(t) = 0.
    On résout donc une équation du second degré et on garde la solution
    positive, car le temps ne peut pas être négatif.
    """
    discriminant = vitesse_y_initiale**2 + 2 * G * HAUTEUR_INITIALE
    return (vitesse_y_initiale + math.sqrt(discriminant)) / G


def calculer_trajectoire(angle_degres):
    """Calcule toutes les informations utiles pour un angle donné."""
    # Les fonctions trigonométriques de Python utilisent les radians.
    angle_radians = math.radians(angle_degres)

    # Décomposition de la vitesse initiale en deux composantes :
    # - vx est la vitesse horizontale, supposée constante pendant le vol ;
    # - vy est la vitesse verticale, modifiée par la pesanteur.
    vitesse_x = VITESSE_INITIALE * math.cos(angle_radians)
    vitesse_y = VITESSE_INITIALE * math.sin(angle_radians)

    # Temps total entre le lancer et le premier contact avec le sol.
    temps_vol = calculer_temps_de_vol(vitesse_y)

    # Distance horizontale parcourue avant l'impact avec le sol.
    distance_impact = vitesse_x * temps_vol

    # La hauteur maximale est atteinte quand la vitesse verticale devient nulle.
    # Formule obtenue à partir des équations du mouvement uniformément accéléré.
    hauteur_maximale = HAUTEUR_INITIALE + (vitesse_y**2) / (2 * G)

    # Écart entre le point d'impact et le but.
    ecart_impact = abs(distance_impact - DISTANCE_BUT)

    # Vitesse verticale juste avant l'impact : vy(t) = v0y - g*t.
    # Elle n'est pas utilisée pour le roulement simplifié, mais elle aide à
    # comprendre que la boule arrive vers le bas au moment du contact.
    vitesse_y_impact = vitesse_y - G * temps_vol

    # Bonus roulement : on suppose que la vitesse horizontale au début du
    # roulement vaut vitesse_x. La distance d'arrêt avec une décélération
    # constante a vaut : d = v² / (2a).
    distance_roulement = vitesse_x**2 / (2 * DECELERATION_ROULEMENT)
    distance_finale = distance_impact + distance_roulement
    ecart_final = abs(distance_finale - DISTANCE_BUT)

    # Points de la trajectoire pour le graphique.
    # On avance de PAS_TEMPS en PAS_TEMPS jusqu'au temps de vol.
    temps = []
    positions_x = []
    positions_y = []
    t = 0.0
    while t <= temps_vol:
        x = vitesse_x * t
        y = HAUTEUR_INITIALE + vitesse_y * t - 0.5 * G * t**2
        temps.append(t)
        positions_x.append(x)
        positions_y.append(max(y, 0))  # évite de dessiner sous le sol
        t += PAS_TEMPS

    # On ajoute exactement le point d'impact pour terminer proprement la courbe.
    temps.append(temps_vol)
    positions_x.append(distance_impact)
    positions_y.append(0)

    return {
        "angle": angle_degres,
        "temps_vol": temps_vol,
        "hauteur_maximale": hauteur_maximale,
        "distance_impact": distance_impact,
        "ecart_impact": ecart_impact,
        "vitesse_y_impact": vitesse_y_impact,
        "distance_roulement": distance_roulement,
        "distance_finale": distance_finale,
        "ecart_final": ecart_final,
        "x": positions_x,
        "y": positions_y,
    }


def afficher_tableau(resultats):
    """Affiche un tableau lisible dans la console."""
    print("\nComparaison des lancers de pétanque")
    print("=" * 112)
    print(
        f"{'Angle':>7} | {'Temps de vol':>12} | {'Hauteur max':>12} | "
        f"{'Impact':>10} | {'Écart impact':>13} | {'Roulement':>11} | "
        f"{'Distance finale':>15} | {'Écart final':>11}"
    )
    print("-" * 112)

    for resultat in resultats:
        print(
            f"{resultat['angle']:>5.0f}° | "
            f"{resultat['temps_vol']:>10.2f} s | "
            f"{resultat['hauteur_maximale']:>10.2f} m | "
            f"{resultat['distance_impact']:>8.2f} m | "
            f"{resultat['ecart_impact']:>11.2f} m | "
            f"{resultat['distance_roulement']:>9.2f} m | "
            f"{resultat['distance_finale']:>13.2f} m | "
            f"{resultat['ecart_final']:>9.2f} m"
        )

    print("=" * 112)


def tracer_trajectoires(resultats):
    """Trace toutes les trajectoires sur un même graphique."""
    plt.figure(figsize=(10, 6))

    for resultat in resultats:
        plt.plot(
            resultat["x"],
            resultat["y"],
            label=f"{resultat['angle']}° : impact à {resultat['distance_impact']:.2f} m",
        )

    # Ligne verticale qui indique la position du but.
    plt.axvline(
        x=DISTANCE_BUT,
        color="red",
        linestyle="--",
        linewidth=2,
        label=f"But à {DISTANCE_BUT:.1f} m",
    )

    # Ligne horizontale représentant le sol.
    plt.axhline(y=0, color="black", linewidth=1)

    plt.title("Trajectoire aérienne d'une boule de pétanque")
    plt.xlabel("Distance horizontale (m)")
    plt.ylabel("Hauteur (m)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    """Fonction principale du programme."""
    # On calcule les résultats pour tous les angles demandés.
    resultats = [calculer_trajectoire(angle) for angle in ANGLES_DEGRES]

    # Affichage numérique sous forme de tableau.
    afficher_tableau(resultats)

    # Recherche de l'angle le plus précis si on regarde seulement le point
    # d'impact, donc avant le roulement.
    meilleur_impact = min(resultats, key=lambda resultat: resultat["ecart_impact"])

    # Recherche de l'angle le plus précis avec le modèle bonus de roulement.
    meilleur_final = min(resultats, key=lambda resultat: resultat["ecart_final"])

    print("\nAnalyse automatique")
    print("-" * 22)
    print(
        "Sans tenir compte du roulement, l'angle le plus précis est "
        f"{meilleur_impact['angle']}° : la boule touche le sol à "
        f"{meilleur_impact['distance_impact']:.2f} m, soit un écart de "
        f"{meilleur_impact['ecart_impact']:.2f} m avec le but."
    )
    print(
        "Avec le roulement simplifié, l'angle le plus précis est "
        f"{meilleur_final['angle']}° : la boule s'arrête à "
        f"{meilleur_final['distance_finale']:.2f} m, soit un écart final de "
        f"{meilleur_final['ecart_final']:.2f} m avec le but."
    )

    # Affichage graphique des trajectoires aériennes.
    tracer_trajectoires(resultats)


# Cette condition permet d'exécuter le programme seulement quand ce fichier est
# lancé directement avec : python petanque_simulation.py
if __name__ == "__main__":
    main()
