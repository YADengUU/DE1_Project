#!/bin/bash

# file for recording runtimes
runtime_log="expand_data_runtime.log"

echo "Replicated, Runtime" > $runtime_log

for i in 1 2 4 6 8 10;do
    scripttorun="pop_journal_$i.py"
    echo "Running $scripttorun"

    # start the cluster
    docker-compose -f docker-compose-2-node.yml up -d

    # wait for a while so that the cluster is fully up running
    wait
    container_id=$(docker ps -qf "name=project_spark-master")
    docker cp $scripttorun ${container_id}:./

    # start-time
    SECONDS=0

    # submit spark job
    docker exec -it $container_id /usr/local/spark/bin/spark-submit --master spark://sparkmaster:7077 $scripttorun

    # calculate and log the runtime
    runtime=$SECONDS
    echo "$i, $runtime">>$runtime_log
    echo "Shutting down the cluster"

    # shut down cluster
    docker-compose -f docker-compose-2-node.yml down
    wait
    
    docker rmi $(docker images -a -q)
    # wait a while before starting the next configuration
    wait
done

echo "Benchmarking completed. Runtimes recorded into $runtime_log"