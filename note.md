# DATABRICKS ASSET BUNDLE

1.  databricks -h
2.  databricks configure -h
3.  databricks configure --host https://adb-3307511481276917.17.azuredatabricks.net/ --profile DEFAULT
4.  `databricks auth profiles` - SHOW Profiles (TEST/DEV/PROD)
6.  `databricks auth describe` - DESCRIBING PROFILES
7.  databricks auth profiles
8.  databricks auth describe --profile TEST
9. databricks bundle validate
10. `databricks bundle summary` = just summary not validation
11. adding new profile / new target - Install Databricks Extension to VSCOde. Shift + CTRL + P then type Databricks open databricks configuration file and then add your targets. (it stores that configuration file in our file system. /Users/novaguliyev/.databrickscfg)  ex:
[DEFAULT]
host  = https://adb-3307511481276917.17.azuredatabricks.net/
token = [REDACTED]

[TEST]
host = https://adb-4137916781113256.16.azuredatabricks.net/
token = [REDACTED]

[PROD]
host = https://adb-2957129268936759.19.azuredatabricks.net/
token = [REDACTED] 

12. databricks bundle deploy --target <target_name ex: test> = deploying different env
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




>> Resources to study
1. Substution and Variables - https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/variables

