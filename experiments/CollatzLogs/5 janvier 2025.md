
J'ai retrouvé mon code pour le graphe de valued path, dans hehe2.py; copié hehe2.ipynb pour jouer.

**Idée:** regarder la composante connexe de zero de paths d'une forme précise

J'ai regardé celle de 01010101, on dirait qu'elle est très structurée: taille 2^n+2:
![[Capture d’écran 2026-01-06 à 09.13.43.png]]

Le problème c'est que, là où je me trompais, 010101 apparait pas naturellement dans les assembly des autres paths de telle sorte que son début = sa fin sur le torus créé par un autre path. Donc on peut pas conclure.

J'ai cherché un peu et j'ai pensé à utiliser plutôt 010101 suivi de 0 verticaux:

![[Capture d’écran 2026-01-06 à 09.16.06.png]]

Mais mon code est inconsistent car il se trompe sur le "next" up de ces paths:

![[Capture d’écran 2026-01-06 à 09.17.29.png]]
Il dit que c'est 0 pour path qui commence par 1 et finit par 2, ce qui est pas possible

Il ya donc un bug dans mon engine :(