cove.controller('Add_new_dataset', function ($scope, $http, $compile, $rootScope, $routeParams) {
    $scope.$on('$viewContentLoaded', function(event){
        if($routeParams.identifier){
            $("#email_valid").modal('show');
        }
    });

    $scope.validate = function(){
        $("#messagegoeshere_validate").empty();
        var email = $('#email').val();
        var hashed_str = $routeParams.identifier;
        var target_url = NEW_DATASET_URL + '?email=' + email + '&suffix=' + hashed_str
        $http.get(target_url)
                .success(function(data){
                    $('#email_input').val(email);
                    $("#email_valid").modal('hide');
                    $('#new_dst_form').show();
                })
                .error(function(error){
                     $("<p>Please check your email, it's not valid.</p>"
                        ).addClass("text-warning").appendTo("#messagegoeshere_validate");
                })
    };

    $scope.submit_new_dst = function(){
        $("#messagegoeshere_submit").empty();
        var dict = {};
        var dst_name = $('#dst_name').val();
        if(!dst_name){
            $("<p>Please check your email, it's not valid.</p>"
                        ).addClass("text-warning").appendTo("#messagegoeshere_submit");
        } 
        var dict = {
            "email" : $('#email_input').val(),
            "suffix" : $routeParams.identifier,
            "name" : dst_name,
            "url" : $('#dst_url').val(),
            "description" : $('#dst_description').val(),
            "license" : "",
            "is_local" : false,
            "author" : "",
            "year" : $('#dst_year').val(),
            "size" : $('#dst_size').val(),
            "contact_name" : "",
            "contact_email" : "",
            "notes" : "",
            "paper" : $('#dst_paper').val(),
            "conference" : $('#dst_conference').val(),
            "tasks" : $('#dst_task').val(),
            "datatypes" : $('#dst_type').val(),
            "annotations" : $('#dst_annotation').val(),
            "thumbnails" : $('#dst_thumbnail').val(),
            "institutions" : $('#dst_institution').val(),
        }
        $http({
            url : NEW_DATASET_URL,
            method : "POST",
            data : JSON.stringify(dict),
            headers: {'Content-Type':'application/json; charset=UTF-8'}
        }).success(function(data){
            $("<p>Successfully add dataset.</p>"
                        ).addClass("text-success").appendTo("#messagegoeshere_submit");
            $('#dst_description').val('');
            $('input[id^="dst_"]').each(function(){
                $(this).val('');
            })

        }).error(function(error){
            $("<p>" + error['error'] +"</p>"
                        ).addClass("text-warning").appendTo("#messagegoeshere_submit");
        })
    };
})