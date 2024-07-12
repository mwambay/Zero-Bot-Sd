## Calcul de la Perplexité

La perplexité (PPL) est une mesure de la qualité d'un modèle de langage. Elle évalue à quel point un modèle prédit une séquence de mots. Plus la perplexité est faible, meilleur est le modèle à prédire les mots dans la séquence.
Étapes du calcul de la perplexité

 ###   Tokenisation du texte :
        Le texte est divisé en tokens (mots ou sous-mots) que le modèle peut comprendre.

 ###   Calcul de la probabilité logarithmique négative (NLL) :
        Pour chaque segment de la phrase (d'une longueur déterminée par le modèle), la probabilité logarithmique négative est calculée. Cette valeur représente la difficulté pour le modèle de prédire le prochain token dans la séquence.
        Le modèle prédit la probabilité de chaque token donné les tokens précédents, et la NLL est une mesure de la somme de ces probabilités logarithmiques inversées.

 ###   Sommation des NLLs :
        Les NLLs de tous les segments sont additionnées pour obtenir la probabilité logarithmique négative totale pour l'ensemble du texte.

 ###   Exponentialisation et normalisation :
        La somme des NLLs est exponentiée pour obtenir la perplexité, qui est une mesure exponentielle de la "surprise" moyenne pour chaque token.
        La formule de la perplexité est :
        Perplexiteˊ=exp⁡(NLL totalenombre de tokens)
        Perplexiteˊ=exp(nombre de tokensNLL totale​)

### Interprétation de la Perplexité

 ###   Perplexité faible :
        Indique que le modèle trouve le texte relativement prévisible et qu'il est probablement de haute qualité.
        Pour un texte généré par une IA entraînée sur un grand corpus de données, on s'attend à une perplexité faible car le modèle est bien adapté aux données qu'il a vues.

  ###  Perplexité élevée :
        Indique que le modèle trouve le texte difficile à prédire, suggérant que le texte est de moins bonne qualité ou moins conforme aux données sur lesquelles le modèle a été entraîné.
        Pour un texte écrit par un humain, surtout s'il est créatif ou complexe, la perplexité peut être plus élevée.

### Utilisation pour déterminer l'origine du texte

### Le modèle utilise des seuils pour classifier le texte :

  ###  Si la perplexité est en dessous d'un certain seuil (faible perplexité) :
        Le texte est probablement généré par une IA car il est très prévisible pour le modèle.

   ### Si la perplexité est au-dessus d'un certain seuil mais en dessous d'un autre (perplexité moyenne) :
        Le texte pourrait contenir des parties générées par une IA, mais une évaluation plus poussée est nécessaire.

   ### Si la perplexité est au-dessus du seuil supérieur (perplexité élevée) :
        Le texte est probablement écrit par un humain, car il est moins prévisible pour le modèle.

En résumé, la perplexité mesure la capacité du modèle à prédire les tokens dans le texte. Elle est utilisée pour estimer si un texte est généré par une IA ou un humain en comparant la perplexité calculée avec des seuils prédéfinis.
