package main

import (
	"github.com/gin-gonic/gin"
	"github.com/gin-gonic/gin/binding"
	log "github.com/sirupsen/logrus"
)

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


// configuration structure for the service deployment
type ServiceDeploymentConfiguration struct {
	IntentId string
	Namespace string
	// Network configurations 
	NetworkSubnetCidr string 
	NetworkGatewayIp string
	NetworkIngressRate int32 
	NetworkEgressRate int32 
	// Application specific 
	ApplicationName string
	ApplicationChart string 
	ApplicationChartRepository string 
	ApplicationChartRepositoryUrl string
	ApplicationReplicaCount  int16
	// Compute specific
	CpuLimits int32
	CpuRequest int32 
	MemoryLimits int32 
	MemoryRequest int32 
	// Caching specific 
	CachingLimit int32 
	CachingRequest int32
	
}

// Function that takes in input the received decision and check what type of decision 
// was received to map it to the appropriate handler 
func HandleDecision(decision *Decision, c *gin.Context) (any, error){
	if decision.Decision =="DEPLOYMENT_DECISION" {
		log.Info("A deployment decision was received")
		// we are dealing with a deployment decision 
		var deploymentDecision ServiceDeploymentDecision
		// if it cannot be bound then it is not a decision 
		if err := c.ShouldBindBodyWith(&deploymentDecision, binding.JSON); err != nil {
			log.Error(err)
			return nil, err
		}
		log.Debug(deploymentDecision)
		log.Info("Decision Mapped and converted to Service Deployment Decision")
		// sending the decision to the decision mapper
		return HandleServiceDeploy(&deploymentDecision)
	}else{
		return nil, nil
	}
}

func HandleServiceDeploy(decision *ServiceDeploymentDecision) (any, error){
	log.Info("Mapping the received decision into configuration object")
	// mapping the decision into a configuration object to be processed 
	deploymentConfiguration := ServiceDeploymentConfiguration{
		IntentId: decision.IntentId, 
		Namespace: "default",
		NetworkSubnetCidr: "10.10.0.0/16",
		NetworkGatewayIp: "10.10.0.1",
		NetworkIngressRate: decision.Params.Resources.Network,
		NetworkEgressRate: decision.Params.Resources.Network,
		ApplicationName: decision.IntentId + "-" + decision.Params.Service.Name,
		ApplicationReplicaCount: 1,
		ApplicationChart: decision.Params.Service.Name,
		ApplicationChartRepository: decision.Params.Service.Repository,
		ApplicationChartRepositoryUrl: decision.Params.Service.RepositoryUrl,
		CpuLimits: decision.Params.Resources.Cpu,
		CpuRequest: decision.Params.Resources.Cpu,
		MemoryLimits: decision.Params.Resources.Memory,
		MemoryRequest: decision.Params.Resources.Memory,
		CachingLimit: decision.Params.Resources.Storage,
		CachingRequest: decision.Params.Resources.Storage,
	}
	log.Info("Generated deployment configuration ")
	log.Info(deploymentConfiguration)
	// pass the configuration to be rendered
	return RenderConfigurations(&deploymentConfiguration)
}