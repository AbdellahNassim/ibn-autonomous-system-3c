package main

import (
	"context"
	"flag"
	"path/filepath"

	log "github.com/sirupsen/logrus"
	v1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/api/meta"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/apis/meta/v1/unstructured"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/runtime/schema"
	"k8s.io/apimachinery/pkg/runtime/serializer/yaml"
	"k8s.io/client-go/dynamic"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/restmapper"
	"k8s.io/client-go/tools/clientcmd"
	"k8s.io/client-go/util/homedir"
)

// this function will deploy the subnet
func DeploySubnet(subnetYaml string, namespace string, config *rest.Config)(error){
	log.Info(subnetYaml)
	// getting client 
	// the client will allow us to communicate with cluster
	client, err := createClientSet(config)
	if err!= nil{
		return err
	}
	log.Info("Creating namespace "+namespace)
	namespaceObject := &v1.Namespace{ObjectMeta: metav1.ObjectMeta{Name: namespace}}
	_, err = client.CoreV1().Namespaces().Create(context.TODO(), namespaceObject, metav1.CreateOptions{});
	if err!=nil{
		log.Error("Error creating namespace")
		log.Error(err)
		return err
	}

	// decoding subnet.yaml to get the kind and version of the resource
	object, groupVersion, err := decodeYaml(subnetYaml)
	if err !=nil{
		return err
	}
	// Now that we have identified the groupVersion and kind 
	// we need to map it to actual kubernetes resource
	// get resources mapper 
	mapper, err := createResourcesMapper(client)
	if err!=nil{
		return err
	}
	// get the mapping 
	// here we will map the resources that we deserialized into a kubernetes 
	// resource
	mapping, err := mapper.RESTMapping(groupVersion.GroupKind(),
									   groupVersion.Version)
	if err != nil {
    	log.Error(err)
		return err
	}
	// getting client resource
	clientResource,unstructuredObj,  err := getClientResource(mapping,object,config,namespace)
	if err !=nil {
		return err
	}
	// creating resource 
	_, err = clientResource.Create(context.TODO() ,unstructuredObj, metav1.CreateOptions{})
	if err != nil {
	    log.Error(err)
		return err
	}
	return nil 
}

// getting client of the identified resource
func getClientResource(mapping *meta.RESTMapping,runtimeObject runtime.Object, config *rest.Config, namespace string)(dynamic.ResourceInterface, *unstructured.Unstructured , error){
	// 获Creating dynamic rest client 
	// This will allow us to get the client for a certain type of resources
	dynamicREST, err := dynamic.NewForConfig(config)
	if err != nil {
	    log.Error(err)
		return nil,nil, err
	}
	
	
	unstructuredObj := runtimeObject.(*unstructured.Unstructured)
	var resourceREST dynamic.ResourceInterface

	//  namespace 范围内的资源提供不同的接口
	if mapping.Scope.Name() == meta.RESTScopeNameNamespace {
		unstructuredObj.SetNamespace(namespace)
	    resourceREST = 
	      dynamicREST.
	      Resource(mapping.Resource).
	      Namespace(unstructuredObj.GetNamespace())
	} else {
	    resourceREST = dynamicREST.Resource(mapping.Resource)
	}
	return resourceREST, unstructuredObj, nil
}







// decoding the yaml to get the kind of the kubernetes object
func decodeYaml(subnetYaml string)(runtime.Object, *schema.GroupVersionKind, error){
	// using the kubernetes deserializer
	runtimeObject, groupVersionAndKind, err := yaml.
        NewDecodingSerializer(unstructured.UnstructuredJSONScheme).
        Decode([]byte(subnetYaml), nil, nil)
    if err != nil {
        log.Error(err)
		return nil,nil,err
    }
	return runtimeObject, groupVersionAndKind, nil
}


// get resource mapper 
func createResourcesMapper(clientset *kubernetes.Clientset)(meta.RESTMapper, error){
	// get api group resources 
	resources, err := restmapper.GetAPIGroupResources(clientset.Discovery())
	if err != nil {
	    log.Error(err)
		return nil, err
	}
	// 创建 'Discovery REST Mapper'，获取查询的资源的类型
	mapper:= restmapper.NewDiscoveryRESTMapper(resources)
	return mapper, nil
}



// creating client set 
func createClientSet(config *rest.Config)(*kubernetes.Clientset, error){
	// the clientset allow us to communicate with the cluster !
	clientset, err := kubernetes.NewForConfig(config)
	if err != nil {
	    log.Error(err)
		return nil, err
	}
	return clientset, nil
}




// Initializing the kube config object 
func initializeKubeConfig()(*rest.Config, error){
	var kubeconfig *string
	// check if we can load the config from home directory 
	if home := homedir.HomeDir(); home != "" {
		kubeconfig = flag.String("kubeconfig", filepath.Join(home, ".kube", "config"), "(optional) absolute path to the kubeconfig file")
	} else {
		// else we need to pass in the absolute path 
		// TODO 
		kubeconfig = flag.String("kubeconfig", "", "absolute path to the kubeconfig file")
	}
	flag.Parse()

	// use the current context in kubeconfig
	config, err := clientcmd.BuildConfigFromFlags("", *kubeconfig)
	if err != nil {
		log.Error("Could not initialize kubernetes client")
		log.Error(err)
		return nil, err
	}
	return config, nil
}