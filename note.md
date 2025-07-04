# DATABRICKS ASSET BUNDLE

>> Resources to study
1. Substution and Variables - https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/variables


1.  databricks -h
2.  databricks configure -h
3.  databricks configure --host https://adb-3307511481276917.17.azuredatabricks.net/ --profile DEFAULT
4.  `databricks auth profiles` - SHOW Profiles (TEST/DEV/PROD)
6.  `databricks auth describe` - DESCRIBING PROFILES
7.  databricks auth profiles
8.  databricks auth describe --profile TEST
9. databricks bundle validate
10. `databricks bundle summary` = just summary not validation
11. adding new profile / new target - Install Databricks Extension to VSCOde. Shift + CTRL + P then type "Open Databricks Configuration File" and then add your targets. (it stores that configuration file in our file system. /Users/novaguliyev/.databrickscfg)  ex:
[DEFAULT]
host  = https://adb-3307511483434434343.17.azuredatabricks.net/
token = [REDACTED]

[TEST]
host = https://adb-4137916783434343434.16.azuredatabricks.net/
token = [REDACTED]

[PROD]
host = https://adb-295712926343434343.19.azuredatabricks.net/
token = [REDACTED] 

12. databricks bundle deploy --target <target_name ex: test> = deploying different env
    if you are running from local. `databricks bundle deploy -t <target_name> -p <target_profile_name_from your local dbx configuration file: ex:  TEST>
    so, databricks bundle deploy -t test -p TEST
13. databricks bundle destroy = removes deployment from workspace
14. Databricks Asset Bundle only deploy changes, so it does incremental changes deployment. 
    you can see `last_modified_timestamp` value under .databricks/bundle/<env>/sync-snapshots/<sometext>.json

15. what if you manually removed the lets say notebook from UI manually?? how incremental will work. If you remove manually, once you redeploy it will not automatically bring those back because it does not know that you removed, instead it uses its own last_modified_timestamp. 
if you removed something manually and want to redeploy everything again not incremental for now, just remove  `.databricks` folder from folders section.
16. Lookup Variables - In DAB lookup variables are the variables extract the ID of requested object. It might get alerts, cluster_policies, clusters, dashboard, instance_pool, job, metastore, pipeline, service_principal. You just provide name of the object and it extract ID of that object and you can use id wherever you want. 
17. `databricks bundle validate -o json` = shows everything (all configurations of job) as json representation
18. to create a .wheel file. create venv 
    1. python3 -m venv .dab_venv 
    2. source .dab_venv/bin/activate
    3. pip3 install setuptools
    4. pip3 install wheel
    5. create setup.py file in the project root directory. write text 
    6. run this command from terminal in venv `python3 setup.py bdist_wheel`
    7. created file under dist folder is your package and version of package is appended to name.
    8. copy the path of that .whl file and go to terminal `pip3 install <path_of_wheel>`
    9. pip list, you will see your package there. then you can easily import whatever you want
19. Delta Live Tables CI/CD - With new changes now, we can write to multiple schema in dlt. before we were only allowed to write one destination schema. and all dynamic values need to be passed in at a pipeline level as spark cluster configuration `ADVANCED -> Configuration`. from notebook we will access them via `spark.conf.get`.
11. In dev environment usually we use PAT tokens and users use that PAT token and they are mainly their entraid, but in TEST/PROD we don't want them to have an access to those environments and update anything. therefore, we will use service principals. First we should create a service principal. 
Go to Azure Portal -> App Registration -> give a name ex: <sp-databricks-prod-eus2> and then create. 
go to databricks workspace test/prod -> settings from top right -> Identity & Access -> Add service principals. -> Add new -> it is microsoft entra id spn click it -> copy Application ID and give name (usually keep the same name of spn name.) -> Then click on created service principal -> Allow it to create a cluster.
Then go to your SPN from App registration -> Manage -> Generate a New Client Secret -> create one and give name -> then copy value [redacted] 
Now, if you remember previously from our local in order to deploy to our test environment in our 
/Users/novaguliyev/.databrickscfg file we specified PAT TOkens for Test/Prod as well. but as we agreed now, it is not the recommended way, because user should not have an access to that. 
updat that profile file

[TEST]
host = https://adb-4137916232434343434.16.azuredatabricks.net/
azure_client_id = [REDACTED] - get this from spn in app registration
azure_tenant_id = [REDACTED] - get this from spn in app registration
azure_client_secret = [REDACTED] - This is the secret value which you created above.

Once we do above steps, we do update our databricks.yml file as well and this time for test/prod instead of running it as our username. we run it as service principal. 
Next, because we will run job as service principal in dbx , that service principal should have an access to the catalog or individual objects. Go to portal catalog -> permissions -> look for service principal look for name -> then assign permission.



## Above Configurations are for our local. because we set profiles in our local. 
But in Continuous Delivery we need to set our workflow in Github , Now we will practice it. and will set our credentials in our Github. 
1. To create an environment in github free account - we should switch it to be a public repository.
2. Setting > Environemnts > Name environment: ex: test > Add environment secret - Add azure client id, client secret for spn config.
3. Make sure secret names are all uppercase AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID
4. when you setup `prod` environment -> Make sure add protection rule : required reviewer -> for now, choose your name, because to deploy to prod should require manual approval.
5. Once we created cd-workflow.yml file we should manually approve PROD portion. Because we set approve prod deployment.
