# !/bin/bash
# -*- coding: utf-8 -*-

dir_data="Data"
csv_extension=".csv"
arff_extension=".arff"
model_extension=".model"
results_extension=".results"

training_filename="Train"
developing_filename="Develop"

# MBP
path_weka="/Applications/weka-3-8-1/weka.jar"
# INESC
#path_weka="/usr/share/java/weka.jar"

k=1

number_words_keep=5

normalize=0

ranker_n=1

dir_tmp="tmp"
mkdir -p $dir_tmp

# Clean previous results
rm *.results

# Just TF
java -cp "$path_weka" -Xmx1024m weka.filters.unsupervised.attribute.StringToWordVector -b -i "$dir_data/$training_filename$arff_extension" -o "$dir_tmp/S2WV_TF_$training_filename$arff_extension" -r "$dir_data/$developing_filename$arff_extension" -s "$dir_tmp/S2WV_TF_$developing_filename$arff_extension" -R 2 -W $number_words_keep -C -T -N $normalize -tokenizer "weka.core.tokenizers.WordTokenizer -delimiters \" \\r \""


# Train a Classifier
java -cp "$path_weka" -Xmx1024m weka.classifiers.lazy.IBk -t "$dir_tmp/S2WV_TF_$training_filename$arff_extension" -d "$dir_tmp/S2WV_TF_$training_filename$model_extension" -K $k -c 1 -x 2 -o> "CROSS_FOLD_VALIDATION_S2WV_TF_$training_filename$results_extension"

# Predict
java -cp "$path_weka" -Xmx1024m weka.classifiers.lazy.IBk -l "$dir_tmp/S2WV_TF_$training_filename$model_extension" -T "$dir_tmp/S2WV_TF_$developing_filename$arff_extension" -c 1 -o> "pred$results_extension"
