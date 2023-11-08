# UE MIXTE

## _Service booking_ (en gRPC)

Permet d'avoir la liste de tous les bookings, d'avoir tous les bookings d'une personne et d'ajouter un booking à une personne.

Pour l'utiliser il fait lancer le serveur (booking.py) et le client (user.py)

## _Service movie_ (en GraphQL)

Permet de trouver un film avec son nom, son id, mettre à jour la note d'un film, son nom, ajouter un film, supprimer un film, et trouver les acteurs d'un film

## _Service showtime_ (en gRPC)

Permet d'afficher la liste de tous les films avec leur jour de projection et de filtrer les films projetés un certain jour

Pour l'utiliser, il faut lancer le serveur (showtime.py) et le client (booking.py)

## _Service user_ (en REST et gRPC)

Permet d'ajouter un utilisateur, ainsi que de consulter la liste des utilisateurs et leurs réservations.

Sert aussi de client pour le service booking