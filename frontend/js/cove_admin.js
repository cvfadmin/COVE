cove.controller('AdminCtrl', function ($scope, $http, $compile, $rootScope, $cookieStore) {
    $scope.$on('$viewContentLoaded', function(event){
        if ($cookieStore.get('token')) {
            $scope.load_page();        
        }
        else {
            $('#login-form').modal('show');            
        }
    });

    $scope.load_page = function(){       
        $('#login_button').hide();
        $('#logout_button').show();
        $('#edit_request').empty();
        $('#add_request').empty();
        $('#delete_request').empty();
        $('#new_datasets').empty();
        $('#modified_datasets').empty();
        var token = $cookieStore.get('token');
        var auth = btoa(token + ":")
        $http({
                url : ADMIN_URL,
                method : "GET",
                headers : {"Authorization" : 'Basic ' + auth}
            }).success(function(data){
                var result = data["pending_requests"];
                for(var i = 0; i < result[0].length; i++){
                    var ele = gen_request_html("add", result[0][i], i);
                    $('#add_request').append(ele);
                }
                $compile($('#add_request'))($scope);
                for(var i = 0; i < result[1].length; i++){
                    var ele = gen_request_html("edit", result[1][i], i);
                    $('#edit_request').append(ele);
                }
                $compile($('#edit_request'))($scope);
                for(var i = 0; i < result[2].length; i++){
                    var ele = gen_request_html("delete", result[2][i], i);
                    $('#delete_request').append(ele);
                }
                $compile($('#delete_request'))($scope);
                for(var i = 0; i < result[3].length; i++){
                    console.log("here");
                    if(result[3][i][2]){
                        var ele = $("<a/>").attr({'href':'#/pending_datasets?cur=' + result[3][i][1] + '&prev=' + result[3][i][2],
                                     'target':'_blank'});
                        ele.text(result[3][i][0]);
                        $("#modified_datasets").append(ele);
                        $("#modified_datasets").append($("<br/>"));
                    }
                    else{
                        var ele = $("<a/>").attr({"href":"#/pending_datasets?cur=" + result[3][i][1],
                                     "target":"_blank"});
                        ele.text(result[3][i][0]);
                        $("#new_datasets").append(ele);
                        $("#new_datasets").append($("<br/>"));
                    }
                }
            }).error(function(error){
                $('#login-form').modal('show');
            })
    };

    $scope.approve = function(type, id){
        var token = $cookieStore.get('token');
        var auth = btoa(token + ":")
        var r = confirm("Please confirm your decision.");
        if(r){
            dict = {
                "type": type,
                "id": id,
                "approved": true
            }
            $http({
                url : PROCESS_REQUEST_URL,
                method : "POST",
                data : JSON.stringify(dict),
                headers : {"Authorization" : 'Basic ' + auth}
            }).success(function(data){
                var tmp1 = '#' + type + '_approve_' + id;
                var tmp2 = '#' + type + '_deny_' + id;
                $(tmp1).attr("disabled", true);
                $(tmp2).attr("disabled", true);
                window.location.href=('#/admin');
            }).error(function(error){
                $('#login-form').modal('show');
            })
        }
    }
    $scope.deny = function(type, id){
        var token = $cookieStore.get('token');
        var auth = btoa(token + ":")
        var r = confirm("Please confirm your decision.");
        if(r){
            dict = {
                "type": type,
                "id": id,
                "approved": false
            }
            $http({
                url : PROCESS_REQUEST_URL,
                method : "POST",
                data : JSON.stringify(dict),
                headers : {"Authorization" : 'Basic ' + auth}
            }).success(function(data){
                var tmp1 = '#' + type + '_approve_' + id;
                var tmp2 = '#' + type + '_deny_' + id;
                $(tmp1).attr("disabled", true);
                $(tmp2).attr("disabled", true);
                window.location.href=('#/admin');
            }).error(function(error){
                $('#login-form').modal('show');
            })
        }
    }

    $scope.invite = function(id){
        var token = $cookieStore.get('token');
        var auth = btoa(token + ":")
        var target_url = NEW_DATASET_SUBMISSION_URL + '/' + id;
        console.log(target_url);
        $http({
                url : target_url,
                method : "PUT",
                headers : {"Authorization" : 'Basic ' + auth}
            }).success(function(data){
                $("#invite_button_" + id).attr("disabled", true);
                $("#invite_button_" + id).html('invited');
            })
    };
})     