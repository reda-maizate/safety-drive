## Access the data

Link to the Kaggle dataset: https://www.kaggle.com/competitions/state-farm-distracted-driver-detection/data

If you want to download the data, you can use the following code:
`kaggle competitions download -c state-farm-distracted-driver-detection`

## Data description
This dataset contains 10 classes, below are the descriptions of each one of them :

- **c0** -- The driver was safely driving his/her vehicle (safe driving).

<img src="./input/imgs/train/c0/img_34.jpg" width="200" height="200" />

- **c1** -- The driver was texting with his right hand while driving (texting - right).

<img src="./input/imgs/train/c1/img_6.jpg" width="200" height="200" />

- **c2** -- The driver was talking on the phone with his/her right hand while driving (talking on the phone - right).

<img src="./input/imgs/train/c2/img_94.jpg" width="200" height="200" />

- **c3** -- The driver was texting with his left hand while driving (texting - left).

<img src="./input/imgs/train/c3/img_5.jpg" width="200" height="200" />

- **c4** -- The driver was talking on the phone with his/her left hand while driving (talking on the phone - left).

<img src="./input/imgs/train/c4/img_14.jpg" width="200" height="200" />

- **c5** -- The driver was operating his/her radio while driving (operating the radio).

<img src="./input/imgs/train/c5/img_56.jpg" width="200" height="200" />

- **c6** -- The driver was drinking while driving (drinking).

<img src="./input/imgs/train/c6/img_0.jpg" width="200" height="200" />

- **c7** -- The driver was reaching behind while driving (reaching behind).

<img src="./input/imgs/train/c7/img_81.jpg" width="200" height="200" />

- **c8** -- The driver was applying make-up or styling his hair while driving (hair and makeup).

<img src="./input/imgs/train/c8/img_26.jpg" width="200" height="200" />

- **c9** -- The driver was talking to a passenger while driving (talking to passenger).

<img src="./input/imgs/train/c9/img_19.jpg" width="200" height="200" />

## Data preprocessing


## Terraform (Not accessible yet)

To train the model in the cloud, you need to install Terraform. Then, you need to :

`terraform init`

then

`export AWS_PORFILE=<your-aws-profile>`

then

`export TF_LOG_PROVIDER=INFO`

and finally,

`terraform apply -var-file=<your-terraform-variables-file> -auto-approve`