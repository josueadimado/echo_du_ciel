Placez vos images ici !

Structure recommandée :
- hero-background.jpg (image de fond pour la section hero)
- choir-logo.png (logo de la chorale)
- concert-poster.jpg (affiche du concert)

Après avoir ajouté les images, utilisez-les dans les templates avec :
{% load static %}
<img src="{% static 'lyrics/images/nom-image.jpg' %}" alt="Description">
