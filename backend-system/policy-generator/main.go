package main

import (
	"github.com/gin-gonic/gin"
	"github.com/gin-gonic/gin/binding"
	log "github.com/sirupsen/logrus"
)

// Declare a simple decision structure
type Decision struct{
	Decision string `json:"decision"`
	IntentId string `json:"intent-id"`
	Params map[string]interface{} `json:"params"`
}


func main() {
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

	// starting the router 
	router.Run("localhost:8001")
}