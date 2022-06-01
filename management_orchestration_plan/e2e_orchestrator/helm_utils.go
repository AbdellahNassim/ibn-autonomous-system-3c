package main

import (
	"os"
	"os/exec"

	log "github.com/sirupsen/logrus"
)





type HelmApplication struct{
	Name string `form:"application_name"`
	ChartName string `form:"chart_name"`
	Namespace string `form:"namespace"`
	Repository string `form:"repository"`
	RepositoryUrl string `form:"repository_url"`
}

func DeployApplication(app *HelmApplication, valuesYaml string)(error){
	log.Info("Received application to deploy")
	if err := UpdateLocalRepositoryList(); err!=nil{
		return err
	}
	// adding repository
	AddingRepository(app)
	//
	if err := CreateValuesYamlFile(valuesYaml); err!=nil{
		return err
	}
	if err := InstallApplication(app); err!=nil{
		return err
	}
	// if err := DeleteValuesYamlFile(); err!=nil{
	// 	return err
	// }
	return nil 
}


func InstallApplication(app *HelmApplication)(error){
	log.Info("Installing the application chart")
	out, err:= exec.Command("helm", "install","-f","/tmp/values.yaml", app.Name, app.Repository+"/"+app.ChartName, "-n", app.Namespace).Output()
    if err != nil {
        log.Error(err)
		return err
    }
	log.Info(string(out))
	return nil
}

func DeleteValuesYamlFile()(error){
	log.Info("Deleting values file ")
	e := os.Remove("/tmp/values.yaml")
    if e != nil {
        log.Error(e)
    }
	return nil
}

func CreateValuesYamlFile(valuesYaml string)(error){
	// creating the values.yaml
	log.Info("Creating the values.yaml")
	f, err := os.Create("/tmp/values.yaml")
	if err!=nil{
		log.Error("Error creating file")
		return err
	}
	defer f.Close()
	f.WriteString(valuesYaml)
	f.Sync()
	return nil
}

func UpdateLocalRepositoryList()(error){
	// updating the helm repository 
	log.Info("Updating helm repositories list")
	out, err := exec.Command("helm", "repo", "update").Output()
    if err != nil {
        log.Error(err)
		return err
    }
	log.Info(string(out))
	return nil
}

func AddingRepository(app *HelmApplication){
	// adding the repository 
	log.Info("Adding the application chart repository")
	out, err := exec.Command("helm", "repo", "add", app.Repository, app.RepositoryUrl).Output()
    log.Info(string(out))
	if err != nil {
		// an error can occure if the repo is already added
        log.Error("Repository already exist")
    }
}