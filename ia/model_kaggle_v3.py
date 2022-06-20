import os.path as osp
from glob import glob
import random
import time
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data as data
import torch.optim as optim
import albumentations as A
from albumentations.pytorch import ToTensorV2


def fix_seed(seed):
    # random
    random.seed(seed)
    # Numpy
    np.random.seed(seed)
    # Pytorch
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True


# Fixation de la valeur de la Seed
SEED = 42
fix_seed(SEED)

# Définition d’une description pour chaque classe
activity_map = {
    "c0": "Safe driving",
    "c1": "Texting - right",
    "c2": "Talking on the phone - right",
    "c3": "Texting - left",
    "c4": "Talking on the phone - left",
    "c5": "Operating the radio",
    "c6": "Drinking",
    "c7": "Reaching behind",
    "c8": "Hair and makeup",
    "c9": "Talking to passenger",
}

# Définition des chemins
data_dir = (
    "C:/Users/Bonjour/Etudes&Travail/Projets/PyCharm/DeepLearningSafetyDrive/Data"
)
csv_file_path = osp.join(data_dir, "driver_imgs_list.csv")

df = pd.read_csv(csv_file_path)  # Lecture de fichiers CSV
print(df.head(5))  # Afficher les 5 premières lignes

###############
##### EDA #####
###############

by_drivers = df.groupby("subject")  # Regroupé par pilote
unique_drivers = by_drivers.groups.keys()  # Liste des noms de pilotes

# Nombre de pilotes inclus dans l’ensemble de données
print("unique drivers: ", len(unique_drivers))
# Nombre moyen d’images par pilote
print("mean of images: ", round(df.groupby("subject").count()["classname"].mean()))

train_file_num = len(
    glob(osp.join(data_dir, "train/*/*.jpg"))
)  # Nombre de données d’entraînement
test_file_num = len(glob(osp.join(data_dir, "test/*.jpg")))  # Nombre de données d’essai
category_num = len(df["classname"].unique())  # Nombre de catégories
print("train_file_num: ", train_file_num)
print("test_file_num: ", test_file_num)
print("category_num: ", category_num)

# Nombre de données par classe
px.histogram(
    df, x="classname", color="classname", title="Number of images by categories "
).show()

drivers_id = pd.DataFrame((df["subject"].value_counts()).reset_index())
drivers_id.columns = ["driver_id", "Counts"]
px.histogram(
    drivers_id,
    x="driver_id",
    y="Counts",
    color="driver_id",
    title="Number of images by subjects ",
).show()

# Histogramme du nombre d’images par pilote
# Implémentez-le vous-même
px.histogram(
    df, x="subject", color="subject", title="Number of images by subjects"
).show()

# Dessiner des données pour chaque classe
# Implémentez-le vous-même
plt.figure(figsize=(12, 20))
for i, (key, value) in enumerate(activity_map.items()):
    image_dir = osp.join(data_dir, "train", key, "*.jpg")
    image_path = glob(image_dir)[0]
    image = cv2.imread(image_path)[:, :, (2, 1, 0)]
    plt.subplot(5, 2, i + 1)
    plt.imshow(image)
    plt.title(value)

plt.show()

#########################
##### Prétraitement #####
#########################

# Ajouter une colonne de chemin d’accès au fichier
# Implémentez-le vous-même
df["file_path"] = df.apply(
    lambda x: osp.join(data_dir, "train", x.classname, x.img), axis=1
)

# Convertissez les étiquettes de réponse correctes en nombres et ajoutez des colonnes
# Implémentez-le vous-même
df["class_num"] = df["classname"].map(lambda x: int(x[1]))
print(df.head(5))


########################################
##### Création d’un jeu de données #####
########################################


class DataTransform:
    """
    Classes de prétraitement d’images et d’annotations. Effectuer différentes actions pendant la formation et la vérification.
    Dimensionnez l’image à input_size x input_size.
    Pendant l’entraînement, les données sont augmentées.


    Attributes
    ----------
    input_size : int
        Taille de l’image à redimensionner.
    color_mean : (R, G, B)
        Valeur moyenne de chaque couche de couleur.
    color_std : (R, G, B)
        Écart type de chaque couche de couleur.
    """

    def __init__(self, input_size, color_mean, color_std):
        self.data_transform = {
            # Train uniquement mis en œuvre par vous-même
            "train": A.Compose(
                [
                    A.HorizontalFlip(p=0.5),
                    A.Rotate(-10, 10),
                    A.Resize(input_size, input_size),  # Redimensionner (input_size)
                    A.Normalize(
                        color_mean, color_std
                    ),  # Normalisation des informations de couleur
                    ToTensorV2(),  # Tensorisation
                ]
            ),
            "val": A.Compose(
                [
                    A.Resize(input_size, input_size),  # Redimensionner (input_size)
                    A.Normalize(
                        color_mean, color_std
                    ),  # Normalisation des informations de couleur
                    ToTensorV2(),  # Tensorisation
                ]
            ),
        }

    def __call__(self, phase, image):
        """
        Parameters
        ----------
        phase : 'train' or 'val'
            Spécifie le mode de prétraitement.
        """
        transformed = self.data_transform[phase](image=image)
        return transformed["image"]


