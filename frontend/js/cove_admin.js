cove.controller('AdminCtrl', function ($scope, $http, $compile, $rootScope, $cookieStore) {
    $scope.$on('$viewContentLoaded', function(event){
        $scope.load_page();
    });

    $scope.load_page = function(){
        var token = $cookieStore.get('token');
        var auth = btoa(token + ":")
        $http({
                url : ADMIN_URL,
                method : "GET",
                headers : {"Authorization" : 'Basic ' + auth}
            }).success(function(data){
                var result = data["pending_requests"];
                for(var i = 0; i < result.length; i++){
                    var tr = $("<tr></tr>");
                    var td_0 = $("<td></td>").text(result[i]['email']);
                    var td_1 = $("<td></td>").text(result[i]['firstname']);
                    var td_2 = $("<td></td>").text(result[i]['lastname']);
                    var bt = $("<button>Invite</button>")
                                .attr({"type":"button", "id":"invite_button_" + result[i]['id'], "ng-click":"invite(" + result[i]['id'] + ")"});
                    var td_3 = $("<td></td>").append(bt);
                    tr.append(td_0);
                    tr.append(td_1);
                    tr.append(td_2);
                    tr.append(td_3);
                    $('#table_body').append(tr);
                }
                $compile($("#table_body"))($scope);
            }).error(function(error){
                $('#login-form').modal('show');
            })
    };

    $scope.invite = function(id){
        console.log(id);
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

    $scope.login = function(){
        $("#messagegoeshere_login").empty();
        var username = $("#username").val();
        if(!username){
            $("<p>Please provide username.</p>"
                        ).addClass("text-warning").appendTo("#messagegoeshere_login");
            return;
        }
        var password = $("#password").val();
        if(!password){
            $("<p>Please provide password.</p>"
                        ).addClass("text-warning").appendTo("#messagegoeshere_login");
            return;
        }
        var dict = {
            "username" : username,
            "password" : password
        };
        $http({
            url : ADMIN_URL,
            method : "POST",
            data : JSON.stringify(dict),
            headers: {'Content-Type':'application/json; charset=UTF-8'}
        }).success(function(data){
            $cookieStore.put('token',data['token']);
            $scope.load_page();
            $('#login-form').modal('hide');
        }).error(function(error){
            $("<p>Invalid username or password.</p>"
                        ).addClass("text-warning").appendTo("#messagegoeshere_login");
            return;
        })
    }
})