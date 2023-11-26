import os

directory = "C:/Users/alayo/Desktop/projectpython"


def list_of_files(directory, extension):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names


files_names = list_of_files(directory, "txt")
a = print(files_names)


def noms(l):
    m = []
    for i in range(len(l)):
        nom = ""
        for j in range(11, len(l[i])):
            if ord(l[i][j]) >= 65 and ord(l[i][j]) <= 90 or ord(l[i][j]) >= 97 and ord(l[i][j]) <= 122:
                nom += l[i][j]
        nom = nom[:-3]
        m.append(nom)
    return m


print(noms(files_names))


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
    # Convertir les textes en minuscules
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

def main():
    speeches_folder = 'speeches'
    cleaned_folder = 'cleaned'

    # Créer le dossier cleaned s'il n'existe pas
    if not os.path.exists(cleaned_folder):
        os.makedirs(cleaned_folder)

    # Traiter chaque fichier dans le dossier speeches
    for filename in os.listdir(speeches_folder):
        if filename.endswith('.txt'):
            file_path = os.path.join(speeches_folder, filename)
            process_file(file_path, cleaned_folder)

    print("Conversion et nettoyage terminés.")

if __name__ == "__main__":
    main()
