cove.controller('New_dataset', function ($scope, $http, $compile, $rootScope, $routeParams) {
    $scope.r_type = '';
    $scope.suffix = '';
    $scope.target_id;
    $scope.$on('$viewContentLoaded', function(event){
        if($routeParams.identifier){
            console.log('here');
            $("#email_valid").modal('show');
        }
    });

    $scope.validate = function(){
        console.log('here');
        $("#messagegoeshere_validate").empty();
        var email = $('#email').val();
        var hashed_str = $routeParams.identifier.split("$");
        // if(hashed_str.length == 2){
        //     $scope.target_id = hashed_str[0];
        //     $scope.suffix = hashed_str[1];
        //     $scope.r_type = 'edit';
        //     target_url = NEW_DATASET_URL + '?email=' + email + '&action=edit'+'&suffix=' + $scope.suffix;
        // }
        // else{
        //     $scope.suffix = hashed_str[0];
        //     $scope.r_type = 'add';
        //     target_url = NEW_DATASET_URL + '?email=' + email + '&action=add'+'&suffix=' + $scope.suffix;
        // }
        $scope.target_id = hashed_str[0];
        $scope.suffix = hashed_str[1];
        var target_url = NEW_DATASET_URL + '?email=' + email + '&rqst_id=' + target_id +'&suffix=' + $scope.suffix;
        $http.get(target_url)
                .success(function(data){
                    $('#email_input').val(email);
                    $("#email_valid").modal('hide');
                    $('#new_dst_form').show();
                    $scope.load_data($scope.target_id);
                })
                .error(function(error){
                     $("<p>Please enter a valid email.</p>"
                        ).addClass("text-warning").appendTo("#messagegoeshere_validate");
                })
    };

    $scope.load_data = function(target_id){
        if(target_id){
            //request_url = REQUEST_DST_URL + "id?dataset_id=" + target_id;
            request_url = DATASET_URL + '?id=' + target_id;
            $http.get(request_url)
                .success(function(data){
                    if(data.value != null){
                        $scope.insert_data(data.value);
                    };
                })
                .finally(function(){
                    $scope.is_loading = false;   
                });
        }
    }

    $scope.insert_data = function(data){
        $('#dst_name').val(data['name']);
        $('#dst_url').val(data['url']);
        $('#dst_description').val(data['description']);
        $('#dst_year').val(data['year']);
        $('#dst_author').val(data['creator']);
        $('#dst_task').val(data['tasks'].join(";"));
        $('#dst_topic').val(data['topics'].join(";"));
        $('#dst_keyword').val(data['keywords'].join(";"));
        $('#dst_type').val(data['datatypes'].join(";"));
        $('#dst_annotation').val(data['annotation_types'].join(";"));
        $('#dst_thumbnail').val(data['thumbnail']);
        $('#dst_size').val(data['size']);
        $('#dst_numcat').val(data['num_cat']);
        $('#dst_paper').val(data['related_paper']);
        $('#dst_citation').val(data['citations'].join(";"));
        $('#dst_conference').val(data['conferences'].join(";"));
        $('#dst_institution').val(data['institutions'].join(";"));
    }

    $scope.submit_new_dst = function(){
        $("#messagegoeshere_submit").empty();
        var dict = {};
        var contactor = $('#email_input').val();
        var dst_name = $('#dst_name').val();
        var url = $('#dst_url').val();
        var description = $('#dst_description').val();
        if(!contactor || !dst_name || !url || !description){
            $("<p>Please Enter All Required Fields.</p>"
                        ).addClass("text-warning").appendTo("#messagegoeshere_submit");
            return;
        }
        console.log($scope.r_type);
        var dict = {
            "email" : contactor,
            "action" : $scope.r_type,
            "target_id" : $scope.target_id,
            "suffix" : $scope.suffix,
            "name" : dst_name,
            "url" : $('#dst_url').val(),
            "description" : $('#dst_description').val(),
            "license" : "",
            "is_local" : false,
            "creator" : $('#dst_author').val(),
            "year" : $('#dst_year').val(),
            "size" : $('#dst_size').val(),
            "num_cat" : $('#dst_numcat').val(),
            "contact_name" : "",
            "contact_email" : contactor,
            "topics" : $('#dst_topic').val(),
            "related_paper" : $('#dst_paper').val(),
            "citations" : $('#dst_citation').val(),
            "conferences" : $('#dst_conference').val(),
            "tasks" : $('#dst_task').val(),
            "keywords" : $('#dst_keyword').val(),
            "datatypes" : $('#dst_type').val(),
            "annotations" : $('#dst_annotation').val(),
            "thumbnail" : $('#dst_thumbnail').val(),
            "institutions" : $('#dst_institution').val(),
        }
        $http({
            url : NEW_DATASET_URL,
            method : "POST",
            data : JSON.stringify(dict),
            headers: {'Content-Type':'application/json; charset=UTF-8'}
        }).success(function(data){
            $("<p>Your dataset has been successfully submitted. We will review it and add it to COVE. Thank you!</p>"
                        ).addClass("text-success").appendTo("#messagegoeshere_submit");
            $('#dst_description').val('');
            $('input[id^="dst_"]').each(function(){
                $(this).val('');
            })
            $('#send_new_dst').attr("disabled", true);

        }).error(function(error){
            $("<p>" + error['error'] +"</p>"
                        ).addClass("text-warning").appendTo("#messagegoeshere_submit");
        })
        $('#send_new_dst').attr("disabled", true);
    };
})