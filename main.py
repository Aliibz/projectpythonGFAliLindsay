from Functions import *

# Programme principal
if __name__ == "__main__":
    dossier_corpus = 'cleaned'

    while True:
        print("\nMenu:")
        print("1. Accéder aux traitement de texte")
        print("2. Accéder au Chatbot")

        choix = input("Choisissez une option (1 ou 2) : ")

        if choix == '1':
            # Partie I: traitement de texte
            print("1. Afficher la liste des mots les moins importants")
            print("2. Afficher le(s) mot(s) ayant le score TD-IDF le plus élevé")
            print("3. Afficher le mot le plus répété par Chirac")
            print("4. Afficher le président parlant le plus de la 'Nation'")
            print("5. Afficher le premier président à parler du climat et/ou de l’écologie")
            print("6. Afficher les mots évoqués par tous les présidents")

            choix_partie1 = input("Choisissez une option (1 à 6) : ")

            if choix_partie1 == '1':
                # Afficher la liste des mots les moins importants
                matrice_tf_idf_result, scores_idf_result = calculer_tf_idf(dossier_corpus)
                afficher_mots_peu_importants(matrice_tf_idf_result, scores_idf_result)

            elif choix_partie1 == '2':
                # Afficher le(s) mot(s) ayant le score TD-IDF le plus élevé
                matrice_tf_idf_result, scores_idf_result = calculer_tf_idf(dossier_corpus)
                afficher_mot_plus_importants(matrice_tf_idf_result, scores_idf_result)

            elif choix_partie1 == '3':
                # Afficher le mot le plus répété par Chirac
                mots_plus_repetes_chirac(dossier_corpus)

            elif choix_partie1 == '4':
                # Afficher le président parlant le plus de la 'Nation'
                president_parle_de_nation(dossier_corpus)

            elif choix_partie1 == '5':
                # Afficher le premier président à parler du climat et/ou de l’écologie
                premier_president_climat_ecologie(dossier_corpus)

            elif choix_partie1 == '6':
                # Afficher les mots évoqués par tous les présidents
                mots_evoques_par_tous(dossier_corpus)

            elif choix_partie1 == '0':
                # Quitter le programme
                print("Au revoir !")
                break

            else:
                print("Option invalide.")



        elif choix == '2':
            # Partie II: Chatbot
            question = input("Posez votre question au Chatbot : ")

            # Calculer la matrice TF-IDF
            matrice_tf_idf_result, scores_idf_result = calculer_tf_idf(dossier_corpus)

            # Obtenir le vecteur de la question
            question_vector = TFIDFQuestion(question, scores_idf_result)

            # Trouver le document le plus pertinent
            nom_document_pertinent = document_plus_pertinent(question_vector, matrice_tf_idf_result, os.listdir(dossier_corpus))

            # Trouver le mot avec le score TF-IDF le plus élevé dans la question
            mot_max_tfidf_question = mot_max_tfidf(question_vector, scores_idf_result)

            # Générer la réponse
            reponse = generer_reponse(nom_document_pertinent, mot_max_tfidf_question)

            # Affiner la réponse
            reponse_affinee = affiner_reponse(question, reponse)

            #  Afficher le résultat
            print("Réponse générée par le Chatbot :")
            print(reponse_affinee)

        else:
            print("Option invalide.")