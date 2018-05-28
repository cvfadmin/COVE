cove.controller('DatasetCtrl',function ($scope, $http, $window, $location, $compile, $rootScope, $routeParams){
	$scope.$on('$viewContentLoaded', function(event){

        if($routeParams.id){
            var id_num = $routeParams.id;
            $http.get(DATASET_URL+'?id='+id_num).then(function(results) {
                $scope.id = results.data.id;
                $scope.name = results.data.name;
                $scope.url = results.data.url;
                $scope.thumbnail = results.data.thumbnail;
                $scope.year = results.data.year;
                $scope.creator = results.data.creator;
                $scope.description = results.data.description;
                $scope.size = results.data.size;
                $scope.num_cat = results.data.num_cat;
                $scope.keywords = results.data.keywords;
                $scope.conferences = results.data.conferences;
                $scope.tasks = results.data.tasks;
                $scope.topics = results.data.topics;
                $scope.types = results.data.types;
                $scope.annotations = results.data.annotations;
                $scope.citations = results.data.citations;
                $scope.institutions = results.data.institutions;
                
                
                $scope.sizeTrue = true;        
                $scope.num_catTrue = true;        
                $scope.keywordsTrue = true;
                $scope.conferencesTrue = true;               
                $scope.annotationsTrue = true;              
                $scope.citationsTrue = true;

                if($scope.size == ''){
                     $scope.sizeTrue = false;
                }
                if($scope.num_cat == ''){
                     $scope.num_catTrue = false;
                }
                if($scope.keywords == ''){
                     $scope.keywordsTrue = false;
                }
                if($scope.conferences == ''){
                     $scope.conferencesTrue = false;
                }
                if($scope.annotations == ''){
                     $scope.annotationsTrue = false;
                }
                if($scope.citations == []){
                     $scope.citationsTrue = false;
                }      
            }) 
        }
	});

    $scope.send_delete_request = function(){
        $("#d-messagegoeshere").empty();
        var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        var email = $("#d-email-address").val();
        var bool = re.test(String(email).toLowerCase());
        var id = $routeParams.id;
        var reason = $("#delete-reason").val();
        if(!email || !reason){
            $("<p>Please enter all required fields.</p>"
                            ).addClass("text-warning").appendTo("#d-messagegoeshere");
        }
        else if(!bool){
            $("<p>Please enter an valid email address.</p>"
                            ).addClass("text-warning").appendTo("#d-messagegoeshere");
        }
        else{
            var dict = {
                "email" : email,
                "r_type" : "delete",
                "firstname" : $("#d-first-name").val(),
                "lastname" : $("#d-last-name").val(),
                "target_id" : id,
                "reason" : reason
            };
            $http({
                url :  NEW_REQUEST_URL, 
                method : "POST",
                data : JSON.stringify(dict),
                headers: {'Content-Type':'application/json; charset=UTF-8'}
            }).success(function(data){
                $("<p>" + data['message'] + "</p>"
                        ).addClass("text-success").appendTo("#d-messagegoeshere");
                $("#send_delete_request").attr("disabled", true);
            })  
        }
    };

    $scope.send_edit_request = function(){
        $("#e-messagegoeshere").empty();
        var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        var email = $("#e-email-address").val();
        var bool = re.test(String(email).toLowerCase());
        var id = $routeParams.id;
        if(!email){
            $("<p>Please fill out all required fields.</p>"
                            ).addClass("text-warning").appendTo("#e-messagegoeshere");
        }
        else if(!bool){
            $("<p>Please enter a valid email address.</p>"
                            ).addClass("text-warning").appendTo("#e-messagegoeshere");
        }
        else{
            var dict = {
                "email" : email,
                "r_type" : "edit",
                "firstname" : $("#e-first-name").val(),
                "lastname" : $("#e-last-name").val(),
                "target_id" : id
            };
            $http({
                url : NEW_REQUEST_URL, 
                method : "POST",
                data : JSON.stringify(dict),
                headers: {'Content-Type':'application/json; charset=UTF-8'}
            }).success(function(data){
                $("<p>" + data['message'] + "</p>"
                        ).addClass("text-success").appendTo("#e-messagegoeshere");
                $("#send_edit_request").attr("disabled", true);
            })
        }
    };

    $scope.insert_data = function(data){
        $('#dataset_name').text(data['name']);
        var author = $('<b><i>' + data['creator'] +'</i></b>');
        author.appendTo($('#authors'));
        var description = $('<p></p>').text(data['description']);
        description.appendTo($('#description'))
        var tasks = $('<p></p>').text(data['tasks'].join(", "));
        tasks.appendTo($('#tasks'));
        var datatypes = $('<p></p>').text(data['datatypes'].join(", "));
        datatypes.appendTo($('#datatypes'));
        var topics = $('<p></p>').text(data['topics'].join(", "));
        topics.appendTo($('#topics'));
        for(var i = 0; i < data['thumbnails'].length; i++){ 
            $('<img>', {src: data['thumbnails'][i]}).appendTo($('#thumbnails'));
        }
        var source = $('<a></a>').attr({target: "_blank", href: data['url']}).text(data['url']);
        source.appendTo($('#url'));
    };

    $scope.load_page = function(id){
        request_url = "DATASET_URL+'?id=" + id;
        $http.get(request_url)
                .success(function(data){
                    if(data.value != null){
                        $scope.insert_data(data.value);
                    };
                })
            .finally(function(){
                $scope.is_loading = false;   
            });
    };
})