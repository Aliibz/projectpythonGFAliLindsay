#PARTIE 1
import os
import math
import string

def list_of_files(directory, extension):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

def print_list(files_names):
    for file in files_names:
        print(file)

def extraire(nom_fichier):
    """Extraire les noms des présidents à partir des noms des fichiers texte fournis"""
    # Lire le fichier
    with open(nom_fichier, 'r') as file:
        content = file.read()

    # Diviser le nom
    parties = content.split(" ")
    nom_president = parties[1]

    # Retirer l'extension ".txt"
    nom_president = nom_president.replace(".txt", "")

    return nom_president

def associer(noms_presidents):
    """Associer à chaque président un prénom """
    # Dictionnaire associant le nom du président à son prénom
    prenoms_presidents = {
        'Chirac': 'Jacques',
        'Giscard': 'Valéry',
        'Hollande': 'François',
        'Macron': 'Emmanuel',
        'Mitterrand': 'François',
        'Sarkozy': 'Nicolas'
    }

    # Utiliser une liste pour stocker les prénoms associés
    prenoms_associes = [prenoms_presidents[nom] for nom in noms_presidents]

    return prenoms_associes

def convertir(car):
    """Convertir les textes des 8 fichiers en minuscules"""
    # Convertir un caractère en minuscule en utilisant les codes ASCII
    if 'A' <= car <= 'Z':
        return chr(ord(car) + ord('a') - ord('A'))
    return car

def ponctuation(car):
    """Vérifier si un caractère est une ponctuation manuellement"""
    return car in ",.;:?!()[]{}<>\"'"

def clean_text(text):
    """Convertir les textes en minuscules"""
    text = ''.join(convertir(car) for car in text)

    # Remplacer les caractères spéciaux
    text = text.replace('’', "'")
    text = text.replace('–', ' ')

    # Supprimer la ponctuation
    cleaned_text = ''
    for car in text:
        if not ponctuation(car):
            cleaned_text += car
        else:
            cleaned_text += ' '

    # Supprimer les espaces en double
    cleaned_text = ' '.join(cleaned_text.split())

    return cleaned_text

def process_file(file_path, output_folder):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        cleaned_content = clean_text(content)

    output_file_path = os.path.join(output_folder, os.path.basename(file_path))
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(cleaned_content)

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





#PARTIE 2

#1-
def tokenisation(question):
    """Tokenise la question en mots individuels"""
    # Liste de ponctuations à supprimer
    ponctuations = string.punctuation

    # Supprimer la ponctuation
    question = ''.join(caractere for caractere in question if caractere not in ponctuations)

    # Convertir la question en minuscules
    question = ''.join(caractere.lower() for caractere in question)

 # Tokenisation des mots
    mots = []
    mot_actuel = ''

    for caractere in question:
        if caractere.isspace():
            if mot_actuel:
                mots.append(mot_actuel)
                mot_actuel = ''
        else:
            mot_actuel += caractere

    if mot_actuel:
        mots.append(mot_actuel)

    # Supprimer les mots vides
    mots_vides =' '
    mots = [mot for mot in mots if mot not in mots_vides]

    return mots

# Exemple d'utilisation de la fonction
question_text = "Comment fonctionne la tokenisation des questions?"
question_tokens = tokenisation(question_text)
print(question_tokens)


#2-
def recherche_mot(question, dossier_corpus):
    """Trouve les mots de la question présents dans le corpus"""
    # Tokeniser la question
    mots_question = tokenisation(question)

    # Initialiser un ensemble pour stocker les mots présents dans le corpus
    mots_trouvés= set()

    # Parcourir chaque fichier du corpus
    for fichier in os.listdir(dossier_corpus):
        if fichier.endswith('.txt'):
            chemin_fichier = os.path.join(dossier_corpus, fichier)
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                texte = f.read()
                mots_corpus = set(diviser_texte(texte))

                # Ajouter les mots de la question présents dans le corpus à l'ensemble
                mots_trouvés.update(mot for mot in mots_question if mot in mots_corpus)

    return mots_trouvés


#3-
def TFIDFQuestion(question):
    """Calcule le vecteur TF-IDF pour les termes de la question"""
    # Tokeniser la question
    mots_question = tokenisation(question)

    # Initialiser le vecteur TF-IDF de la question avec des zéros
    vecteur_tfidf_question = [0] * len(scores_idf)

    # Calculer le score TF pour chaque mot de la question
    for mot in mots_question:
        tf = mots_question.count(mot) / len(mots_question)  # TF = fréquence du mot dans la question
        idf = scores_idf.get(mot, 0)  # IDF = score IDF du mot dans le corpus

        # Calculer le score TF-IDF pour le mot
        tfidf = tf * idf

        # Trouver l'indice du mot dans le corpus
        indice_mot_corpus = list(scores_idf.keys()).index(mot)

         # Mettre à jour le vecteur TF-IDF de la question
        vecteur_tfidf_question[indice_mot_corpus] = tfidf

    return vecteur_tfidf_question

#4 -
# Fonction pour calculer le produit scalaire de deux vecteurs
def produit_scalaire(vecteur_A, vecteur_B):
    return sum(a * b for a, b in zip(vecteur_A, vecteur_B))