class Dataset(data.Dataset):
    """
    Attributes
    ----------
    df : DataFrame
        class_num, file_pathのカラムがあるデータフレーム
    phase : 'train' or 'val'
        Mettre en place l’apprentissage ou la formation.
    transform : object
        Instances de la classe de prétraitement
    """

    def __init__(self, df, phase, transform):
        self.df = df
        self.phase = phase
        self.transform = transform

    def __len__(self):
        """Renvoie le nombre d’images"""
        return len(self.df)

    def __getitem__(self, index):
        """Obtenir des données au format Tensor pour les images pré-traitées"""
        image = self.pull_item(index)
        return image, self.df.iloc[index]["class_num"]

    def pull_item(self, index):
        """Obtenir des données au format Tensor pour les images"""

        # Implémentez-le vous-même
        # 1. Chargement de l’image
        image_path = self.df.iloc[index]["file_path"]
        image = cv2.imread(image_path)[:, :, (2, 1, 0)]

        # 2. Effectuer un prétraitement
        return self.transform(self.phase, image)


# Vérification de l’opération

# (RVB) moyenne des couleurs et écart-type
color_mean = (0.485, 0.456, 0.406)
color_std = (0.229, 0.224, 0.225)
input_size = 256

# Partitionnement des données
df_train, df_val = train_test_split(df, stratify=df["subject"], random_state=SEED)

# Implémentez-le vous-même
# Création d’un jeu de données
train_dataset = Dataset(
    df_train,
    phase="train",
    transform=DataTransform(
        input_size=input_size, color_mean=color_mean, color_std=color_std
    ),
)

val_dataset = Dataset(
    df_val,
    phase="val",
    transform=DataTransform(
        input_size=input_size, color_mean=color_mean, color_std=color_std
    ),
)

# Implémentez-le vous-même
# Exemple de récupération de données
image, label = train_dataset[0]
plt.imshow(image.permute(1, 2, 0))
plt.title(label)
plt.show()

####################################
##### Création d’un DataLoader #####
####################################

# Création d’un chargeur de données
batch_size = 64

# Implémentez-le vous-même
train_dataloader = data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True)

val_dataloader = data.DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

# Organiser en objets de dictionnaire
dataloaders_dict = {"train": train_dataloader, "val": val_dataloader}

# Implémentez-le vous-même
# Vérification de l’opération
batch_iterator = iter(dataloaders_dict["val"])  # Convertir en Itarator
images, labels = next(batch_iterator)  # Récupérer le premier élément
print(images.size())  # torch.Size([8, 3, 256, 256])
print(labels.size())  # torch.Size([8])

################################
##### Création d’un modèle #####
################################

from efficientnet_pytorch import EfficientNet

model = EfficientNet.from_pretrained("efficientnet-b0", num_classes=10)


# Implémentez-le vous-même (pratique)
# class Model(nn.Module):
#     def __init__(self, num_classes=10):
#         super(Model, self).__init__()
#         self.net = nn.Sequential(
#             nn.Conv2d(in_channels=3, out_channels=64, kernel_size=3, stride=2, padding=1),
#             nn.BatchNorm2d(num_features=64),
#             nn.ReLU(),
#             nn.Conv2d(in_channels=64, out_channels=16, kernel_size=3, stride=2, padding=1),
#             nn.BatchNorm2d(num_features=16),
#             nn.ReLU(),
#             nn.Flatten(),
#             nn.Linear(in_features=65536, out_features=num_classes)
#         )

#     def forward(self, x):
#         output = self.net(x)
#         return output
#
# model = Model(num_classes=10)

#########################
##### apprentissage #####
#########################

# Enregistrement des points de contrôle
def save_checkpoint(model, optimizer, scheduler, epoch, path):
    torch.save(
        {
            "epoch": epoch,
            "model": model.state_dict(),
            "optimizer": optimizer.state_dict(),
            "scheduler": scheduler.state_dict(),
        },
        path,
    )


