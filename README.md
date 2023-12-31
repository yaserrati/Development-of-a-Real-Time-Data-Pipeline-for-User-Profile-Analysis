  # Development-of-a-Real-Time-Data-Pipeline-for-User-Profile-Analysis
This training program aims to empower participants to design, develop and deploy a real-time data pipeline using PySpark, Kafka, Cassandra and MongoDB. Participants will learn how to efficiently transform, aggregate, and store user data generated by randomuser.me.



# Planification de project:
<img width="854" alt="image" src="https://github.com/yaserrati/Development-of-a-Real-Time-Data-Pipeline-for-User-Profile-Analysis/assets/88887542/eb96beaf-5e60-40eb-8b4e-f2de5099209a">

# Introduction:
Introduction :

Dans un monde où les données sont considérées comme le nouvel or, il est impératif pour les organisations de pouvoir traiter et analyser les données en temps réel pour prendre des décisions éclairées. Ce programme est conçu pour les professionnels de la donnée qui cherchent à acquérir des compétences pratiques dans la mise en œuvre de pipelines de données en temps réel.

Notre projet consiste à mettre en place un pipeline de données en temps réel afin de relever les défis liés à la gestion et à l'analyse de données en temps réel. Nous utiliserons des technologies telles que PySpark, Kafka, Cassandra et MongoDB pour collecter, transformer et stocker les données de manière efficace et sécurisée.

L'objectif de ce rapport est de présenter les différentes étapes du projet et de décrire en détail les solutions mises en œuvre pour chaque étape. Nous commencerons par la configuration de l'environnement en installant les dépendances nécessaires et en mettant en place les outils tels que PySpark, Kafka, Cassandra et MongoDB. Ensuite, nous détaillerons la mise en place des fonctions de sauvegarde des données dans Cassandra et MongoDB.

Une fois l'environnement configuré, nous créerons une session Spark qui nous permettra de traiter les données en temps réel de manière efficace. Nous lirons ensuite les données en streaming à partir du topic Kafka spécifié, en les transformant selon nos besoins. Nous effectuerons des opérations de transformation telles que la construction du nom complet, la validation ou le recalcul de l'âge, et la construction d'une adresse complète.

Les données transformées seront ensuite sauvegardées dans une table Cassandra pour une analyse ultérieure. Nous mettrons également en place des agrégations pour extraire des insights, tels que le nombre d'utilisateurs par nationalité, l'âge moyen des utilisateurs et les domaines de courriel les plus courants. Les résultats agrégés seront stockés dans des collections MongoDB.

Nous surveillerons la sortie de la console pour vérifier les résultats agrégés et détecter d'éventuelles erreurs. Enfin, nous créerons des tableaux de bord interactifs à l'aide de Python Dash pour visualiser les données agrégées au niveau de MongoDB.

Ce rapport détaillera également les mesures de sécurité mises en place pour assurer la conformité avec le RGPD. Nous rédigerons un registre détaillant tous les traitements de données personnelles effectués, les types de données stockées, les finalités du traitement, et les mesures de sécurité mises en place. De plus, nous mettrons en œuvre des procédures de tri et de suppression des données personnelles inutiles ou trop anciennes, conformément aux exigences du RGPD.

En conclusion, la mise en place de ce pipeline de données en temps réel nous permettra de collecter, transformer, stocker et analyser les données de manière efficace et sécurisée. Ce rapport détaillera les différentes étapes du projet ainsi que les solutions mises en œuvre pour relever les défis liés à la gestion des données en temps réel.

# Configuration de l'environnement
La configuration de l'environnement pour la mise en place du pipeline de données en temps réel a été réalisée en installant et en configurant plusieurs composants clés. Les principaux composants déployés étaient ZooKeeper, Cassandra, Kafka, MongoDB, PyDash et Spark.

ZooKeeper est un service de coordination distribué utilisé pour gérer la configuration, le suivi des états et la synchronisation des différents nœuds du cluster Kafka. Il a été installé et configuré pour garantir un fonctionnement stable et fiable de notre infrastructure.
### To start zookeeper:
````
zookeeper-server-start.bat ..\..\config\zookeeper.properties
````

<img width="955" alt="image" src="https://github.com/yaserrati/Development-of-a-Real-Time-Data-Pipeline-for-User-Profile-Analysis/assets/88887542/f34040f3-d55d-408a-a9ee-5d497403b0a3">

Cassandra, une base de données NoSQL haute performance, a été installée pour stocker les données brutes et transformées. Nous avons configuré les paramètres de réplication et de partitionnement pour garantir la disponibilité et la scalabilité des données.

