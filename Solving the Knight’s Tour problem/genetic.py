#genetic.py
from matplotlib import pyplot as plt
import numpy as np

def plot_path(path):
    if not path:
        print("Aucun chemin à afficher")
        return
    fig, ax = plt.subplots(figsize=(10, 10))
    chess = np.add.outer(range(8), range(8)) % 2
    ax.imshow(chess, cmap='binary_r', extent=[-0.5, 7.5, -0.5, 7.5], alpha=0.3)
    x = [pos[0] for pos in path]
    y = [pos[1] for pos in path]
    ax.plot(x, y, linestyle='-', color='blue', linewidth=2, alpha=0.7, zorder=1)
    ax.scatter(x, y, color='blue', s=100, zorder=2, edgecolors='white', linewidth=2)
    ax.scatter(x[0], y[0], color='green', s=300, marker='s', label='Départ', zorder=3, edgecolors='darkgreen', linewidth=3)
    ax.scatter(x[-1], y[-1], color='red', s=300, marker='s', label='Arrivée', zorder=3, edgecolors='darkred', linewidth=3)
    for i, (px, py) in enumerate(path):
        ax.text(px, py, str(i + 1), fontsize=10, ha='center', va='center', color='white', fontweight='bold', zorder=4,
                bbox=dict(boxstyle='circle', facecolor='black', alpha=0.7, pad=0.3))
    ax.set_xticks(range(8))
    ax.set_yticks(range(8))
    ax.set_xticklabels([chr(ord('a') + i) for i in range(8)], fontsize=12, fontweight='bold')
    ax.set_yticklabels([str(i + 1) for i in range(8)], fontsize=12, fontweight='bold')
    ax.grid(True, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
    ax.set_xlim(-0.5, 7.5)
    ax.set_ylim(-0.5, 7.5)
    ax.invert_yaxis()
    ax.set_title(f"Chemin du Cavalier sur Échiquier\nNombre de cases visitées: {len(path)}/64", fontsize=16, fontweight='bold', pad=20)
    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=12, framealpha=0.9)
    ax.set_aspect('equal')
    plt.tight_layout()
    plt.show()

def save_path(path, filename='knight_tour.png'):
    if not path:
        print("Aucun chemin à sauvegarder")
        return
    fig, ax = plt.subplots(figsize=(10, 10))
    chess = np.add.outer(range(8), range(8)) % 2
    ax.imshow(chess, cmap='binary_r', extent=[-0.5, 7.5, -0.5, 7.5], alpha=0.3)
    x = [pos[0] for pos in path]
    y = [pos[1] for pos in path]
    ax.plot(x, y, linestyle='-', color='blue', linewidth=2, alpha=0.7, zorder=1)
    ax.scatter(x, y, color='blue', s=100, zorder=2, edgecolors='white', linewidth=2)
    ax.scatter(x[0], y[0], color='green', s=300, marker='s', label='Départ', zorder=3, edgecolors='darkgreen', linewidth=3)
    ax.scatter(x[-1], y[-1], color='red', s=300, marker='s', label='Arrivée', zorder=3, edgecolors='darkred', linewidth=3)
    for i, (px, py) in enumerate(path):
        ax.text(px, py, str(i + 1), fontsize=10, ha='center', va='center', color='white', fontweight='bold', zorder=4,
                bbox=dict(boxstyle='circle', facecolor='black', alpha=0.7, pad=0.3))
    ax.set_xticks(range(8))
    ax.set_yticks(range(8))
    ax.set_xticklabels([chr(ord('a') + i) for i in range(8)], fontsize=12, fontweight='bold')
    ax.set_yticklabels([str(i + 1) for i in range(8)], fontsize=12, fontweight='bold')
    ax.grid(True, color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
    ax.set_xlim(-0.5, 7.5)
    ax.set_ylim(-0.5, 7.5)
    ax.invert_yaxis()
    ax.set_title(f"Chemin du Cavalier sur Échiquier\nNombre de cases visitées: {len(path)}/64", fontsize=16, fontweight='bold', pad=20)
    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=12, framealpha=0.9)
    ax.set_aspect('equal')
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✓ Chemin sauvegardé dans '{filename}'")

def print_path_info(path):
    if not path:
        print("Aucun chemin disponible")
        return
    print("\n" + "=" * 60)
    print("INFORMATIONS SUR LE CHEMIN DU CAVALIER")
    print("=" * 60)
    print(f"Nombre de cases visitées: {len(path)}/64")
    print(f"Progression: {(len(path)/64)*100:.1f}%")
    print(f"Position de départ: {path[0]}")
    print(f"Position finale: {path[-1]}")
    print("\n📍 Détail du chemin (notation échecs):")
    print("-" * 60)
    for i, (x, y) in enumerate(path):
        col = chr(ord('a') + x)
        row = y + 1
        print(f"{i+1:2d}: {col}{row}", end="  ")
        if (i + 1) % 8 == 0:
            print()
    if len(path) % 8 != 0:
        print()
    print("-" * 60)
    unique_positions = len(set(path))
    if unique_positions < len(path):
        print(f"⚠ Attention: {len(path) - unique_positions} position(s) visitée(s) plusieurs fois")
    else:
        print("✓ Toutes les positions sont uniques")
    print("=" * 60 + "\n")
