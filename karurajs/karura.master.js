/*
 * kintone javaScriptカスタマイズのテンプレート
 * 
 * Licensed under the MIT License
 */

 var Karura = (function() {
    "use strict";

    var _karura = {}

    _karura.read_fields = function(app_id, record){
        var registered_code = [];
        var ignores = ["CREATED_TIME", "CREATOR", "RECORD_NUMBER", "SPACER", "STATUS_ASSIGNEE", "MODIFIER", "UPDATED_TIME", "STATUS", "CATEGORY"];
        record.record.field_settings.value = []  // todo: do not clear if same app, existing setting

        kintone.api("/k/v1/app/form/fields", "GET", {"app": app_id}).then(function(resp){
            var forms = resp.properties;
            for(var f in forms){
                if(ignores.indexOf(forms[f].type) > -1){
                    continue;
                }
                var newRow = {
                    value: {
                        "field_name": {
                            type: "SINGLE_LINE_TEXT",
                            value: forms[f].label
                        },
                        "field_code": {
                            type: "SINGLE_LINE_TEXT",
                            value: f
                        },
                        "field_usage": {
                            type: "DROP_DOWN",
                            value: "予測に使わない"
                        }
                    }
                }
                record.record.field_settings.value.push(newRow);
            }
            kintone.app.record.set(record);
        })
    }

    _karura.begin_train = function(app_id, record){
        var payload = {"app_id": app_id, "fields": {}};
        var table = record.record.field_settings.value;
        var usages = ["予測に使う", "予測値"];
        var exist_target = false;
        var exist_feature = false;

        for(var i = 0; i < table.length; i++){
            var code = table[i].value["field_code"].value;
            var usage = table[i].value["field_usage"].value;
            var usage_id = usages.indexOf(usage);
            if(usage_id == 0){
                exist_feature = true;
            }
            if(usage_id == 1){
                exist_target = true;
            }
            payload.fields[code] = {"usage": usage_id};
        }

        //check
        if(exist_feature && exist_target){
            console.log(payload);
        }else{
            alert("少なくとも一つの予測に使用するフィールド、予測するフィールが必要です");
        }

    }

    kintone.events.on(["app.record.edit.show", "app.record.create.show"], function(event){
        //set the form field setup button
        var read_fields = document.createElement("button");
        read_fields.id = "read_fields"
        read_fields.innerHTML = "フィールドを読み込む"
        read_fields.onclick = function(){
            var record = kintone.app.record.get();
            var app_id = record["record"]["app_id"]["value"];
            if(app_id){
                Karura.read_fields(app_id, record);
            }else{
                alert("アプリ番号がまだ入力されていません");
            }
        }
        kintone.app.record.getSpaceElement("read_fields").appendChild(read_fields);

        //set the begin training button
        var begin_train = document.createElement("button");
        begin_train.id = "begin_train"
        begin_train.innerHTML = "学習を開始する"
        begin_train.onclick = function(){
            var record = kintone.app.record.get();
            var app_id = record["record"]["app_id"]["value"];
            if(app_id){
                Karura.begin_train(app_id, record);
            }else{
                alert("アプリ番号がまだ入力されていません");
            }
        }
        kintone.app.record.getSpaceElement("train_button").appendChild(begin_train);

    });

    return _karura

})();
