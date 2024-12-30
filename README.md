# SAE3.02

Welcome


Le lien vers la vidéo: https://youtu.be/BqmgFBR5n-8?feature=shared


Un sujet plus simple
Après avoir lu le sujet plus complet, je vous propose de travailler sur les éléments
suivants :
• Coder un serveur
  o Le serveur reçoit une requête d’un client
    § S’il a déjà un programme qui s’exécute d’un autre client, il renvoie un message indiquant qu’il doit se connecter à un autre serveur.
    § S’il n’a pas de programme qui s’exécute
      • Le serveur reçoit le programme
      • Le serveur compile le programme si nécessaire
      • Le serveur exécute le programme
      • Le serveur renvoie au client les résultats du programme
  o Au démarrage, le serveur doit pouvoir s’exécuter sur un port donné en argument - je peux démarrer plusieurs serveurs si je le souhaite -

• Coder un client
  o Le client doit être sous forme d’une interface graphique
  o L’utilisateur upload le programme à envoyer au serveur
  o L’utilisateur spécifie le nom ou l’IP de la machine
  o Le programme est envoyé au serveur
        § Si le serveur rejette le programme, un nouveau nom/IP/port peut être proposé sans interrompre le programme
        § Si le serveur accepte le programme, le client attends (sans bloquer l’interface qui aVichera un compteur de temps) et aViche le résultat lorsque le serveur lui renvoie le résultat.
