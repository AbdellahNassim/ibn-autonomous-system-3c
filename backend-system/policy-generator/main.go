package main

import (
	"fmt"

	"github.com/gin-gonic/gin"
	"github.com/gin-gonic/gin/binding"
)

// Declare a simple decision structure
type Decision struct{
	Decision string `json:"decision"`
	IntentId string `json:"intent-id"`
	Params map[string]interface{} `json:"params"`
}

// ServiceDeploymentDecision inherite from the generate Decision
type ServiceDeploymentDecision struct{
	Params DeploymentParams `json:"params"`
	Decision
}

// Service Deployment Params
type DeploymentParams struct{
	Service Service `json:"service"`
	Resources Resources `json:"resources"`
}

// Service structure 
type Service struct{
	Name string `json:"name"`
	Repository string `json:"repository"`
	RepositoryUrl string `json:"repository_url"`
}

// Resources structure 
type Resources struct{
	Cpu int32 `json:"cpu"`
	Memory int32 `json:"memory"`
	Network int32 `json:"network"`
	Storage int32 `json:"storage"`
}

func main() {
	// creating the router 
	router := gin.Default()

	router.POST("/decisions", func (c *gin.Context)  {
		// check that we actually received a decision
		var decision Decision
		// if it cannot be bound then it is not a decision 
		if err := c.ShouldBindBodyWith(&decision, binding.JSON); err != nil {
			return
		}
		if decision.Decision =="DEPLOYMENT_DECISION" {
			// we are dealing with a deployment decision 
			var deploymentDecision ServiceDeploymentDecision
			// if it cannot be bound then it is not a decision 
			if err := c.ShouldBindBodyWith(&deploymentDecision, binding.JSON); err != nil {
				fmt.Println(err)
				return
			}
			fmt.Println("Decision Mapped and converted to Service Deployment Decision")
			// sending the decision to the decision mapper
			HandleServiceDeploy(&deploymentDecision)
		}

		fmt.Println(decision.Params)
		c.JSON(200, gin.H{
			"status": "Decision Received Successfully",
		})
	})

	// starting the router 
	router.Run("localhost:8001")
}