Kafka, une plateforme de streaming distribuée, a été installée pour la collecte et la diffusion en temps réel des données. Nous avons configuré les topics et les partitions pour assurer une ingestion efficace des données en streaming.
### To Start Kafka:
````
kafka-server-start.bat ..\..\config\server.properties
````


MongoDB, une base de données orientée documents, a été utilisée pour stocker les résultats agrégés et faciliter la visualisation des données à l'aide de tableaux de bord interactifs. Nous avons configuré les collections et les index pour optimiser les performances de lecture et d'écriture.

<img width="194" alt="image" src="https://github.com/yaserrati/Development-of-a-Real-Time-Data-Pipeline-for-User-Profile-Analysis/assets/88887542/2f0e2ed4-aff9-4eac-8571-3be838c91dab">

PyDash, une bibliothèque Python, a été utilisée pour créer des tableaux de bord interactifs permettant de visualiser les données en temps réel. Nous avons configuré les tableaux de bord en fonction des besoins spécifiques de l'organisation.

Enfin, Spark, un framework de traitement des données distribué, a été configuré pour gérer les transformations et les agrégations des données en temps réel. Nous avons configuré les ressources et les paramètres de Spark pour garantir des performances optimales lors du traitement des données.

L'installation et la configuration de ces composants ont été essentielles pour créer un environnement robuste et fonctionnel capable de traiter et d'analyser efficacement les données en temps réel. Chaque composant a été soigneusement configuré pour garantir une intégration fluide et une performance optimale dans l'ensemble du pipeline de données.


# Collecte des données en temps réel avec Kafka
Pour la collecte des données en temps réel, nous avons développé un script Python nommé "Preducer.py". Ce script utilise la bibliothèque KafkaProducer pour envoyer les données collectées vers un topic Kafka spécifié.

Le script commence par définir le nom du topic Kafka dans lequel les données seront publiées. Ensuite, il configure les paramètres de connexion à Kafka en spécifiant l'adresse et le port du serveur Kafka.

Dans la boucle principale du script, nous avons utilisé la bibliothèque requests pour effectuer une requête vers l'API RandomUser.me et récupérer les données utilisateur. Nous avons ajouté des mécanismes de gestion des erreurs pour gérer les éventuelles exceptions liées aux requêtes HTTP ou au format JSON des réponses.

Une fois les données récupérées, nous les avons sérialisées au format JSON à l'aide de la fonction json.dumps(). Ensuite, nous avons utilisé la méthode send() du KafkaProducer pour envoyer les données vers le topic Kafka spécifié. La méthode flush() est également appelée pour s'assurer que les données sont immédiatement écrites dans le topic.

En cas d'erreur ou d'exception lors de la collecte ou de l'envoi des données, des messages d'erreur appropriés sont affichés pour faciliter le débogage.

Pour éviter de saturer l'API RandomUser.me ou le serveur Kafka, nous avons ajouté une pause de 6 secondes entre chaque collecte de données.

Ce script Python a été efficace pour collecter les données en temps réel à partir de l'API RandomUser.me et les envoyer vers le topic Kafka spécifié. Il a permis d'assurer une collecte continue et régulière des données, ce qui a constitué la première étape cruciale de notre pipeline de données en temps réel.

# Transformation et agrégation des données et Stockage des données dans Cassandra et MongoDB

Pour stocker les données collectées, nous avons utilisé deux bases de données : Cassandra et MongoDB. 

Pour Cassandra, nous avons créé une connexion à l'aide de la bibliothèque Cassandra-Driver. Un keyspace nommé "jane_keyspace" a été créé en utilisant une stratégie de réplication simple avec un facteur de réplication de 1. Ensuite, nous avons défini une table appelée "users_table" avec des colonnes correspondant aux attributs des données collectées, tels que l'ID, le genre, le nom, l'adresse e-mail, le numéro de téléphone, etc. Les données ont été filtrées pour s'assurer que l'ID est non nul et que l'âge est supérieur ou égal à 18. Les données nettoyées ont ensuite été écrites en utilisant la fonction writeStream de Spark, avec les options appropriées pour indiquer le chemin de sauvegarde des checkpoints, le nom du keyspace et le nom de la table dans Cassandra. Ainsi, les données ont été stockées de manière incrémentielle au fur et à mesure de leur collecte.

