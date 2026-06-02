#main.py
import time
from Population import Population
from genetic import plot_path, save_path, print_path_info

POPULATION_SIZE = 50
MUTATION_RATE = 0.001 
MAX_GENERATIONS = 10000

def main():
    print("=" * 80)
    print(" " * 20 + "RÉSOLUTION DU PROBLÈME DU CAVALIER")
    print(" " * 15 + "PAR ALGORITHME GÉNÉTIQUE")
    print("=" * 80)
    print("\n📊 PARAMÈTRES DE L'ALGORITHME:")
    print("-" * 40)
    print(f" • Taille de la population : {POPULATION_SIZE}")
    print(f" • Taux de mutation : {MUTATION_RATE * 100}%")
    print(f" • Générations maximum : {MAX_GENERATIONS}")
    print("-" * 40)
    print("\n🚀 Démarrage de l'algorithme...\n")

    population = Population(POPULATION_SIZE)
    best_fitness_ever = 0
    best_solution_ever = None
    all_solutions = []
    start_time = time.time()
    while population.generation <= MAX_GENERATIONS:
        population.check_population()
        max_fit, best_solution = population.evaluate()
        mean_fit = sum(k.fitness for k in population.knights) / POPULATION_SIZE
        if population.generation % 20 == 0:
            print(f"Fitness moyen : {mean_fit:.2f}")
        if max_fit > best_fitness_ever:
            best_fitness_ever = max_fit
            best_solution_ever = best_solution
            print(f"🎯 NOUVEAU RECORD ! Génération {population.generation:4d} | Fitness: {max_fit:2d}/64 | Progrès: {(max_fit/64)*100:5.1f}%")
        if max_fit > 40 and max_fit not in [s[1] for s in all_solutions]:
            all_solutions.append((best_solution, max_fit, population.generation))
        if population.generation % 50 == 0:
            progress = (max_fit / 64) * 100
            print(f"⏳ Génération {population.generation:4d} | Meilleur fitness: {max_fit:2d}/64 | Progrès: {progress:5.1f}%")
        if max_fit == 64:
            print("\n" + "=" * 80)
            print("🎉✨ SOLUTION PARFAITE TROUVÉE ! ✨🎉")
            print("=" * 80)
            break
        population.create_new_generation(MUTATION_RATE)

    end_time = time.time()
    execution_time = end_time - start_time
    print("\n📈 RÉSULTATS FINAUX:")
    print("-" * 40)
    print(f" • Temps d'exécution : {execution_time:.2f} secondes")
    print(f" • Générations écoulées : {population.generation}")
    print(f" • Meilleure fitness : {best_fitness_ever}/64")
    statut = '✅ RÉSOLU' if best_fitness_ever == 64 else '❌ Non résolu (limite atteinte)'
    print(f" • Statut : {statut}")
    print(f" • Solutions intéressantes trouvées : {len(all_solutions)}")
    print("-" * 40)
    if best_solution_ever:
        print_path_info(best_solution_ever.path)
    print("\n🎨 GÉNÉRATION DES VISUALISATIONS...")
    for i, (solution, fitness, gen) in enumerate(all_solutions):
        filename = f'knight_tour_gen{gen}_fit{fitness}.png'
        save_path(solution.path, filename)
    print(f"✅ {len(all_solutions)} visualisations sauvegardées avec succès!")
    print("\n" + "=" * 80)
    response = input("🎮 Voulez-vous lancer l'interface graphique animée? (o/n): ").lower()
    if response in ["o", "oui"]:
        try:
            from interface import KnightTourGame
            game = KnightTourGame(best_solution_ever, all_solutions)
            game.run()
        except ImportError:
            print("❌ Erreur: Impossible d'importer l'interface graphique.")
            print("   Assurez-vous que le fichier interface.py est présent.")
        except Exception as e:
            print(f"❌ Erreur lors du lancement de l'interface: {e}")

if __name__ == "__main__":
    main()
