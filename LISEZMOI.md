# Bienvenu au **Generative Animated Engine v3.1.0** 🐤

[8 minutes de lecture]

**Ce dépôt s'appelait jalagar/Generative_Gif_Engine mais maintenant qu'il supporte GIF, MP4, il a été renommé jalagar/animated-art-engine. v3.1.0 est le début de l'ère de l'animation.**

**Allez voir -pour les anglophones- [Youtube Tutorial](https://www.youtube.com/watch?v=z3jMEx6PRUc) ou [Youtube Tutorial](https://www.youtube.com/watch?v=wjifmH3rmFw) pour les francophones!**

Cette application python et node génère des gifs/MP4, basés sur des calques pour créer de l'art NFT animé ! C'est plus rapide, plus simple et
produit des gifs/MP4 de meilleure qualité que tout autre outil génératif animé en open source. Ça contient aussi de nombreuses autres fonctionnalités, y compris, mais sans s'y limiter, l'empilement des calques, les conditions si-alors, supporte les réseaux ETH/Solana/Tezos, les images d'aperçu, l'insertion de super-rares/légendes faits main, les formats gifs/MP4, et le traitement par lots (batch) poure prendre en charge des centaines de calques et le multitraitement.

Exportez votre animation sous forme de séquence d'images png, organisez vos dossiers de calques avec rareté, et le code fait le reste ! Je prévois de maintenir activement ce dépôt et de l'améliorer avec divers outils pour les mois à venir, alors assurez-vous de poser des questions dans la discussion et d'y décrire vos problèmes.

Il y a 3 étapes:

1. [Python] Convertit les calques en spritesheets à l'aide de [PIL](https://pillow.readthedocs.io/en/stable/). Cette étape peut être ignorée si vous avez déjà les spritesheets, mais
    est utile si vous souhaitez démarrer avec des fichiers png, et facilite la vie de l'artiste !

2. [Node] Créez des spritesheets génératifs à partir des calques de l'étape 1.
    - L'idée originale vient du [MichaPipo's Generative Gif Engine](https://github.com/MichaPipo/Generative_Gif_Engine) mais maintenant la plupart du code de cette étape est dérivé de [nftchef's Generative Engine](https://github.com /nftchef/art-engine) qui est lui-même dérivé de [HashLips Generative Art Engine](https://github.com/HashLips/generative-art-node). Veuillez consulter Hashlip's [📺 Youtube](https://www.youtube.com/channel/UC1LV4_VQGBJHTJjEWUmy8nA) / [👄 Discord](https://discord.com/invite/qh6MWhMJDN) / [🐦 Twitter](https:/ /twitter.com/hashlipsnft) / [ℹ️ Website](https://hashlips.online/HashLips) pour une explication plus détaillée sur le fonctionnement du processus de génération.

3. [Python + gifski/ffmpeg] Convertissez les spritesheets en gifs/MP4 en utilisant Python et [gifski](https://github.com/ImageOptim/gifski) ou [ffmpeg](https://ffmpeg.org/) pour MP4 .

Allez voir [Medium post](https://jalagar-eth.medium.com/how-to-create-generative-animated-nft-art-in-under-an-hour-e7dab1785c56) and [How does it work?](#how-does-it-work) pour plus d'informations!

Voici un exemple de résultat final (ou vous pouvez télécharger le code et l'exécuter et voir plus de balles rebondissantes :)). Il est également visible sur[OpenSea](https://opensea.io/collection/genesis-bouncing-ball).

<img src="./README_Assets/0.gif" width="200"><img src="./README_Assets/1.gif" width="200"><img src="./README_Assets/2.gif" width="200"><img src="./README_Assets/3.gif" width="200">

**EDIT l'outil prends maintenant en compte le z-index/stacking, le grouping, les conditions if-then, et les incompatibilités**. Voir [this section for more information](#nftchef-improvements-z-indexstacking-grouping-if-then-statements-and-incompatibilities). Ci dessous un exemple avec un calque à la fois au dessus et en dessous de la balle.

<img src="./README_Assets/z-index/0.gif" width="200">

## Pré-requis

Installez un IDE de votre choix. [Recomended](https://code.visualstudio.com/download)

Installez la dernière version de Node [Node.js](https://nodejs.org/en/download/)

- Lancez la commande suivante pour vérifier que Node est bien installé:

        node -v

Installez la dernière version de Python [Python 3](https://www.python.org/downloads/). J'utilise actuellement la 3.8.1 mais tout au dessus de la version 3.6 devrait fonctionnner.

- Lancez la commande suivante pour vérifier que python est bien installé:

        python3 --version 

Si vous voulez des Gifs en sortie:

Installez [gifski](https://gif.ski/). Je recommande l'utilisation de brew `brew install gifski` si vous êtes sous Mac OSX. Si vous n'avez pas brew vous pouvez l'installer ainsi [brew](https://brew.sh/) ssur Mac OSX. Ou sous Windows vous pouvez l'installer grâce à [Chocolatey](https://community.chocolatey.org/): `choco install gifski`.

Sous Linux, certaines personnes ont des soucis avec `gifski`. Vous allez devoir régler la configuration `gifTool` sur `imageio` à la place (instructions plus bas).

Si aucune de ces méthodes ne fonctionnent, suivez les instructions sur [gifski Github](https://github.com/ImageOptim/gifski). Gifski est essentiel car il propose le meilleur outil de génération parmi tout ceux que j'ai pu essayé (PIL, imageio, ImageMagic, librairies js).

Si vous voulez des MP4 en sortie:

Installez [ffmpeg](https://ffmpeg.org/). Je recommande l'utilisation de brew `brew install ffmpeg` si vous êtes sous Mac OSX. Si vous n'avez pas brew vous pouvez l'installer ainsi [brew](https://brew.sh/) sur Mac OSX. Ou sous Windows vous pouvez l'installer grâce à [Chocolatey](https://community.chocolatey.org/): `choco install ffmpeg`.

Si vous envisagez de développer sur ce dépôt, exécutez `pre-commit` pour installer les hooks de pré-commit.

Si vous êtes sous Windows, vous pouvez éventuellement installer [Make](https://www.gnu.org/software/make/) en exécutant `choco install make`. Make est déjà préinstallé sur Mac.


### Installation

- Téléchargez ce dépôt puis extrayez tous les fichiers.
- Lancez la commande dans le terminal et à la racine du dossier:

        make first_time_setup

Si vous avez le moindre problème avec cette commande, essayez de lancer les suivantes séparément :

       python3 -m pip install --upgrade Pillow && pip3 install -r requirements.txt

       cd step2_spritesheet_to_generative_sheet && npm i

Chaque environnement est différent, donc essayez aussi de faire une recherche Google sur votre souci. Ci dessous une liste de problèmes connus:

- [M1 Mac: Canvas prebuild isn't built for ARM computers](https://github.com/Automattic/node-canvas/issues/1825) donc vous devez l'installer ici [from their Github](https://github.com/Automattic/node-canvas/wiki#installation-guides)
- `cd` La commande pourrait ne pas fonctionner, selon le terminal que vous utilisez. Vous devrez peut-être éditer `Makefile` et utiliser `CHDIR` ou son équivalent.
- Si vous êtes sur Windows 10 il est possible que 'make' ne soit pas reconnu. Essayez `choco install make` ou suivez ces [instructions](https://pakstech.com/blog/make-windows/#:~:text=make%20%3A%20The%20term%20'make',choose%20Path%20and%20click%20Edit). Vous pouvez aussi copier-coller les instructions dans le fichier `Makefile` manuellement.
- Si vous êtes sous Windows il est possible que vous obteniez une erreur où 'python3' n'existe pas, essayez de modifier le fichier `Makefile`et remplacez python3 par python. Merci!
- Si brew n'est pas installé, regardez la doc de [gifski](https://github.com/ImageOptim/gifski) pour les autres moyens d'installer gifski et regardez la doc de [ffmpeg](https://ffmpeg.org/) pour les MP4.

## Comment lancer le programme?

Déplacez vos fichiers png ou gif dans le dossier `/layers` ou chaque calque doit lui-même se trouver dans un dossier, et chaque dossier de traits contient plusieurs dossiers d'attributs qui eux-mêmes contiennent les images individuelles (frames) du futur GIF, un fichier GIF, ou un fichier PNG . Par exemple si vous voulez définir des calques pour le fonds (background), vous aurez les dossiers `/layers/background/blue#20` et `/layers/background/red#20`.

Dans chaque dossier d'attributs, les frames doivent être nommées ainsi : `0.png` -> `X.png` ou alors : `0.gif`. Voir le code ou [step 1](#step-1) pour la structure des dossiers. Le code gérera n'importe quel nombre de calques, vous pouvez donc avoir un calque avec deux frames, un autre calque avec une frame et encore un autre avec 20 frames, et tant que vous passez `numberOfFrames` = 20, les calques seront répétés jusqu'à ce qu'ils atteignent 20 images par GIF ou MP4.

**EDIT** Vous pouvez maintenant laisser les noms de vos frames comme vous le souhaitez et définir `useFileNumbering` sur `false`. Cela facilite la tâche si vous avez des centaines de frames et que vous ne souhaitez pas les renommer.

Mettez à jour le fichier `global_config.json` avec:

1.  **`'totalSupply'`** : Nombre total de gifs/MP4 à générer.
2.  **`'height'`** : Hauteur de vos frames. Celle-ci devrait être égale à la largeur. La valeur par défaut est de 350 (voir [https://docs.opensea.io/docs/metadata-standards#:~:text=We%20recommend%20using%20a%20350%20x%20350%20image](OpenSea recommendation))
3.  **`'width'`** : Largeur de vos frames. Celle-ci devrait être égale à la hauteur. La valeur par défaut est de 350 (voir [https://docs.opensea.io/docs/metadata-standards#:~:text=We%20recommend%20using%20a%20350%20x%20350%20image](OpenSea recommendation))
4.  **`'framesPerSecond'`** : Nombre d'images par seconde. Ce ne sera pas exact car PIL prend en millisecondes entières par image
     (donc 12 fps = 83,3 ms par image mais arrondi à un int = 83 ms). Cela ne sera pas reconnaissable à l'œil nu, mais mérite d'être signalé.
5.  **`'numberOfFrames'`** : Nombre total d'images. Par exemple, vous pourriez avoir 24 images, mais vous voulez le rendre à 12 fps.
6.  **`'description'`** : Description pour les métadonnées.
7.  **`'baseUri'`** : baseUri à spécifier dans les métadonnées.
8.  **`'saveIndividualFrames'`** : Utile si vous souhaitez enregistrer les frames finaux individuels, par exemple si vous souhaitez laisser les gens choisir une seul frame pour leur page de profil.
9. **`'layersFolder'`**: C'est le dossier que vous souhaitez utiliser pour les calques. La valeur par défaut est `layers`, mais cela vous permet d'avoir plusieurs versions/possibilités pour vos calques, et de les exécuter côte à côte. Le dépôt actuel a quatre exemples de dossiers, `layers`, `layers_grouping`, `layers_if_then`, `layers_z_index` qui démontrent les possibilités du [nftchef's repo](https://generator.nftchef.dev/).
10. **`'quality'`**: Qualité en sortie, 1-100.
11. **`'gifTool'`**: Choisis la méthode de génération, `gifski` ou `imageio`. Gifski est meilleur, mais certaines personnes ont des soucis avec sous Linux. Egalement, `imageio` fonctionnera bien pour le pixel art, donc si vous ne voulez pas télécharger  Gifski vous pouvez régler cette option sur `imageio`.
12. **`'MP4Tool'`**: Choisis la méthode de génération pour les MP4. Supporte seulement `ffmpeg` pour le moment.
13. **`'outputType'`**: Selectionnez `gif` ou `mp4`.
14. **`'useBatches'`**: Réglez sur `true` si vous souhaitez utiliser le [batching](#batching). Sinon ne fait rien.
15. **`'numFramesPerBatch'`**: Nombre de frames pour chaque lot (batching). Regardez [batching](#batching) pour plus d'informations. Ne fait quelquechose que si `useBatches` est réglé sur `true`.
16. **`'loopGif'`**: `true` Si vous voulez boucler le gif (lecture en boucle), sinon `false`.
17. **`'useMultiprocessing'`**: `true` Si vous voulez utilise rle multi-traitement, ce qui va accélérer les étapes 1 et 3. Vous pouvez configurer le nombre de processeurs à utiliser avec `processorCount`. Utilisez avec parcimonie, je recommanderais d'augmenter lentement `processorCount` et de monitorer l'usage de votre CPU, car cela pourrait faire crasher votre ordinateur.
18. **`'processorCount'`**: Nombre de processeurs à utiliser avec le multi-traitement. Le goulot est `multiprocessing.cpu_count()`. Utilisez avec parcimonie.
19. **`'useFileNumbering'`**: Utilisez la numérotation 0.png -> X.png, ou non. Si vous souhaitez uniquement utiliser vos noms de fichiers, définissez-le sur `false`.
20. **`'enableAudio'`**: BETA. Vous pouvez maintenant ajouter de l'audio en tant que calque. Voir [Add Specific Audio Trait Section](#adding-specific-audio-per-trait) pour plus d'informations.
21. **`'numLoopMP4'`**: Nombre de boucles pour vos MP4.

Mettez à jour `step2_spritesheet_to_generative_sheet/src/config.js` et les lignes de code suivant `layerConfigurations`. Si vous voulez une
configuration basique, éditez simplement `layersOrder`, mais si vous voulez profiter des possibilités du [nftchef's repo](https://generator.nftchef.dev/), survolez le fichier afin de visualiser des exemples et modifiez `layerConfigurations` en conséquence.

- Pour lancer le processus du début à la fin, en une seule fois:

        make all

Vos fichiers de sortie au format Gif apparaitront dans  `build/gif`, et vos fichiers de sortie MP4 apparaitront dans `build/mp4`.Les métadonnées Json  pour ETH et compatibles EVM apparaitront dans `build/json`. Essayez par vous-mêmes avec les options et calques par défaut!

Si vous voulez jongler entre la génération de Gifs et de MP4, vous pouvez modifier `global_config.json`, et simplement lancer `make step3`.

## Comment cela fonctionne?

### Etape 1

Pour que la partie du code [nftchef's Generative Gif Engine](https://github.com/nftchef/art-engine) fonctionne, les calques en fichiers d'entrée doivent être au format [Sprite Sheet](https://gamedevelopment.tutsplus.com/tutorials/an-introduction-to-spritesheet-animation--gamedev-13099).
Cependant, cela est fastidieux et peu intuitif pour de nombreux artistes qui utilisent des outils exportant des images individuelles.

L'étape 1 convertit simplement des images individuelles au format spritesheet, avec un pourcentage de rareté. Vous fournissez les calques dans le dossier `/layers` avec la rareté dans le nom du dossier. Chaque image doit être numérotée de 0 -> X, et n'accepte que le format `.png`.

**Si vous n'incluez pas le pourcentage de rareté dans le nom du dossier d'attributs, cet attribut sera ignoré**

Vous pouvez fournir n'importe quel nombre d'images dans chaque dossier de calque, le code les répétera jusqu'à ce qu'il atteigne `numberOfFrames`.
Il coupera également ceux qui ont trop de frames.

Exemple de structure de dossier de calques avec quatre calques
et deux traits pour chaque calque :

```
layers
└───Background
│   └───Grey#50
│       │   0.png
│   └───Pink#50
│       │   0.png
└───Ball
│   └───Blue#50
│       │   0.png
│       │   1.png
│       │   2.png
│       │   ...
│   └───Green#50
│       │   0.png
│       │   1.png
│       │   2.png
│       │   ...
└───Hat
│   └───Birthday#50
│       │   0.png
│       │   1.png
│       │   2.png
│       │   ...
│   └───Cowboy#50
│       │   0.png
│       │   1.png
│       │   2.png
│       │   ...
└───Landscape
│   └───Cupcake#50
│       │   0.png
│   └───Green Tower#50
│       │   0.png
```

**Exemple de calque**:

**Background**:

Grey:

<img src="./README_Assets/layers/Background/Grey/0.png" width="200">

Pink:

<img src="./README_Assets/layers/Background/Pink/0.png" width="200">

**Ball**:

Blue:

<img src="./README_Assets/layers/Ball/Blue/0.png" width="150"><img src="./README_Assets/layers/Ball/Blue/1.png" width="150"><img src="./README_Assets/layers/Ball/Blue/2.png" width="150"><img src="./README_Assets/layers/Ball/Blue/3.png" width="150"><img src="./README_Assets/layers/Ball/Blue/4.png" width="150">...

Green:

<img src="./README_Assets/layers/Ball/Green/0.png" width="150"><img src="./README_Assets/layers/Ball/Green/1.png" width="150"><img src="./README_Assets/layers/Ball/Green/2.png" width="150"><img src="./README_Assets/layers/Ball/Green/3.png" width="150"><img src="./README_Assets/layers/Ball/Green/4.png" width="150">...

**Hat**:

Birthday:

<img src="./README_Assets/layers/Hat/Birthday/0.png" width="150"><img src="./README_Assets/layers/Hat/Birthday/1.png" width="150"><img src="./README_Assets/layers/Hat/Birthday/2.png" width="150"><img src="./README_Assets/layers/Hat/Birthday/3.png" width="150"><img src="./README_Assets/layers/Hat/Birthday/4.png" width="150">...

Cowboy:

<img src="./README_Assets/layers/Hat/Cowboy/0.png" width="150"><img src="./README_Assets/layers/Hat/Cowboy/1.png" width="150"><img src="./README_Assets/layers/Hat/Cowboy/2.png" width="150"><img src="./README_Assets/layers/Hat/Cowboy/3.png" width="150"><img src="./README_Assets/layers/Hat/Cowboy/4.png" width="150">...

**Landscape**:

Cupcake:

<img src="./README_Assets/layers/Landscape/Cupcake/0.png" width="150">

Green Tower:

<img src="./README_Assets/layers/Landscape/Green Tower/0.png" width="150">

J'utilise python ici à la place des librairies javascript parceque je me suis rendu compte que le traitement d'image par le biais de [PIL](https://pillow.readthedocs.io/en/stable/) est bien plus rapide, sans perte de qualité.
Ces avantages sont beaucoup plus visibles à l'étape 3.

Vous pouvez lancer l'étape 1 grâce à la commande:

        make step1

Cela convertira les fichiers png en spritesheets et la sortie ressemblera à quelque chose comme cela:

Sortie:

**Background**:

Grey#50.png:

<img src="./README_Assets/step1/Background/Grey.png" width="1000">

Pink#50.png:

<img src="./README_Assets/step1/Background/Pink.png" width="1000">

**Ball**:

Blue#50.png:

<img src="./README_Assets/step1/Ball/Blue.png" width="1000">

Green#50.png:

<img src="./README_Assets/step1/Ball/Green.png" width="1000">

**Hat**:

Birthday#50.png:

<img src="./README_Assets/step1/Hat/Birthday.png" width="1000">

Cowboy#50.png:

<img src="./README_Assets/step1/Hat/Cowboy.png" width="1000">

**Landscape**:

Cupcake#50.png:

<img src="./README_Assets/step1/Landscape/Cupcake.png" width="1000">

Green Tower#50.png:

<img src="./README_Assets/step1/Landscape/Green Tower.png" width="1000">

**EDIT L'outil prends maintenant en compte le z-index/stacking, le grouping et les conditions if-then **. Voir [nftchef's docs](https://generator.nftchef.dev/readme/) pour plus d'informations. Les calques à cette étape devront correspondre au format attendu à l'étape 2. Voir l'exemple de dossier de calques pour plus d'informations.

**EDIT prends maintenant en compte les calques au format Gif**.
Vous pouvez fournir vos calques au format Gif, et le code va les scinder en frames.
Voir `layers_gif_example`. 
Cela créera un dossier temporaire dans `step1_layers_to_spritesheet/temp` avec les frames séparées au format png, et les analysera dans ce dossier afin de créer les fichiers de sortie. Vérifiez bien d'avoir réglé `numberOfFrames` dans le fichier global_config.json.

### Etape 2

L'étape 2 prend les spritesheets de l'étape 1 et génère toutes les combinaisons possibles en fonction de la rareté. C'est ici que toute la magie opère ! En sortie cela crée une multitude de spritesheets avec tous les calques superposés les uns sur les autres.

L'idée originale vient de [MichaPipo's Generative Gif Engine](https://github.com/MichaPipo/Generative_Gif_Engine) mais maintenant la majeure partie du code a été forkée depuis [nftchef's Generative Engine](https://github.com/nftchef/art-engine) qui est lui-même un fork de [HashLips Generative Art Engine](https://github.com/HashLips/generative-art-node).
S'il vous plaît allez voir Hashlip [📺 Youtube](https://www.youtube.com/channel/UC1LV4_VQGBJHTJjEWUmy8nA) / [👄 Discord](https://discord.com/invite/qh6MWhMJDN) / [🐦 Twitter](https://twitter.com/hashlipsnft) / [ℹ️ Website](https://hashlips.online/HashLips) pour une explication plus détaillée sur le fonctionnement général.

J'ai récemment modifié cette partie du code de [nftchef's Generative Engine](https://github.com/nftchef/art-engine) ce qui ajoute les possibilités suivantes:
- Déclarations if-then. Vous pouvez avoir un code d'art génératif qui dit "si ce calque..." , alors cet autre calque est selectionné. Il y a un exemple de calques sous `layers_if_then` qui a la logique suivante : si la balle est rose, porte un "birthday" ou un "cowboy hat", ou si la balle est violette, alors porte un "mini ball hat". Voir [nftchef's docs](https://generator.nftchef.dev/readme/branching-if-then) pour plus d'informations.
- Déclarations par groupes. 
Vous pouvez maintenant regrouper vos traits dans des groupes spécifiques. Ainsi dans le 
`layers_grouping` nous avons des balles et des chapeaux communs, des balles et chapeaux rares, et le premier `totalSupply - 1` est commun, le dernier est rare. Cela sortira dans l'ordre, mais vous pouvez les mélanger en réglant `shuffleLayerConfigurations` dans `config.js` sur `true`.
- z-index autrement connu sous le nom d'ordre d'empilement. Vous pouvez maintenant avoir plusieurs ordres d'empilement pour le même calque, par exemple un panier de basket, qui a des parties plaçées au dessus et en dessous de la balle. Voir [nftchef's docs](https://generator.nftchef.dev/readme/z-index-layer-order) pour plus d'informations.

Vous devrez mettre à jour `global_config.json` et`layerConfigurations` dans `step2_spritesheet_to_generative_sheet/src/config.js`.

Vous pouvez lancer l'étape 2 grâce à la commande:

        make step2

Exemple de sortie avec le dossier `layers` (seuls les 4 premiers sont montrés, il y en a 16 au total):

<img src="./README_Assets/step2/0.png" width="1000">
<img src="./README_Assets/step2/1.png" width="1000">
<img src="./README_Assets/step2/2.png" width="1000">
<img src="./README_Assets/step2/3.png" width="1000">

Exemple de sortie avec le dossier `layers_z_index`:

<img src="./README_Assets/z-index/0.png" width="200">

### Etape 3

L'étape 3 prends les spritesheets de l'étape 2 et produit les gifs/MP4. Initialement j'utilisais [PIL](https://pillow.readthedocs.io/en/stable/), mais j'ai eu des soucis concernant la qualité d'image.

Dans le dépôt original de MichaPipo, ils ont utilisé des bibliothèques javascript pour créer les gifs. Celles-ci copiaient pixel par pixel, et la logique était un peu compliquée. Créer seulement 15 gifs prenait 4 minutes, et j'ai remarqué que certaines des couleurs hexadécimales des pixels étaient désactivées. Également : en fonction de l'utilisation du processeur, le programme plantait. J'ai passé des jours à déboguer, avant de décider de repartir de zéro dans un autre langage.

J'ai ensuite essayé imageio et quelques bibliothèques Python, mais elles avaient toutes des problèmes pour générer des gifs.

J'ai passé des semaines à trouver le meilleur outil pour ce travail, puis je suis tombé sur [gifski](https://gif.ski/). Cela
crée des gifs incroyablement propres et fonctionne le mieux.

Maintenant, générer 15 gifs prend moins de 30 secondes et s'affiche avec une qualité de pixel parfaite !

Vous pouvez modifier le `framesPerSecond` dans `global_config.json` et vous pouvez exécuter l'étape 3 avec la commande :

        make step3

Cela vous permet de ne pas avoir à tout régénérer pour jouer avec les fps.


Exemple de sortie avec les 16 permutations (cliquez sur chaque gif pour la version 1000x1000) :

<img src="./README_Assets/step3/0.gif" width="150"><img src="./README_Assets/step3/1.gif" width="150"><img src="./README_Assets/step3/2.gif" width="150"><img src="./README_Assets/step3/3.gif" width="150"><img src="./README_Assets/step3/4.gif" width="150"><img src="./README_Assets/step3/5.gif" width="150"><img src="./README_Assets/step3/6.gif" width="150"><img src="./README_Assets/step3/7.gif" width="150"><img src="./README_Assets/step3/8.gif" width="150"><img src="./README_Assets/step3/9.gif" width="150"><img src="./README_Assets/step3/10.gif" width="150"><img src="./README_Assets/step3/11.gif" width="150"><img src="./README_Assets/step3/12.gif" width="150"><img src="./README_Assets/step3/13.gif" width="150"><img src="./README_Assets/step3/14.gif" width="150"><img src="./README_Assets/step3/15.gif" width="150">

Si vous définissez `saveIndividualFrames` sur `true` dans `global_config.json`, cela divisera également les gifs en frames individuelles et les enregistrera dans `images`. Ceci est utile si vous voulez que les gens puissent choisir une seule frame pour une photo de profil.

Quelques données:

Le dépôt de MichaPipo:

- 15 NFT - 5 minutes avec parfois des pixels incorrects.
- 100 NFT - une heure (avec l'ordinateur presque inutilisable).

Le nouveau générateur de gifs:

- 15 NFT - 30 secondes et pas de problèmes de pixels.
- 100 NFT - 3 minutes and 17 secondes sans problèmes de pixels.
- 1000 NFT - 45 minutes sans problèmes de pixels ni de CPU.

**REMARQUES**
`imageio` était de loin la meilleure librairie python, je l'ai donc ajoutée en option au cas où vous ne voudriez pas télécharger 
`gifski`. `imageio` fonctionnera bien la plupart du temps pour le pixel art et je sais que certaines personnes ont eu des soucis avec 
`gifski` sous Linux (mais pas sous Windows ou Mac).

Vous pouvez définir l'outil gif à utiliser dans `global_config.json` en définissant `gifTool` sur `gifski` (par défaut) ou `imageio`.

Si vous souhaitez basculer entre la génération de gif et celle de MP4, vous devez remplacer `outputType` par `mp4` et exécuter uniquement `make step3`.

### améliorations avec NFTChef : z-index/stacking, grouping, déclarations if-then, et incompatibilité

L'outil propose maintenant le z-index/stacking, le grouping, les déclarations if-then, et les incompatibilités. Voir [nftchef's docs](https://generator.nftchef.dev/readme/) pour plus d'informations.

Si vous ne voulez pas lire la doc:

- **z-index/stacking**: Vous pouvez avoir le même calque au dessus et en dessous d'un autre calque (voir basketball au-dessus). Vous devez spécifier `z_,` devant le nom, par exemple `z1,` ou `z2,`. Voir `layers_z_index` pour un exemple, et essayez de régler `layersFolder` sur `layers_z_index` pour le voir en action et vérifiez `layerConfigurationsZIndex` dans `config.js` pour la configuration.
- **grouping**: Vous pouvez regrouper les traits ensemble dans un groupe, comme communs/rares. Ensuite vous pouvez spécifier combien vous voulez en quantité pour chaque. Voir le dossier `layers_grouping` et `layerConfigurationsGrouping` dans `config.js`.
- **if-then**: Vous pouvez spécifier "si ce trait"... "Alors il aura cet autre trait". Par exemple, si la balle est rose, alors choisis parmi ces deux chapeaux. Voir le dossier `layers_if_then` et `layerConfigurationsIfThen` dans `config.js`.
- **incompatibilités**: Vous pouvez spécifier si vous souhaitez qu'un calque soit incompatible avec un autre calque. Par exemple, si vous ne voulez pas que l'arrière-plan clignotant ait une balle multicolore. REMARQUE, cela ne fonctionne que si les noms de calques sont tous uniques, sinon cela peut entraîner un comportement inattendu.
 Voir `layers_incompatible` et `const incompatible` dans `config.js`. Vous pouvez dé-commenter la ligne et exécuter le code avec `layersFolder` réglé sur`layers_incompatible` pour voir ceci fonctionner.

### Ajouter un audio spécifique pour un trait

🧪 OPTION BETA 

Vous pouvez maintenant ajouter un son spécifique par trait. Par exemple, si vous voulez des bruits de vent avec un fond venteux,
et des bruits de forêt avec un fond forestier.

Placez simplement le fichier audio dans le dossier de calque correspondant, et l'étape 3 le prendra et le mettra sur le mp4. Vous pouvez voir un exemple dans le dossier `layers_audio`. Essayez en réglant `layersFolder` sur `layers_audio` et `enableAudio` sur `true`, ensuite lancez `make all`. Le mp4 sera de la même longueur que le total des frames, et l'audio sera tronqué s'il est trop long.

L'outil prend en charge `mp3`, `wav` et `m4a`. S'il existe plusieurs fichiers audio pour le même NFT, il
combinera les fichiers audio et les superposera.

### Etendre une collection existante en GIF/MP4

🧪 OPTION BETA

[Video Walkthrough](https://www.youtube.com/watch?v=HvXOdGGspGo)

Si vous avez des métadonnées existantes pour une collection existante et que vous souhaitez soit créer une nouvelle collection avec des GIF/MP4, soit envoyer une version GIF/MP4 de l'image statique aux détenteurs, cette fonctionnalité est pour vous ! OU si vous souhaitez exporter sous forme de spritesheet pouvant être importée dans un métaverse pixel, cette fonctionnalité est faite pour vous !

There are a few configurations to you can use the tool:
1. If you already have a `_dna.json` generated by NFT Chef's repo, and a `_metadata.json` file which contains all the JSON files. Load the `_dna.json` into the `build` folder, and load the `_metadata.json` into the `build/json` folder. Setup your layers following the format above. Setup `global_config.json` and `config.js` and run `make regenerate`.
This is the most accurate and consistent way of generating GIFs based on existing layers and will work with NFT Chef's features.
2. If you generated using Hashlips' art engine, you won't have a `_dna.json`. You will only have `_metadata.json` which contains all the JSON files. Load this into the `build/json` folder, setup layers, setup `global_config.json`, `config.js` and run `make regenerate`. This under the hood attempts to regenerate
the DNA based on the JSON. This should work, but there may be features that are not backwards compatible so let me know if you come across such a case.
3. You don't have a `_metadata.json` file. Load all the individual `.json` files into `build/json`. Setup layers, setup `global_config.json`, `config.js` and run `make regenerate`. This is more annoying to do (if you have a ton of files), but will regenerate the `_metadata.json`, the `_dna.json`, and then regenerate the collection.

If you only want to regenerate spritesheets, you can set `SKIP_STEP_ONE` to `True` and `SKIP_STEP_THREE` to `True` in `regenerate.py`. Then instead
of putting your layers in the `layers` folder, you put them in `step1_layers_to_spritesheet/output` as an entire layer, and then
run `make regenerate`. The spritesheets will be in `step2_spritesheet_to_generative_sheet/output`.

If you need more than 32 frames at 1000x1000, follow the batches configuration and then run `make regenerate`. This will only work if you are doing
all the steps and not skipping any.

Please let me know if you have any issues or use cases I did not think of.

Il existe quelques configurations pour que vous puissiez utiliser l'outil :
1. Si vous avez déjà un `_dna.json` généré par le dépôt de NFT Chef, et un fichier `_metadata.json` qui contient tous les fichiers JSON. Chargez le `_dna.json` dans le dossier `build` et chargez le `_metadata.json` dans le dossier `build/json`. Configurez vos calques en suivant le format ci-dessus. Configurez `global_config.json` et `config.js` et exécutez `make regenerate`.
C'est le moyen le plus précis et le plus cohérent pour générer des GIF basés sur des calques existants et fonctionnera avec les spécificités de NFT Chef.
2. Si vous avez généré en utilisant le générateur d'art de Hashlips, vous n'aurez pas de `_dna.json`. Vous n'aurez que `_metadata.json` qui contient tous les fichiers JSON. Chargez le dans le dossier `build/json`, configurez vos calques, configurez `global_config.json`, `config.js` et exécutez `make regenerate`. Cela permets d'essayer de régénérer le DNA basé sur le JSON. Cela devrait fonctionner, mais il peut y avoir des fonctionnalités qui ne sont pas rétrocompatibles, alors faites-le moi savoir si vous rencontrez un souci.
3. Vous n'avez pas de fichier `_metadata.json`. Chargez tous les fichiers `.json` individuels dans `build/json`. Configurez vos calques, configurez `global_config.json`, `config.js` et exécutez `make regenerate`. C'est plus ennuyeux à faire (si vous avez une tonne de fichiers), mais cela régénérera le `_metadata.json`, le `_dna.json`, puis régénérera votre collection.

Si vous souhaitez ne régénérer que les spritesheets, vous pouvez définir `SKIP_STEP_ONE` sur `True` et `SKIP_STEP_THREE` sur `True` dans `regenerate.py`. Alors à la place de mettre vos calques dans le dossier `layers`, vous les mettez dans `step1_layers_to_spritesheet/output` en tant que calques entiers, puis exécutez `faire régénérer`. Les spritesheets seront dans `step2_spritesheet_to_generative_sheet/output`.

Si vous avez besoin de plus de 32 images à 1000x1000, suivez la configuration par lots (batch), puis exécutez "make regenerate". Cela ne fonctionnera que si vous suivez toutes les étapes sans en sauter aucune.

S'il vous plaît faite-le moi savoir si vous avez des soucis ou des cas d'utilisation auxquels je n'ai pas pensé.


### Statistiques de rareté

Vous pouvez vérifier les statistiques de rareté de votre collection avec :

        make rarity


### Exclure un calque du DNA

Si vous souhaitez qu'une couche soit _ignorée_ dans la vérification de l'unicité du DNA, vous pouvez définir `bypassDNA : true` dans l'objet `options`. Cela permets de s'assurer que le reste des traits est unique sans considérer les calques `Background` comme des traits, par exemple. Les calques _sont_ inclus dans l'image finale.

```js
layersOrder: [
      { name: "Background" },
      { name: "Background" ,
        options: {
          bypassDNA: false;
        }
      },
```

### Generation de hashage de provenace

Si vous avez besoin de générer un hachage de provenance (et, oui, vous devriez, [lire à ce sujet ici](https://medium.com/coinmonks/the-elegance-of-the-nft-provenance-hash-solution-823b39f99473 ) ),

exécutez l'utilitaire suivant

```
make provenance
```

Cela ajoutera un `imageHash` à chaque fichier `.json`, puis les concaténera
et hashera la valeur du fichier en une chaîne (string), qui est le hashage de "provenance".

**Les informations de provenance sont enregistrées** dans le répertoire de construction dans `_provenance.json`. Ce fichier contient le hashage de provenance final ainsi que la (longue) chaîne (string) de hashage concaténée.

\*Remarque, si vous régénérez les gifs, **Vous devrez également régénérer ce hashage**.

### Enlever un trait

Si vous devez supprimer un trait des attributs générés pour TOUS les fichiers .json de métadonnées générés, vous pouvez utiliser la commande removeTrait util.

`cd step2_spritesheet_to_generative_sheet && node utils/removeTrait.js "Nom du trait"`

Si vous souhaitez imprimer des logs supplémentaires, utilisez l'indicateur -d

`cd step2_spritesheet_to_generative_sheet && node utils/removeTrait.js "Nom du trait" -d`

### Mettre à jour les métadonnées

Vous pouvez changer la description et le base Uri de vos métadonnées même après avoir lançé tout le code en mettant à jour `global_config.json` et en executant la commande:

        make update_json

### Insérer aléatoirement des objets rares - Replace Util

Si vous souhaitez ajouter manuellement des versions "dessinées à la main" ou uniques dans le pool d'éléments générés, cet utilitaire prend un dossier source (celui de vos nouvelles illustrations) et l'insère dans le répertoire "build", en les attribuant à des identifiants aléatoires.

#### Requirements

- Placez vos gifs dans ultraRares/gifs
- Placez les fichiers json correspondants dans les dossiers ultraRares/json

example:

```
├── ultraRares
│   ├── gifs
│   │   ├── 0.gif
│   │   └── 1.gif
│   └── json
│       ├── 0.json
│       └── 1.json
```

**Vous devez avoir les fichiers json correspondants pour chacun de vos gifs/éléments.**

#### Configuration du JSON.

Étant donné que ce script randomise les jetons à remplacer/placer, _il est important_ de mettre à jour correctement les métadonnées avec le tokenId résultant #.

**_Partout_ où vous avez besoin du numéro d'édition dans les métadonnées, utilisez l'identifiant `##`.**

```json
  "edition": "##",
```

**N'oubliez pas l'URI de vos images!**

```json
  "name": "## super rare sunburn ",
  "image": "ipfs://NewUriToReplace/##.png",
  "edition": "##",
```

#### Executer

Lancez la commande `make replace`. Si vous devez remplacer le nom du dossier, vous devrez peut-être modifier le `Makefile` directement avec le dossier.

**Notez que cela ne mettra pas à jour _dna.json car ces nouveaux JSON n'ont pas d'ADN. Cela modifiera cependant _metadata.json.**

### Metadonnées pour Solana

🧪 OPTION BETA

Après avoir exécuté "make all", vous pouvez lancer la génération des métadonnées Solana en deux étapes :
- Modifiez `step2_spritesheet_to_generative_sheet/Solana/solanaConfig.js`
- `make solana` pour générer les métadonnées Solana. Cela créera un dossier de sortie `build/solana` avec les gifs et les métadonnées.

La plupart du code provient de [nftchef](https://github.com/nftchef/art-engine/blob/nested-folder-structure/utils/metaplex.js).

Je n'ai essayé cela sur aucun réseau de test ou principal Solana, veuillez donc signaler tout problème ou créer un PR pour les résoudre !

### Tezos metadata

🧪 OPTION BETA

Je n'ai pas essayé cela sur un réseau de test ou principal Tezos, alors veuillez signaler tout problème ou créer un PR pour les résoudre !

Voir [Tezos README](step2_spritesheet_to_generative_sheet/documentation/other-blockchains/tezos.md) pour plus d'informations.

### Lots (Batching)

Voulez-vous une résolution plus élevée, plus d'images et des gifs/MP4 plus grands ? Le batching est fait pour vous ! Actuellement, le step2 est limité à des fichiers de 32 000 pixels. Donc pour contourner ce problème, nous devons regrouper l'ensemble du processus en plusieurs parties, puis les combiner à la fin.

Définissez `useBatches` dans `global_config.json` sur `true`, puis définissez `numFramesPerBatch` sur un nombre pair de `numberOfFrames`.

Ensuite, lancez `make all_batch`. Cela exécute d'abord `make step1` + `make step2` pour générer les métadonnées initiales, puis `python3 batch.py`
qui va créer les images restantes en fonction des métadonnées initiales.


### Aperçu Gif/MP4

Si vous voulez un aperçu gif/MP4 d'un sous-ensemble de gifs (comme avec le Hashlips), lancez la commande

`make preview`

Cela affichera `preview.gif`/`preview.mp4` dans le dossier `build`. Le nombre d'aperçus par défaut est de 4, mais vous pouvez le modifier dans
`step3_generative_sheet_to_output/preview.py` en haut `NUM_PREVIEW_OUTPUT`. Actuellement, il sélectionnera au hasard les gifs/MP4,
si vous voulez le premier X en sortie, définissez `SORT_ORDER` sur `OrderEnum.ASC` et si vous voulez le dernier X en sortie,
définissez `SORT_ORDER` sur `OrderEnum.DESC`.


## REMARQUES IMPORTANTES

All of the code in step1 and step3 was written by me. The original idea for the repo came from [MichaPipo's Generative Gif Engine](https://github.com/MichaPipo/Generative_Gif_Engine) but now most of the code in step 2 is forked from [nftchef's Generative Engine](https://github.com/nftchef/art-engine) which is forked from [HashLips Generative Art Engine](https://github.com/HashLips/generative-art-node).

Tout le code des étapes 1 et 3 a été écrit par moi. L'idée originale du dépôt vient de [MichaPipo's Generative Gif Engine](https://github.com/MichaPipo/Generative_Gif_Engine) mais la plupart du code de l'étape 2 est maintenant dérivé du [nftchef's Generative Engine](https://github .com/nftchef/art-engine) qui est lui-même dérivé de [HashLips Generative Art Engine](https://github.com/HashLips/generative-art-node).


**FAQ**

Q : Pourquoi avez-vous décidé d'utiliser Python pour les étapes 1 et 3 ?

R : J'ai trouvé que Python [PIL](https://pillow.readthedocs.io/en/stable/) fonctionne mieux et plus rapidement que les bibliothèques JS, et le code est plus simple pour moi. Au départ, j'ai essayé PIL, imageio et quelques bibliothèques Python, mais elles avaient toutes des problèmes concernant la génération de gifs. J'ai passé des semaines à trouver le meilleur outil pour ce travail et je suis tombé sur [gifski](https://gif.ski/). Cela permets la création de gifs incroyablement propres et fonctionne le mieux.

Ma philosophie est de choisir le bon outil pour le bon travail. Si quelqu'un trouve une meilleure bibliothèque pour ce travail spécifique, faites-le moi savoir !

Q : Pourquoi n'avez-vous pas utilisé Python pour l'étape 2 ?

R : La communauté de développement NFT qui écrit la logique compliquée de l'art génératif code principalement en javascript. Je veux faciliter la mise à jour de mon code et incorporer les meilleures fonctionnalités des autres dépôts aussi facilement que possible, et tout refaire en Python serait fastidieux. Imaginez les étapes 1 et 3 comme des outils d'assistance en Python, et l'étape 2 est à l'origine de la majeure partie de la logique de développement.

Q : Quels types de fichiers prenez-vous en charge ?

Type d'entrée : gif ou png

Type de sortie : gif ou MP4

Q : Quels réseaux sont supportés ?

Ethereum, Solana, Tezos.

Assurez-vous de me suivre pour plus de mises à jour sur ce projet :

[Twitter](https://twitter.com/jalagar_eth)

[GitHub](https://github.com/jalagar/)

[Moyen](https://jalagar-eth.medium.com/)

Mon adresse ETH est 0x4233EfcB109BF6618071759335a7b9ab84F2F4f3 si vous avez envie d'être généreux :). Je viens de quitter mon travail pour travailler à plein temps sur les NFT donc tout est apprécié.

Si vous voulez voir ce code en action, nous l'utilisons pour mon entreprise de fitness et de santé mentale Fitness Friends. Rejoignez le Discord si vous avez besoin d'aide avec le moteur d'art animé, vous pouvez obtenir un accès direct à moi dans le canal #dev :

[Twitter](https://twitter.com/FitFriends_NFT)

[Site Web](https://www.fitnessfriends.io/)

[Discord] (discord.gg/Nn36NUK9ba)


**TRADUCTION FR**

Pxlsyl

[Twitter](https://twitter.com/PxlSyl)

[Site Web](https://www.pxlsyl.art/)

[Discord] (discord.gg/agkZjACtwA)

