import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys

# configurat° lencodage UTF-8 pour windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

base_url = "https://www.free-work.com/fr/tech-it/jobs"
DELAY = 3  # Pause ethique de 3s entre chaque page


print("Testons la connexion au site free-work!!!")
response = requests.get(base_url, headers=headers)
print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    print("Connexion reussie")
else:
    print(f"Erreur de connexion. Code: {response.status_code}")
    exit()

# Etape 3 et 4 du tp: Gestion de la Pagination et des erreurs
print("\n Extraction des offres avec pagination")
nombre_pages = 2  # nbr de pages a scraper (mettre 2 pour 50-100 offres) 
all_jobs = []  # liste pour stocker ttes les offres

for page_number in range(1, nombre_pages + 1):
    # Construire l'URL dynamiquement
    if page_number == 1:
        url = base_url
    else:
        url = f"{base_url}?page={page_number}"

    print(f"\nPage {page_number}/{nombre_pages}: {url}")

    # Recuperer la page
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Erreur sur la page {page_number}. Code: {response.status_code}")
        continue

    # parser le HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # on cherche les liens vers les offres
    liens_offres = soup.find_all('a', href=True)
    offres_urls = [lien for lien in liens_offres if '/jobs/' in lien['href'] and lien['href'].count('/') > 3]

    print(f"Nombre d'offres trouvees: {len(offres_urls)}")

    # Etape 4 du tp: Robustesse extraction avec une gestion des errors
    for i, offre_lien in enumerate(offres_urls, 1):
        try:
            # extraire le titre depuis la page de liste
            titre_element = offre_lien.find('span', class_=lambda x: x and 'job-title' in x)
            titre = titre_element.get_text(strip=True) if titre_element else "N/C"

            # ici on construi l'url complete de l'offre
            url_detail = f"https://www.free-work.com{offre_lien['href']}"

            # recup la page de detail
            response_detail = requests.get(url_detail, headers=headers)

            if response_detail.status_code == 200:
                soup_detail = BeautifulSoup(response_detail.content, 'html.parser')

                # extrair le titre (h2 avec classe font-semibold text-xl)
                titre_element = soup_detail.find('h2', class_=lambda x: x and 'font-semibold' in x and 'text-xl' in x)
                titre = titre_element.get_text(strip=True) if titre_element else "N/C"

                # Filtrer les pages "Ce qu'il faut savoir sur..." (ce ne sont pas de vraies offres)
                if "Ce qu" in titre and "il faut savoir sur" in titre:
                    print(f" [IGNORE] {titre} (page d'info)")
                    continue
                if titre.startswith("DEVIENS") or titre.startswith("Déposez votre CV"):
                    print(f" [IGNORE] {titre} (page générique)")
                    continue

                # extraire l'entreprise (div avec classe font-bold)
                entreprise_element = soup_detail.find('div', class_='font-bold')
                entreprise = entreprise_element.get_text(strip=True) if entreprise_element else "N/C"

                # extraire le salaire (TJM ou annuel)
                tjm = "N/C"
                salaire_annuel = "N/C"
                spans = soup_detail.find_all('span', class_='text-sm truncate w-full')
                for span in spans:
                    texte = span.get_text(strip=True)
                    # Verifier que c'est bien un montant (contient € ou EUR)
                    if '€' not in texte and 'EUR' not in texte:
                        continue

                    # Si c'est un TJM (contient /j) et pas encore trouve
                    if ('/j' in texte or '€⁄j' in texte) and tjm == "N/C":
                        tjm = texte
                    # Si c'est un salaire annuel (contient /an ou k) et pas encore trouve
                    elif (('/an' in texte or '€⁄an' in texte) or ('k' in texte and '€' in texte)) and salaire_annuel == "N/C":
                        salaire_annuel = texte

                # exraire la description (div avec classe fw-text-highlight line-clamp-4)
                description_element = soup_detail.find('div', class_=lambda x: x and 'fw-text-highlight' in x and 'line-clamp-4' in x)
                description = description_element.get_text(strip=True)[:300] if description_element else "N/C"

                # on stock les donnees
                all_jobs.append({
                    'titre': titre,
                    'entreprise': entreprise,
                    'tjm': tjm,
                    'salaire_annuel': salaire_annuel,
                    'description': description
                })

                print(f"  [{len(all_jobs)}] {titre} - {entreprise}")

            else:
                print(f" Erreur detail {response_detail.status_code}")

            # on respecte ici la Pause entre chaque offre
            time.sleep(1)

        except Exception as e:
            print(f" Erreur lors de l'extraction: {str(e)}")
            # on continu avec loffre svte en cas d'erreur
            continue

    # pause ethique entre chaque page (sauf la derniere)
    if page_number < nombre_pages:
        print(f"Pause de {DELAY} secondes avant la page suivante...")
        time.sleep(DELAY)

print(f"\n Total: {len(all_jobs)} offres extraites")

# sstockage des donnes 
if all_jobs:
    # creer un DataFrame pandas
    df = pd.DataFrame(all_jobs)

    # on l'exporte en csv
    df.to_csv("offres_emploi.csv", index=False, encoding='utf-8-sig')

    print(f"\nFichier CSV cree: offres_emploi.csv")
    print(f"Nombre de lignes: {len(df)}")
    print(f"\nApercu des colonnes: {list(df.columns)}")
    print(f"\nPremiere offre:")
    if len(df) > 0:
        print(f"  Titre: {df.iloc[0]['titre']}")
        print(f"  Entreprise: {df.iloc[0]['entreprise']}")
        print(f"  TJM: {df.iloc[0]['tjm']}")
        print(f"  Salaire annuel: {df.iloc[0]['salaire_annuel']}")
        print(f"  Description: {df.iloc[0]['description'][:100]}...")
else:
    print("\nAucune offre extraite. Pas de fichier CSV cree.")
