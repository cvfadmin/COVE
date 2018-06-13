cove.controller('PendingDST',function ($scope, $http, $window, $location, $cookieStore, $compile, $routeParams){
    $scope.$on('$viewContentLoaded', function(event){
        $("#pending_dst_display").empty();
        var cur_dst, prev_dst;
        var request_url = 'http://127.0.0.1:5000/api/view_pending_dst?cur=' + $routeParams.cur;
        if($routeParams.prev){
            request_url += '&prev=' + $routeParams.prev;
        }
        
        if ($cookieStore.get('token')) {     
            var token = $cookieStore.get('token');
            var auth = btoa(token + ":")
            $http({
                    url : request_url,
                    method : "GET",
                    headers : {"Authorization" : 'Basic ' + auth}
                }).success(function(data){
                    cur_dst = data.value[0];
                    prev_dst = data.value[1];
                    $scope.load_data(cur_dst, prev_dst);
                }).error(function(error){
                    $('#login-form').modal('show');
                })      
        }
        else {
            $('#login-form').modal('show');            
        }

    });

    $scope.load_data = function(cur, prev){
        $('#login_button').hide();
        $('#logout_button').show(); 
        var ele = gen_display_html(cur, prev);
        $("#pending_dst_display").append(ele);
        $compile($('#pending_dst_display'))($scope);
    };

    $scope.dst_deny = function(){
        var token = $cookieStore.get('token');
        var auth = btoa(token + ":")
        var r = confirm("Please confirm your decision.");
        if(r){
            dict = {
                "id": $routeParams.cur,
                "target_id" :$routeParams.prev,
                "approved": false
            }
            var request_url = 'http://127.0.0.1:5000/api/view_pending_dst'
            $http({
                url : request_url,
                method : "POST",
                data : JSON.stringify(dict),
                headers : {"Authorization" : 'Basic ' + auth}
            }).success(function(data){
                $("#dst_approve").attr("disabled", true);
                $("#dst_deny").attr("disabled", true);
                window.location.href=('#/admin');
                window.location.reload();
            }).error(function(error){
                console.log("here");
                $('#login-form').modal('show');
            })
        }
    };

    $scope.dst_approve = function(){
        var token = $cookieStore.get('token');
        var auth = btoa(token + ":")
        var r = confirm("Please confirm your decision.");
        if(r){
            dict = {
                "id": $routeParams.cur,
                "target_id" :$routeParams.prev,
                "approved": true
            }
            console.log(dict);
            var request_url = 'http://127.0.0.1:5000/api/view_pending_dst'
            $http({
                url : request_url,
                method : "POST",
                data : JSON.stringify(dict),
                headers : {"Authorization" : 'Basic ' + auth}
            }).success(function(data){
                $("#dst_approve").attr("disabled", true);
                $("#dst_deny").attr("disabled", true);
                window.location.href=('#/admin');
                window.location.reload();
            }).error(function(error){
                $('#login-form').modal('show');
            })
        }
    };
})
