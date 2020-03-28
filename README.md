# Kantar DevOps: Application Test

This project has the propose to develop an application that collects the 100 last tweets from pre-determined tags and stores them into a database, where it can be consumed via a REST API.

To ensure the most scalable and productive result, Docker used to isolate each step/module into a container.

## Development Schedule
Here are the steps planned for this project, where each topic represent a day:
1. Study and design the application workflow 
2. Model the database
3. Develop a microservice to collect the last tweets from the tags
4. Develop the REST API
5. Design and develop a React web application to consume the data.
6. Implement the logging and monitoring features
    - For logging, Splunk was used
    - For monitoring, Prometheus was used
7. Write the documentation

## Modules Instructions

### Database

MySQL container was used as the engine for the database, the diagram used is described below:
![](https://i.imgur.com/TCohIB8.png)

The file in the folder `./mysql` contains the initial configurations (`init.sql`) for the database, where it checks if the table exists before creating a new one.

### Data Collection and Storage

To collect the data from Twitter, Tweepy[[1]][tweepy] was used to get information from the API in an easy way. To store the data collected PyMySQL[[2]][pymysql] was used to store in the table.

### REST API

To deploy the REST API, the Flask framework was used to create a fast and reliable microservice.

Three request modes are available in this API.

1. Get the top 5 most followed user:
    ```json
    [
      {
        "followers": 425364,
        "user": "Ehickioya"
      },
        ...
      {
        "followers": 53272,
        "user": "PitaRampal"
      }
    ]
    ```

2. Get the number of post per hour at each day:
    ```json
    [
      {
        "day": 19,
        "month": 3,
        "hour": 2,
        "posts": 1
      },
        ...
      {
        "day": 26,
        "month": 3,
        "hour": 17,
        "posts": 230
      }
    ]
    ```

3.  Get the number of posts with determined language for each tag:
    ```json
    [
      {
        "hashtag": "apigateway",
        "language": "en",
        "posts": 95
      },
      ...
      {
        "hashtag": "oauth",
        "language": "ja",
        "posts": 4
      }
    ]
    ```

To make the request to the API, just use the URL `http://localhost:2222/get_info?id=X`, where X is the number of the request described above. If the ID is not in the range, the API response with the following message: 
```json
{"error":{"code":400,"message":"No parameter was given","reason":"invalidParameter"}}
```

### Web Page

To develop the web page React was used, below is the compilation of the page consuming the API.
![react](https://i.imgur.com/jnGlHrM.png "react")

Note: As a personal preference I would use Vue.js

### Logging

After starting the Splunk container, it's necessary to add an HTTP Event Collector to get the log in formations about the REST API.

![Splunk](https://i.imgur.com/8WN4DAr.png "Splunk")

When you get the token, you should add it in the `docker-compose.yaml` file located in the folder docker, under the tag options, as showed below:

```yaml
logging:
    driver: splunk
    options:
        splunk-token:  'TOKEN_HERE'
        splunk-url: https://172.17.0.2:8088
        splunk-insecureskipverify: "true"
```

Exemplo de logs obtidos:
![logs](https://i.imgur.com/qzpR1X3.png "logs")


### Monitoring

To monitor our application, it's necessary to modify some JSON parameter in the Docker Daemon, since Linux was used to develop it, those are the steps:

1. Change the JSON Daemon file located at `/etc/docker/daemon.json` and insert the following line:

    ```json
    {
      "metrics-addr" : "127.0.0.1:9323",
      "experimental" : true
    }
    ```

2.  Create a temporary YAML file to configure Prometheus:

    ```yaml
    global:
      scrape_interval:     15s 
      evaluation_interval: 15s 
      external_labels:
          monitor: 'codelab-monitor'
      - job_name: 'prometheus'
        static_configs:
          - targets: ['localhost:9090']
      - job_name: 'docker'
        static_configs:
          - targets: ['localhost:9323']
    ```

3.  Run the service/container with swarm mode activated: 

    ```bash
    docker service create --replicas 1 --name my-prometheus \
        --mount type=bind,source=/tmp/prometheus.yml,destination=/etc/prometheus/prometheus.yml \
        --publish published=9090,target=9090,protocol=tcp \
        prom/prometheus
    ```

For further instructions and information about the documentation, please refer to this [site](https://docs.docker.com/config/daemon/prometheus/ "site").

Below are the number of request made:

![requests](https://i.imgur.com/JjkiWsm.png "requests")

## How to run?

Before running the application, some steps are needed to start the docker swarm.

1. Start the Swarm mode in docker `docker swarm init`
2. Create a registry service to store the images created `docker service create --name registry --publish published=5000,target=5000 registry:2`
3. Start Splunk logging `docker run -d -p 8000:8000 -e "SPLUNK_START_ARGS=--accept-license" -e "SPLUNK_PASSWORD=password" --name splunk splunk/splunk:latest`

Then, we can run the application, to do it just go to the folder docker and run `docker-compose up`.

## Conclusion

The schedule for this project followed as planned, although some difficulties appeared during the development. For example, some tools such as Splunk and Prometheus was new to me, so I had to study and understand their particular features to make the deployment.

Those tools listed above created a huge interest in me, and I'll keep studying to learn the best practices to deliver the state of art.

Lastly, I would like to say thank you for your interest and patient. I hope we can work together soon!

[tweepy]: https://www.tweepy.org/
[pymysql]: https://github.com/PyMySQL/PyMySQL