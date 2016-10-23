# Karura

## Concept

* Machine Learning For Everybody

## Basic Synario

* Make App for Karura
* Add setting (create record) in Karura
 * app_id
 * select field: field items is loaded automatically -> which is feature, target
* push "train" button
* setting is sent to server, server try to learn it.
 * extract data from app by app_id and feature/target field
 * format the data -> category variable, normalization and so on.
 * select model (by record count and count of features)
 * train the model
 * save model to disk
 * return the result: accuracy, message etc -> use websocket like feature to show the progress
* done the training
* when create or edit the record, suggest the prediction

## Components

* Karura App: kintone app
* karura.master.js: javascript customize script for Karura App
 * lookup_fields: add fields to inner table if not exist. (if exist, don't override it)
 * train: send application setting to server
 * show_progress: confirm the progress (use interval function)
* karura.client.js: javascript customize script for target app
 * predict: show the predict button next to the field.
* Karura Server: Python server
 * train: receive json data for application setting, and train the model by it
 * predict: receive record data, and return the predicted.

## Detail about train process

* read and save the setting.
* setting is required to predict
* extract data from app: (may have to handle over 100 records in the future)
* analyze the field and save it to understand/normalize the field value (especially text field)
* format the record data
* select model
* feature selection
* train the model
* get results
* save the model
