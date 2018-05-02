cove.controller('HomeCtrl', function ($scope, $route, $http, $location, $window, $compile, $rootScope, $routeParams) {

    $scope.tasks = [];
    $scope.topics = [];
    $scope.types = [];
    $http.get(HOME_URL).then(function(results) {
        $scope.tasks = results.data.tasks;
        $scope.topics = results.data.topics;
        $scope.types = results.data.types;
    }) 

    $(document).ready(function(){			
    	$('#filter').click(function() {
    		$('#filters').slideToggle('slow');
    	});
    });


    // TO-DO
   // $http.get(SEARCH_URL).then(function(results) {   
        // total row count


        // sets range of rows to query for chosen page        
   //     var limit = 

        // This sets the range of rows to query for the chosen $pagenum
     //   $limit = 'LIMIT ' .($pagenum - 1) * $page_rows .',' .$page_rows;
        // This is your query again, it is for grabbing just one page worth of rows by applying $limit
     //   $query = "SELECT * ".$query_base." ORDER BY id_num ASC $limit"; 
      //  $result = mysqli_query($link, $query);
        //echo '<pre>',print_r(mysqli_fetch_all($result)),'</pre>';

   // })
    
    // TO-DO

               

    $scope.$on('$viewContentLoaded', function(event){
        if($routeParams.query_type){
            if($routeParams.query_type === "text"){
                $scope.search_type = "Text";
                $scope.search_text = $routeParams.query;
            }
            else if($routeParams.query_type === "problem"){
                $scope.search_type = "Problem";
                $scope.search_text = $routeParams.problem;
            }
            else if($routeParams.query_type === "dataset"){
                $scope.search_type = "Dataset";
                $scope.search_text = $routeParams.dataset;
            }
            else if($routeParams.query_type === "annotation"){
                $scope.search_type = "Annotation";
                $scope.search_text = $routeParams.annotation;
            }
            else if($routeParams.query_type === "category"){
                $scope.search_type = "Category";
                $scope.search_text = $routeParams.category;
            }
            else if($routeParams.query_type === "name"){
                $scope.search_type = "Name";
                $scope.search_text = $routeParams.name;
            }
            else if($routeParams.query_type === "institution"){
                $scope.search_type = "Institution";
                $scope.search_text = $routeParams.institution;
            }
            else if($routeParams.query_type === "conference"){
                $scope.search_type = "Conference";
                $scope.search_text = $routeParams.conference;
            }
            else if($routeParams.query_type === "advanced"){
                $scope.is_advance = true;
                if($scope.search_datasample){
                    $scope.search_queries[0] = $routeParams.dataset;
                    $scope.search_queries[1] = $routeParams.category;
                    $scope.search_queries[2] = $routeParams.annotation;
                }
                else{
                    $scope.search_queries_dst[0] = $routeParams.task;
                    $scope.search_queries_dst[1] = $routeParams.year;
                    $scope.search_queries_dst[2] = $routeParams.insti;
                    $scope.search_queries_dst[3] = $routeParams.conf;
                    $scope.search_queries_dst[4] = $routeParams.dtype;
                    $scope.search_queries_dst[5] = $routeParams.atype;
                    $scope.search_queries_dst[6] = $routeParams.topic;
                }
            }
            else{
                console.log("undefined behavior");
            }
            $scope.ret_num = $routeParams.num;
            if($scope.search_datasample){
                $('#search_dataset_option').css("display" , "none");
                $('#search_datasample_option').css("display" , "");
                $('#search_target').text("Datasample(" + $scope.ret_num + ")");
            }
            else{
                $('#search_target').text("Dataset");
                $('#search_dataset_option').css("display" , "");
                $('#search_datasample_option').css("display" , "none");

            }
            if(!$scope.is_advance){
                $("#type_button").text($scope.search_type);
            }
            $scope.search(0);
        }
    });

    $scope.set_type = function(type){
        $("#type_button").text(type);
        $scope.search_type = type;
    };

    $scope.set_num = function(num){
        $('#search_target').text("Datasample(" + num + ")");
        $scope.ret_num = num;
        if(!$scope.search_datasample){
            $scope.search_type = 'Text';
            $("#type_button").text("Search by");
        }
        $scope.search_datasample = true;
        if($scope.is_advance){
            $("#advanced_hide_dst").css("display" , "none");
            $("#advanced_hide").fadeIn(600);
        }
        $('#search_dataset_option').css("display" , "none");
        $('#search_datasample_option').css("display" , "");
    };

    $scope.search_dataset = function(){
        $('#search_target').text("Dataset");
        if($scope.is_advance){
            $("#advanced_hide").css("display" , "none");
            $("#advanced_hide_dst").fadeIn(600);
        }
        if($scope.search_datasample){
            $scope.search_type = 'Name';
            $("#type_button").text("Search by");
        }
        $scope.search_datasample = false;
        $('#search_dataset_option').css("display" , "");
        $('#search_datasample_option').css("display" , "none");
    }

    $scope.go_to_download = function(){
        $window.open("#/download", "_self");
        // var new_tab = $window.open("/#/download", '_blank');
        // new_tab.download_list = $rootScope.download_list;
    };
    $scope.advance_span = function(){
        if($("#dd_icon").hasClass("octicon-chevron-down")){
            $scope.is_advance = true;
            $("#type_button").text("Search by");
            if($scope.search_datasample){
                $("#advanced_hide").fadeIn(600);
            }
            else{
                $("#advanced_hide_dst").fadeIn(600);
            }
            $("#dd_icon").removeClass("octicon-chevron-down");
            $("#dd_icon").addClass("octicon-chevron-up");
            $(".jumbotron").css("padding-bottom", "1.5rem");
        }
        else{
            $scope.is_advance = false;
            if($scope.search_datasample){
                $("#advanced_hide").fadeOut(400);
            }
            else{
                $("#advanced_hide_dst").fadeOut(400);
            }
            $("#dd_icon").addClass("octicon-chevron-down");
            $("#dd_icon").removeClass("octicon-chevron-up");
            $(".jumbotron").css("padding-bottom", "1.5rem");
        }
    };

    $scope.insert_title = function(){
        var reminder = "Below are result " + ($scope.search_datasample ? "datasamples" : "datasets") + " for your query: ";
        if($scope.is_advance){
            if($scope.search_datasample){
                if($scope.search_queries[0]){
                    reminder += "dataset = " + $scope.search_queries[0] + ", ";
                }
                if($scope.search_queries[1]){
                    reminder += "category = " + $scope.search_queries[1] + ", ";
                }
                if($scope.search_queries[2]){
                    reminder += "annotation = " + $scope.search_queries[2] + ", ";
                }
            }
            else{
                if($scope.search_queries_dst[0]){
                    reminder += "task = " + $scope.search_queries_dst[0] + ", ";
                }
                if($scope.search_queries_dst[1]){
                    reminder += "year = " + $scope.search_queries_dst[1] + ", ";
                }
                if($scope.search_queries_dst[2]){
                    reminder += "institution = " + $scope.search_queries_dst[2] + ", ";
                }
                if($scope.search_queries_dst[3]){
                    reminder += "conference = " + $scope.search_queries_dst[3] + ", ";
                }
                if($scope.search_queries_dst[4]){
                    reminder += "data_type = " + $scope.search_queries_dst[4] + ", ";
                }
                if($scope.search_queries_dst[5]){
                    reminder += "annotation = " + $scope.search_queries_dst[5] + ", ";
                }
                if($scope.search_queries_dst[6]){
                    reminder += "topic = " + $scope.search_queries_dst[6] + ", ";
                }
            }
        }
        else{
            reminder += $scope.search_type + " = " + $scope.search_text + ($scope.search_datasample ? "," : ".");
        }
        if($scope.search_datasample){
            reminder += " you can group them by: ";
        }
        else{
            reminder += " Click to view introduciton."
        }
        var title = $('<div/>',{
                    id: "title_message",
                    css: {
                        "background-color": "rgb(235, 230, 228)",
                        "font-size": "28px",
                        "padding-bottom": "0.5rem",
                        "margin-bottom": "2px",
                    },
                    text: reminder,
                });
        if($scope.search_datasample){
            var button = $(gen_group_button());
            title.append(button);
        }
        title.insertBefore($('#browse-side'));        
        $compile($('#title_message'))($scope);
    }

    $scope.group_by_dataset = function(){
        $("#group_button").text("dataset");
        $rootScope.browse_list = [];
        if($scope.browse_list_by_dataset.length === 0){
            for(var i=0; i<$scope.datasample_list.length; ++i){
                var sample = $scope.datasample_list[i];
                var find = 0;
                for(var j=0; j<$scope.browse_list_by_dataset.length; ++j){
                    if(sample.dataset_name == $scope.browse_list_by_dataset[j].display_name){
                        find = 1;
                        $scope.browse_list_by_dataset[j].sample_list.push(sample);
                    }
                }
                if(find === 0){
                    var temp = new displaycard(sample.dataset_name, $scope.global_id);
                    temp.sample_list.push(sample);
                    $rootScope.browse_list.push(temp);
                    $scope.browse_list_by_dataset.push(temp);
                    ++$scope.global_id;
                }
            }
        }
        else{
            for(var i=0; i < $scope.browse_list_by_dataset.length; i++){
                $rootScope.browse_list.push($scope.browse_list_by_dataset[i]);
            }
        }
        $rootScope.construct_browse_disp(false);
    };

    $scope.group_by_annotation = function(){
        $("#group_button").text("annotation");
        $rootScope.browse_list = [];
        if($scope.browse_list_by_annotation.length === 0){
            for(var i=0; i<$scope.datasample_list.length; ++i){
                var sample = $scope.datasample_list[i];
                var find = 0;
                for(var j=0; j<$scope.browse_list_by_annotation.length; ++j){
                    if(sample.annotation == $scope.browse_list_by_annotation[j].display_name){
                        find = 1;
                        $scope.browse_list_by_annotation[j].sample_list.push(sample);
                    }
                }
                if(find === 0){
                    var temp = new displaycard(sample.annotation, $scope.global_id);
                    temp.sample_list.push(sample);
                    $rootScope.browse_list.push(temp);
                    $scope.browse_list_by_annotation.push(temp);
                    ++$scope.global_id;
                }
            }
        }
        else{
            for(var i=0; i < $scope.browse_list_by_annotation.length; i++){
                $rootScope.browse_list.push($scope.browse_list_by_annotation[i]);
            }
        }
        $rootScope.construct_browse_disp(false);
    };

    $scope.group_by_dontgroup = function(){
        $("#group_button").text("dont\' group");
        $('#browse-side').empty();
        var browse_list = [];
        for(var i=0; i<$scope.datasample_list.length; ++i){
            browse_list.push($scope.datasample_list[i].pic_url);
        }
        var barrels = new Barrels($('#browse-side'), browse_list, 180);
    };

    $scope.click_search_button = function(){
        if($scope.is_advance){
            if($scope.search_datasample){                
                $scope.search_queries[0] = $("#adv-dataset").val();            
                $scope.search_queries[1] = $("#adv-cat").val();
                $scope.search_queries[2] = $("#adv-annote").val();
            }
            else{
                $scope.search_queries_dst[0] = $("#adv-task").val();
                $scope.search_queries_dst[1] = $("#adv-year").val();
                $scope.search_queries_dst[2] = $("#adv-insti").val();
                $scope.search_queries_dst[3] = $("#adv-confer").val();
                $scope.search_queries_dst[4] = $("#adv-dtype").val();
                $scope.search_queries_dst[5] = $("#adv-atype").val();
                $scope.search_queries_dst[6] = $("#adv-topic").val();
            }
        }
        else{
            $scope.search_text = $("#search-text").val();
        }
        $scope.search(1);
    }

    $scope.search = function(flag){ //flag to infer whether to replace state or not
        $scope.datasample_list = [];
        $scope.browse_list_by_annotation = [];
        $scope.browse_list_by_dataset = [];
        var request_url = "";
        var target_url = window.location.protocol + "//" + window.location.host;
        if($scope.is_advance){
            if($scope.search_datasample){
                request_url = REQUEST_URL + 'advanced?dataset=' + $scope.search_queries[0] + 
                '&category=' + $scope.search_queries[1] +'&annotation='+ $scope.search_queries[2] + 
                '&num=' + $scope.ret_num.toString();
                target_url += "/#/search/" + 'advanced?dataset=' + $scope.search_queries[0] + 
                '&category=' + $scope.search_queries[1] +'&annotation='+ $scope.search_queries[2] + 
                '&num=' + $scope.ret_num.toString();
            }
            else{
                request_url = REQUEST_DST_URL + 'advanced?task=' + $scope.search_queries_dst[0] + 
                '&year=' + $scope.search_queries_dst[1] +'&insti='+ $scope.search_queries_dst[2] + 
                '&conf='+ $scope.search_queries_dst[3] + '&dtype='+ $scope.search_queries_dst[4] +
                '&atype='+ $scope.search_queries_dst[5] + '&topic='+ $scope.search_queries_dst[6] +
                '&num=' + $scope.ret_num.toString();
                target_url = "/#/search_dataset/" + 'advanced?task=' + $scope.search_queries_dst[0] + 
                '&year=' + $scope.search_queries_dst[1] +'&insti='+ $scope.search_queries_dst[2] + 
                '&conf='+ $scope.search_queries_dst[3] + '&dtype='+ $scope.search_queries_dst[4] +
                '&atype='+ $scope.search_queries_dst[5] + '&topic='+ $scope.search_queries_dst[6] +
                '&num=' + $scope.ret_num.toString();
            }
        }
        else if($scope.search_type === "Text"){ 
            request_url = REQUEST_URL + 'text?query='+ $scope.search_text + '&num=' + $scope.ret_num.toString();
            target_url += "/#/search/" + 'text?query='+ $scope.search_text + '&num=' + $scope.ret_num.toString();
        }
        else if($scope.search_type === "Problem"){
            $window.alert('This function hasn\'t implemented yet.');
        }
        else if($scope.search_type === "Dataset"){
            request_url = REQUEST_URL + 'dataset?dataset=' + $scope.search_text + '&num=' + $scope.ret_num.toString();
            target_url += "/#/search/" + 'dataset?dataset=' + $scope.search_text + '&num=' + $scope.ret_num.toString();
        }
        else if($scope.search_type === "Category"){
            request_url = REQUEST_URL + 'category?category=' + $scope.search_text + '&num=' + $scope.ret_num.toString();
            target_url += "/#/search/" + 'category?category=' + $scope.search_text + '&num=' + $scope.ret_num.toString();
        }
        else if($scope.search_type === "Annotation"){
            if($scope.search_datasample){
                request_url = REQUEST_URL + 'annotation?annotation=' + $scope.search_text + '&num=' + $scope.ret_num.toString();
                target_url += "/#/search/" + 'annotation?annotation=' + $scope.search_text + '&num=' + $scope.ret_num.toString();
            }
            else{
                request_url = REQUEST_DST_URL + 'annotation?annotation=' + $scope.search_text + '&num=10';
                target_url += "/#/search_dataset/" + 'annotation?annotation=' + $scope.search_text + '&num=10';
            }
        }
        else if($scope.search_type === "Name"){
            request_url = REQUEST_DST_URL + 'name?name=' + $scope.search_text + '&num=10';
            target_url += "/#/search_dataset/" + 'name?name=' + $scope.search_text + '&num=10';
        }
        else if($scope.search_type === "Conference"){
            request_url = REQUEST_DST_URL + 'conference?conference=' + $scope.search_text + '&num=10';
            target_url += "/#/search_dataset/" + 'conference?conference=' + $scope.search_text + '&num=10';
        }
        else if($scope.search_type === "Year"){
            request_url = REQUEST_DST_URL + 'year?year=' + $scope.search_text + '&num=10';
            target_url += "/#/search_dataset/" + 'year?year=' + $scope.search_text + '&num=10';
        }
        else if($scope.search_type === "Data_type"){
            request_url = REQUEST_DST_URL + 'dtype?dtype=' + $scope.search_text + '&num=10';
            target_url += "/#/search_dataset/" + 'dtype?dtype=' + $scope.search_text + '&num=10';
        }
        else if($scope.search_type === "Institution"){
            request_url = REQUEST_DST_URL + 'institution?institution=' + $scope.search_text + '&num=10';
            target_url += "/#/search_dataset/" + 'institution?institution=' + $scope.search_text + '&num=10';
        }
        else{
            console.log("undefined behavior");
        }
        console.log(request_url);
        console.log(target_url);
        if(flag === 1){
            history.replaceState({}, "a", target_url);
        }
        if(request_url !== ""){
            $('#browse-side-thumb').empty();
            $scope.is_loading = true;
            $http.get(request_url)
                .success(function(data){
                    if(data.value != null){
                        $scope.datasample_list = [];
                        var value = data.value;
                        for(var i=0; i<value.length; ++i){
                            var dataset_name = value[i].name;
                            var dataset_url = window.location.protocol + "//" + window.location.host + "/#/dataset/" + value[i].id;
                            var temp_card = new displaycard(dataset_name, $scope.global_id, false, dataset_url);
                            for(var j=0; j<value[i].datasample_preview.length; ++j){
                                var sample = value[i].datasample_preview[j];
                                for(var k=0; k<sample.annotation.length; ++k){
                                    var temp = new datasample(dataset_name, sample.type, sample.id, sample.path, sample.annotation[k]);
                                    temp_card.sample_list.push(temp);
                                    $scope.datasample_list.push(temp);
                                }
                            }
                            $scope.browse_list_by_dataset.push(temp_card);
                            ++$scope.global_id;
                        }
                        $("#title_message").remove();
                        $scope.insert_title();
                        $scope.group_by_dataset();
                    };
                })
            .finally(function(){
                $scope.is_loading = false;   
            });
        }
    };
});