# Chargement des points de contrôle
def load_checkpoint(model, optimizer, scheduler, path):
    checkpoint = torch.load(path)
    model.load_state_dict(checkpoint["model"])
    optimizer.load_state_dict(checkpoint["optimizer"])
    scheduler.load_state_dict(checkpoint["scheduler"])


# Fonctions pour entraîner le modèle
def train_model(
    model,
    dataloaders_dict,
    criterion,
    scheduler,
    optimizer,
    device,
    num_epochs,
    save_path,
):
    # Réseau vers GPU
    model.to(device)

    best_val_loss = float("inf")
    best_preds = None

    # Boucle dans l’époque
    for epoch in range(num_epochs):

        # Économisez l’heure de début
        t_epoch_start = time.time()
        epoch_train_loss = 0.0  # somme des pertes d’époque
        epoch_val_loss = 0.0  # somme des pertes d’époque
        preds = []
        trues = []

        print("-------------")
        print(f"Epoch {epoch + 1}/{num_epochs}")
        print("-------------")

        # Boucle de formation et de vérification par époque
        for phase in ["train", "val"]:
            if phase == "train":
                model.train()  # Mettez le modèle en mode d’entraînement
            else:
                model.eval()  # Mettez le modèle en mode validation
                print("-------------")

            # Boucle d’itérateur
            for i, (images, labels) in enumerate(dataloaders_dict[phase]):

                # Si vous pouvez utiliser le GPU, envoyez des données au GPU
                images = images.to(device)
                labels = labels.to(device)

                # Calcul de propagation vers l’avant
                with torch.set_grad_enabled(phase == "train"):
                    outputs = model(images)
                    loss = criterion(outputs, labels)

                    # Rétropropagation pendant l’entraînement
                    if phase == "train":
                        loss.backward()  # Calcul du gradient
                        optimizer.step()
                        optimizer.zero_grad()  # Initialisation des dégradés
                        epoch_train_loss += loss.item() / len(
                            dataloaders_dict[phase].dataset
                        )
                    # Pendant la validation
                    else:
                        preds += [outputs.detach().cpu().softmax(dim=1).numpy()]
                        trues += [labels.detach().cpu()]
                        epoch_val_loss += loss.item() / len(
                            dataloaders_dict[phase].dataset
                        )

                    # Afficher les progrès en cours de route
                    if i % 10 == 0:
                        print(
                            f"[{phase}][{i + 1}/{len(dataloaders_dict[phase])}] loss: {loss.item() / images.size(0): .4f}"
                        )

        if phase == "train":
            scheduler.step()  # Mise à jour du planificateur d’optimisation

        # Taux de perte et de précision par phase d’époque
        t_epoch_finish = time.time()
        print("-------------")
        print(
            f"epoch {epoch + 1} epoch_train_Loss:{epoch_train_loss:.4f} epoch_val_loss:{epoch_val_loss:.4f} time: {t_epoch_finish - t_epoch_start:.4f} sec."
        )
        print(
            f"epoch_val_acc: {accuracy_score(np.concatenate(trues), np.concatenate(preds).argmax(axis=1))}"
        )

        # Enregistrez le modèle avec l’époque de perte de validation la plus faible
        if best_val_loss > epoch_val_loss:
            best_preds = np.concatenate(preds)
            best_val_loss = epoch_val_loss
            save_checkpoint(model, optimizer, scheduler, epoch, save_path)
            print("save model")
    return best_val_loss, best_preds


# 1Fonction pour faire l’apprentissage lfold
def run_one_fold(df_train, df_val, fold, device):
    # Création d’un jeu de données
    train_dataset = Dataset(
        df_train,
        phase="train",
        transform=DataTransform(
            input_size=args.input_size,
            color_mean=args.color_mean,
            color_std=args.color_std,
        ),
    )

    val_dataset = Dataset(
        df_val,
        phase="val",
        transform=DataTransform(
            input_size=args.input_size,
            color_mean=args.color_mean,
            color_std=args.color_std,
        ),
    )

    # Création d’un chargeur de données
    train_dataloader = data.DataLoader(
        train_dataset, batch_size=args.batch_size, shuffle=True
    )

    val_dataloader = data.DataLoader(
        val_dataset, batch_size=args.batch_size, shuffle=False
    )

    # Organiser en objets de dictionnaire
    dataloaders_dict = {"train": train_dataloader, "val": val_dataloader}

    # Définition du modèle
    model = EfficientNet.from_pretrained(args.model_name, num_classes=args.num_classes)
    optimizer = optim.Adam(model.parameters(), lr=args.lr)  # Techniques d’optimisation
    criterion = nn.CrossEntropyLoss()  # Fonction de perte
    scheduler = optim.lr_scheduler.ExponentialLR(
        optimizer, gamma=args.gamma
    )  # Planificateur

    save_path = f"{args.model_name}_fold_{fold}.pth"
    best_val_loss, best_preds = train_model(
        model,
        dataloaders_dict,
        criterion,
        scheduler,
        optimizer,
        device,
        num_epochs=args.epochs,
        save_path=save_path,
    )
    return best_val_loss, best_preds


