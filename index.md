---
author: "Ludovica Pannitto"
layout: "default"
---

# **LISA - un tagger semantico *leggero* per l'italiano**
*Tesi di laurea triennale in Informatica Umanistica - Università di Pisa*

Relatore: Prof. Alessandro Lenci, Correlatore: Dott. Felice dell'Orletta

Il testo della relazione è disponibile seguendo [questo](http://ellepannitto.github.io/LISA/relazione/relazione.pdf) link.
Per una versione più breve, sono disponibili le [slides](http://ellepannitto.github.io/LISA/relazione/slides.pdf).

#### Abstract:
Il lavoro ha come oggetto lo sviluppo di un tagger semantico per i nomi italiani. Il task, di SuperSense Tagging, è presentato in letteratura come a metà strada tra un task di Word Sense Disambiguation (WSD) e un task di Named Entity Recognition (NER), e consiste nell’annotare ogni entità in un contesto con la categoria giusta in riferimento ad una certa tassonomia.
Anche a questo livello fenomeni linguistici come la metonimia introducono notevoli casi di ambiguità (*Il tavolo tre chiede il conto* - *Il cameriere fa accomodare i clienti al tavolo tre*).
La necessità di una classificazione minimale e linguisticamente plausibile, insieme con il desiderio di una classificazione non assoluta del tipo di entità del mondo reale, ma relativa rispetto all’argomento linguistico realizzato dall’entità, ha portato ad elaborare, presso il Laboratorio di Linguistca Computazionale dell’Università di Pisa, la Light Semantic Ontology.
Da questa è stato derivato un tagset per l'annotazione di supersensi su una risorsa automaticamente processata fino al livello sintattico.
Il task è stato poi affrontato come un task supervisionato di classificazione multiclasse, per la costruzione del modello è stata utilizzata una Support Vector Machine con kernel lineare.
I risultati mostrano la rilevanza dei vari tipi di informazione utilizzata, in particolare relativamente all'utilizzo di feature che codificano informazione sintattica e semantica.
Si dimostrano necessarie ulteriori indagini riguardo agli errori prodotti in fase di classificazione e una più ampia esplorazione di altre fonti di informazione da cui ricavare feature diverse rispetto a quelle testate.


