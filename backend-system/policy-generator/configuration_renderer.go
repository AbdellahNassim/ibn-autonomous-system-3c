package main

import (
	"bytes"
	"path/filepath"
	"text/template"

	log "github.com/sirupsen/logrus"
)

// function to render the mapped configurations
// this function will use 2 sub functions that
func RenderConfigurations(configuration *ServiceDeploymentConfiguration) (any, error){
	log.Info("Rendering the configuration")
	log.Info(configuration)
	// Generating subnet configuration 
	subnetYaml, err := CommConfigRenderer(configuration)
	if err != nil{
		return nil, err
	}
	valuesYaml, err := CompCachingConfigRenderer(configuration)
	if err != nil{
		return nil, err
	}
	log.Info(subnetYaml)
	log.Info(valuesYaml)
	return nil,nil
}






// function to render the communication configurations 
// it will generate the subnet.yaml file 
func CommConfigRenderer(config *ServiceDeploymentConfiguration) (string,error){
	subnetTemplateFilePath := "./templates/subnet-template.yaml"
	log.Info("Reading Subnet Template file " + subnetTemplateFilePath)
	// reading the template file 
	networkSubnetTemplate, err := template.New(filepath.Base(subnetTemplateFilePath)).ParseFiles(subnetTemplateFilePath)
	//check if error occured 
	if err != nil{
		log.Error(err)
		return "", err
	}
	// template file read successfully 
	// creating templates data 
	subnetTemplateData := map[string]string{
		"SubnetName": config.IntentId +"_subnet",
		"SubnetNamespace": config.IntentId,
		"SubnetCidr": config.NetworkSubnetCidr,
		"SubnetGateway": config.NetworkGatewayIp,
	}
	// rendering the template with data 
	var policyBuffer bytes.Buffer
    if err := networkSubnetTemplate.Execute(&policyBuffer, subnetTemplateData); err != nil {
		log.Info("Error while rendering the template with data ")
		log.Error(err)
        return "", err
    }
	log.Info("Subnet Configuration generated successfully")
	return policyBuffer.String(), nil
}

// function to render the computing caching configuration 
// It will generate the values.yaml file 
func CompCachingConfigRenderer(config *ServiceDeploymentConfiguration)(string, error){
	valuesTemplateFile := "./templates/values-template.yaml"
	log.Info("Reading values Template file " + valuesTemplateFile)
	// reading the template file 
	valuesTemplate, err := template.New(filepath.Base(valuesTemplateFile)).ParseFiles(valuesTemplateFile)
	//check if error occured 
	if err != nil{
		log.Error("Error while reading the template")
		log.Error(err)
		return "", err
	}
	// template file read successfully 
	// creating templates data 
	subnetTemplateData := map[string]int32{
		"NetworkPodEgressRate": config.NetworkEgressRate,
		"NetworkPodIngressRate": config.NetworkIngressRate,
		"CpuLimits": config.CpuLimits,
		"MemoryLimits": config.MemoryLimits,
		"StorageLimits": config.CachingLimit,
		"CpuRequests": config.CpuRequest,
		"MemoryRequests": config.MemoryRequest,
		"StorageRequests": config.CachingRequest,
		"ApplicationReplicaCount": int32(config.ApplicationReplicaCount),
	}
	// rendering the template with data 
	var policyBuffer bytes.Buffer
    if err := valuesTemplate.Execute(&policyBuffer, subnetTemplateData); err != nil {
		log.Info("Error while rendering the template with data ")
		log.Error(err)
        return "", err
    }
	log.Info(policyBuffer.String())
	log.Info("Values Configuration generated successfully")
	return policyBuffer.String(), nil
}