En ce qui concerne MongoDB, nous avons utilisé la bibliothèque Pymongo pour établir une connexion avec la base de données MongoDB locale. L'URI de connexion était "mongodb://localhost:27017", et nous avons défini le nom de la base de données comme "users_profiles" et le nom de la collection comme "user_collection". Cependant, le code pour l'écriture des données dans MongoDB a été commenté et n'a pas été exécuté.

En conclusion, nous avons mis en place un système de stockage pour les données collectées en utilisant Cassandra et MongoDB. Les données ont été écrites dans Cassandra en utilisant Spark pour une sauvegarde incrémentielle, tandis que l'écriture des données dans MongoDB n'a pas été réalisée dans le code fourni. Ces étapes de stockage ont permis de créer une base solide pour le traitement ultérieur des données dans le pipeline.

# Surveillance et validation des résultats

# Visualisation des données à l'aide de tableaux de bord interactifs

<img width="874" alt="image" src="https://github.com/yaserrati/Development-of-a-Real-Time-Data-Pipeline-for-User-Profile-Analysis/assets/88887542/9fe9b3ae-aff2-4eb7-ac96-6086537857ee">

<img width="443" alt="image" src="https://github.com/yaserrati/Development-of-a-Real-Time-Data-Pipeline-for-User-Profile-Analysis/assets/88887542/19c40dd5-b436-41cf-b8c5-a8e250020cbf">




# Mesures de sécurité et conformité avec le RGPD
Dans le cadre de la conformité avec le RGPD, des mesures de sécurité ont été mises en place pour garantir la confidentialité et la protection des données sensibles. Parmi ces mesures, nous avons appliqué un processus de chiffrement sur certaines colonnes sensibles telles que l'email, le numéro de téléphone et l'adresse.

Pour réaliser le chiffrement, nous avons utilisé l'algorithme de hachage SHA-256. Cet algorithme transforme les données en une empreinte numérique unique et irréversible. Ainsi, même en cas de compromission des données, il serait extrêmement difficile de retrouver les informations d'origine.

Dans notre pipeline de données, nous avons utilisé la fonction sha2 de PySpark pour appliquer le chiffrement sur les colonnes concernées. Par exemple, le code suivant illustre le chiffrement des colonnes "email", "phone" et "address" :
````
#  encrypt  email, password,phone, and cell using SHA-256
result_df = result_df.withColumn("email", F.sha2(result_df["email"], 256))
result_df = result_df.withColumn("phone", F.sha2(result_df["phone"], 256))
result_df = result_df.withColumn("address", F.sha2(result_df["address"], 256))
````
Ce processus de chiffrement renforce la protection des données sensibles en rendant les informations d'identification personnelles pratiquement indéchiffrables sans la clé correspondante. Ainsi, même en cas d'accès non autorisé aux données, les informations personnelles restent sécurisées.

En appliquant ce chiffrement sur les colonnes sensibles, nous avons respecté les principes fondamentaux du RGPD en garantissant la confidentialité et la protection des données personnelles. Les données chiffrées peuvent être utilisées en toute sécurité pour des analyses ultérieures sans compromettre la vie privée des individus concernés.

Il convient de noter que la sécurité et la protection des données ne se limitent pas au chiffrement. D'autres mesures de sécurité, telles que la gestion des accès et les politiques de confidentialité, doivent également être mises en place pour garantir une conformité complète avec les exigences du RGPD.

# Conclusion :

En conclusion, la mise en place de ce pipeline de données en temps réel a permis de collecter, transformer, stocker et analyser les données de manière efficace et sécurisée. Grâce à l'utilisation de technologies telles que PySpark, Kafka, Cassandra et MongoDB, les organisations ont pu prendre des décisions éclairées en temps réel.

Le pipeline a utilisé Kafka pour collecter les données en streaming de manière fiable et évolutive. Les données ont ensuite été transformées et agrégées pour extraire des insights pertinents. Les résultats ont été stockés dans Cassandra pour une analyse ultérieure, tandis que les agrégations étaient stockées dans MongoDB pour une visualisation interactive.

Des mesures de sécurité ont été mises en place pour garantir la conformité avec le RGPD. Un registre des traitements de données personnelles a été établi et des procédures de tri et de suppression des données inutiles ont été appliquées.

En résumé, ce projet a permis aux organisations de tirer parti des données en temps réel pour prendre des décisions éclairées. Le pipeline a fourni des fonctionnalités de collecte, de transformation, de stockage et d'analyse des données en temps réel, ouvrant ainsi de nouvelles opportunités dans le domaine de la gestion des données en temps réel.
