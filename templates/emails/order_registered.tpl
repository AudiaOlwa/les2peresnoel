{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello {{ user.name }}
{% endblock %}

{% block html %}
    <div style="text-align: center;">
        <img src="{{ logo_url }}" alt="MPERESBONHEUR" style="max-width: 150px;">
    </div>
    <h1>Bonjour {{ first_name | capfirst}},</h1>
    <p>Nous vous remercions pour votre commande. Votre commande a été enregistrée avec succès.</p>
    <p>Voici votre numéro de suivi :</p>
    <h2>{{ tracking_number }}</h2>
    <p>Vous pouvez suivre votre commande en utilisant ce numéro.</p>
    <p>Merci de votre confiance,</p>
    <p>L'équipe de MPERESBONHEUR</p>
{% endblock %}