cove.controller('DownloadCtrl', function ($scope, $http, $window, $compile, $rootScope){
    $scope.dataset_list = {};
    $scope.target_dataset = {};
    $scope.view_list = [];
    $scope.dataset_count = 0;
    $scope.$on('$viewContentLoaded', function(event){
        console.log("This is the download page");
        $scope.after_loading();
    });

    $scope.after_loading = function(){
        for(let item of $rootScope.download_list){
            $scope.view_list.push(item.pic_url);
            if(!(item.dataset_name in $scope.dataset_list)){
                $scope.dataset_list[item.dataset_name] = {};
            }
            if(!(item.type in $scope.dataset_list[item.dataset_name])){
                $scope.dataset_list[item.dataset_name][item.type] = new Set();
            }
            $scope.dataset_list[item.dataset_name][item.type].add(item.annotation);
        }
        $scope.construct_filter();
        $scope.construct_download_page();
    };

    $scope.construct_filter = function(){
        var tmp = $("<ul/>");
        for(var dataset in $scope.dataset_list){
            var new_dataset = $('<li>' + dataset +'</li>');
            var tmp_1 = $("<ul/>");
            for(var type in $scope.dataset_list[dataset]){
                var new_type = $('<li>' + type +'</li>');
                var tmp_2 = $("<ul/>");
                $scope.dataset_list[dataset][type].forEach(function(value){
                    var new_anno = $('<li>' + value +'</li>').attr('data-key', dataset + '$' + type + '$' +value);
                    tmp_2.append(new_anno);
                })
                new_type.append(tmp_2);
                tmp_1.append(new_type);
            }
            new_dataset.append(tmp_1);
            tmp.append(new_dataset);
        }
        $('#filter').append(tmp);
        $('#filter').jstree({
            "checkbox" : {
                "keep_selected_style" : false
            },
            "plugins" : ["checkbox"]
        });
    };

    $scope.check_dataset = function(id){
        var dataset_check = '#dataset_check_' + id;
        var annotation_check = '#annotation_check_' + id + ' input';
        console.log($(annotation_check));
        if(!($(dataset_check).is(':checked'))){
            $(annotation_check).each(function(){
                $(this).prop("disabled", true);
            });
        }
        else{
            $(annotation_check).each(function(){
                $(this).prop('disabled', false);
            });
        }
    };

    $scope.construct_download_page = function(){
        $('#browse-side').empty();
        var barrels = new Barrels($('#browse-side'), $scope.view_list, 160);
    };

    $scope.filter = function(){
        $scope.target_dataset = {};
        $scope.view_list = [];
        var selectedElements = $('#filter').jstree("get_selected", true);
        $.each(selectedElements, function () {
            if (this.data.key){
                var keys = this.data.key.split('$');
                if(!(keys[0] in $scope.target_dataset)){
                    $scope.target_dataset[keys[0]] = {};
                }
                if(!(keys[1] in $scope.target_dataset[keys[0]])){
                    $scope.target_dataset[keys[0]][keys[1]] = new Set();
                }
                $scope.target_dataset[keys[0]][keys[1]].add(keys[2]);
            }
        });
        for(let item of $rootScope.download_list){
            if((item.dataset_name in $scope.target_dataset) && (item.type in $scope.target_dataset[item.dataset_name]) && ($scope.target_dataset[item.dataset_name][item.type].has(item.annotation))){
                $scope.view_list.push(item.pic_url);
            }
        }
        console.log($scope.view_list);
        $scope.construct_download_page();
    };

    // $scope.filter = function(){
    //     $scope.target_dataset = {};
    //     $scope.view_list = [];
    //     for(var i = 0; i < $scope.dataset_count; i++){
    //         var dataset_check = '#dataset_check_' + i;
    //         if($(dataset_check).is(':checked')){
    //             var dataset_name = $(dataset_check).val();
    //             $scope.target_dataset[dataset_name] = new Set();
    //             var annotation_check = '#annotation_check_' + i + ' :checked';
    //             $(annotation_check).each(function(){
    //                 console.log($(this).val());
    //                 $scope.target_dataset[dataset_name].add($(this).val());
    //             })
    //         }
    //     }
    //     for(let item of $rootScope.download_list){
    //         if(item.dataset_name in $scope.target_dataset && $scope.target_dataset[item.dataset_name].has(item.annotation)){
    //             $scope.view_list.push(item.pic_url);
    //         }
    //     }
    //     console.log($scope.view_list.length);
    //     $scope.construct_download_page();
    // };

    $scope.empty_download_list = function(){
        $('#browse-side').empty();
        $rootScope.download_list = [];
        $('#dataset_check').find('div').remove();
        $('#annotation_check').find('div').remove();
    };

    $scope.click_modal = function(card_id){
        $('#myModal').modal('show');
        $compile($('#modal-submit'))($scope);
    };
    /*$('#myModal').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget); // Button that triggered the modal
        var recipient = button.data('cardid'); // Extract info from data-* attributes
        console.log(recipient);
        //var modal = $(this)
        //modal.find('.modal-title').text('New message to ' + recipient)
        //modal.find('.modal-body input').val(recipient)
        $compile($('#modal-submit'))($scope);
    });*/
    $scope.send_download = function(){
        var email_text = $("#email-text").val();
        var request_url = REQUEST_URL + "download";
        console.log(request_url);
        var request = new Object();
        request['email_address'] = email_text;
        var temp_list = [];
        for(var i = 0; i < $rootScope.download_list.length; ++i){
            for(var j = 0; j < $rootScope.download_list[i].sample_list.length; ++j){
                temp_list.push($rootScope.download_list[i].sample_list[j]);
            }
        }
        request['list'] = temp_list;
        $.ajax({
            type: "POST",
            url: request_url,
            contentType: "application/json; charset=UTF-8",
            data: JSON.stringify(request),
            success: function(result){
                console.log("success");
                $('#myModal').modal('hide');
            },
            error: function(error){
                console.log("error");
            }
        })
    };
})
