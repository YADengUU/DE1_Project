#!/bin/bash

# array of docker-compose files for different configuration with numbers of nodes
compose_files=("docker-compose-1-node.yml" "docker-compose-2-node.yml" "docker-compose-3-node.yml" "docker-compose-4-node.yml" "docker-compose-5-node.yml" "docker-compose-6-node.yml" "docker-compose-7-node.yml" "docker-compose-8-node.yml")

# file for recording runtimes
runtime_log="spark_runtime.log"

echo "Nodes, Runtime" > $runtime_log

for file in "${compose_files[@]}"
do
    # extract the number of nodes from the docker-compose filename
    nodes=$(echo $file | grep -o -E '[0-9]+')
    echo "Starting cluster with configuration: $file"

    # start the cluster
    docker-compose -f $file up -d

    # wait for a while so that the cluster is fully up running
    wait
    container_id=$(docker ps -qf "name=project_spark-master")
    docker cp popular_journals.py $container_id:./

    # start-time
    start=$(date +%s)

    # submit spark job
    docker exec -it $container_id /usr/local/spark/bin/spark-submit --master spark://sparkmaster:7077 popular_journals.py

    # end timer
    end_time=$(date +%s)

    # calculate and log the runtime
    runtime=$((end_time-start_time))
    echo "$nodes, $runtime">>$runtime_log
    echo "Shutting down the cluster: $file"

    # shut down cluster
    docker-compose -f $file down
    wait
    
    docker rmi $(docker images -a -q)
    # wait a while before starting the next configuration
    wait
done

echo "Benchmarking completed. Runtimes recorded into $runtime_log"