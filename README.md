This challenge is split into three sections. The completion of the **Collector** section is required for the submission to be evaluated. For extra points, take a jab at **Distribution**, **Containerization** or both sections. 

**The Submission is not considered complete unless questions for respective section are answered!**

# Shipping metrics around

Development of the brand new foobar counting service has come to an end and it is time to release it to general public. 
Each individual server keeps track of `/foo` and `/bar`	requests, exposing metrics via `/stats` endpoint.

You can find service code in `./src` directory; Execute `npm start` to run it.   
Feel free to call endpoints to interact with the service 
```
curl http://127.0.0.1:9999/stats
// => '{"foo":0,"bar":0}'
curl -XPOST http://127.0.0.1:9999/foo
// => OK
curl http://127.0.0.1:9999/stats
// => '{"foo":1,"bar":0}'
```

## Collector 

Your task is to collect metrics from `/stats` endpoint and expose them to the rest of the team, such that following questions could be answered:

    Ans: Please see the attached screenshot of Kibana dashboard I created: Foo_Bar_Statistics.PNG .  Other option is to import foobarstats.ndjosn file(which is the exported kibana object) into your Kibana instance. It will create all the Kibana objects for you.

- How many `foo` invocations happened at this point in time across all instances of the service? How many `bar`'s?

	Ans: The data table shown in the Kibana screenshot shows the latest foo and bar counts.

- What is the ratio of `foo` to `bar`?

	Ans: The 5th column shows the ratio of foo/bar. Its computed in the data table.

- Which instance had the max value of `foo` or `bar` in the past 24 hours?

	Ans: The last column(Max of foo or bar in the time range) shows the count for the max hits of foo or bar for all the servers.

Write a metric collector to ship metrics to [google cloud monitoring service](https://cloud.google.com/monitoring). Assume instance hosting collector has required permissions to write metric data. 

Metric collector(foo_bar_collector.py) has been written to ship metrics to the elasticsearch engine and kibana instead of google cloud monitoring due to some free trial and registration error on GCP (An unexpected error has occurred. Please try again later. [OR-CRMMT-01]). It was already communicated to Ryan before finalizing Elasticssearch.

### Questions for the section

- Why did you chose to go with this implementation?

		I had 2 options in my mind to create a collector:
		1. Instrument inside the application where I can add additional steps with the src to create a invocation log and store it in an analytical engine, whenever user make POST calls for foo or bar.
		2. Create a collector as a separate service which will keep pulling foo bar information as a CI process and store it in an analytical engine.
		I chose the 2nd approach because I considered that touching the code is not a good idea at this time. 1st approach would be better if the product team is not having any concerns with changing their code.
		As far as the technogies are concerned, the description is as follows:
		1. To write collector, I used python because Scripting allows me to rapidly tie together complex systems and express ideas without worrying about details like memory management or build systems.
		It is easy to write and run. Whenever I don't need a full stack server, I prefer python scripting. 
		2. To store and analyze logs I chose elasticsearch and Kibana. I would have gone with Google Monitoring but I was getting error while registration (An unexpected error has occurred. Please try again later. [OR-CRMMT-01])and was not able to resolve it even after trying multiple soultions.
			Elasticsearch is freely available to install and deploy locally or on VMs. Its setup and running the services are very quick and easy process.
			I don't have working experience with it and I have read about it. Its a high speed search and storage tool and Kibana provides a strong capability to visualize data. 
			Its REST based API makes it more comfortable for me to code in python.
		
- Which corners did you cut (if any)? Why? How do you think this should have been done?

	If I was doing it as a real project I would have preferred to instrument src by talking to its owner where it would have logged the foo bar statistics whenever there was user hit.
	It would be better as compared to a 3rd party collector where it keeps calling the application because its not 100% real time if the frequency of the CI job(running collector) is low.

## Distribution 

As a stretch goal, implement a way to distribute collector to remote machine(s). Consider versioning, dependencies & platform differences. 

### Questions for the section

- Why did you chose to go with this solution? Which alternatives (if any) did you evaluate?

    I have used puppet(psuedocode in file "puppet_code_to_distribute_foobarcollector.txt") to distribute collector to remote machines as I have worked on puppet and more familiar with it as infrastructure as code. It is a model-driven and having its own domain-specific language. It can be used for more complex systems.

    An alternative to puppet is Ansible as it is simple (has master but no agents). Commands can be written in any programming language and it uses YAML syntax.

## Containerization

As a stretch goal, bake collector into a docker image to be deployed as a side car with the service.  

- Why did you use this base image?
    
	Since I have created the collector in python, I used a light weight python image only. On top of it I simply installed the additional libraries I used in the collector script.
