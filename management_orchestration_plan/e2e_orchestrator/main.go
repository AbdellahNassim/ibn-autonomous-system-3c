package main

import (
	"io/ioutil"
	"net/http"
	"os"

	"github.com/gin-gonic/gin"
	log "github.com/sirupsen/logrus"
)


func main() {

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
	if os.Getenv("E2E_ORCHESTRATOR_PORT")!="" {
		// starting the router 
		router.Run(":"+os.Getenv("E2E_ORCHESTRATOR_PORT"))
	}else{
		// starting the router 
		router.Run(":8001")
	}
}
