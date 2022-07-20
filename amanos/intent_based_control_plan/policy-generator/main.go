package main

import (
	"errors"
	"os"

	"github.com/gin-gonic/gin"
	"github.com/gin-gonic/gin/binding"
	"github.com/joho/godotenv"
	log "github.com/sirupsen/logrus"
)

// Declare a simple decision structure
type Decision struct{
	Decision string `json:"decision"`
	IntentId string `json:"intent-id"`
	Params map[string]interface{} `json:"params"`
}


func main() {
	// check if we are using the debug environment 
	if os.Getenv("DEBUG")!="0" {
		// loading environment variables from .env 
		godotenv.Load()
	}
	if _, err := checkEnvVariables(); err != nil{
		return 
	}
	
	// creating the router 
	router := gin.Default()
	// initializing logger
	log.SetFormatter(&log.TextFormatter{
		FullTimestamp: true,
	})

	router.POST("/decisions", func (c *gin.Context)  {
		log.Info("Received decision in the /decisions")
		// check that we actually received a decision
		var decision Decision
		// if it cannot be bound then it is not a decision 
		if err := c.ShouldBindBodyWith(&decision, binding.JSON); err != nil {
			return
		}
		// passing to the decision mapper to handle decision
		_, err := HandleDecision(&decision, c)	
		if err != nil {
			c.JSON(500, gin.H{
				"status": "An error occurred while processing the decision ",
			})
		}else{
			c.JSON(200, gin.H{
				"status": "Decision Received Successfully",
			})
		}
		
	})

	if os.Getenv("POLICY_GENERATOR_PORT")!="" {
		// starting the router 
		router.Run(":"+os.Getenv("POLICY_GENERATOR_PORT"))
	}else{
		// starting the router 
		router.Run("localhost:8080")
	}
	
}

// check that environment variables were set 
func checkEnvVariables()(any, error){
	if os.Getenv("MANO_URL") ==""{
		log.Error("MANO_URL env variable was not set ")
		return nil, errors.New("environment variable not set ")
	}
	return nil, nil
}
