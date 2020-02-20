$DEV1/scripts/training_setup_dev1.sh
tar xf documents.tar
hdfs dfs -mkdir data-input
hdfs dfs -put documents data-input/documents
sudo chmod 777 --recursive /home/training
tar xf solution.tar

