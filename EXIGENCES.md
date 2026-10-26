# Exigences de sécurité de l'application des notes

| # | Exigence : « Le système doit… » | Vérification | Étape du SDLC | Test |
|---|---|---|---|---|
| S1 | Protéger la recherche contre les injections SQL. | Une entrée malveillante ne doit pas modifier la requête SQL. | Développement et tests | test_recherche_resiste_a_l_injection |
| S2 | Refuser toute modification de note sans authentification. | Une requête sans jeton doit retourner HTTP 401. | Développement et tests | test_modification_refusee_sans_identification |
| S3 | Interdire aux étudiants de modifier les notes. | Un étudiant doit recevoir HTTP 403. | Développement et tests | test_modification_refusee_a_un_etudiant |
| S4 | Autoriser un enseignant à modifier uniquement les notes de son module. | Un enseignant d'un autre module doit recevoir HTTP 403. | Développement et tests | test_modification_refusee_a_un_autre_module |
| S5 | Vérifier que chaque note est un nombre compris entre 0 et 20. | Une note invalide doit retourner HTTP 400. | Développement et tests | test_note_invalide_refusee |
| S6 | Permettre à l'enseignant autorisé de modifier une note. | La modification doit retourner HTTP 200 et la nouvelle note doit être enregistrée. | Développement et tests | test_modification_par_l_enseignant_du_module |
| S7 | Ne pas exposer de détails techniques en cas d'erreur. | La réponse d'erreur ne doit pas révéler de détails sur la base de données. | Tests de sécurité | test_erreur_sans_detail_technique |