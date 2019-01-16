To install on ubuntu
sudo apt-get update
sudo apt-get install     apt-transport-https     ca-certificates     curl     software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
sudo apt-get install docker-ce
docker --version
sudo service docker start
sudo docker pull djjayeeta/hsiseg_3_web
sudo docker run -i -t djjayeeta/hsiseg_3_web:firsttry /bin/bash




## ==================HSI segmentation part=====================


To run on Indian pines data follow the steps:

Follow them sequentially

1) Install brew, wget with brew(brew install wget --with-libressl), python3 and pip3, create a virtualenv,  install all dependencies using pip3(in the virtualenv) from requirements.txt

2) run the command to preprocess the data

    ```python3 preprocessing_indian_pines.py```


3) create db using the following command
    
    ```python3 schema.py```

4) ```python3 run_type1_test.py```

5) ```python3 type2_patch.py```

6) ```python3 run_type2_test.py```


TESTS:

There are two types of tests using BASSNet + PU learning
Type 1:

Positive Class: A positive class labels is selected from a list, randomly some pixels are selected from that class for training

Negative Class: From a list of negative class labels, randomly some pixels are selected from that class for training

Testing and Training Data: The two types of data are non-overlapping

Parameters to tune:

File : run_type1_test.py

A) train_pos_percentage : Percentage of pixels from total pixels of positive class that will be included in training, 60% of training positive pixels will be labelled in PU learning

Ex: According to groundtooth image for class label k no of pixels  = 1057

train_pos_percentage = 30

Then randomly (1057 * 30)//100 = 317 pixels will be selected for PU training out of which 190 pixels will be labelled and rest 127 unlabelled, rest 740 pixels will be used for testing

B) train_neg_percentage : Percentage of pixels from total pixels of negative class list (include_class_list - positive_class) that will be included in training

Ex: According to groundtooth image for negative class labels list [ i, j ] total no of pixels  = 2078
train_neg_percentage = 30
Then according to the value of is_random_neg parameter(described below) 30 percent of 2078 i.e 623 pixels will be selected for training as unlabelled data and rest for testing

C) include_class_list : Class label list included in this test, negative class list = list(set(include_class_list) - set(positive_class))

Ex include_class_list = [2, 3, 5, 6, 8, 10, 11, 12, 14]
Then each item in include_class_list will be considered as positive label and rest as negative label,
When class label 2 is considered as positive class then negative class labels list is [3, 5, 6, 8, 10, 11, 12, 14]
Note: Class labels should be present in groundtooth image

D) is_random_neg : Boolean value to indicate the way of selection for negative unlabelled training data,
If set to true then all the data from negative class list are accumulated and randomly train_neg_percentage of the total data is selected.
In the above case it might happen that training data might not have any pixel for class k in negative class list.
If set to false then train_neg_percentage pixels of data is randomly selected for each class in negative class list.
The above ensures that training data has some pixels of each class in negative class list

E) gpu : Zero-origin GPU ID (negative value indicates CPU)

Note: For every test the coressponding output is saved in DB. If you want to rerun a test for the same combination of
 (positive class, negative labels list, test type) then delete the entry from PUstats.

To run the tests, tune the above parameters and run the following command:

    python3 run_type1_test.py

The results will be stored in PUstats with test_type='type_1' and visual results will be saved in results folder, each row in PUstats coressponds to a test with a visual result file name that can be found in the result folder

Type 2:
Positive Class: A positive class labels is selected from a list, spatially closely related pixels are selected from that class for training.
For a class label j selected as a positive class, a square patch of size k * k is selected which has minimum percnt_pos(described below) pixels of the postive class.
To get the value of k for a class label j we need to do some preprocessing

Negative Class: From a list of negative class labels, all pixels are selected from that class for training

Testing and Training Data: The two types of data are fully-overlapping

Parameters to tune:

File : type2_patch.py
A) percnt_pos : Minimum percentage of total positive pixels that should be present in the patch

Ex: percnt_pos = 30
For every class [1,2...n] present in the groundtooth image we try of find a patch of size k where 5% of length of image <= k <= 25% of length of image,
such that the square patch will have atleast 30% pixels of that class. We store the boundary of the patch for each class in PatchClass table.

To preprocess data for testing Type 2 :
Tune percnt_pos parameter and run the following command

    python3 type2_patch.py


Running the test:

Parameters to tune:

File : run_type2_test.py

A) include_class_list : Class label list included in this test, negative class list = list(set(include_class_list) - set(positive_class))

Ex include_class_list = [2, 3, 5, 6, 8, 10, 11, 12, 14]
Then each item in include_class_list will be considered as positive label and rest as negative label,
When class label 2 is considered as positive class then negative class labels list is [3, 5, 6, 8, 10, 11, 12, 14]
Note: Class labels should be present in groundtooth image

B) gpu : Zero-origin GPU ID (negative value indicates CPU)

To run the test:

Tune include_class_list and gpu and run the following command

    python3 run_type2_test.py

The results will be stored in PUstats with test_type='type_2' and visual results will be saved in results folder, each row in PUstats coressponds to a test with a visual result file name that can be found in the result folder