# Fonctions qui font kfold learning
def run_k_fold(df):
    # Vérifiez si le GPU est disponible
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Appareil utilisé：", device)

    # Validation croisée de la division K en couches
    skf = StratifiedKFold(n_splits=args.folds, shuffle=True, random_state=SEED)
    oof = pd.DataFrame(index=df.index)
    for fold, (train_index, val_index) in enumerate(skf.split(df, df["subject"])):
        print(f"\n\nFOLD: {fold}")
        print("-" * 50)
        df_train, df_val = df.loc[train_index], df.loc[val_index]
        best_val_loss, best_preds = run_one_fold(df_train, df_val, fold, device)
        oof.loc[val_index, activity_map.keys()] = best_preds
    return oof


# Paramètres d’apprentissage
class args:
    model_name = "efficientnet-b3"
    color_mean = (0.485, 0.456, 0.406)
    color_std = (0.229, 0.224, 0.225)
    input_size = 256
    num_classes = 10
    batch_size = 64
    epochs = 10
    folds = 5
    lr = 1e-3
    gamma = 0.98
    debug = True
    train = False


if args.debug:
    df_train = df.iloc[:1000]
else:
    df_train = df.copy()

if args.train:
    oof = run_k_fold(df_train)
    accuracy = accuracy_score(df_train["class_num"], oof.values.argmax(axis=1))
    print(f"\n\naccuracy: {accuracy}")

##########################################
##### Prédiction des données de test #####
##########################################

# Implémentez-le vous-même
# Fonctions permettant de déduire les données de test
def inference(model, dataloader, device):
    model.to(device)
    model.eval()
    preds = []
    for i, (images, labels) in enumerate(dataloader):
        images = images.to(device)
        with torch.no_grad():
            outputs = model(images)
        preds += [outputs.detach().cpu().softmax(dim=1).numpy()]

        if i % 10 == 0:
            print(f"[test][{i + 1}/{len(dataloader)}]")

    preds = np.concatenate(preds)
    return preds


# L’inférence est faite sur k modèles, et l’ensemble
def inference_k_fold(df_test):
    test_dataset = Dataset(
        df_test,
        phase="val",
        transform=DataTransform(
            input_size=args.input_size,
            color_mean=args.color_mean,
            color_std=args.color_std,
        ),
    )
    test_dataloader = data.DataLoader(
        test_dataset, batch_size=args.batch_size, shuffle=False
    )

    model = EfficientNet.from_pretrained(args.model_name, num_classes=args.num_classes)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    for fold in range(args.folds):
        print(f"\n\nFOLD: {fold}")
        print("-" * 50)
        model.load_state_dict(torch.load(f"{args.model_name}_fold_{fold}.pth")["model"])
        df_test.loc[:, activity_map.keys()] += (
            inference(model, test_dataloader, device) / args.folds
        )


if args.debug:
    results = pd.read_csv(
        "C:/Users/Bonjour/Etudes&Travail/Projets/PyCharm/DeepLearningSafetyDrive/Data/result_v3.csv"
    )
    results.to_csv("result_v3.csv", index=False)
else:
    # Chargement des données de test
    df_test = pd.read_csv(osp.join(data_dir, "sample_submission_v3.csv"))

    # Prétraitement
    df_test["file_path"] = df_test.apply(
        lambda row: osp.join(data_dir, f"my_test/{row.img}"), axis=1
    )
    df_test["class_num"] = 0
    df_test.loc[:, activity_map.keys()] = 0

    # Moyenne k résultats d’inférence et les stocker dans les résultats
    inference_k_fold(df_test)
    results = df_test.drop(["file_path", "class_num"], axis=1)
    results.iloc[:, 1:] = results.iloc[:, 1:].clip(0, 1)
    results.to_csv("result_v3.csv", index=False)
