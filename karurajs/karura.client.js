/*
 * karura.master.js
 * JavaScript customize for Karura Master Application
 * Licensed under the MIT License
 */

(function(){
    "use strict";

    kintone.events.on(["app.record.edit.show", "app.record.create.show"], function(event){
        var KARURA_HOST = "https://f5049006.ngrok.io";
        var ignores = ["CREATED_TIME", "CREATOR", "RECORD_NUMBER", "SPACER", "STATUS_ASSIGNEE", "MODIFIER", "UPDATED_TIME", "STATUS", "CATEGORY"];

        var messageArea = document.createElement("span");
        messageArea.id = "messageArea";
        var setMessage = function(message, isError){
            var el = document.getElementById("messageArea");
            el.className = "label-prediction ";
            if(isError !== undefined){
                el.className += isError ? "type-error" : "type-success";
            }
            el.innerHTML = message;
        }

        var predictButton = document.createElement("button");
        predictButton.id = "predictButton";
        predictButton.innerHTML = "予測する";
        predictButton.className = "btn-karura-predict"
        predictButton.onclick = function(){
            var url = KARURA_HOST + "/predict";
            var appId = kintone.app.getId();
            var record = kintone.app.record.get();
            var body = {}
            for(var k in record.record){
                if(ignores.indexOf(record.record[k].type) > -1){
                    continue;
                }
                body[k] = record.record[k].value;
            }
            kintone.proxy(url, "POST", {}, body).then(function(args){
                    var body = args[0];
                    var result = JSON.parse(body);
                    if("prediction" in result){
                        setMessage("OK牧場", false);
                        var prediction = result.prediction;
                        for(k in prediction){
                            var field_code = k + "_prediction";
                            if(field_code in record.record){
                                record.record[field_code].value = prediction[k];
                            }
                        }
                    }else{
                        setMessage("some error occured", true);                        
                    }
                    kintone.app.record.set(record);
                });

        }

        var space = kintone.app.record.getHeaderMenuSpaceElement()
        space.appendChild(predictButton);
        space.appendChild(messageArea);

    })

})();
