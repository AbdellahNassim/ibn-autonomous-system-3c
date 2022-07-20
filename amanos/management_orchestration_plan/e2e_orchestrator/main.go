package main

import (
	"errors"
	"io/ioutil"
	"net"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
	"github.com/goccy/go-json"
	"github.com/joho/godotenv"
	"github.com/prometheus/prometheus/prompb"
	log "github.com/sirupsen/logrus"
)


func main() {

	// check if we are using the debug environment 
	// because generally in production environment we don't use env files 
	if os.Getenv("DEBUG")!="0" {
		// loading environment variables from .env 
		godotenv.Load()
	}

	if _, err := checkEnvVariables(); err != nil{
		return 
	}

	// creating the router 
	router := gin.Default()
	// initializing k8s config 
	// initializing the kube configuration
	config,err := initializeKubeConfig()
	if err!= nil{
		panic(err)
	}


	router.POST("/subnets", func(c *gin.Context) {
		log.Info("Received a post request to deploy subnet")
		// get namespace from query 
		namespace := c.Query("namespace")
		if namespace == ""{
			c.JSON(http.StatusBadRequest, gin.H{
				"error": "no namespace was found",
			})
		}

		body, err := ioutil.ReadAll(c.Request.Body)
		if err != nil {
			log.Error("error reading the request body")
			log.Error(err)
		}
		// read the body in string format 
		SubnetYaml := string(body)
		if DeploySubnet(SubnetYaml, namespace, config) != nil{
			c.JSON(http.StatusInternalServerError, gin.H{
				"error": "couldn't deploy the subnet an error occurred",
			})
		}
	})

	router.POST("/applications", func(c *gin.Context){
		log.Info("Received a post request to deploy an application")
		// reading the body 
		body, err := ioutil.ReadAll(c.Request.Body)
		if err != nil {
			log.Error("error reading the request body")
			log.Error(err)
			c.JSON(http.StatusBadRequest, gin.H{
				"error": "couldn't load the request body",
			})
		}

		// checking the query set 
		var application HelmApplication 
		if err :=c.ShouldBindQuery(&application); err != nil{
			log.Error("couldn't extract parameters from query set")
			log.Error(err)
		}

		// read the body in string format 
	 	ValuesYaml := string(body)
		if DeployApplication(&application, ValuesYaml)!=nil{
			c.JSON(http.StatusInternalServerError, gin.H{
				"error": "couldn't deploy the application an error occurred",
			})
		}
	})

	// start the application orchestrator metrics collection server
	err = StartMetricsServer()
	if err != nil {
		panic(err)
	}


	if os.Getenv("E2E_ORCHESTRATOR_PORT")!="" {
		// starting the router 
		router.Run(":"+os.Getenv("E2E_ORCHESTRATOR_PORT"))
	}else{
		// starting the router 
		router.Run(":8001")
	}
}

// check that environment variables were set 
func checkEnvVariables()(any, error){
	if os.Getenv("DATA_MANAGEMENT_HOST") ==""{
		log.Error("DATA_MANAGEMENT_HOST env variable was not set ")
		return nil, errors.New("environment variable not set ")
	}
	return nil, nil
}




/**
	TimeSerieMetric represents a structure of the received metric from prometheus
	It is used in order to aggregate and filter the metrics.
**/
type TimeSerieMetric struct {
	TimeStamp float64
	MetricName string
	MetricValue float64
	Namespace string
	PodName string
}




/**
	This function will be called from the different orchestrators
	It will aggregate/filter then stream the data to the intent based control plan
**/
func AggregateTimeSeries(timeSerieLabels []prompb.Label, timeSerieSample prompb.Sample){
	// the name of the metric
	var metricName string =""
    // the namespace of the the collected metric
	var namespace string = ""
	// the pod name of the collected metric
	var podName string = ""
	// basically here we loop on the labels of the time serie to filer out some metrics 
	for _, label := range timeSerieLabels {		
		if (label.Name =="namespace"){
			// if the metric is related to a system component or prometheus  then we filter 
			if ((label.Value == "kube-system") || (label.Value =="prometheus")){
				return;
			}
			namespace = label.Value
		}
		if (label.Name == "__name__"){
			metricName = label.Value
		}
		if (label.Name =="resource"){
			// if the label is about kubernetes request|limit then we should split 
			// based on if it is a cpu or memory request|limit
			metricName = metricName + "_"+label.Value
		}
		if (label.Name == "pod"){
			podName = label.Value
		}
	}
	// if the system doesn't have the namespace label we filter out
	if (namespace!= ""){
		timeSerieMetric := TimeSerieMetric{
			TimeStamp: float64(timeSerieSample.Timestamp),
			MetricName: metricName,
			MetricValue: timeSerieSample.Value,
			Namespace: namespace,
			PodName : podName,
		}
		// stream data to the intent based control plan 
		SendTelemetryData(timeSerieMetric)
	}
}


/**
	Calls the Data Management socket and send the telemetry data 
**/
func SendTelemetryData(telemetryMetric TimeSerieMetric){
	// get env variables 
	dataManagementHost := os.Getenv("DATA_MANAGEMENT_HOST")
	dataManagementPort := os.Getenv("DATA_MANAGEMENT_PORT")
	// connect to the socket 
	con, err := net.Dial("tcp", dataManagementHost+":"+dataManagementPort)
	if err != nil {
		log.Error("An error has occured while trying to connect to "+ dataManagementHost+":"+ dataManagementPort)
		log.Error(err)
	}
	// close connection as last step 
	defer con.Close()
	// encode the data as json 
	timeSerieJson, err := json.Marshal(telemetryMetric)
	if err != nil{
		log.Error("An error has occured while encoding json telemetry data")
		log.Error(err)
	}
	// send data to the socket 
	con.Write(timeSerieJson)
}