# ============================================================
# Application de consultation et de modification des notes
# ============================================================

import os
import sqlite3
import auth

from flask import Flask, jsonify, request

app = Flask(__name__)

# Fichier où sont conservées les notes de l'école
DB = "notes.db"


# Prépare le registre des notes au démarrage
def init_db():
    with sqlite3.connect(DB) as con:
        con.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY,
                etudiant TEXT,
                module TEXT,
                note REAL
            )
            """
        )

        if con.execute("SELECT COUNT(*) FROM notes").fetchone()[0] == 0:
            con.executemany(
                """
                INSERT INTO notes (etudiant, module, note)
                VALUES (?, ?, ?)
                """,
                [
                    ("Amina", "DevSecOps", 15.5),
                    ("Youssef", "DevSecOps", 12.0),
                ],
            )


init_db()


# Page d'accueil
@app.route("/")
def accueil():
    return (
        "<!DOCTYPE html><html lang='fr'><head><meta charset='utf-8'>"
        "<title>Notes des étudiants</title></head><body>"
        "<h1>Consultation des notes</h1>"
        "<p><a href='/notes'>Voir les notes</a></p></body></html>"
    )


# Vérification de l'état de l'application
@app.route("/health")
def health():
    return jsonify(status="ok", version="1.0")


# Consultation des notes
@app.route("/notes", methods=["GET"])
def lister_notes():
    etudiant = request.args.get("etudiant", "")

    with sqlite3.connect(DB) as con:
        rows = con.execute(
            """
            SELECT id, etudiant, module, note
            FROM notes
            WHERE etudiant LIKE ?
            """,
            (f"%{etudiant}%",),
        ).fetchall()

    return jsonify(
        [
            {
                "id": row[0],
                "etudiant": row[1],
                "module": row[2],
                "note": row[3],
            }
            for row in rows
        ]
    )


# Modification sécurisée d'une note
@app.route("/notes/<int:note_id>", methods=["PUT"])
def modifier_note(note_id):

    # S2 : authentification obligatoire
    utilisateur = auth.utilisateur_connecte()

    if utilisateur is None:
        return jsonify(erreur="Authentification requise"), 401

    # S3 : seuls les enseignants peuvent modifier les notes
    if utilisateur.get("role") != "enseignant":
        return jsonify(erreur="Accès interdit"), 403

    # S5 : validation des données reçues
    donnees = request.get_json(silent=True)

    if not isinstance(donnees, dict):
        return jsonify(erreur="Données invalides"), 400

    note = donnees.get("note")

    if isinstance(note, bool) or not isinstance(note, (int, float)):
        return jsonify(
            erreur="La note doit être un nombre entre 0 et 20"
        ), 400

    if not 0 <= note <= 20:
        return jsonify(
            erreur="La note doit être un nombre entre 0 et 20"
        ), 400

    try:
        with sqlite3.connect(DB) as con:

            # Vérifier que la note existe
            resultat = con.execute(
                "SELECT module FROM notes WHERE id = ?",
                (note_id,),
            ).fetchone()

            if resultat is None:
                return jsonify(erreur="Note introuvable"), 404

            module = resultat[0]

            # S4 : vérifier le module de l'enseignant
            if utilisateur.get("module") != module:
                return jsonify(erreur="Accès interdit"), 403

            # S6 : mettre à jour la note avec une requête paramétrée
            con.execute(
                "UPDATE notes SET note = ? WHERE id = ?",
                (note, note_id),
            )

        return jsonify(message="Note modifiée avec succès"), 200

    except sqlite3.Error:
        # S7 : ne pas exposer les détails techniques
        app.logger.exception(
            "Erreur interne lors de la modification d'une note"
        )
        return jsonify(
            erreur="Une erreur interne est survenue"
        ), 500


# Démarrage du serveur en local
if __name__ == "__main__":
    app.run(
        host=os.environ.get("APP_HOST", "127.0.0.1"),
        port=5000,
    )
