# Edc-sync-data-report

The module tracks edc sync models data between two community server and central server.

###### Sync Models Registration - Register Models

Run the following management command

*  1
 > python manage.py register_sync_models
     --app_label "specify app_label" --site_id "specify site id"
 >> Register all models for the specified app_label and site_id
 
* 2
> python manage.py register_sync_models
     --app_label "specify app_label" --site_id "specify site id" --model_name "specify model_name" 
 >> Register a model for the specified app_label and site_id 

###### Sync Models Registration - Delete registered models

* 1
> python manage.py unregister_sync_models
     --app_label "specify app_label" --site_id "specify site id" --model_name "specify model_name" 
 >> Delete models for the specified app_label

###### Sync scheduler

Install the Redis Server on Client and Server VM. (it is a dependency for django_q)

There are 3 tasks to be configured.

1. send_sync_report, should be registered with djangoq admin scheduler
2. prepare_confirmation_ids, should be registered with djangoq admin scheduler
3. prepare_summary_count_data, should be registered with djangoq admin scheduler

Client Configuration
You need to add the following task on django_q admin
1. Add prepare_confirmation_ids:
2. Add prepare_summary_count_data

Server Configuration
 1. Add : send_sync_report
 
Run the following command as background service
> python manage.py qcluster
