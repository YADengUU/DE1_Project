This is the coursework for Data Engineering 1. The project uses Scopus citation datasets available from Kaggle.com.
The aim of the application is to select the most popular (cited) journals per year, and their corresponding subject areas,
as a simple version of citation analysis.
With files further organized and stored in the HDFS cluster, the project deploys Spark cluster with different number of worker nodes
to test the horizontal scalability of the application. The ability to handle expanded datasets is assessed by replicated datasets,
with the comparison of its performance with Pandas running locally.

All experiments are automated with the two shell scripts (test_horizontal.sh & test_large_data.sh). Before using the docker-compose files, one should notice to edit the
paths to the worker nodes' Dockerfiles correctly.
