import os
import math


def diviser_texte(texte, separateur=' '):
    """Divise une chaîne de caractères"""
    mots = []
    mot_actuel = ''

    for car in texte:
        if car == separateur:
            if mot_actuel:
                mots.append(mot_actuel)
                mot_actuel = ''
        else:
            mot_actuel += car

    if mot_actuel:
        mots.append(mot_actuel)

    return mots


def calculer_tf_idf(dossier):
    """Calcule la matrice TF - IDF"""
    documents = []

    # Lire les documents
    for fichier in os.listdir(dossier):
        if fichier.endswith('.txt'):
            chemin_fichier = os.path.join(dossier, fichier)
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                documents.append(f.read())

    # Calculer IDF
    presence_mot = {}
    total_documents = len(documents)

    for document in documents:
        for mot in set(diviser_texte(document)):
            presence_mot[mot] = presence_mot.get(mot, 0) + 1

    scores_idf = {mot: math.log(total_documents / compte) for mot, compte in presence_mot.items()}

    # Calculer TF-IDF
    matrice_tf_idf = []

    for document in documents:
        scores_tf = {}
        for mot in diviser_texte(document):
            scores_tf[mot] = scores_tf.get(mot, 0) + 1

        vecteur_tf_idf = [scores_tf.get(mot, 0) * scores_idf[mot] for mot in scores_idf]
        matrice_tf_idf.append(vecteur_tf_idf)

    return matrice_tf_idf, scores_idf


def afficher_mots_peu_importants(tf_idf_matrix, idf_scores):
    """Affiche la liste des mots les moins importants"""
    mots_peu_importants = [mot for mot, score in idf_scores.items() if all(v == 0 for v in tf_idf_matrix[0])]
    print("Les mots les moins importants sont :", mots_peu_importants)


def afficher_mot_plus_importants(tf_idf_matrix, idf_scores):
    """Affiche le(s) mot(s) ayant le score TD-IDF le plus élevé"""
    mot_importants = max(idf_scores, key=idf_scores.get)
    print("Le(s) mot(s) ayant le score TD-IDF le plus élevé est/sont :", mot_importants)


def mots_plus_repetes_chirac(dossier_corpus):
    """Affiche le mot le plus répété par Chirac"""
    mots_repetes = {}
    mot_max, occurences_max = None, 0

    for fichier in os.listdir(dossier_corpus):
        if fichier.endswith('.txt') and 'Chirac' in fichier:
            chemin_fichier = os.path.join(dossier_corpus, fichier)
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                texte = f.read()
                mots = diviser_texte(texte)
                for mot in mots:
                    mots_repetes[mot] = mots_repetes.get(mot, 0) + 1
                    if mots_repetes[mot] > occurences_max:
                        mot_max, occurences_max = mot, mots_repetes[mot]

    print(f"Le mot le plus répété par Chirac est '{mot_max}' avec {occurences_max} occurrences.")


def president_parle_de_nation(dossier_corpus):
    """Affiche le(s) nom(s) du (des) président(s) qui a (ont) parlé de la « Nation » et celui qui l’a répété le plus de fois"""
    occurrences_par_president = {}
    president_max_occurrences, occurences_max = None, 0

    for fichier in os.listdir(dossier_corpus):
        if fichier.endswith('.txt'):
            chemin_fichier = os.path.join(dossier_corpus, fichier)
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                texte = f.read()
                if 'Nation' in texte:
                    president = fichier.split('_')[1]
                    occurrences_par_president[president] = occurrences_par_president.get(president, 0) + texte.count(
                        'Nation')
                    if occurrences_par_president[president] > occurences_max:
                        president_max_occurrences, occurences_max = president, occurrences_par_president[president]

    if president_max_occurrences is not None:
        print(
            f"Le président parlant le plus de la 'Nation' est {president_max_occurrences} avec {occurences_max} occurrences.")
    else:
        print("Aucun président n'a parlé de la 'Nation'.")


def premier_president_climat_ecologie(dossier_corpus):
    """Affiche le premier président à parler du climat et/ou de l’écologie"""
    presidents_climat_ecologie = set()

    fichiers = os.listdir(dossier_corpus)
    i = 0
    while i < len(fichiers):
        fichier = fichiers[i]
        if fichier.endswith('.txt'):
            chemin_fichier = os.path.join(dossier_corpus, fichier)
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                texte = f.read()

def mots_evoques_par_tous(dossier_corpus):
    """Affiche les mots évoqués par tous les présidents"""
    mots_par_president = {}

    # Parcours manuel du dossier
    fichiers = os.listdir(dossier_corpus)
    i = 0
    while i < len(fichiers):
        fichier = fichiers[i]
        if fichier.endswith('.txt'):
            chemin_fichier = os.path.join(dossier_corpus, fichier)

            # Ouverture manuelle du fichier
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                texte = f.read()
                mots = set(diviser_texte(texte))
                president = fichier.split('_')[1]

                if president not in mots_par_president:
                    mots_par_president[president] = mots
                else:
                    # Intersection manuelle des ensembles
                    mots_par_president[president] = set.intersection(mots_par_president[president], mots)

        i += 1

    # Intersection manuelle des ensembles
    mots_communs = set.intersection(*mots_par_president.values())

    if mots_communs:
        print("Les mots évoqués par tous les présidents sont :", mots_communs)
    else:
        print("Aucun mot commun évoqué par tous les présidents.")



# Programme principal
if __name__ == "__main__":
    dossier_corpus = 'cleaned'

    while True:
        print("\nMenu:")
        print("1. Afficher la liste des mots les moins importants")
        print("2. Afficher le(s) mot(s) ayant le score TD-IDF le plus élevé")
        print("3. Indiquer le(s) mot(s) le(s) plus répété(s) par le président Chirac")
        print("4. Indiquer le(s) nom(s) du (des) président(s) qui a (ont) parlé de la « Nation » et celui qui l’a répété le plus de fois")
        print("5. Indiquer le premier président à parler du climat et/ou de l’écologie")
        print("6. Hormis les mots dits « non importants », quel(s) est(sont) le(s) mot(s) que tous les présidents ont évoqués")

        choix = input("Choisissez une option (1 à 6) : ")

        if choix == '1':
            matrice_tf_idf_result, scores_idf_result = calculer_tf_idf(dossier_corpus)
            afficher_mots_peu_importants(matrice_tf_idf_result, scores_idf_result)
        elif choix == '2':
            matrice_tf_idf_result, scores_idf_result = calculer_tf_idf(dossier_corpus)
            afficher_mot_plus_importants(matrice_tf_idf_result, scores_idf_result)
        elif choix == '3':
            mots_plus_repetes_chirac(dossier_corpus)
        elif choix == '4':
            president_parle_de_nation(dossier_corpus)
        elif choix == '5':
            premier_president_climat_ecologie(dossier_corpus)
        elif choix == '6':
            mots_evoques_par_tous(dossier_corpus)
        else:
            print("Option invalide.")