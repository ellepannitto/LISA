---
author: "Ludovica Pannitto"
layout: "default"
---

Tesi di Laurea Triennale in Informatica Umanistica

Titolo: **LISA**

Abstract: 

*Il presente lavoro ha come oggetto lo sviluppo di un tagger semantico per i nomi italiani. 
Il SuperSense Tagging (SST), a metà strada tra un task di Word Sense Disambiguation (WSD) e un task di Named Entity Recognition (NER), consiste nell’annotare ogni entità in un contesto con la categoria giusta in riferimento ad una certa tassonomia.
Sebbene la definizione delle categorie sia in generale più chiara della definizione di word-sense, fenomeni linguistici come la metonimia introducono notevoli casi di ambiguità.
La necessità di una classificazione minimale e linguisticamente plausibile, insieme con la constatazione che molti dei supersensi derivati dalle classi lessicografiche di WordNet sono problematici, ad esempio la distinzione nel dominio degli astratti o degli eventi, ha portato ad elaborare, presso il Laboratorio di Linguistca Computazionale dell’Università di Pisa, la Light Semantic Ontology.
Da questa è stato derivato un tagset per l'annotazione di supersensi su una risorsa automaticamente processata fino al livello sintattico.
Il task è stato affrontato come un task supervisionato di classificazione multiclasse, per la costruzione del modello è stata utilizzata una Support Vector Machine con kernel lineare.
I risultati mostrano che informazioni su Part of Speech e Morfologia, insieme a pattern di sottocategorizzazione anche identificati semplicemente in n-grammi di parti del discorso, sono le più rilevanti. Per quel che riguarda l’informazione sintattica e semantica, come collocazioni o associazioni semantiche, queste sembrano riuscire a fornire un supporto informativo solo se provenienti da risorse che godono di un alto livello di accuratezza.
Un’analisi più approfondita degli errori commessi in fase di classificazione porterebbe senza dubbio a una maggiore consapevolezza sul funzionamento del sistema e ci permetterebbe di comprenderne meglio le debolezze e i punti di forza.
In Agirre e Stevenson 2007 si suggeriscono altre rilevanti fonti di informazione, citiamo tra le altre esempio l’uso di informazione globale riguardante il dominio o di pattern argomentali, e ciò suggerisce come molto lavoro di feature engineering possa ancora essere fatto. Un altro ambito non toccato da questo lavoro ma trattato in letteratura è l’introduzione di informazione tratta da rappresentazioni delle parole create in modo non supervisionato, ad esempio tramite word embeddings o cluster.*

Puoi scaricare il codice o visualizzarlo su github usando uno dei pulsanti qua sopra.

La risorsa annotata è disponibile seguendo [questo](http://example.com/ "risosrsa annotata") link

La tesi è disponibile seguendo [questo](http://ellepannitto.github.io/Lisa/lisa.pdf "relazione") link

