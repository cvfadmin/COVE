var cove = angular.module('CoveFront', ['ngRoute','ngCookies']);
var HOME_URL = 'http://127.0.0.1:5000/api'
var RESULTS_URL = 'http://127.0.0.1:5000/api/results';
var DATASET_URL = 'http://127.0.0.1:5000/api/dataset';
var REQUEST_DST_URL = 'http://127.0.0.1:5000/api/search_dataset/';
var NEW_DATASET_SUBMISSION_URL = 'http://127.0.0.1:5000/api/request';
var ADMIN_URL = 'http://127.0.0.1:5000/api/admin';
var NEW_DATASET_URL = 'http://127.0.0.1:5000/api/new_dataset';

var NUM_ROWS = 2;
var NUM_COL = 4;
var TOTAL_DISP = NUM_ROWS * NUM_COL;

cove.run(function($rootScope, $compile, $http){
    $rootScope.download_list = new Set();
    $rootScope.browse_list = [];
    $rootScope.expand = function(id){
        var card = $("#card_" + id.toString());
        var card_display = $("#display_card_" + id.toString());
        console.log(card_display);
        var cur = $("#dd_icon_"+id.toString());
        if(cur.hasClass("octicon-chevron-down")){
            cur.removeClass("octicon-chevron-down");
            cur.addClass("octicon-chevron-up");
            card.height("auto");
            card_display.height("auto");
            $(".jumbotron").css("padding-bottom", "1.5rem");
        }
        else{
            cur.removeClass("octicon-chevron-up");
            cur.addClass("octicon-chevron-down");
            card.height("230px");
            card_display.height("160px")
            $(".jumbotron").css("padding-bottom", "1.5rem");
        }
    };

    $rootScope.add_card_to_download = function(card_id){
        console.log("add");
        for(var i = 0; i < $rootScope.browse_list.length; i++){
            if($rootScope.browse_list[i].card_id === card_id){
                for(var j = 0; j < $rootScope.browse_list[i].sample_list.length; j++){
                    $rootScope.download_list.add($rootScope.browse_list[i].sample_list[j]);                    
                }
                break;
            }
        }
    };

    $rootScope.delete_card = function(card_id, is_download = false){
        $('#card_'+card_id.toString()).remove();
        if(is_download){
            for(var i=0;i<$rootScope.download_list.length; ++i){
                if($rootScope.download_list[i].card_id === card_id){
                    $rootScope.download_list.splice(i,1);
                    break;
                }
            }
        }
        else{
            for(var i=0;i<$rootScope.browse_list.length; ++i){
                if($rootScope.browse_list[i].card_id === card_id){
                    console.log("delete");
                    $rootScope.browse_list.splice(i,1);
                    break;
                }
            }
        }
    };

    $rootScope.send_submission_request = function(){
        $("#messagegoeshere").empty();
        var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        var email = $("#email-address").val();
        console.log(email);
        var bool = re.test(String(email).toLowerCase());
        if(!bool){
            $("<p>Please enter an valid email address.</p>"
                            ).addClass("text-warning").appendTo("#messagegoeshere");
        }
        else{
            var dict = {
                "email" : email,
                "firstname" : $("#first-name").val(),
                "lastname" : $("#last-name").val()
            };
            $http({
                url : NEW_DATASET_SUBMISSION_URL, 
                method : "POST",
                data : JSON.stringify(dict),
                headers: {'Content-Type':'application/json; charset=UTF-8'}
            }).success(function(data){
                $("<p>" + data['message'] + "</p>"
                        ).addClass("text-success").appendTo("#messagegoeshere");
                $("#send_submission_request").attr("disabled", true);
            })
        }
    }

    $rootScope.construct_browse_disp = function(download = true){
        $('#browse-side').empty();
        var cur_list = [];
        if(download){
            for(var i = 0; i < $rootScope.download_list.length; i++){
                cur_list.push($rootScope.download_list[i]);
            }
        }
        else{
            for(var i = 0; i < $rootScope.browse_list.length; i++){
                cur_list.push($rootScope.browse_list[i]);
            }
        }
        for(var i=0; i< cur_list.length; ++i){
            if(cur_list[i].sample_list.length == 0){
                download = true;
            }
            var card = $(gen_displaycard_header(cur_list[i].card_id, cur_list[i].display_name, download, cur_list[i].url));
            if(cur_list[i].sample_list.length != 0){
                var card_display = $('<div/>',{
                    id: "display_card_" + cur_list[i].card_id,
                    css: {
                        "padding-bottom": "0.5rem",
                        "padding-left" : "5px",
                        "padding-right" : "5px",
                        "height" : "160",
                        "overflow" : "scroll"
                    }
                });
                var pic_urls = [];
                for(var j = 0; j < cur_list[i].sample_list.length; j++){
                    pic_urls.push(cur_list[i].sample_list[j].pic_url);
                }
                var barrels = new Barrels(card_display, pic_urls, 160);
                card.append(card_display);
                var expand_button = $(gen_expand_button(cur_list[i].card_id));
                card.append(expand_button);
            }
            else{
                var warning_msg = $('<div/>',{
                    css: {
                        "padding-bottom": "0.5rem",
                        "padding-left" : "5px",
                        "padding-right" : "5px",
                        "height" : "auto",
                        "overflow" : "scroll"
                    }
                });
                $('<p align= "center"> Sorry, we don\' have this dataset stored in our website, you can refer to it at the link below: </p>').appendTo(warning_msg);
                $('<p align= "center"><a href = "' + cur_list[i].url + '" target = "_blank" >' + cur_list[i].url +'</a></p>').appendTo(warning_msg);
                warning_msg.appendTo(card);
                card.height("auto");
            }
            $('#browse-side').append(card);

        }
        $compile($('#browse-side'))($rootScope);
    };
})

cove.config(['$routeProvider', function ($routeProvider) {
    $routeProvider
        // Home
        .when("/", {templateUrl: "partials/home.html", controller: "HomeCtrl", search_datasample : true})
        .when("/result", {templateUrl: "partials/search_results.html", controller: "BrowseCtrl", search_datasample : true})
        .when("/dataset", {templateUrl: "partials/dataset.html", controller: "DatasetCtrl", search_datasample : true})
      
        .when("/search/:query_type", {templateUrl: "partials/home.html", controller: "BrowseCtrl", search_datasample : true})
        .when("/search_dataset/:query_type", {templateUrl: "partials/home.html", controller: "BrowseCtrl", search_datasample : false})
        // Download
        .when("/download", {templateUrl: "partials/download.html", controller: "DownloadCtrl"})
        // .when("/dataset/:dataset_id", {
        //     templateUrl: function(params){
        //         console.log('partials/dataset_frontpage/'+ params.dataset_id + '.html');
        //         return 'partials/dataset_frontpage/'+ params.dataset_id + '.html';
        //         console.log("here");
        //     },
        //     controller: "Dataset_intro"
        // });
        .when("/dataset/:dataset_id", {templateUrl: "partials/dataset_frontpage/1.html", controller: "Dataset_intro"})
        .when("/admin", {templateUrl : "partials/admin.html", controller: "AdminCtrl"})
        .when("/new_dataset/:identifier", {templateUrl: "partials/new_dataset_submit.html", controller: "Add_new_dataset"});
}]);
