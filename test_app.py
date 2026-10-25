# Vérifications automatiques de l'application
from app import app

client = app.test_client()


# Vérifier la page d'accueil
def test_accueil():
    reponse = client.get("/")
    assert reponse.status_code == 200


# Vérifier l'état du service
def test_health():
    reponse = client.get("/health")
    assert reponse.status_code == 200
    assert reponse.get_json()["status"] == "ok"


# Vérifier la liste des notes
def test_liste_notes():
    reponse = client.get("/notes")
    assert reponse.status_code == 200
    assert len(reponse.get_json()) >= 2


# Vérifier la recherche d'un étudiant
def test_recherche_etudiant():
    reponse = client.get("/notes?etudiant=Amina")
    assert reponse.status_code == 200
    assert reponse.get_json()[0]["note"] == 15.5