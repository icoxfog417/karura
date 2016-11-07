# karura

Easy machine learning platform on the kintone.

![karura-architecture](./doc/karura_architecture.PNG)

## All 3 steps to use prediction in your kintone app

Choose app that you want to do "prediction" (it is your client app). Then...

1. Add karura plugin to your client app, and add field to input predicted value.  
![step1.PNG](./doc/step1.PNG)  
(if you have "price" field and you want to predict it, you have to add "price_prediction" field.)
2. Define prediction target, and items to use for prediction.  
![step2.PNG](./doc/step2.PNG)  
You have to check your `app id`. You can confirm it in kintone system administration > app administration.
3. Train karura  
![step3.PNG](./doc/step3.PNG)

**Congraturation! You can use prediction in your client app!!**

![prediction.PNG](./doc/prediction.PNG)

## Installation

In the [karura-kintone](https://github.com/icoxfog417/karura/tree/master/karura-kintone), there are file for client and master.

* `karura-client-plugin.zip`: plugin for karura client app
* `karura-master-app.zip`: karura master app

That's all you need.

Optional

You can create your own karura server. If you want to do it, you can deploy your own karura by Heroku Button.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