# Fonction pour calculer la norme d'un vecteur
def norme_vecteur(vecteur):
    return math.sqrt(sum(x**2 for x in vecteur))

# Fonction pour calculer la similarité de cosinus entre deux vecteurs
def similarite_cosinus(vecteur_A, vecteur_B):
    produit_scalaire_AB = produit_scalaire(vecteur_A, vecteur_B)
    norme_A = norme_vecteur(vecteur_A)
    norme_B = norme_vecteur(vecteur_B)

    if norme_A == 0 or norme_B == 0:
        return 0  # Éviter une division par zéro

    return produit_scalaire_AB / (norme_A * norme_B)

# Fonction pour trouver le document le plus similaire à la question
def document_plus_similaire(question_vector, tf_idf_matrix):
    scores_similarite = []

    for document_vector in tf_idf_matrix:
        sim = similarite_cosinus(question_vector, document_vector)
        scores_similarite.append(sim)

    index_document_plus_similaire = scores_similarite.index(max(scores_similarite))
    return index_document_plus_similaire, scores_similarite


matrice_tf_idf_result, scores_idf_result = calculer_tf_idf(dossier_corpus)

# Obtenir le vecteur de la question
question = "Votre question ici"
question_vector = TFIDFQuestion(question)

# Calculer la similarité avec chaque document
indice_document_similaire, scores_similarite = document_plus_similaire(question_vector, matrice_tf_idf_result)

#  Afficher le résultat
print(f"Le document le plus similaire à la question est le document {indice_document_similaire + 1}")
print(f"Scores de similarité : {scores_similarite}")


# Fonction pour trouver le document le plus pertinent à partir de la similarité
def document_plus_pertinent(question_vector, tf_idf_matrix, document_names):
    scores_similarite = []

    for document_vector in tf_idf_matrix:
        sim = similarite_cosinus(question_vector, document_vector)
        scores_similarite.append(sim)

    index_document_plus_pertinent = scores_similarite.index(max(scores_similarite))
    nom_document_plus_pertinent = document_names[index_document_plus_pertinent]

    return nom_document_plus_pertinent

# ...

#  Calculer la matrice TF-IDF
matrice_tf_idf_result, scores_idf_result = calculer_tf_idf(dossier_corpus)

# Obtenir le vecteur de la question
question = "Votre question ici"
question_vector = TFIDFQuestion(question)

# Trouver le document le plus pertinent
nom_document_pertinent = document_plus_pertinent(question_vector, matrice_tf_idf_result, os.listdir(dossier_corpus))

# Afficher le résultat
print(f"Le document le plus pertinent à la question est : {nom_document_pertinent}")

# Fonction pour trouver le mot avec le score TF-IDF le plus élevé dans le vecteur de la question
def mot_max_tfidf(question_vector, scores_idf):
    mots_question = [mot for mot, score_idf in scores_idf.items()]
    indices_mots_question = [list(scores_idf.keys()).index(mot) for mot in mots_question]

    # Trouver l'indice du mot avec le score TF-IDF le plus élevé
    indice_mot_max_tfidf = max(indices_mots_question, key=lambda x: question_vector[x])
    mot_max_tfidf = mots_question[indice_mot_max_tfidf]

    return mot_max_tfidf


# Fonction pour générer une réponse à partir du document pertinent
def generer_reponse(nom_document_pertinent, mot_max_tfidf):
    chemin_fichier = os.path.join(dossier_corpus, nom_document_pertinent)

    with open(chemin_fichier, 'r', encoding='utf-8') as f:
        texte = f.read()
        phrases = texte.split('.')
        for phrase in phrases:
            if mot_max_tfidf in phrase:
                return phrase.strip()

    return "Aucune phrase trouvée."

# ...

# Partie 1: Calculer la matrice TF-IDF
matrice_tf_idf_result, scores_idf_result = calculer_tf_idf(dossier_corpus)

#  Obtenir le vecteur de la question
question = "Peux-tu me dire comment une nation peut-elle prendre soin du climat ?"
question_vector = TFIDFQuestion(question)

# Trouver le document le plus pertinent
nom_document_pertinent = document_plus_pertinent(question_vector, matrice_tf_idf_result, os.listdir(dossier_corpus))

# Trouver le mot avec le score TF-IDF le plus élevé dans la question
mot_max_tfidf_question = mot_max_tfidf(question_vector, scores_idf_result)

# Générer la réponse
reponse = generer_reponse(nom_document_pertinent, mot_max_tfidf_question)

# Afficher le résultat
print(f"Le mot avec le TF-IDF le plus élevé dans la question est : {mot_max_tfidf_question}")
print(f"La réponse générée est : {reponse}")


# Fonction pour affiner la réponse en fonction de la forme de la question
def affiner_reponse(question, reponse):
    question_starter = question.split()[0] if question else ""

    # Liste de propositions non exhaustives
    question_starters = {
        "Comment": "Après analyse, ",
        "Pourquoi": "Car, ",
        "Peux-tu": "Oui, bien sûr!"
    }

    modele_reponse = question_starters.get(question_starter, "")

    if modele_reponse:
        reponse = modele_reponse + reponse

    # Mettre une majuscule en début de phrase et un point à la fin
    reponse = reponse.capitalize().strip() + "."

    return reponse

# ...

