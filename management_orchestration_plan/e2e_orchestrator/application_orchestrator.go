package main

import (
	"net/http"
	"os"
	"os/exec"

	"github.com/prometheus/prometheus/prompb"
	"github.com/prometheus/prometheus/storage/remote"
	log "github.com/sirupsen/logrus"
)





type HelmApplication struct{
	Name string `form:"application_name"`
	ChartName string `form:"chart_name"`
	Namespace string `form:"namespace"`
	Repository string `form:"repository"`
	RepositoryUrl string `form:"repository_url"`
}





// start the remote write server
// this server will receive chuncks of metrics from prometheus
func StartMetricsServer()(error){
	// creating a simple route to receive metrics
	http.HandleFunc("/receive", func(w http.ResponseWriter, r *http.Request) {
		// create a simple variable with writeRequest protobuf
		req, err := remote.DecodeWriteRequest(r.Body)
		// if decoding is error we return and print error
		if err != nil {
			log.Fatal("An error occured whilde decoding request")
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}
		log.Debug("A write request was received from prometheus")
		// once the write request is decoded we will try to filter data 
		// loop over the time series data 
		for _, ts := range req.Timeseries {
			// for each time serie

			// collect the labels of the metric 
			labels := ts.Labels
			// a sample is the timestamp and value of the metric
			var sample *prompb.Sample = nil

			// collect the value of the metric and the timestamp	
			for _, s := range ts.Samples {
				sample = &s
			}

			// send metric to the e2e orchestrator 
			AggregateTimeSeries(labels,*sample)
		}
	})

	// start the server
	err := http.ListenAndServe(":8003", nil)
	if err != nil {
		log.Fatal("An error occured while launching the application's metrics collector")
		return err
	}
	return nil
}





// Function to deploy the application in mec domain
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

// delete the temporary created values.yaml file 
func DeleteValuesYamlFile()(error){
	log.Info("Deleting values file ")
	e := os.Remove("/tmp/values.yaml")
    if e != nil {
        log.Error(e)
    }
	return nil
}

// create temporary values.yaml to set values of the application
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

// update helm chart repository 
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


// add the transcoder application repository
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